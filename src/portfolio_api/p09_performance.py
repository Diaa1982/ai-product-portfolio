from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class KPIReviewInput:
    kpi_master: dict[str, Any]
    result: dict[str, Any]
    source_row_hash: str
    data_cutoff: str
    prior_actual: float | None
    owner_explanation: str
    inference: str
    recommendation: str
    corrective_actions: list[dict[str, Any]]
    target_treatment: str
    proposed_target: float | None
    review_due_at: str
    submitted_at: str
    executive_briefing: bool = False


@dataclass
class KPIReviewResult:
    review_id: str
    kpi_id: str
    data_quality_status: str
    data_issues: list[str]
    performance_score: float | None
    performance_status: str
    variance: float | None
    trend: str
    review_calendar_status: str
    fact: str
    calculation: str
    owner_explanation: str
    inference: str
    recommendation: str
    corrective_actions: list[dict[str, Any]]
    target_treatment: str
    proposed_target_status: str
    approval_required: bool
    required_approver_role: str
    source_reference: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CorporatePerformanceReview:
    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self._validate_config()

    def _validate_config(self) -> None:
        bands = self.config["default_status_thresholds"]
        if not bands["exceeded"] > bands["achieved"] > bands["attention"]:
            raise ValueError("Default thresholds must descend")

    def validate(self, item: KPIReviewInput) -> list[str]:
        issues: list[str] = []
        for field in self.config["required_master_fields"]:
            if item.kpi_master.get(field) in (None, ""):
                issues.append(f"missing_master:{field}")
        for field in self.config["required_result_fields"]:
            if item.result.get(field) in (None, ""):
                issues.append(f"missing_result:{field}")
        if item.kpi_master.get("Direction") not in self.config["directions"]:
            issues.append("invalid_direction")
        if item.kpi_master.get("Frequency") not in self.config["frequencies"]:
            issues.append("invalid_frequency")
        if item.kpi_master.get("Aggregation_Method") not in self.config["aggregation_methods"]:
            issues.append("invalid_aggregation_method")
        if item.result.get("Data_Status") == "Official":
            if not item.result.get("Evidence_Reference"):
                issues.append("official_result_missing_evidence")
            if not item.result.get("Approval_Date"):
                issues.append("official_result_missing_approval_date")
        if len(item.source_row_hash) != 64 or any(c not in "0123456789abcdef" for c in item.source_row_hash.lower()):
            issues.append("invalid_source_row_hash")
        if not item.data_cutoff:
            issues.append("missing_data_cutoff")
        for i, action in enumerate(item.corrective_actions):
            for field in ("action", "owner_role", "due_date", "priority", "completion_measure"):
                if not action.get(field):
                    issues.append(f"corrective_action_{i}_missing:{field}")
        return sorted(set(issues))

    def calculate(self, master: dict[str, Any], result: dict[str, Any]) -> tuple[float | None, str, float | None, str]:
        target = float(result["Target"])
        actual = float(result["Actual"])
        direction = master["Direction"]
        tolerance = float(master.get("Tolerance") or 0)
        variance = round(actual - target, 4)
        special = direction in {"Range", "Milestone", "Binary"} or target <= 0 or actual < 0
        if direction == "Exact":
            score = 100.0 if abs(actual - target) <= tolerance else max(0.0, round((1 - abs(actual-target)/max(abs(target),1))*100, 2))
        elif special:
            return None, "Specialized Review", variance, "specialized_rule_required"
        elif direction == "Higher":
            score = round(actual / target * 100, 2)
        elif direction == "Lower":
            if actual == 0:
                score = 105.0
            else:
                score = round(target / actual * 100, 2)
        else:
            raise ValueError("Unsupported direction")

        approved = master.get("Approved_Thresholds")
        thresholds = approved or self.config["default_status_thresholds"]
        if score >= float(thresholds["exceeded"]):
            status = "Exceeded"
        elif score >= float(thresholds["achieved"]):
            status = "Achieved"
        elif score >= float(thresholds["attention"]):
            status = "Attention"
        else:
            status = "Off Target"
        return score, status, variance, "calculated"

    @staticmethod
    def _calendar_status(due_at: str, submitted_at: str) -> str:
        due = datetime.fromisoformat(due_at.replace("Z", "+00:00"))
        submitted = datetime.fromisoformat(submitted_at.replace("Z", "+00:00"))
        return "On Time" if submitted <= due else "Late"

    def review(self, item: KPIReviewInput) -> KPIReviewResult:
        issues = self.validate(item)
        score, status, variance, calculation_state = self.calculate(item.kpi_master, item.result)
        actual = float(item.result["Actual"])
        if item.prior_actual is None:
            trend = "No Prior Period"
        elif actual > item.prior_actual:
            trend = "Increasing"
        elif actual < item.prior_actual:
            trend = "Decreasing"
        else:
            trend = "Stable"
        fact = f"{item.kpi_master['KPI_Name']} actual is {actual} against target {item.result['Target']} for {item.result['Period']}."
        calculation = f"Direction={item.kpi_master['Direction']}; variance={variance}; score={score}; method={calculation_state}."
        approval_required = item.executive_briefing or item.target_treatment != "Retain" or bool(item.corrective_actions)
        return KPIReviewResult(
            review_id=str(uuid.uuid4()), kpi_id=str(item.kpi_master["KPI_ID"]),
            data_quality_status="Valid" if not issues else "Invalid",
            data_issues=issues, performance_score=score,
            performance_status="Data Invalid" if issues else status,
            variance=variance, trend=trend,
            review_calendar_status=self._calendar_status(item.review_due_at, item.submitted_at),
            fact=fact, calculation=calculation, owner_explanation=item.owner_explanation,
            inference=item.inference, recommendation=item.recommendation,
            corrective_actions=item.corrective_actions,
            target_treatment=item.target_treatment,
            proposed_target_status="NOT APPROVED" if item.proposed_target is not None else "Not Proposed",
            approval_required=approval_required,
            required_approver_role="EXECUTIVE_APPROVER" if item.executive_briefing else "PERFORMANCE_OWNER",
            source_reference={"source_row_hash":item.source_row_hash,"data_cutoff":item.data_cutoff,
                              "evidence_reference":item.result.get("Evidence_Reference"),
                              "data_source":item.kpi_master.get("Data_Source"),
                              "period":item.result.get("Period")},
            created_at=utc_now(),
        )

    @staticmethod
    def approve(review_id: str, action: str, approver_role: str, decision: str, reason: str) -> dict[str, Any]:
        roles={"performance_review":"PERFORMANCE_OWNER","executive_briefing":"EXECUTIVE_APPROVER","target_change":"EXECUTIVE_APPROVER","corrective_action":"PERFORMANCE_OWNER"}
        if action not in roles: raise ValueError("Unsupported approval action")
        if approver_role != roles[action]: raise PermissionError("Approver role is not authorized")
        if decision not in {"approved","rejected","returned"}: raise ValueError("Invalid decision")
        if not review_id.strip() or len(reason.strip())<3: raise ValueError("Review ID and reason are required")
        return {"decision_id":str(uuid.uuid4()),"review_id":review_id,"action":action,
                "approver_role":approver_role,"decision":decision,"reason":reason,"decided_at":utc_now()}
