from __future__ import annotations
import hashlib,json
from dataclasses import asdict,dataclass
from datetime import date,datetime
from pathlib import Path
from typing import Any

@dataclass
class ProcessPortfolioInput:
    assessment_id:str; as_of_date:str; repository_name:str; repository_version:str
    processes:list[dict[str,Any]]; maturity_evidence:list[dict[str,Any]]; migration_evidence:dict[str,str]

@dataclass
class ProcessPortfolioResult:
    assessment_id:str; validation_status:str; exceptions:list[dict[str,str]]; process_metrics:dict[str,Any]
    traceability:dict[str,Any]; maturity:dict[str,Any]; review_due:list[dict[str,str]]
    migration_readiness:dict[str,Any]; improvement_recommendations:list[dict[str,str]]; audit_digest:str; limitations:list[str]
    def to_dict(self): return asdict(self)

class EnterpriseProcessIntelligence:
    def __init__(self,path:str|Path):
        self.config=json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def _date(v,n):
        try:return datetime.strptime(v,"%Y-%m-%d").date()
        except Exception as e:raise ValueError(f"{n} must be YYYY-MM-DD") from e
    def analyze(self,case:ProcessPortfolioInput)->ProcessPortfolioResult:
        asof=self._date(case.as_of_date,"as_of_date"); rows=case.processes; exceptions=[]
        ids=[x.get("process_id") for x in rows]; guids=[x.get("process_guid") for x in rows]
        for value in {x for x in ids if x and ids.count(x)>1}:exceptions.append({"process_id":value,"exception":"duplicate_process_id"})
        for value in {x for x in guids if x and guids.count(x)>1}:exceptions.append({"process_id":value,"exception":"duplicate_process_guid"})
        byid={x.get("process_id"):x for x in rows if x.get("process_id")}
        linked=0; total_links=0; review_due=[]
        levels={k:0 for k in self.config["hierarchy"]}
        for p in rows:
            pid=p.get("process_id",""); level=p.get("level","")
            if level not in levels: exceptions.append({"process_id":pid,"exception":"invalid_level"});continue
            levels[level]+=1
            for f in ["process_id","process_guid","name","owner_role","status","version"]:
                if not p.get(f):exceptions.append({"process_id":pid,"exception":f"missing_{f}"})
            if level!="L1":
                parent=byid.get(p.get("parent_id")); expected=f"L{int(level[1])-1}"
                if not parent:exceptions.append({"process_id":pid,"exception":"orphan_process"})
                elif parent.get("level")!=expected:exceptions.append({"process_id":pid,"exception":"invalid_parent_level"})
            allowed=self.config["notation"][level]
            if p.get("notation") not in allowed:exceptions.append({"process_id":pid,"exception":"notation_mismatch"})
            for f in self.config["required_links"]:
                if f=="parent_id" and level=="L1":continue
                total_links+=1
                if p.get(f):linked+=1
                else:exceptions.append({"process_id":pid,"exception":f"missing_link_{f}"})
            reviewed=p.get("last_review_date")
            if reviewed:
                d=self._date(reviewed,f"{pid}.last_review_date")
                if (asof-d).days>365:review_due.append({"process_id":pid,"reason":"annual_review_overdue"})
            else:review_due.append({"process_id":pid,"reason":"review_date_missing"})
            for t in p.get("review_triggers",[]):
                if t in self.config["review_rules"]["triggers"]:review_due.append({"process_id":pid,"reason":f"trigger:{t}"})
        maturity_rows=[]
        for m in case.maturity_evidence:
            score=m.get("score"); refs=m.get("evidence_references",[])
            if score not in range(1,6) or not refs:maturity_rows.append({"domain":m.get("domain"),"status":"INSUFFICIENT_EVIDENCE","score":None})
            else:maturity_rows.append({"domain":m.get("domain"),"status":"EVIDENCED","score":score,"label":self.config["maturity_scale"][str(score)]})
        scored=[x["score"] for x in maturity_rows if x.get("score")]
        maturity={"domains":maturity_rows,"average":round(sum(scored)/len(scored),2) if scored else None,"formal_maturity_rating":False}
        missing_migration=[x for x in self.config["migration_controls"] if not case.migration_evidence.get(x)]
        migration={"status":"READY_FOR_CONTROLLED_POC" if not missing_migration else "BLOCKED","missing_controls":missing_migration,"vendor_selection_permitted":False,"production_migration_permitted":False}
        coverage=round(linked/total_links*100,2) if total_links else None
        rec=[]
        if exceptions:rec.append({"type":"repository_quality","status":"DRAFT","recommendation":"Resolve ownership, hierarchy, notation, duplicate and traceability exceptions."})
        if review_due:rec.append({"type":"review_program","status":"DRAFT","recommendation":"Route annual and triggered reviews through approved governance."})
        if coverage is not None and coverage<100:rec.append({"type":"enterprise_traceability","status":"DRAFT","recommendation":"Complete service, KPI, risk/control, application, policy and output links."})
        payload={"case":asdict(case),"exceptions":exceptions,"migration":migration}
        digest=hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
        metrics={"process_count":len(rows),"by_level":levels,"active_count":sum(x.get("status")=="ACTIVE" for x in rows),"unique_process_ids":len(set(x for x in ids if x)),"unique_guids":len(set(x for x in guids if x))}
        return ProcessPortfolioResult(case.assessment_id,"VALID" if not exceptions else "EXCEPTIONS_FOUND",exceptions,metrics,{"required_links_assessed":total_links,"completed_links":linked,"coverage_percent":coverage},maturity,review_due,migration,rec,digest,["Synthetic-only technical candidate; no production repository access is authorized.","APQC mapping is customized to the approved enterprise architecture; it is not adopted blindly.","AI may identify exceptions and recommend improvements but cannot approve, publish, delete or migrate processes, select a vendor, sign a contract or declare compliance."])
    def classify_change(self,structural:bool,legal:bool,cross_unit:bool,control:bool,metadata_only:bool)->dict[str,Any]:
        level="minor" if metadata_only and not any([structural,legal,cross_unit,control]) else "major" if any([structural,legal,control]) else "moderate"
        return {"classification":level,"route":self.config["change_routes"][level],"human_approval_required":True,"autonomous_publication_permitted":False}
    def check_action(self,action:str)->dict[str,Any]:
        n=action.strip().lower().replace(" ","_");p=n in self.config["protected_actions"]
        return {"action":n,"permitted":not p,"human_authority_required":p,"reason":"Approved process governance authority required" if p else "Analytical support permitted with repository citations and audit logging"}
