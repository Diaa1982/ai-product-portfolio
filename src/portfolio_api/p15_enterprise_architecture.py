from __future__ import annotations

import hashlib,json
from collections import deque
from dataclasses import asdict,dataclass
from pathlib import Path
from typing import Any

@dataclass
class EnterpriseArchitectureInput:
    assessment_id:str; repository_name:str; repository_version:str; as_of_date:str
    elements:list[dict[str,Any]]; relationships:list[dict[str,Any]]; evidence_register:list[dict[str,Any]]
    impact_targets:list[str]; proposed_change:dict[str,Any]; assumptions:list[str]

@dataclass
class EnterpriseArchitectureResult:
    assessment_id:str; repository_status:str; inventory:dict[str,Any]; traceability:dict[str,Any]
    quality_exceptions:list[dict[str,str]]; impact_analysis:list[dict[str,Any]]
    application_portfolio:list[dict[str,Any]]; architecture_debt:dict[str,Any]
    decision_record:dict[str,Any]; audit_digest:str; limitations:list[str]
    def to_dict(self):return asdict(self)

class EnterpriseArchitectureIntelligence:
    def __init__(self,path:str|Path):self.config=json.loads(Path(path).read_text(encoding="utf-8"))
    def analyze(self,case:EnterpriseArchitectureInput)->EnterpriseArchitectureResult:
        evidence={x.get("evidence_id") for x in case.evidence_register if x.get("evidence_id") and x.get("valid") is True}
        ids=[x.get("element_id") for x in case.elements];byid={x.get("element_id"):x for x in case.elements if x.get("element_id")};exceptions=[]
        for duplicate in sorted({x for x in ids if x and ids.count(x)>1}):exceptions.append({"element_id":duplicate,"exception":"duplicate_element_id"})
        counts={x:0 for x in self.config["element_types"]};debt_items=[]
        for e in case.elements:
            eid=e.get("element_id","UNKNOWN");typ=e.get("element_type")
            if typ not in counts:exceptions.append({"element_id":eid,"exception":"invalid_element_type"})
            else:counts[typ]+=1
            for f in ["element_id","name","element_type","owner_role","lifecycle_status"]:
                if not e.get(f):exceptions.append({"element_id":eid,"exception":f"missing_{f}"})
            refs=e.get("evidence_refs",[])
            if not refs or any(x not in evidence for x in refs):exceptions.append({"element_id":eid,"exception":"missing_or_invalid_evidence"})
            if typ=="data_object" and not e.get("data_classification"):debt_items.append({"element_id":eid,"debt":"unclassified_data"})
            if typ=="technology" and e.get("support_status")=="unsupported":debt_items.append({"element_id":eid,"debt":"unsupported_technology"})
            if typ=="interface" and not e.get("security_control_refs"):debt_items.append({"element_id":eid,"debt":"uncontrolled_interface"})
        outgoing={x:[] for x in byid};incoming={x:[] for x in byid};link_pairs=set()
        for r in case.relationships:
            rid=r.get("relationship_id","UNKNOWN");a=r.get("from_id");b=r.get("to_id");typ=r.get("relationship_type")
            if a not in byid or b not in byid:exceptions.append({"element_id":rid,"exception":"orphan_relationship"});continue
            if a==b:exceptions.append({"element_id":rid,"exception":"self_relationship"})
            if typ not in self.config["relationship_types"]:exceptions.append({"element_id":rid,"exception":"invalid_relationship_type"})
            key=(a,b,typ)
            if key in link_pairs:exceptions.append({"element_id":rid,"exception":"duplicate_relationship"})
            link_pairs.add(key);outgoing[a].append(b);incoming[b].append(a)
            refs=r.get("evidence_refs",[])
            if not refs or any(x not in evidence for x in refs):exceptions.append({"element_id":rid,"exception":"relationship_evidence_missing"})
        required=self.config["required_traceability"]
        assessed=completed=0;missing=[]
        for e in case.elements:
            typ=e.get("element_type");eid=e.get("element_id")
            for target_type in required.get(typ,[]):
                assessed+=1
                connected=[x for x in outgoing.get(eid,[])+incoming.get(eid,[]) if byid[x].get("element_type")==target_type]
                if connected:completed+=1
                else:missing.append({"element_id":eid,"missing_link_to":target_type})
        coverage=round(completed/assessed*100,2) if assessed else 0
        impacts=[]
        for target in case.impact_targets:
            if target not in byid:impacts.append({"target_id":target,"status":"UNKNOWN_TARGET","affected":[]});continue
            seen={target};q=deque([(target,0)]);affected=[]
            while q:
                node,depth=q.popleft()
                for nxt in sorted(set(outgoing.get(node,[])+incoming.get(node,[]))):
                    if nxt not in seen:
                        seen.add(nxt);q.append((nxt,depth+1));affected.append({"element_id":nxt,"name":byid[nxt].get("name"),"element_type":byid[nxt].get("element_type"),"distance":depth+1,"criticality":byid[nxt].get("criticality",1)})
            impacts.append({"target_id":target,"status":"DRAFT_IMPACT_ANALYSIS","affected":sorted(affected,key=lambda x:(x["distance"],x["element_id"])),"human_validation_required":True})
        apps=[]
        groups={}
        for e in case.elements:
            if e.get("element_type")!="application":continue
            g=e.get("duplicate_group")
            if g:groups.setdefault(g,[]).append(e.get("element_id"))
        for e in case.elements:
            if e.get("element_type")!="application":continue
            fit=e.get("business_fit",3);health=e.get("technical_health",3);critical=e.get("criticality",3);g=e.get("duplicate_group")
            rec="INVESTIGATE_DUPLICATION" if g and len(groups.get(g,[]))>1 else "MODERNIZE" if critical>=4 and health<=2 else "INVESTIGATE_RETIREMENT" if fit<=2 and critical<=2 else "TOLERATE"
            apps.append({"application_id":e.get("element_id"),"name":e.get("name"),"business_fit":fit,"technical_health":health,"criticality":critical,"recommendation":rec,"status":"DRAFT","decommission_authorized":False})
            if rec in {"INVESTIGATE_DUPLICATION","MODERNIZE","INVESTIGATE_RETIREMENT"}:debt_items.append({"element_id":e.get("element_id"),"debt":rec.lower()})
        change=self.classify_change(**{k:bool(case.proposed_change.get(k,False)) for k in ["legal","security","cross_layer","high_criticality","metadata_only"]})
        adr={"adr_id":case.proposed_change.get("adr_id","ADR-DRAFT"),"title":case.proposed_change.get("title","Proposed architecture change"),"status":"DRAFT_FOR_DESIGN_AUTHORITY","change_classification":change["classification"],"alternatives":case.proposed_change.get("alternatives",[]),"principle_refs":case.proposed_change.get("principle_refs",[]),"risk_refs":case.proposed_change.get("risk_refs",[]),"evidence_refs":case.proposed_change.get("evidence_refs",[]),"approval_recorded":False,"autonomous_repository_change_permitted":False}
        payload={"case":asdict(case),"exceptions":exceptions,"impacts":impacts,"adr":adr};digest=hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
        return EnterpriseArchitectureResult(case.assessment_id,"VALID" if not exceptions else "EXCEPTIONS_FOUND",{"element_count":len(case.elements),"relationship_count":len(case.relationships),"by_type":counts},{"required_links_assessed":assessed,"completed_links":completed,"coverage_percent":coverage,"missing_links":missing},exceptions,impacts,apps,{"item_count":len(debt_items),"items":debt_items,"formal_risk_acceptance":False},adr,digest,["Synthetic-only technical deployment candidate; no live repository, ERP, performance, risk, HR, Microsoft 365, Power BI, ARIS or BIC integration is represented.","TOGAF terms are used as an alignment reference; the product does not claim formal TOGAF adoption or certification.","Application rationalization and architecture-debt outputs are diagnostic drafts, not vendor selection, investment, migration or decommission decisions.","Design Authority and accountable owners approve architecture changes, publication, security/cloud/data decisions and repository migration."])
    def classify_change(self,legal:bool,security:bool,cross_layer:bool,high_criticality:bool,metadata_only:bool)->dict[str,Any]:
        level="minor" if metadata_only and not any([legal,security,cross_layer,high_criticality]) else "major" if any([legal,security,high_criticality]) else "moderate" if cross_layer else "minor"
        return {"classification":level,"route":self.config["change_routes"][level],"human_approval_required":True,"autonomous_publication_permitted":False}
    def check_action(self,action:str)->dict[str,Any]:
        n=action.strip().lower().replace(" ","_");p=n in self.config["protected_actions"]
        return {"action":n,"permitted":not p,"human_authority_required":p,"reason":"Design Authority or accountable owner approval required" if p else "Architecture analysis permitted with repository evidence and audit logging"}
