from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class PFMMaturityInput:
    assessment_id: str
    entity_profile: str
    as_of_date: str
    assessment_mode: str
    scope_statement: str
    criteria_results: list[dict[str, Any]]
    evidence_register: list[dict[str, Any]]
    assessors: list[dict[str, Any]]
    performance_history: dict[str, Any]
    external_comparisons: list[dict[str, Any]]
    moderation: dict[str, Any]
    assumptions: list[str]


@dataclass
class PFMMaturityResult:
    assessment_id: str
    assessment_status: str
    overall_maturity: dict[str, Any]
    domain_results: list[dict[str, Any]]
    conformance: dict[str, Any]
    evidence_qa: list[dict[str, str]]
    moderation: dict[str, Any]
    recognition: dict[str, Any]
    surveillance: dict[str, Any]
    improvement_plan: list[dict[str, Any]]
    audit_digest: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]: return asdict(self)


class PFMMaturityCertification:
    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))

    def assess(self, case: PFMMaturityInput) -> PFMMaturityResult:
        if case.assessment_mode not in self.config["assessment_modes"]:
            raise ValueError("invalid assessment_mode")
        try: as_of = datetime.strptime(case.as_of_date, "%Y-%m-%d")
        except ValueError as exc: raise ValueError("as_of_date must be YYYY-MM-DD") from exc
        evidence = {x.get("evidence_id"): x for x in case.evidence_register if x.get("evidence_id")}
        assessor_ids = {x.get("assessor_id") for x in case.assessors if x.get("assessor_id")}
        qa: list[dict[str, str]] = []
        evaluated: list[dict[str, Any]] = []

        for row in case.criteria_results:
            cid=row.get("criterion_id","UNKNOWN"); domain=row.get("domain"); proposed=row.get("proposed_level")
            if domain not in self.config["domains"]: qa.append({"criterion_id":cid,"issue":"invalid_domain"})
            if proposed not in range(1,7): qa.append({"criterion_id":cid,"issue":"invalid_proposed_level"}); proposed=1
            if row.get("assessor_id") not in assessor_ids: qa.append({"criterion_id":cid,"issue":"unknown_assessor"})
            if row.get("reviewer_id") not in assessor_ids: qa.append({"criterion_id":cid,"issue":"unknown_reviewer"})
            if row.get("assessor_id")==row.get("reviewer_id"): qa.append({"criterion_id":cid,"issue":"assessor_reviewer_conflict"})
            refs=row.get("evidence_refs",[]); resolved=[evidence[x] for x in refs if x in evidence and evidence[x].get("valid") is True]
            if len(resolved)!=len(refs) or not refs: qa.append({"criterion_id":cid,"issue":"missing_or_invalid_evidence"})
            types={x.get("evidence_type") for x in resolved}; cap=proposed
            if not refs or not resolved: cap=1
            if proposed>=4 and not {"kpi_achievement","governance_effectiveness"}.issubset(types):
                cap=min(cap,3);qa.append({"criterion_id":cid,"issue":"level_4_evidence_not_met"})
            if proposed>=5:
                independent=any(x.get("independently_verified") is True for x in resolved)
                sustained=case.performance_history.get("sustained_quarters",0)>=4
                external=bool(case.external_comparisons)
                audited="audited_evidence" in types
                if not all([independent,sustained,external,audited]):
                    cap=min(cap,4);qa.append({"criterion_id":cid,"issue":"level_5_evidence_not_met"})
            if proposed>=6:
                required={"system_demonstration","continuous_monitoring","benefits_tracking","human_oversight"}
                if not required.issubset(types) or case.performance_history.get("sustained_quarters",0)<8:
                    cap=min(cap,5);qa.append({"criterion_id":cid,"issue":"level_6_evidence_not_met"})
            evaluated.append({"criterion_id":cid,"domain":domain,"weight":float(row.get("weight",1)),"mandatory":bool(row.get("mandatory",False)),"proposed_level":proposed,"evidenced_level":cap,"level_label":self.config["maturity_levels"][str(cap)],"evidence_count":len(resolved),"status":"EVIDENCED" if cap==proposed and resolved else "CAPPED_BY_EVIDENCE"})

        domains=[]
        for domain in self.config["domains"]:
            rows=[x for x in evaluated if x["domain"]==domain]
            if not rows:
                domains.append({"domain":domain,"score":None,"level":None,"status":"NOT_ASSESSED"});continue
            total=sum(x["weight"] for x in rows)
            score=round(sum(x["evidenced_level"]*x["weight"] for x in rows)/total,2) if total else None
            level=math.floor(score) if score else None
            domains.append({"domain":domain,"score":score,"level":level,"label":self.config["maturity_levels"].get(str(level)),"status":"EVIDENCED"})
        scored=[x for x in domains if x["score"] is not None]
        average=round(sum(x["score"] for x in scored)/len(scored),2) if scored else None
        mandatory=[x["evidenced_level"] for x in evaluated if x["mandatory"]]
        overall=min(math.floor(average),min(mandatory)) if average is not None and mandatory else math.floor(average) if average is not None else None

        principles=case.moderation.get("mandatory_principles",{})
        missing_principles=[x for x in self.config["mandatory_principles"] if principles.get(x) is not True]
        independence=case.moderation.get("independent_reviewer_confirmed") is True
        conflicts=case.moderation.get("conflicts_disclosed") is True
        moderation_ready=not qa and not missing_principles and independence and conflicts and case.assessment_mode!="self_assessment"
        candidate=self.config["recognition_classes"].get(str(overall)) if overall else None
        status="MODERATION_READY" if moderation_ready else "SELF_ASSESSMENT_ONLY" if case.assessment_mode=="self_assessment" else "EVIDENCE_OR_GOVERNANCE_GAPS"
        recognition={"scheme_status":"WORKING_DRAFT_NOT_ADOPTED","candidate_class":candidate if moderation_ready else None,"candidate_only":True,"certificate_issued":False,"official_certification":False,"authorized_scheme_owner_decision_required":True,"assurance_opinion_issued":False}
        plan=[]
        for d in domains:
            if d["level"] is None or d["level"]<4:
                plan.append({"domain":d["domain"],"priority":"HIGH" if d["level"] is None or d["level"]<3 else "MEDIUM","action":"Close evidence and capability gaps through an owner-approved improvement initiative.","status":"DRAFT"})
        payload={"case":asdict(case),"evaluated":evaluated,"qa":qa,"recognition":recognition}
        digest=hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
        return PFMMaturityResult(case.assessment_id,status,{"evidenced_average":average,"evidenced_level":overall,"level_label":self.config["maturity_levels"].get(str(overall)),"formal_rating":False,"criterion_count":len(evaluated)},domains,{"mandatory_principles_passed":not missing_principles,"missing_principles":missing_principles,"compliance_conclusion":False},qa,{"independent_reviewer_confirmed":independence,"conflicts_disclosed":conflicts,"appeal_status":case.moderation.get("appeal_status","NOT_OPEN"),"ready":moderation_ready,"human_decision_required":True},recognition,{"quarterly_kpi_review_due":(as_of+timedelta(days=90)).date().isoformat(),"annual_reassessment_due":(as_of+timedelta(days=365)).date().isoformat(),"automatic_renewal":False},plan,digest,["Synthetic-only technical deployment candidate; no official scheme, accreditation or certification authority is represented.","The six-level maturity and Bronze–Diamond recognition structure is a configurable working draft, not an adopted international standard.","GAPFS/G-APFM references do not replace statutory law, IPSAS, GFSM, PEFA, INTOSAI or sovereign accountability.","Material decisions, moderation, recognition, certification, surveillance, appeals and renewal remain human-governed."])

    def check_action(self, action: str) -> dict[str, Any]:
        normalized=action.strip().lower().replace(" ","_");protected=normalized in self.config["protected_actions"]
        return {"action":normalized,"permitted":not protected,"human_authority_required":protected,"reason":"Authorized scheme owner or assessment authority required" if protected else "Assessment support permitted with evidence and audit logging"}
