from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class IPSASReviewInput:
    case_id: str
    review_type: str
    reporting_period: str
    entity_id: str
    source_system: str
    evidence_references: list[str]
    applicable_policy_reference: str
    requirement_reference: str
    assumptions: list[str]
    confidence_score: float
    materiality_threshold: float
    reporting_impact: bool
    human_approval_reference: str | None
    journal_id: str | None
    debit_total: float | None
    credit_total: float | None
    entry_date: str | None
    period_start: str | None
    period_end: str | None
    account_code_valid: bool | None
    supporting_document_present: bool | None
    approval_status: str | None
    preparer_role: str | None
    approver_role: str | None
    ledger_balance: float | None
    external_balance: float | None
    unreconciled_items: list[dict[str, Any]]
    disclosure_items: list[dict[str, Any]]
    comparative_current: str | None
    comparative_prior: str | None
    comparative_required: bool


@dataclass
class IPSASReviewResult:
    result_id: str
    case_id: str
    review_type: str
    review_status: str
    compliance_conclusion: str
    evidence_strength: str
    facts: dict[str, Any]
    calculations: dict[str, Any]
    exceptions: list[dict[str, Any]]
    assumptions: list[str]
    recommendations: list[str]
    evidence_references: list[str]
    human_review_required: bool
    required_reviewer_role: str
    audit_record: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class IPSASComplianceReviewer:
    """Evidence-led exception review. It never issues a formal compliance conclusion."""

    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self._validate_config()

    def _validate_config(self) -> None:
        if set(self.config["review_types"]) != {
            "journal_quality", "reconciliation", "disclosure_checklist"
        }:
            raise ValueError("Three controlled accounting review types are required")
        if self.config.get("formal_compliance_determination_allowed") is not False:
            raise ValueError("Formal compliance determination must remain disabled")

    @staticmethod
    def _exception(code: str, severity: str, evidence: str, action: str) -> dict[str, Any]:
        return {"code": code, "severity": severity, "evidence": evidence, "recommended_action": action}

    def _base_validation(self, item: IPSASReviewInput) -> list[dict[str, Any]]:
        exceptions: list[dict[str, Any]] = []
        if item.review_type not in self.config["review_types"]:
            exceptions.append(self._exception("UNSUPPORTED_REVIEW_TYPE", "High", item.review_type, "Route to product owner."))
        if not item.evidence_references:
            exceptions.append(self._exception("MISSING_SOURCE_EVIDENCE", "High", "No evidence reference", "Obtain authoritative supporting evidence."))
        if not item.applicable_policy_reference.strip():
            exceptions.append(self._exception("MISSING_POLICY_REFERENCE", "High", "No organization-approved policy reference", "Accounting owner must identify the applicable approved policy."))
        if not item.requirement_reference.strip():
            exceptions.append(self._exception("MISSING_REQUIREMENT_REFERENCE", "High", "No cited requirement", "Qualified reviewer must cite the applicable requirement."))
        if not item.entity_id.strip() or not item.reporting_period.strip() or not item.source_system.strip():
            exceptions.append(self._exception("INCOMPLETE_CONTEXT", "High", "Entity, period or source missing", "Complete the accounting review context."))
        if not 0 <= item.confidence_score <= 1:
            exceptions.append(self._exception("INVALID_CONFIDENCE", "High", str(item.confidence_score), "Provide a confidence value from 0 to 1."))
        return exceptions

    def _review_journal(self, item: IPSASReviewInput) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        exceptions: list[dict[str, Any]] = []
        required = (item.journal_id, item.debit_total, item.credit_total, item.entry_date,
                    item.period_start, item.period_end, item.account_code_valid,
                    item.supporting_document_present, item.approval_status,
                    item.preparer_role, item.approver_role)
        if any(value is None or value == "" for value in required):
            exceptions.append(self._exception("INCOMPLETE_JOURNAL_FIELDS", "High", "Required journal field missing", "Complete the journal review record."))
            return {}, exceptions
        difference = round(float(item.debit_total) - float(item.credit_total), 2)
        if abs(difference) > float(self.config["thresholds"]["balance_tolerance"]):
            exceptions.append(self._exception("UNBALANCED_JOURNAL", "High", f"Debit-credit difference={difference}", "Accounting reviewer should investigate and determine any correction."))
        if not item.account_code_valid:
            exceptions.append(self._exception("INVALID_ACCOUNT_CODE", "High", str(item.journal_id), "Validate against the approved chart of accounts."))
        if not item.supporting_document_present:
            exceptions.append(self._exception("MISSING_SUPPORT", "High", str(item.journal_id), "Obtain and validate supporting documentation."))
        if item.approval_status not in self.config["journal_approval_statuses"]:
            exceptions.append(self._exception("INVALID_APPROVAL_STATUS", "High", str(item.approval_status), "Use an approved workflow status."))
        elif item.approval_status != "Approved":
            exceptions.append(self._exception("JOURNAL_NOT_APPROVED", "High", item.approval_status, "Route to the authorized accounting approval workflow."))
        if item.preparer_role == item.approver_role:
            exceptions.append(self._exception("SEGREGATION_OF_DUTIES_CONFLICT", "High", str(item.preparer_role), "Assign an independent authorized approver."))
        try:
            entry = date.fromisoformat(str(item.entry_date))
            start = date.fromisoformat(str(item.period_start))
            end = date.fromisoformat(str(item.period_end))
            if not start <= entry <= end:
                exceptions.append(self._exception("PERIOD_CUTOFF_EXCEPTION", "High", str(item.entry_date), "Review cut-off and period treatment against approved policy."))
        except ValueError:
            exceptions.append(self._exception("INVALID_DATE", "High", str(item.entry_date), "Correct the ISO date values."))
        amount = max(abs(float(item.debit_total)), abs(float(item.credit_total)))
        if amount >= item.materiality_threshold:
            exceptions.append(self._exception("MATERIAL_JOURNAL_REVIEW", "Medium", f"Amount={amount}", "Obtain accounting-manager review with evidence."))
        return {"debit_credit_difference": difference, "reviewed_amount": amount}, exceptions

    def _review_reconciliation(self, item: IPSASReviewInput) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        exceptions: list[dict[str, Any]] = []
        if item.ledger_balance is None or item.external_balance is None:
            exceptions.append(self._exception("INCOMPLETE_RECONCILIATION_BALANCES", "High", "Balance missing", "Provide both ledger and external/subledger balances."))
            return {}, exceptions
        difference = round(item.ledger_balance - item.external_balance, 2)
        if abs(difference) > float(self.config["thresholds"]["reconciliation_tolerance"]):
            exceptions.append(self._exception("UNRECONCILED_BALANCE", "High", f"Difference={difference}", "Investigate and reconcile against authoritative records."))
        aged_count = 0
        unsupported_count = 0
        for record in item.unreconciled_items:
            if int(record.get("age_days", 0)) > int(self.config["thresholds"]["aging_days"]):
                aged_count += 1
            if not record.get("evidence_reference"):
                unsupported_count += 1
        if aged_count:
            exceptions.append(self._exception("AGED_UNRECONCILED_ITEMS", "Medium", f"Count={aged_count}", "Assign owners and escalation dates."))
        if unsupported_count:
            exceptions.append(self._exception("UNSUPPORTED_RECONCILIATION_ITEMS", "High", f"Count={unsupported_count}", "Attach authoritative evidence for each item."))
        return {"reconciliation_difference": difference, "aged_item_count": aged_count,
                "unsupported_item_count": unsupported_count}, exceptions

    def _review_disclosure(self, item: IPSASReviewInput) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        exceptions: list[dict[str, Any]] = []
        if not item.disclosure_items:
            exceptions.append(self._exception("MISSING_DISCLOSURE_CHECKLIST", "High", "No checklist items", "Provide the approved disclosure template."))
            return {}, exceptions
        missing = partial = unsupported = 0
        for disclosure in item.disclosure_items:
            status = disclosure.get("status")
            if status not in self.config["disclosure_statuses"]:
                exceptions.append(self._exception("INVALID_DISCLOSURE_STATUS", "High", str(status), "Use a controlled disclosure status."))
            elif status == "Missing":
                missing += 1
            elif status == "Partial":
                partial += 1
            if not disclosure.get("evidence_reference") or not disclosure.get("policy_reference"):
                unsupported += 1
        if missing:
            exceptions.append(self._exception("DISCLOSURE_GAPS", "High", f"Missing={missing}", "Qualified reporting reviewer should assess and complete the disclosure."))
        if partial:
            exceptions.append(self._exception("PARTIAL_DISCLOSURES", "Medium", f"Partial={partial}", "Complete and evidence the checklist items."))
        if unsupported:
            exceptions.append(self._exception("UNSUPPORTED_DISCLOSURES", "High", f"Unsupported={unsupported}", "Add evidence and approved policy references."))
        if item.comparative_required and (not item.comparative_current or not item.comparative_prior):
            exceptions.append(self._exception("MISSING_COMPARATIVE_INFORMATION", "High", "Current or prior comparative missing", "Provide and validate required comparative information."))
        return {"disclosure_item_count": len(item.disclosure_items), "missing_count": missing,
                "partial_count": partial, "unsupported_count": unsupported}, exceptions

    def review(self, item: IPSASReviewInput) -> IPSASReviewResult:
        exceptions = self._base_validation(item)
        calculations: dict[str, Any] = {}
        if item.review_type == "journal_quality":
            calculations, domain_exceptions = self._review_journal(item)
        elif item.review_type == "reconciliation":
            calculations, domain_exceptions = self._review_reconciliation(item)
        elif item.review_type == "disclosure_checklist":
            calculations, domain_exceptions = self._review_disclosure(item)
        else:
            domain_exceptions = []
        exceptions.extend(domain_exceptions)

        insufficient = (
            item.confidence_score < float(self.config["thresholds"]["minimum_confidence"])
            or any(e["code"] in {"MISSING_SOURCE_EVIDENCE", "MISSING_POLICY_REFERENCE", "MISSING_REQUIREMENT_REFERENCE", "INCOMPLETE_CONTEXT"} for e in exceptions)
        )
        material = item.reporting_impact or any(e["severity"] == "High" for e in exceptions)
        human_review_required = True
        if insufficient:
            review_status = "INSUFFICIENT_INFORMATION"
        elif material and not item.human_approval_reference:
            review_status = "HUMAN_REVIEW_REQUIRED"
        elif item.human_approval_reference:
            review_status = "HUMAN_DECISION_RECORDED"
        else:
            review_status = "REVIEW_READY"
        conclusion = (
            "Potential exceptions identified; formal compliance determination reserved for qualified human review."
            if exceptions else
            "No exception identified by configured checks; formal compliance determination not performed."
        )
        evidence_strength = "Insufficient" if insufficient else ("Moderate" if exceptions else "Strong")
        recommendations = [e["recommended_action"] for e in exceptions]
        if not recommendations:
            recommendations = ["Qualified accounting reviewer should confirm evidence, policy and professional judgement."]
        facts = {"reporting_period": item.reporting_period, "entity_id": item.entity_id,
                 "source_system": item.source_system, "policy_reference": item.applicable_policy_reference,
                 "requirement_reference": item.requirement_reference, "reporting_impact": item.reporting_impact}
        created = utc_now()
        digest = hashlib.sha256(json.dumps({"facts": facts, "calculations": calculations,
                                             "exceptions": exceptions}, sort_keys=True).encode()).hexdigest()
        audit = {"event_id": str(uuid.uuid4()), "case_id": item.case_id,
                 "config_version": self.config["config_version"], "review_type": item.review_type,
                 "calculation_digest": digest, "human_approval_reference": item.human_approval_reference,
                 "recorded_at": created}
        return IPSASReviewResult(
            result_id=str(uuid.uuid4()), case_id=item.case_id, review_type=item.review_type,
            review_status=review_status, compliance_conclusion=conclusion,
            evidence_strength=evidence_strength, facts=facts, calculations=calculations,
            exceptions=exceptions, assumptions=item.assumptions,
            recommendations=list(dict.fromkeys(recommendations)), evidence_references=item.evidence_references,
            human_review_required=human_review_required, required_reviewer_role="ACCOUNTING_MANAGER_OR_EQUIVALENT",
            audit_record=audit, created_at=created,
        )

    def check_action(self, action: str) -> dict[str, Any]:
        protected = action.strip().lower() in {x.lower() for x in self.config["protected_autonomous_actions"]}
        return {"action": action, "permitted_for_ai": not protected,
                "decision": "DENY_AUTONOMOUS_EXECUTION" if protected else "REVIEW_SUPPORT_ONLY",
                "human_authority_required": protected,
                "reason": "Accounting analysis cannot replace authorized professional judgement or execution."}
