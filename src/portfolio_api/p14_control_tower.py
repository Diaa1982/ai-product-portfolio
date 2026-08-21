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
class UseCaseProfile:
    use_case_id: str
    title: str
    purpose: str
    owner_role: str
    data_owner_role: str
    data_classification: str
    external_autonomous_action: bool
    consequential_decision: bool
    prohibited_financial_action: bool
    sensitive_personal_data: bool
    decision_support_at_scale: bool
    public_facing: bool
    human_reviewed_output: bool
    agentic_autonomy_level: int
    evidence_references: list[str]


@dataclass
class RiskResult:
    assessment_id: str
    risk_tier: str
    deployment_blocked: bool
    reasons: list[str]
    required_controls: list[str]
    required_governance_roles: list[str]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GateResult:
    gate: str
    gate_name: str
    status: str
    missing_controls: list[str]
    missing_conditions: list[str]
    required_approver_roles: list[str]
    autonomous_approval_permitted: bool
    next_gate: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AIGovernanceControlTower:
    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self._validate_config()

    def _validate_config(self) -> None:
        if list(self.config["gates"]) != ["G0", "G1", "G2", "G3", "G4"]:
            raise ValueError("Gates must be configured in G0-G4 order")
        if self.config["final_production_approver_role"] != "CEO":
            raise ValueError("Final production approval must remain human CEO")

    def classify_risk(self, profile: UseCaseProfile) -> RiskResult:
        if profile.data_classification not in {"Public", "Internal", "Confidential", "Restricted"}:
            raise ValueError("Unsupported data classification")
        if not 0 <= profile.agentic_autonomy_level <= 4:
            raise ValueError("Agentic autonomy level must be 0-4")
        reasons: list[str] = []
        blocked = profile.prohibited_financial_action
        if blocked:
            reasons.append("autonomous_financial_action_prohibited")
        if profile.external_autonomous_action:
            reasons.append("external_autonomous_action")
        if profile.consequential_decision:
            reasons.append("consequential_decision")
        if profile.agentic_autonomy_level >= 4:
            reasons.append("maximum_agentic_autonomy")

        if blocked or profile.external_autonomous_action or profile.consequential_decision or profile.agentic_autonomy_level >= 4:
            tier = "Critical"
        elif profile.decision_support_at_scale or profile.sensitive_personal_data or profile.data_classification == "Restricted" or profile.agentic_autonomy_level == 3:
            tier = "High"
            reasons.append("scaled_or_sensitive_decision_support")
        elif profile.human_reviewed_output or profile.public_facing or profile.data_classification == "Confidential" or profile.agentic_autonomy_level == 2:
            tier = "Moderate"
            reasons.append("assisted_human_reviewed_output")
        else:
            tier = "Low"
            reasons.append("internal_productivity_low_autonomy")

        controls: list[str] = []
        for level in self.config["risk_tier_order"][: self.config["risk_tier_order"].index(tier) + 1]:
            controls.extend(self.config["controls_by_tier"][level])
        roles = list(self.config["roles_by_tier"][tier])
        return RiskResult(str(uuid.uuid4()), tier, blocked, sorted(set(reasons)),
                          list(dict.fromkeys(controls)), roles, utc_now())

    def evaluate_gate(self, profile: UseCaseProfile, gate: str, control_evidence: dict[str, str],
                      prior_approvals: list[str], qa_passed: bool,
                      independent_testing_passed: bool) -> GateResult:
        if gate not in self.config["gates"]:
            raise ValueError("Unknown governance gate")
        risk = self.classify_risk(profile)
        gate_cfg = self.config["gates"][gate]
        required_controls = list(gate_cfg["required_controls"])
        if risk.risk_tier in {"High", "Critical"}:
            required_controls += gate_cfg.get("high_impact_controls", [])
        missing_controls = sorted({c for c in required_controls if not control_evidence.get(c)})
        missing_conditions: list[str] = []
        if risk.deployment_blocked:
            missing_conditions.append("prohibited_financial_action_must_be_removed")
        if gate in {"G3", "G4"} and not qa_passed:
            missing_conditions.append("mandatory_qa_not_passed")
        if gate in {"G3", "G4"} and risk.risk_tier in {"High", "Critical"} and not independent_testing_passed:
            missing_conditions.append("independent_testing_not_passed")
        required_roles = list(gate_cfg["required_approver_roles"])
        if gate == "G4":
            required_prior = set(self.config["required_prior_approvals_by_risk"][risk.risk_tier])
            absent = sorted(required_prior - set(prior_approvals))
            missing_conditions.extend(f"missing_prior_approval:{role}" for role in absent)
        status = "ready_for_human_decision" if not missing_controls and not missing_conditions else "blocked"
        gates = list(self.config["gates"])
        next_gate = gates[gates.index(gate) + 1] if gate != "G4" else None
        return GateResult(gate, gate_cfg["name"], status, missing_controls,
                          missing_conditions, required_roles, False, next_gate)

    def approve_gate(self, use_case_id: str, gate: str, approver_role: str,
                     decision: str, reason: str, gate_status: str) -> dict[str, Any]:
        if gate not in self.config["gates"]:
            raise ValueError("Unknown governance gate")
        if gate_status != "ready_for_human_decision":
            raise PermissionError("Blocked gate cannot be approved")
        allowed = self.config["gates"][gate]["required_approver_roles"]
        if approver_role not in allowed:
            raise PermissionError("Approver role is not authorized for this gate")
        if approver_role.startswith("AGENT"):
            raise PermissionError("Agents cannot approve governance gates")
        if gate == "G4" and approver_role != "CEO":
            raise PermissionError("G4 production authorization requires CEO")
        if decision not in {"approved", "rejected", "returned"}:
            raise ValueError("Invalid decision")
        if not use_case_id.strip() or len(reason.strip()) < 3:
            raise ValueError("Use case ID and reason are required")
        return {"decision_id": str(uuid.uuid4()), "use_case_id": use_case_id,
                "gate": gate, "approver_role": approver_role, "decision": decision,
                "reason": reason, "decided_at": utc_now()}

    def monitor(self, use_case_id: str, metrics: dict[str, Any]) -> dict[str, Any]:
        critical_flags = ["security_breach", "privacy_breach", "unauthorized_action",
                          "financial_control_breach", "audit_log_failure"]
        high_flags = ["fairness_threshold_breach", "explainability_failure", "performance_breach"]
        critical = [name for name in critical_flags if metrics.get(name) is True]
        high = [name for name in high_flags if metrics.get(name) is True]
        drift = float(metrics.get("drift_score", 0))
        if not 0 <= drift <= 1:
            raise ValueError("Drift score must be 0-1")
        if drift >= self.config["monitoring_thresholds"]["critical_drift"]:
            critical.append("critical_drift")
        elif drift >= self.config["monitoring_thresholds"]["high_drift"]:
            high.append("high_drift")
        if critical:
            severity, action = "Critical", "safe_shutdown_and_incident_command"
        elif high:
            severity, action = "High", "pause_and_human_review"
        else:
            severity, action = "Low", "continue_monitoring"
        return {"incident_id": str(uuid.uuid4()), "use_case_id": use_case_id,
                "severity": severity, "triggered_controls": critical + high,
                "required_action": action, "pause_required": severity in {"Critical", "High"},
                "human_incident_owner_required": severity in {"Critical", "High"},
                "created_at": utc_now()}
