from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RevenueReconciliationInput:
    case_id: str
    form_id: str
    reporting_period: str
    currency: str
    service_provider: str
    receiving_bank_account: str
    settlement_bank_account: str
    responsible_employee_role: str
    source_system: str
    evidence_references: list[str]
    assumptions: list[str]
    received_amount: float
    refund_amount: float
    fraud_transactions: float
    commission_type: str
    commission_rate_percent: float
    vat_type: str
    vat_rate_percent: float
    internal_reference: str
    bank_reference: str
    internal_amount: float
    bank_amount: float
    duplicate_internal: bool
    duplicate_bank: bool
    preparer_role: str
    approver_role: str
    materiality_threshold: float
    expected_settlement: float | None
    expected_net_transfer: float | None
    human_approval_reference: str | None = None


@dataclass
class RevenueReconciliationResult:
    reconciliation_id: str
    case_id: str
    form_id: str
    validation_status: str
    validation_issues: list[str]
    match_status: str
    facts: dict[str, Any]
    calculations: dict[str, float]
    exceptions: list[dict[str, Any]]
    assumptions: list[str]
    recommendations: list[str]
    evidence_references: list[str]
    human_review_required: bool
    decision_status: str
    audit_record: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RevenueReconciler:
    """Deterministic revenue, settlement, commission and bank matching controls."""

    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self._validate_config()

    def _validate_config(self) -> None:
        expected = {"Frm.601.2025.01", "Frm.172.2024.02", "Frm.221.2018.01"}
        if set(self.config["forms"]) != expected:
            raise ValueError("The three approved synthetic POC forms must be configured")
        if self.config["fixed_commission_amount"] != 100 or self.config["fixed_vat_rate_percent"] != 5:
            raise ValueError("Fixed synthetic POC commission/VAT rules changed")

    @staticmethod
    def _exception(code: str, severity: str, evidence: str, action: str) -> dict[str, Any]:
        return {"code": code, "severity": severity, "evidence": evidence, "recommended_action": action}

    def validate(self, item: RevenueReconciliationInput) -> list[str]:
        issues: list[str] = []
        if item.form_id not in self.config["forms"]:
            issues.append("unsupported_form")
        if item.reporting_period != self.config["synthetic_profile"]["reporting_period"]:
            issues.append("invalid_reporting_period")
        if item.currency != self.config["synthetic_profile"]["currency"]:
            issues.append("invalid_currency")
        for field in ("service_provider", "receiving_bank_account", "settlement_bank_account",
                      "responsible_employee_role", "source_system", "internal_reference", "bank_reference"):
            if not getattr(item, field).strip():
                issues.append(f"missing_{field}")
        if not item.evidence_references:
            issues.append("missing_evidence")
        if item.commission_type not in self.config["commission_types"]:
            issues.append("invalid_commission_type")
        if item.vat_type not in self.config["vat_types"]:
            issues.append("invalid_vat_type")
        if item.form_id == "Frm.172.2024.02" and item.commission_type != "agreed_percentage":
            issues.append("form_172_requires_agreed_percentage")
        if not 0 <= item.commission_rate_percent <= 100:
            issues.append("invalid_commission_rate")
        if not 0 <= item.vat_rate_percent <= 100:
            issues.append("invalid_vat_rate")
        for field in ("received_amount", "refund_amount", "fraud_transactions", "internal_amount",
                      "bank_amount", "materiality_threshold"):
            if getattr(item, field) < 0:
                issues.append(f"negative_value:{field}")
        if item.preparer_role == item.approver_role:
            issues.append("segregation_of_duties_conflict")
        if item.duplicate_internal:
            issues.append("duplicate_internal_transaction")
        if item.duplicate_bank:
            issues.append("duplicate_bank_transaction")
        return sorted(set(issues))

    def calculate(self, item: RevenueReconciliationInput) -> dict[str, float]:
        settlement = item.received_amount - item.refund_amount - item.fraud_transactions
        if item.commission_type in {"fixed_100", "fixed_100_vat_5"}:
            commission = float(self.config["fixed_commission_amount"])
        elif item.commission_type == "agreed_percentage":
            commission = settlement * item.commission_rate_percent / 100
        else:
            commission = 0.0

        if item.vat_type == "zero_percent":
            vat = 0.0
        elif item.vat_type == "fixed_100_vat_5":
            vat = float(self.config["fixed_commission_amount"]) * float(self.config["fixed_vat_rate_percent"]) / 100
        elif item.vat_type == "agreed_percentage":
            vat = commission * item.vat_rate_percent / 100
        else:
            vat = 0.0
        total_invoice = commission + vat
        net_transfer = settlement - total_invoice
        bank_variance = item.bank_amount - item.internal_amount
        discount_amount = max(0.0, item.internal_amount - item.bank_amount)
        return {"settlement_amount": round(settlement, 2), "commission_amount": round(commission, 2),
                "vat_amount": round(vat, 2), "total_invoice": round(total_invoice, 2),
                "net_transfer": round(net_transfer, 2), "bank_variance": round(bank_variance, 2),
                "discount_amount": round(discount_amount, 2)}

    def _match_status(self, item: RevenueReconciliationInput, calculations: dict[str, float]) -> str:
        if item.internal_reference != item.bank_reference:
            return "UNMATCHED_REFERENCE"
        tolerance = float(self.config["matching_tolerance"])
        if abs(calculations["bank_variance"]) <= tolerance:
            return "MATCHED"
        if calculations["discount_amount"] > tolerance:
            return "MATCHED_WITH_DISCOUNT_VARIANCE"
        return "MATCHED_WITH_AMOUNT_VARIANCE"

    def reconcile(self, item: RevenueReconciliationInput) -> RevenueReconciliationResult:
        issues = self.validate(item)
        calculations = self.calculate(item)
        match_status = self._match_status(item, calculations)
        exceptions: list[dict[str, Any]] = []
        if match_status == "UNMATCHED_REFERENCE":
            exceptions.append(self._exception("UNMATCHED_BANK_LINE", "High", f"{item.internal_reference}!={item.bank_reference}", "Investigate source references and assign an exception owner."))
        elif match_status == "MATCHED_WITH_DISCOUNT_VARIANCE":
            exceptions.append(self._exception("DISCOUNTED_MATCH", "Medium", f"Discount={calculations['discount_amount']}", "Validate the discount basis against approved evidence and agreement."))
        elif match_status == "MATCHED_WITH_AMOUNT_VARIANCE":
            exceptions.append(self._exception("MATCHED_AMOUNT_VARIANCE", "Medium", f"Variance={calculations['bank_variance']}", "Investigate and evidence the amount variance."))
        if calculations["settlement_amount"] < 0:
            exceptions.append(self._exception("NEGATIVE_SETTLEMENT", "High", str(calculations["settlement_amount"]), "Revenue owner should validate refunds and fraud adjustments."))
        if calculations["net_transfer"] < 0:
            exceptions.append(self._exception("NEGATIVE_NET_TRANSFER", "High", str(calculations["net_transfer"]), "Treasury and revenue owners should review before any transfer."))
        if abs(calculations["bank_variance"]) >= item.materiality_threshold:
            exceptions.append(self._exception("MATERIAL_BANK_VARIANCE", "High", str(calculations["bank_variance"]), "Escalate for authorized financial review."))

        tolerance = float(self.config["reconciliation_tolerance"])
        if item.expected_settlement is not None and abs(calculations["settlement_amount"] - item.expected_settlement) > tolerance:
            issues.append("settlement_reconciliation_mismatch")
        if item.expected_net_transfer is not None and abs(calculations["net_transfer"] - item.expected_net_transfer) > tolerance:
            issues.append("net_transfer_reconciliation_mismatch")

        high = any(e["severity"] == "High" for e in exceptions)
        human_review_required = bool(exceptions or issues)
        if (high or issues) and not item.human_approval_reference:
            issues.append("human_approval_required")
        decision_status = "BLOCKED" if issues else ("EXCEPTION_REVIEW_READY" if exceptions else "RECONCILED_FOR_HUMAN_CONFIRMATION")
        recommendations = [e["recommended_action"] for e in exceptions]
        if not recommendations:
            recommendations = ["Responsible revenue employee should confirm the reconciled evidence before treasury transfer processing."]
        facts = {"reporting_period": item.reporting_period, "currency": item.currency,
                 "service_provider": item.service_provider, "receiving_bank_account": item.receiving_bank_account,
                 "settlement_bank_account": item.settlement_bank_account,
                 "internal_reference": item.internal_reference, "bank_reference": item.bank_reference,
                 "responsible_employee_role": item.responsible_employee_role}
        created = utc_now()
        digest = hashlib.sha256(json.dumps({"facts": facts, "calculations": calculations,
                                             "exceptions": exceptions}, sort_keys=True).encode()).hexdigest()
        audit = {"event_id": str(uuid.uuid4()), "case_id": item.case_id,
                 "form_id": item.form_id, "config_version": self.config["config_version"],
                 "calculation_digest": digest, "validation_issues": sorted(set(issues)),
                 "human_approval_reference": item.human_approval_reference, "recorded_at": created}
        return RevenueReconciliationResult(
            reconciliation_id=str(uuid.uuid4()), case_id=item.case_id, form_id=item.form_id,
            validation_status="Valid" if not issues else "Invalid", validation_issues=sorted(set(issues)),
            match_status=match_status, facts=facts, calculations=calculations, exceptions=exceptions,
            assumptions=item.assumptions, recommendations=list(dict.fromkeys(recommendations)),
            evidence_references=item.evidence_references, human_review_required=human_review_required,
            decision_status=decision_status, audit_record=audit, created_at=created,
        )

    def check_action(self, action: str) -> dict[str, Any]:
        protected = action.strip().lower() in {x.lower() for x in self.config["protected_autonomous_actions"]}
        return {"action": action, "permitted_for_ai": not protected,
                "decision": "DENY_AUTONOMOUS_EXECUTION" if protected else "RECONCILIATION_SUPPORT_ONLY",
                "human_authority_required": protected,
                "reason": "Reconciliation analysis does not create financial, tax, refund, accounting or treasury authority."}
