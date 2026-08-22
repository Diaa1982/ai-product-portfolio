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
class FiscalSnapshotInput:
    case_id: str
    reporting_period: str
    currency: str
    division_id: str
    cost_center: str
    account_code: str
    source_record_id: str
    source_system: str
    evidence_references: list[str]
    assumptions: list[str]
    organization_master_loaded: bool
    chart_of_accounts_loaded: bool
    approved_budget_loaded: bool
    original_budget: float
    supplementary_budget: float
    transfer_amount: float
    period_plan: float
    actual_expenditure: float
    commitments: float
    revenue_target: float
    revenue_actual: float
    opening_cash: float
    cash_inflow: float
    cash_outflow: float
    minimum_cash_buffer: float
    kpi_direction: str
    kpi_target: float
    kpi_actual: float
    kpi_attention_tolerance_percent: float
    inherent_risk_score: float
    control_effectiveness_percent: float
    requester_role: str
    approver_role: str
    proposed_action_amount: float
    maximum_authority_amount: float
    action_type: str
    duplicate_transaction: bool = False
    expected_revised_budget: float | None = None
    expected_closing_cash: float | None = None
    human_approval_reference: str | None = None


@dataclass
class FiscalInsightResult:
    insight_id: str
    case_id: str
    validation_status: str
    validation_issues: list[str]
    reconciliation_status: str
    facts: dict[str, Any]
    calculations: dict[str, float | str | None]
    risks: list[dict[str, str]]
    assumptions: list[str]
    recommendations: list[str]
    evidence_references: list[str]
    confidence: str
    authority_status: str
    decision_status: str
    audit_record: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PFMBrain:
    """Deterministic control backbone for governed PFM analytical insights."""

    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self._validate_config()

    def _validate_config(self) -> None:
        profile = self.config["synthetic_dataset_profile"]
        if profile["division_count"] != 8 or profile["account_count"] != 60:
            raise ValueError("Synthetic profile must retain the approved PFM Brain baseline")
        if len(self.config["acceptance_cases"]) != 20:
            raise ValueError("Exactly twenty acceptance cases are required")
        if self.config["load_order"][:2] != ["organization_master", "chart_of_accounts"]:
            raise ValueError("Master data must load before transactional domains")

    def validate(self, item: FiscalSnapshotInput) -> list[str]:
        issues: list[str] = []
        if item.reporting_period != self.config["synthetic_dataset_profile"]["fiscal_year"]:
            issues.append("invalid_reporting_period")
        if item.currency != self.config["synthetic_dataset_profile"]["currency"]:
            issues.append("invalid_currency")
        if not item.organization_master_loaded:
            issues.append("organization_master_not_loaded")
        if not item.chart_of_accounts_loaded:
            issues.append("chart_of_accounts_not_loaded")
        if not item.approved_budget_loaded:
            issues.append("approved_budget_not_loaded")
        for name in ("division_id", "cost_center", "account_code", "source_record_id", "source_system"):
            if not getattr(item, name).strip():
                issues.append(f"missing_{name}")
        if not item.evidence_references:
            issues.append("missing_evidence")
        if item.kpi_direction not in self.config["kpi_directions"]:
            issues.append("invalid_kpi_direction")
        if not 0 <= item.kpi_attention_tolerance_percent <= 100:
            issues.append("invalid_kpi_tolerance")
        if not 0 <= item.inherent_risk_score <= 100:
            issues.append("invalid_inherent_risk_score")
        if not 0 <= item.control_effectiveness_percent <= 100:
            issues.append("invalid_control_effectiveness")
        if item.requester_role == item.approver_role:
            issues.append("segregation_of_duties_conflict")
        if item.duplicate_transaction:
            issues.append("duplicate_transaction")
        nonnegative = (
            "original_budget", "supplementary_budget", "period_plan", "actual_expenditure",
            "commitments", "revenue_target", "revenue_actual", "opening_cash", "cash_inflow",
            "cash_outflow", "minimum_cash_buffer", "proposed_action_amount", "maximum_authority_amount",
        )
        for name in nonnegative:
            if getattr(item, name) < 0:
                issues.append(f"negative_value:{name}")
        return sorted(set(issues))

    @staticmethod
    def _kpi_status(direction: str, target: float, actual: float, tolerance_percent: float) -> str:
        tolerance = tolerance_percent / 100
        if direction == "Higher":
            if actual >= target:
                return "On Target"
            return "Attention" if actual >= target * (1 - tolerance) else "Off Target"
        if direction == "Lower":
            if actual <= target:
                return "On Target"
            return "Attention" if actual <= target * (1 + tolerance) else "Off Target"
        return "Invalid"

    def _control_result(self, effectiveness: float) -> str:
        thresholds = self.config["control_thresholds"]
        if effectiveness >= thresholds["effective_minimum_percent"]:
            return "Effective"
        if effectiveness >= thresholds["partially_effective_minimum_percent"]:
            return "Partially Effective"
        return "Failed"

    @staticmethod
    def _risk_band(score: float) -> str:
        if score >= 70:
            return "High"
        if score >= 40:
            return "Medium"
        return "Low"

    def analyze(self, item: FiscalSnapshotInput) -> FiscalInsightResult:
        issues = self.validate(item)
        revised_budget = item.original_budget + item.supplementary_budget + item.transfer_amount
        available_budget = revised_budget - item.actual_expenditure - item.commitments
        budget_variance = item.actual_expenditure - item.period_plan
        revenue_shortfall = max(0.0, item.revenue_target - item.revenue_actual)
        closing_cash = item.opening_cash + item.cash_inflow - item.cash_outflow
        cash_buffer_gap = closing_cash - item.minimum_cash_buffer
        kpi_status = self._kpi_status(
            item.kpi_direction, item.kpi_target, item.kpi_actual,
            item.kpi_attention_tolerance_percent,
        )
        control_result = self._control_result(item.control_effectiveness_percent)
        residual_risk_score = item.inherent_risk_score * (1 - item.control_effectiveness_percent / 100)
        residual_risk_band = self._risk_band(residual_risk_score)

        reconciliation_issues: list[str] = []
        tolerance = float(self.config["reconciliation_tolerance"])
        if item.expected_revised_budget is not None and abs(revised_budget - item.expected_revised_budget) > tolerance:
            reconciliation_issues.append("revised_budget_mismatch")
        if item.expected_closing_cash is not None and abs(closing_cash - item.expected_closing_cash) > tolerance:
            reconciliation_issues.append("closing_cash_mismatch")
        issues.extend(reconciliation_issues)

        protected = item.action_type.lower() in {
            action.lower() for action in self.config["protected_autonomous_actions"]
        }
        within_limit = item.proposed_action_amount <= item.maximum_authority_amount
        if protected:
            authority_status = "PROTECTED_ACTION_HUMAN_AUTHORITY_REQUIRED"
        elif not within_limit:
            authority_status = "EXCEEDS_AUTHORITY_ESCALATE"
        else:
            authority_status = "WITHIN_LIMIT_HUMAN_APPROVAL_REQUIRED"

        risks: list[dict[str, str]] = []
        if available_budget < 0:
            risks.append({"risk": "budget_exceeded", "rating": "High"})
        if revenue_shortfall > 0:
            risks.append({"risk": "revenue_shortfall", "rating": "Medium"})
        if cash_buffer_gap < 0:
            risks.append({"risk": "cash_buffer_breach", "rating": "High"})
        if kpi_status == "Off Target":
            risks.append({"risk": "kpi_off_target", "rating": "Medium"})
        if control_result == "Failed":
            risks.append({"risk": "control_failed", "rating": "High"})
        if residual_risk_band == "High":
            risks.append({"risk": "high_residual_risk", "rating": "High"})
        if item.proposed_action_amount >= float(self.config["critical_action_amount"]):
            risks.append({"risk": "critical_value_action", "rating": "High"})
        if reconciliation_issues:
            risks.append({"risk": "report_reconciliation_failed", "rating": "High"})

        high_risk = any(risk["rating"] == "High" for risk in risks)
        approval_needed = protected or not within_limit or high_risk
        if approval_needed and not item.human_approval_reference:
            issues.append("human_approval_required")
        decision_status = "BLOCKED" if issues else "ANALYSIS_READY_FOR_HUMAN_USE"

        recommendations: list[str] = []
        if issues:
            recommendations.append("Resolve validation, reconciliation, authority and approval exceptions before operational use.")
        if available_budget < 0:
            recommendations.append("Escalate the budget exceedance to the authorized budget authority for review.")
        if cash_buffer_gap < 0:
            recommendations.append("Prepare liquidity options for treasury authority review; do not release or prioritize payments autonomously.")
        if revenue_shortfall > 0:
            recommendations.append("Validate the revenue variance and prepare an updated forecast with cited evidence.")
        if not recommendations:
            recommendations.append("Present the reconciled analytical record to the accountable human reviewer.")

        calculations: dict[str, float | str | None] = {
            "revised_budget": round(revised_budget, 2),
            "available_budget": round(available_budget, 2),
            "budget_variance": round(budget_variance, 2),
            "revenue_shortfall": round(revenue_shortfall, 2),
            "closing_cash": round(closing_cash, 2),
            "cash_buffer_gap": round(cash_buffer_gap, 2),
            "kpi_status": kpi_status,
            "control_result": control_result,
            "residual_risk_score": round(residual_risk_score, 2),
            "residual_risk_band": residual_risk_band,
        }
        facts = {
            "reporting_period": item.reporting_period, "currency": item.currency,
            "division_id": item.division_id, "cost_center": item.cost_center,
            "account_code": item.account_code, "source_record_id": item.source_record_id,
            "source_system": item.source_system, "action_type": item.action_type,
            "proposed_action_amount": item.proposed_action_amount,
            "maximum_authority_amount": item.maximum_authority_amount,
        }
        created_at = utc_now()
        digest = hashlib.sha256(
            json.dumps({"facts": facts, "calculations": calculations}, sort_keys=True).encode("utf-8")
        ).hexdigest()
        audit = {
            "event_id": str(uuid.uuid4()), "case_id": item.case_id,
            "source_record_id": item.source_record_id, "calculation_digest": digest,
            "validation_issues": sorted(set(issues)), "reconciliation_issues": reconciliation_issues,
            "human_approval_reference": item.human_approval_reference,
            "config_version": self.config["config_version"], "recorded_at": created_at,
        }
        return FiscalInsightResult(
            insight_id=str(uuid.uuid4()), case_id=item.case_id,
            validation_status="Valid" if not issues else "Invalid",
            validation_issues=sorted(set(issues)),
            reconciliation_status="Reconciled" if not reconciliation_issues else "Mismatch",
            facts=facts, calculations=calculations, risks=risks, assumptions=item.assumptions,
            recommendations=recommendations, evidence_references=item.evidence_references,
            confidence="High" if not issues else "Low", authority_status=authority_status,
            decision_status=decision_status, audit_record=audit, created_at=created_at,
        )

    def dataset_readiness(self, loaded_domains: list[str]) -> dict[str, Any]:
        order = self.config["load_order"]
        loaded = list(dict.fromkeys(loaded_domains))
        missing = [domain for domain in order if domain not in loaded]
        sequence_valid = [domain for domain in order if domain in loaded] == loaded
        prerequisites_valid = not loaded or loaded[:2] == order[:2]
        return {
            "loaded_domains": loaded, "missing_domains": missing,
            "sequence_valid": sequence_valid and prerequisites_valid,
            "ready_for_analysis": not missing and sequence_valid and prerequisites_valid,
            "required_order": order,
        }
