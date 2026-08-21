from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LIFECYCLE = ["discover", "evaluate", "prioritize", "approve", "develop", "deploy", "operate", "retire"]
FINAL_APPROVAL_ACTIONS = {
    "proposal",
    "final_client_output",
    "strategic_recommendation",
    "high_risk_recommendation",
    "service_rule_change",
    "pricing_rule_change",
    "unresolved_escalation",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AssessmentInput:
    title: str
    assessment_mode: str
    business_problem: str
    desired_outcome: str
    business_owner: str
    process_trigger: str
    process_closure: str
    ai_task: str
    success_criteria: list[str]
    prohibited_automated_decisions: list[str]
    low_confidence_behavior: str
    data_sources: list[dict[str, Any]]
    evidence_references: list[str]
    value_scores: dict[str, float]
    feasibility_scores: dict[str, float]
    risk_scores: dict[str, float]
    assumptions: list[str] = field(default_factory=list)


@dataclass
class AssessmentResult:
    assessment_id: str
    lifecycle_stage: str
    completeness_status: str
    missing_information: list[str]
    value_score: float
    feasibility_score: float
    priority_score: float
    risk_score: float
    risk_tier: str
    portfolio_classification: str
    recommendation: str
    required_gate: str
    required_approver_role: str
    evidence_references: list[str]
    assumptions: list[str]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class UseCaseAssessor:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self._validate_config()

    def _validate_config(self) -> None:
        weights = self.config["dimension_weights"]
        if round(weights["value"] + weights["feasibility"], 8) != 1.0:
            raise ValueError("Value and feasibility weights must total 1.0")
        for section in ("value_criteria", "feasibility_criteria", "risk_criteria"):
            total = sum(item["weight"] for item in self.config[section])
            if round(total, 8) != 1.0:
                raise ValueError(f"{section} weights must total 1.0")

    @staticmethod
    def _weighted(criteria: list[dict[str, Any]], scores: dict[str, float]) -> float:
        total = 0.0
        for criterion in criteria:
            score = float(scores.get(criterion["id"], 0))
            if not 0 <= score <= 5:
                raise ValueError(f"Score {criterion['id']} must be between 0 and 5")
            total += score * criterion["weight"]
        return round(total, 4)

    def required_information(self, intake: AssessmentInput) -> list[str]:
        missing: list[str] = []
        fields = {
            "title": intake.title,
            "assessment_mode": intake.assessment_mode,
            "business_problem": intake.business_problem,
            "desired_outcome": intake.desired_outcome,
            "business_owner": intake.business_owner,
            "process_trigger": intake.process_trigger,
            "process_closure": intake.process_closure,
            "ai_task": intake.ai_task,
            "success_criteria": intake.success_criteria,
            "prohibited_automated_decisions": intake.prohibited_automated_decisions,
            "low_confidence_behavior": intake.low_confidence_behavior,
            "data_sources": intake.data_sources,
            "evidence_references": intake.evidence_references,
        }
        for name, value in fields.items():
            if value in (None, "", []):
                missing.append(name)
        if intake.assessment_mode not in self.config["supported_modes"]:
            missing.append("valid_assessment_mode")
        allowed_classes = {"Public", "Internal", "Confidential", "Restricted"}
        for source in intake.data_sources:
            for required in ("name", "owner", "classification", "quality_status"):
                if not source.get(required):
                    missing.append(f"data_sources.{required}")
            if source.get("classification") not in allowed_classes:
                missing.append("data_sources.valid_classification")
        for config_key, scores in (
            ("value_criteria", intake.value_scores),
            ("feasibility_criteria", intake.feasibility_scores),
            ("risk_criteria", intake.risk_scores),
        ):
            for criterion in self.config[config_key]:
                if criterion["id"] not in scores:
                    missing.append(f"scores.{criterion['id']}")
        return sorted(set(missing))

    @staticmethod
    def portfolio_class(value: float, feasibility: float, threshold: float) -> str:
        high_value = value >= threshold
        high_feasibility = feasibility >= threshold
        if high_value and high_feasibility:
            return "Quick Win"
        if high_value and not high_feasibility:
            return "Strategic Bet"
        if not high_value and high_feasibility:
            return "Fill-In"
        return "Question Mark"

    def assess(self, intake: AssessmentInput) -> AssessmentResult:
        missing = self.required_information(intake)
        value = self._weighted(self.config["value_criteria"], intake.value_scores)
        feasibility = self._weighted(self.config["feasibility_criteria"], intake.feasibility_scores)
        risk = self._weighted(self.config["risk_criteria"], intake.risk_scores)
        weights = self.config["dimension_weights"]
        priority = round(value * weights["value"] + feasibility * weights["feasibility"], 4)
        classification = self.portfolio_class(value, feasibility, self.config["portfolio_threshold"])

        if risk >= self.config["risk_thresholds"]["high"]:
            tier = "high"
        elif risk >= self.config["risk_thresholds"]["medium"]:
            tier = "medium"
        else:
            tier = "low"

        if missing:
            recommendation = "Insufficient information — return to discovery and obtain missing evidence."
            gate, stage = "DISCOVERY_COMPLETENESS", "discover"
        elif tier == "high":
            recommendation = "Proceed only to independent risk review and CEO decision; do not automate consequential decisions."
            gate, stage = "HIGH_RISK_RECOMMENDATION", "evaluate"
        elif priority >= self.config["decision_thresholds"]["prioritize"]:
            recommendation = "Prioritize for business case and controlled pilot design."
            gate, stage = "PRIORITIZATION", "prioritize"
        else:
            recommendation = "Retain in portfolio backlog and strengthen value, feasibility or evidence."
            gate, stage = "EVALUATION", "evaluate"

        return AssessmentResult(
            assessment_id=str(uuid.uuid4()), lifecycle_stage=stage,
            completeness_status="complete" if not missing else "insufficient_information",
            missing_information=missing, value_score=value, feasibility_score=feasibility,
            priority_score=priority, risk_score=risk, risk_tier=tier,
            portfolio_classification=classification, recommendation=recommendation,
            required_gate=gate, required_approver_role=self.config["final_approver_role"],
            evidence_references=intake.evidence_references, assumptions=intake.assumptions,
            created_at=utc_now(),
        )

    @staticmethod
    def approve(assessment_id: str, action: str, approver_role: str, decision: str, reason: str) -> dict[str, Any]:
        if not assessment_id.strip():
            raise ValueError("Assessment ID is required")
        if action not in FINAL_APPROVAL_ACTIONS:
            raise ValueError("Unsupported final-approval action")
        if approver_role != "CEO":
            raise PermissionError("Final approval requires CEO role")
        if decision not in {"approved", "rejected", "returned"}:
            raise ValueError("Invalid decision")
        if len(reason.strip()) < 3:
            raise ValueError("Decision reason is required")
        return {"approval_id": str(uuid.uuid4()), "assessment_id": assessment_id, "action": action,
                "approver_role": approver_role, "decision": decision, "reason": reason, "decided_at": utc_now()}
