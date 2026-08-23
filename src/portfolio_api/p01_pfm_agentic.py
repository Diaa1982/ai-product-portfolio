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
class PFMCaseInput:
    case_id: str
    workflow_type: str
    current_agent: str
    next_agent: str
    business_outcome: str
    payload: dict[str, Any]
    success_criteria: list[str]
    evidence_references: list[str]
    assumptions: list[str]
    approved_budget: float
    revised_budget: float
    period_plan: float
    actuals: float
    commitments: float
    cash_available: float
    obligations_due: float
    due_date: str
    validation_passed: bool
    high_risk: bool = False
    human_approval_reference: str | None = None


@dataclass
class PFMAnalysisResult:
    analysis_id: str
    case_id: str
    workflow_type: str
    current_agent: str
    next_agent: str
    available_balance: float
    utilization_percent: float | None
    commitment_pressure_percent: float | None
    variance_percent: float | None
    liquidity_gap: float
    alerts: list[str]
    risk_rating: str
    validation_status: str
    validation_issues: list[str]
    handoff_status: str
    approval_interruption: bool
    escalation_route: str | None
    failure_route: str | None
    recommendation: str
    evidence_references: list[str]
    assumptions: list[str]
    audit_event: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PFMAgenticOrchestrator:
    """Decision-support orchestration for PFM analysis; never a financial authority."""

    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self._validate_config()
        self.agents = {agent["agent_id"]: agent for agent in self.config["agents"]}

    def _validate_config(self) -> None:
        agents = self.config.get("agents", [])
        if len(agents) != 9:
            raise ValueError("PFM design baseline must define exactly nine functional agents")
        ids = [agent["agent_id"] for agent in agents]
        if len(set(ids)) != len(ids):
            raise ValueError("Agent IDs must be unique")
        for agent in agents:
            unknown = set(agent["allowed_next_agents"]) - set(ids)
            if unknown:
                raise ValueError(f"Unknown next agents for {agent['agent_id']}: {sorted(unknown)}")

    def validate(self, item: PFMCaseInput) -> list[str]:
        issues: list[str] = []
        if item.workflow_type not in self.config["workflow_types"]:
            issues.append("unsupported_workflow_type")
        if item.current_agent not in self.agents:
            issues.append("unknown_current_agent")
        if item.next_agent not in self.agents:
            issues.append("unknown_next_agent")
        if item.current_agent in self.agents and item.next_agent in self.agents:
            allowed = self.agents[item.current_agent]["allowed_next_agents"]
            if item.next_agent not in allowed:
                issues.append("invalid_agent_transition")
        if not item.validation_passed:
            issues.append("source_validation_failed")
        if not item.evidence_references:
            issues.append("missing_evidence_references")
        if not item.success_criteria:
            issues.append("missing_success_criteria")
        if not item.business_outcome.strip():
            issues.append("missing_business_outcome")
        if not item.payload:
            issues.append("missing_handoff_payload")
        for name in (
            "approved_budget", "revised_budget", "period_plan", "actuals",
            "commitments", "cash_available", "obligations_due",
        ):
            if getattr(item, name) < 0:
                issues.append(f"negative_input:{name}")
        if not item.due_date:
            issues.append("missing_due_date")
        return sorted(set(issues))

    def calculate(self, item: PFMCaseInput) -> dict[str, float | None]:
        available_balance = item.revised_budget - item.actuals - item.commitments
        utilization = item.actuals / item.revised_budget if item.revised_budget else None
        commitment_pressure = item.commitments / item.revised_budget if item.revised_budget else None
        variance = abs(item.actuals - item.period_plan) / abs(item.period_plan) if item.period_plan else None
        return {
            "available_balance": round(available_balance, 2),
            "utilization_percent": round(utilization * 100, 2) if utilization is not None else None,
            "commitment_pressure_percent": round(commitment_pressure * 100, 2) if commitment_pressure is not None else None,
            "variance_percent": round(variance * 100, 2) if variance is not None else None,
            "liquidity_gap": round(item.cash_available - item.obligations_due, 2),
        }

    def analyze(self, item: PFMCaseInput) -> PFMAnalysisResult:
        issues = self.validate(item)
        metrics = self.calculate(item)
        thresholds = self.config["alert_thresholds"]
        alerts: list[str] = []
        if metrics["variance_percent"] is None:
            alerts.append("ZERO_PERIOD_PLAN_SPECIALIZED_REVIEW")
        elif metrics["variance_percent"] > float(thresholds["variance_percent"]):
            alerts.append("VARIANCE_ABOVE_THRESHOLD")
        if metrics["utilization_percent"] is not None and metrics["utilization_percent"] > float(thresholds["utilization_percent"]):
            alerts.append("UTILIZATION_ABOVE_THRESHOLD")
        if metrics["available_balance"] < 0:
            alerts.append("NEGATIVE_AVAILABLE_BALANCE")
        if item.actuals + item.commitments > item.revised_budget:
            alerts.append("ACTUALS_AND_COMMITMENTS_EXCEED_REVISED_BUDGET")
        if metrics["liquidity_gap"] < 0:
            alerts.append("NEGATIVE_LIQUIDITY_GAP")

        critical = {
            "NEGATIVE_AVAILABLE_BALANCE",
            "ACTUALS_AND_COMMITMENTS_EXCEED_REVISED_BUDGET",
            "NEGATIVE_LIQUIDITY_GAP",
        }
        if item.high_risk or critical.intersection(alerts):
            risk = "High"
        elif alerts:
            risk = "Medium"
        else:
            risk = "Low"

        approval_interruption = risk == "High" and not item.human_approval_reference
        if approval_interruption:
            issues.append("high_risk_human_approval_required")
        handoff = "READY" if not issues else "BLOCKED"
        recommendation = (
            "Human reviewer may authorize the documented handoff after confirming evidence, controls and delegated authority."
            if handoff == "READY"
            else "Do not start the downstream agent; resolve validation and approval issues, then re-evaluate."
        )
        event_id = str(uuid.uuid4())
        now = utc_now()
        audit_event = {
            "event_id": event_id,
            "case_id": item.case_id,
            "workflow_state": handoff,
            "input": item.payload,
            "output": {"metrics": metrics, "alerts": alerts, "risk_rating": risk},
            "success_criteria": item.success_criteria,
            "approval_interruption": approval_interruption,
            "human_approval_reference": item.human_approval_reference,
            "recorded_at": now,
        }
        return PFMAnalysisResult(
            analysis_id=event_id, case_id=item.case_id, workflow_type=item.workflow_type,
            current_agent=item.current_agent, next_agent=item.next_agent,
            available_balance=float(metrics["available_balance"]),
            utilization_percent=metrics["utilization_percent"],
            commitment_pressure_percent=metrics["commitment_pressure_percent"],
            variance_percent=metrics["variance_percent"],
            liquidity_gap=float(metrics["liquidity_gap"]), alerts=alerts,
            risk_rating=risk, validation_status="Valid" if not issues else "Invalid",
            validation_issues=sorted(set(issues)), handoff_status=handoff,
            approval_interruption=approval_interruption,
            escalation_route=self.config["escalation_route"] if risk == "High" else None,
            failure_route=self.config["failure_route"] if issues else None,
            recommendation=recommendation, evidence_references=item.evidence_references,
            assumptions=item.assumptions, audit_event=audit_event, created_at=now,
        )

    def check_action(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower()
        protected = {item.lower() for item in self.config["protected_autonomous_actions"]}
        is_protected = normalized in protected
        return {
            "action": action,
            "permitted_for_ai": not is_protected,
            "decision": "DENY_AUTONOMOUS_EXECUTION" if is_protected else "ANALYSIS_ONLY_ALLOWED",
            "human_authority_required": is_protected,
            "reason": (
                "This action is reserved for an authorized human under applicable law, policy and delegation."
                if is_protected else
                "AI may prepare analysis or a recommendation, subject to validation and human review."
            ),
        }

    def approve_handoff(self, case_id: str, approver_role: str, decision: str, reason: str) -> dict[str, Any]:
        if approver_role not in self.config["human_approval_roles"]:
            raise PermissionError("Approver role is not configured for PFM handoffs")
        if decision not in {"approved", "rejected", "returned"}:
            raise ValueError("Invalid decision")
        if not case_id.strip() or len(reason.strip()) < 3:
            raise ValueError("Case ID and reason are required")
        return {
            "approval_reference": str(uuid.uuid4()), "case_id": case_id,
            "approver_role": approver_role, "decision": decision,
            "reason": reason, "decided_at": utc_now(),
            "authority_note": "The configured role must be mapped to a valid organizational delegation before production use.",
        }
