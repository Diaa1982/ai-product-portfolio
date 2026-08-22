from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any


@dataclass
class PartnershipInput:
    case_id: str
    partner_id: str
    partnership_id: str
    partner_name: str
    entity_name: str
    responsible_person: str
    contact: str
    email: str
    start_date: str
    end_date: str
    partnership_status: str
    strategic_classification: str
    geographic_classification: str
    initiative: str
    innovation: str
    expected_value: str
    objectives: list[str]
    notes: str
    partnership_owner_role: str
    agreement_source_id: str
    agreement_version: str
    agreement_items: list[dict[str, Any]]
    claims: list[dict[str, Any]]
    evidence_items: list[dict[str, Any]]
    evaluation_cycle: str
    as_of_date: str
    response_requested_at: str
    owner_responded: bool
    reminders_recorded: int
    assumptions: list[str] = field(default_factory=list)


@dataclass
class PartnershipResult:
    case_id: str
    register_record: dict[str, Any]
    extracted_items: list[dict[str, Any]]
    extraction_exceptions: list[dict[str, str]]
    claim_evidence_assessments: list[dict[str, Any]]
    utilization: dict[str, Any]
    obligation_exceptions: list[dict[str, Any]]
    expiry_monitoring: dict[str, Any]
    notification_draft: dict[str, Any]
    recommendations: list[dict[str, str]]
    bilingual_report: dict[str, Any]
    audit_digest: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PartnershipManagementCopilot:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))

    @staticmethod
    def _date(value: str, field_name: str) -> date:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be YYYY-MM-DD") from exc

    def analyze(self, case: PartnershipInput) -> PartnershipResult:
        status_codes = {x["code"] for x in self.config["partnership_statuses"]}
        if case.partnership_status not in status_codes:
            raise ValueError("Unknown partnership status")
        if not case.partner_id or not case.partnership_id:
            raise ValueError("Partner_ID and Partnership_ID are required")
        if not case.agreement_source_id or not case.agreement_version:
            raise ValueError("A signed/current agreement source and version are required")
        as_of = self._date(case.as_of_date, "as_of_date")
        end = self._date(case.end_date, "end_date")
        start = self._date(case.start_date, "start_date")
        if end < start:
            raise ValueError("end_date cannot precede start_date")
        evidence = {x.get("evidence_id", ""): x for x in case.evidence_items if x.get("evidence_id")}
        claims = {x.get("item_id", ""): x for x in case.claims}
        extracted: list[dict[str, Any]] = []
        extraction_exceptions: list[dict[str, str]] = []
        assessments: list[dict[str, Any]] = []
        obligation_exceptions: list[dict[str, Any]] = []
        realized_total = 0.0
        planned_total = 0.0
        for raw in case.agreement_items:
            item = dict(raw)
            item_id = item.get("item_id", "")
            item["confirmation_status"] = "DRAFT_PENDING_AUTHORIZED_CONFIRMATION"
            extracted.append(item)
            for field_name in ["clause_citation", "item_type", "owner_role", "beneficiary", "expected_result", "evidence_type"]:
                if not item.get(field_name):
                    extraction_exceptions.append({"item_id": item_id, "field": field_name, "exception": "missing_required_extracted_field"})
            due = None
            try:
                due = self._date(item.get("due_date", ""), f"agreement_items.{item_id}.due_date")
            except ValueError:
                extraction_exceptions.append({"item_id": item_id, "field": "due_date", "exception": "ambiguous_or_missing_date"})
            claim = claims.get(item_id, {})
            claimed_status = claim.get("claimed_status", "")
            actual = float(claim.get("actual_quantity_or_value", 0) or 0)
            planned = float(item.get("quantity_or_value", 0) or 0)
            refs = claim.get("evidence_references", [])
            linked = [evidence[r] for r in refs if r in evidence]
            accepted_relevant = [x for x in linked if x.get("submission_status") == "ACCEPTED" and float(x.get("relevance_score", 0)) >= self.config["minimum_relevance_score"]]
            if due and due > as_of and not claimed_status:
                realization = "Not Yet Due"
            elif claimed_status in {"Realized", "Partially Realized"} and not accepted_relevant:
                realization = "Insufficient Evidence"
            elif accepted_relevant and planned > 0 and actual >= planned:
                realization = "Realized"
            elif accepted_relevant and actual > 0:
                realization = "Partially Realized"
            elif due and due > as_of:
                realization = "Not Yet Due"
            else:
                realization = "Not Realized"
            if planned > 0:
                planned_total += planned
                if accepted_relevant:
                    realized_total += min(actual, planned)
            assessment = {"item_id": item_id, "claimed_status": claimed_status or "No claim", "assessed_status": realization, "planned_quantity_or_value": planned, "accepted_evidenced_actual": actual if accepted_relevant else 0, "linked_evidence": refs, "accepted_relevant_evidence": [x.get("evidence_id") for x in accepted_relevant], "evidence_submission_is_acceptance": False, "review_required": True}
            assessments.append(assessment)
            if realization in {"Not Realized", "Insufficient Evidence"} or (due and due < as_of and realization != "Realized"):
                obligation_exceptions.append({"item_id": item_id, "exception": "overdue_or_missing_evidence" if due and due < as_of else "missing_or_weak_evidence", "status": realization, "due_date": item.get("due_date"), "owner_role": item.get("owner_role"), "clause_citation": item.get("clause_citation")})
        utilization_percent = round(realized_total / planned_total * 100, 2) if planned_total else None
        days_remaining = (end - as_of).days
        if days_remaining < 0:
            expiry_status = "EXPIRED"
        elif days_remaining <= 30:
            expiry_status = "DUE_WITHIN_30_DAYS"
        elif days_remaining <= 60:
            expiry_status = "DUE_WITHIN_60_DAYS"
        elif days_remaining <= 90:
            expiry_status = "DUE_WITHIN_90_DAYS"
        else:
            expiry_status = "NO_THRESHOLD_TRIGGER"
        requested = self._date(case.response_requested_at, "response_requested_at")
        response_due = requested.fromordinal(requested.toordinal() + self.config["response_policy"]["owner_response_days"])
        if case.owner_responded:
            notification = {"status": "NO_REMINDER_REQUIRED", "delivery_mode": "NONE", "send_permitted": False}
        elif as_of <= response_due:
            notification = {"status": "OWNER_RESPONSE_PENDING", "response_due_date": response_due.isoformat(), "delivery_mode": "DRAFT_USER_INITIATED", "send_permitted": False}
        elif case.reminders_recorded < self.config["response_policy"]["maximum_reminders"]:
            notification = {"status": "DRAFT_REMINDER", "reminder_number": case.reminders_recorded + 1, "recipient_role": case.partnership_owner_role, "delivery_mode": "DRAFT_USER_INITIATED", "send_permitted": False}
        else:
            notification = {"status": "DRAFT_ESCALATION", "recipient_role": self.config["response_policy"]["escalation_role"], "delivery_mode": "DRAFT_USER_INITIATED", "send_permitted": False}
        recommendations: list[dict[str, str]] = []
        if utilization_percent is not None and utilization_percent < 50:
            recommendations.append({"type": "increase_utilization", "status": "DRAFT", "reason": "Accepted-evidence utilization is below 50%; accountable review required."})
        if any(x["assessed_status"] == "Insufficient Evidence" for x in assessments):
            recommendations.append({"type": "increase_awareness", "status": "DRAFT", "reason": "Evidence requirements or acceptance status need owner/reviewer action."})
        if expiry_status in {"EXPIRED", "DUE_WITHIN_30_DAYS", "DUE_WITHIN_60_DAYS"}:
            recommendations.append({"type": "prepare_closure_review", "status": "DRAFT", "reason": "Expiry threshold reached; prepare continue, renegotiate or closure decision pack."})
        register = {"Partner_ID": case.partner_id, "Partnership_ID": case.partnership_id, "partner_name": case.partner_name, "entity_name": case.entity_name, "responsible_person": case.responsible_person, "contact": case.contact, "email": case.email, "start_date": case.start_date, "end_date": case.end_date, "status": case.partnership_status, "strategic_classification": case.strategic_classification, "geographic_classification": case.geographic_classification, "initiative": case.initiative, "innovation": case.innovation, "expected_value": case.expected_value, "objectives": case.objectives, "notes": case.notes, "owner_role": case.partnership_owner_role, "source_id": case.agreement_source_id, "source_version": case.agreement_version}
        report = {"title_en": f"Partnership performance and utilization — {case.partner_name}", "title_ar": f"تقرير أداء واستفادة الشراكة — {case.partner_name}", "achievements": [x for x in assessments if x["assessed_status"] == "Realized"], "obligation_status": assessments, "evidence_exceptions": obligation_exceptions, "utilization_percent": utilization_percent, "expiry_status": expiry_status, "risks_constraints": extraction_exceptions, "recommended_actions": recommendations, "source_links": [case.agreement_source_id] + [x.get("source_link", "") for x in case.evidence_items if x.get("source_link")], "decision_note_en": "Draft analysis only; authorized reviewers and business/legal owners decide.", "decision_note_ar": "التحليل مسودة فقط، ويتخذ المراجعون وملاك الأعمال والشؤون القانونية المخولون القرارات."}
        payload = {"case": asdict(case), "assessments": assessments, "exceptions": obligation_exceptions, "notification": notification}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        return PartnershipResult(case.case_id, register, extracted, extraction_exceptions, assessments, {"planned_quantity_or_value": planned_total, "accepted_evidenced_quantity_or_value": realized_total, "utilization_percent": utilization_percent, "calculation_owner": "application"}, obligation_exceptions, {"end_date": case.end_date, "days_remaining": days_remaining, "status": expiry_status}, notification, recommendations, report, digest, ["Synthetic-only technical candidate using a user-initiated Copilot pattern; no background triggers or autonomous workflow.", "Extraction, evidence relevance, utilization and recommendations are drafts requiring authorized review.", "The copilot cannot sign, amend or terminate agreements, send notices, accept evidence, make commitments or issue legal opinions."])

    def review_change(self, partnership_id: str, action: str, requester_role: str, first_reviewer_role: str, first_decision: str, final_approver_role: str, final_decision: str, override_reason: str, change_reference: str) -> dict[str, Any]:
        if action not in {"add", "modify", "delete"}:
            raise ValueError("Change action must be add, modify or delete")
        roles = self.config["review_roles"]
        if first_reviewer_role != roles["first_review"] or final_approver_role != roles["final_approval"]:
            raise PermissionError("Configured two-stage Strategy review roles are required")
        if requester_role in {first_reviewer_role, final_approver_role} or first_reviewer_role == final_approver_role:
            raise PermissionError("Requester, reviewer and final approver must be segregated")
        if first_decision != final_decision and not override_reason:
            raise ValueError("Final override requires justification")
        if not change_reference:
            raise ValueError("Change reference is required")
        return {"partnership_id": partnership_id, "action": action, "requester_role": requester_role, "first_review": {"role": first_reviewer_role, "decision": first_decision}, "final_review": {"role": final_approver_role, "decision": final_decision, "override_reason": override_reason}, "change_reference": change_reference, "status": "APPROVED_FOR_REGISTER_UPDATE" if first_decision == "approved" and final_decision == "approved" else "NOT_APPROVED", "autonomous_update_permitted": False, "history_retention_required": True}

    def check_action(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower().replace(" ", "_")
        protected = normalized in set(self.config["protected_actions"])
        return {"action": normalized, "permitted": not protected, "human_authority_required": protected, "reason": "Authorized business, Strategy or legal authority required" if protected else "Draft analytical support is permitted with source citations and review logging"}
