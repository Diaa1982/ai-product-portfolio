from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ProcessAuditInput:
    audit_id: str
    period: str
    division: str
    unit: str
    process_id: str
    process_name: str
    process_version: str
    process_approved_at: str
    process_owner_role: str
    auditor_role: str
    lead_auditor_role: str
    audit_scope: str
    criteria_version: str
    documented_steps: list[str]
    actual_steps: list[str]
    criteria_results: list[dict[str, Any]]
    evidence_items: list[dict[str, str]]
    transaction_samples: list[dict[str, Any]]
    sampling_plan_reference: str
    evidence_plan_reference: str
    finding_review_reference: str | None = None
    human_approval_reference: str | None = None
    assumptions: list[str] = field(default_factory=list)


@dataclass
class ProcessAuditResult:
    audit_id: str
    assurance_status: str
    overall_score_percent: float | None
    conformance_percent: float | None
    domain_scores: dict[str, float | None]
    assessed_weight: float
    excluded_criteria: list[dict[str, str]]
    documented_vs_actual: dict[str, Any]
    evidence_assessment: dict[str, Any]
    findings: list[dict[str, Any]]
    corrective_action_requirements: list[dict[str, Any]]
    gate_evaluation: dict[str, Any]
    management_assurance_report: dict[str, Any]
    audit_digest: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProcessAuditAI:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.criteria = {x["id"]: x for x in self.config["criteria"] if x.get("active", True)}

    def _evidence_types(self, refs: list[str], evidence: dict[str, dict[str, str]]) -> set[str]:
        return {evidence[r].get("type", "") for r in refs if r in evidence and evidence[r].get("type") in self.config["evidence_types"]}

    def audit(self, case: ProcessAuditInput) -> ProcessAuditResult:
        if not case.process_owner_role or not case.lead_auditor_role:
            raise ValueError("Process owner and lead auditor roles are required")
        if case.auditor_role == case.process_owner_role:
            raise PermissionError("Auditor and process owner must be segregated")
        if case.criteria_version != self.config["config_version"]:
            raise ValueError("Criteria version does not match the active controlled library")
        evidence = {x.get("reference", ""): x for x in case.evidence_items if x.get("reference")}
        included: list[dict[str, Any]] = []
        excluded: list[dict[str, str]] = []
        findings: list[dict[str, Any]] = []
        for row in case.criteria_results:
            criterion_id = row.get("criterion_id", "")
            criterion = self.criteria.get(criterion_id)
            if not criterion:
                excluded.append({"criterion_id": criterion_id, "reason": "unknown_or_inactive_criterion"})
                continue
            if not row.get("applicable", True):
                excluded.append({"criterion_id": criterion_id, "reason": "not_applicable"})
                continue
            rating = row.get("auditor_rating")
            if rating is None:
                excluded.append({"criterion_id": criterion_id, "reason": "auditor_rating_required"})
                continue
            if rating not in range(0, 6):
                raise ValueError(f"Rating for {criterion_id} must be an integer from 0 to 5")
            refs = row.get("evidence_references", [])
            types = self._evidence_types(refs, evidence)
            if len(types) < self.config["minimum_evidence_types"]:
                excluded.append({"criterion_id": criterion_id, "reason": "insufficient_evidence_triangulation"})
                continue
            suggested = row.get("ai_suggested_rating")
            if suggested is not None and suggested != rating and not row.get("override_reason"):
                raise ValueError(f"Auditor override reason required for {criterion_id}")
            weight = float(criterion["weight"])
            included.append({"criterion_id": criterion_id, "domain": criterion["domain"], "rating": rating, "weight": weight, "weighted_score": rating / 5 * weight, "evidence_references": refs, "evidence_types": sorted(types), "ai_suggested_rating": suggested, "auditor_override_reason": row.get("override_reason", "")})
            if rating <= 3:
                severity = "Major" if (rating <= 1 or (criterion.get("critical") and rating <= 2)) else "Minor" if rating == 2 else "Observation"
                findings.append({"finding_id": f"{case.audit_id}-{criterion_id}", "criterion_id": criterion_id, "domain": criterion["domain"], "severity_recommendation": severity, "status": "DRAFT_FOR_AUDITOR_REVIEW", "evidence_references": refs, "human_issue_required": True})
        total_weight = sum(x["weight"] for x in included)
        total_weighted = sum(x["weighted_score"] for x in included)
        score = round(total_weighted / total_weight * 100, 2) if total_weight else None
        domain_scores: dict[str, float | None] = {}
        for domain in [x["code"] for x in self.config["domains"]]:
            rows = [x for x in included if x["domain"] == domain]
            weight = sum(x["weight"] for x in rows)
            domain_scores[domain] = round(sum(x["weighted_score"] for x in rows) / weight * 100, 2) if weight else None
        sample_checks = ["sequence_matches", "controls_operated", "authorized_approvals", "inputs_outputs_match", "roles_match", "timestamps_valid", "cross_unit_consistent"]
        assessed_samples = [x for x in case.transaction_samples if x.get("evidence_references")]
        conforming = [x for x in assessed_samples if all(x.get(check) is True for check in sample_checks) and not x.get("workaround_detected", False)]
        conformance = round(len(conforming) / len(assessed_samples) * 100, 2) if assessed_samples else None
        documented_missing = [x for x in case.documented_steps if x not in case.actual_steps]
        actual_extra = [x for x in case.actual_steps if x not in case.documented_steps]
        comparison = {"documented_steps": len(case.documented_steps), "actual_steps": len(case.actual_steps), "missing_in_execution": documented_missing, "unapproved_or_undocumented_steps": actual_extra, "sample_count": len(assessed_samples), "conforming_sample_count": len(conforming), "test_dimensions": sample_checks}
        mandatory_ids = {x["id"] for x in self.config["criteria"] if x.get("mandatory") and x.get("active", True)}
        included_ids = {x["criterion_id"] for x in included}
        missing_mandatory = sorted(mandatory_ids - included_ids)
        evidence_assessment = {"status": "SUFFICIENT_FOR_MANAGEMENT_ASSURANCE" if not missing_mandatory and assessed_samples else "INSUFFICIENT_EVIDENCE", "evidence_item_count": len(evidence), "assessed_criteria_count": len(included), "missing_mandatory_criteria": missing_mandatory, "triangulation_minimum_types": self.config["minimum_evidence_types"]}
        gate_missing = []
        for name, value in {"scope": case.audit_scope, "criteria_version": case.criteria_version, "lead_auditor": case.lead_auditor_role, "process_owner": case.process_owner_role, "approved_process_version": case.process_version and case.process_approved_at, "sampling_plan": case.sampling_plan_reference, "evidence_plan": case.evidence_plan_reference, "triangulated_evidence": evidence_assessment["status"] == "SUFFICIENT_FOR_MANAGEMENT_ASSURANCE", "auditor_ratings": not missing_mandatory, "finding_review": case.finding_review_reference}.items():
            if not value:
                gate_missing.append(name)
        gate = {"gate": "G3_FINDINGS", "status": "READY_FOR_RECORDED_HUMAN_DECISION" if not gate_missing and case.human_approval_reference else "BLOCKED", "missing_requirements": gate_missing + ([] if case.human_approval_reference else ["human_approval_reference"]), "autonomous_approval_permitted": False}
        status = "MANAGEMENT_ASSURANCE_DRAFT" if evidence_assessment["status"].startswith("SUFFICIENT") else "INSUFFICIENT_EVIDENCE"
        capa = [{"finding_id": x["finding_id"], "required": x["severity_recommendation"] in {"Major", "Minor"}, "root_cause_required": True, "owner_due_date_required": True, "closure_evidence_required": True, "independent_effectiveness_verification_required": True} for x in findings if x["severity_recommendation"] in {"Major", "Minor"}]
        report = {"title_en": f"Process Management Assurance — {case.process_name}", "title_ar": f"تقرير ضمان إدارة العمليات — {case.process_name}", "division": case.division, "unit": case.unit, "period": case.period, "process_version": case.process_version, "assurance_lenses": self.config["assurance_lenses"], "overall_score_percent": score, "conformance_percent": conformance, "finding_summary": {level: sum(1 for x in findings if x["severity_recommendation"] == level) for level in ["Major", "Minor", "Observation"]}, "conclusion": "Evidence-based management assurance draft; not an ISO certification, DGEP compliance declaration or formal audit opinion."}
        payload = {"case": asdict(case), "included": included, "comparison": comparison, "findings": findings, "gate": gate}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        return ProcessAuditResult(case.audit_id, status, score, conformance, domain_scores, total_weight, excluded, comparison, evidence_assessment, findings, capa, gate, report, digest, ["Synthetic-data technical candidate; production evidence is not authorized.", "Scores are deterministic from auditor-approved ratings and applicable weights; AI does not assign final ratings.", "No formal audit opinion, ISO 9001 certification or DGEP compliance conclusion is issued."])

    def verify_capa(self, finding_id: str, action_owner_role: str, verifier_role: str, closure_evidence: list[str], effectiveness_passed: bool, approval_reference: str | None) -> dict[str, Any]:
        if action_owner_role == verifier_role:
            raise PermissionError("Action owner cannot independently verify the same CAPA")
        missing = []
        if not closure_evidence: missing.append("closure_evidence")
        if not effectiveness_passed: missing.append("effectiveness_passed")
        if not approval_reference: missing.append("approval_reference")
        return {"finding_id": finding_id, "status": "VERIFIED_FOR_AUTHORIZED_CLOSURE" if not missing else "BLOCKED", "missing_requirements": missing, "close_finding_permitted": False, "authorized_human_closure_required": True}

    def division_dashboard(self, audits: list[dict[str, Any]]) -> dict[str, Any]:
        by_division: dict[str, list[dict[str, Any]]] = {}
        for item in audits:
            by_division.setdefault(item.get("division", "Unassigned"), []).append(item)
        rows = []
        for division, items in sorted(by_division.items()):
            scores = [x["overall_score_percent"] for x in items if x.get("overall_score_percent") is not None]
            rows.append({"division": division, "audit_count": len(items), "average_assurance_score": round(sum(scores) / len(scores), 2) if scores else None, "major_findings": sum(x.get("major_findings", 0) for x in items), "minor_findings": sum(x.get("minor_findings", 0) for x in items), "open_capa": sum(x.get("open_capa", 0) for x in items)})
        return {"divisions": rows, "filters": ["division", "unit", "process", "owner", "period", "criticality", "status", "severity"], "calculation_owner": "application", "ai_calculation_permitted": False}

    def check_action(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower().replace(" ", "_")
        protected = normalized in set(self.config["protected_actions"])
        return {"action": normalized, "permitted": not protected, "human_authority_required": protected, "reason": "Authorized auditor or assurance authority required" if protected else "Analytical support is permitted with evidence and audit logging"}
