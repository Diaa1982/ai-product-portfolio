from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal
import uuid

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Product Growth Agent",
    version="1.0.0",
    description="Control plane and contract surface for an enterprise Product Growth Agent.",
)


class GrowthTask(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    objective: str
    business_context: Dict[str, Any] = Field(default_factory=dict)
    time_horizon: Optional[str] = None
    population: Optional[str] = None
    constraints: Dict[str, Any] = Field(default_factory=dict)
    available_sources: List[str] = Field(default_factory=list)
    requested_output: Optional[str] = None
    approval_context: Dict[str, Any] = Field(default_factory=dict)


class A2AMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None
    from_agent: str
    to_agent: str
    type: Literal["request", "response", "event", "approval_request", "approval_response"]
    objective: str
    priority: Literal["low", "normal", "high", "critical"] = "normal"
    context: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    payload: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Optional[Dict[str, Any]] = None
    evidence_refs: List[str] = Field(default_factory=list)
    timestamp: Optional[str] = None


class ExperimentProposal(BaseModel):
    name: str
    hypothesis: str
    primary_metric: str
    guardrail_metrics: List[str]
    population: str
    control: str
    treatment: str
    randomization_unit: str
    exposure_definition: str
    minimum_detectable_effect: Optional[float] = None
    duration_assumption: Optional[str] = None
    exclusion_criteria: List[str] = Field(default_factory=list)
    stopping_rule: str
    decision_rule: str
    implementation_owner: str
    rollback_plan: str


HIGH_IMPACT_ACTIONS = {
    "launch_production_experiment",
    "stop_production_experiment",
    "send_customer_communication",
    "change_paid_media_budget",
    "launch_paid_media_campaign",
    "change_pricing",
    "change_discount",
    "change_packaging_or_entitlement",
    "modify_billing",
    "export_identifiable_customer_data",
}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "agent": "product-growth-agent",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/v1/tasks")
def submit_task(task: GrowthTask):
    missing = []
    if not task.available_sources:
        missing.append("No analytical data source declared.")

    return {
        "task_id": task.task_id,
        "status": "needs_data" if missing else "ready_for_agent_runtime",
        "decision_frame": {
            "objective": task.objective,
            "population": task.population,
            "time_horizon": task.time_horizon,
            "constraints": task.constraints,
        },
        "mandatory_cycle": [
            "define",
            "verify_data",
            "baseline",
            "diagnose",
            "segment",
            "form_hypotheses",
            "prioritize",
            "design",
            "control",
            "orchestrate",
            "measure",
            "learn",
            "scale_iterate_stop",
        ],
        "missing_inputs": missing,
        "next_component": "model_runtime_and_tool_router",
    }


@app.post("/v1/a2a/messages")
def receive_a2a(message: A2AMessage):
    return {
        "accepted": True,
        "message_id": message.message_id,
        "correlation_id": message.correlation_id,
        "to_agent": message.to_agent,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/v1/experiments/propose")
def propose_experiment(proposal: ExperimentProposal):
    checks = {
        "has_primary_metric": bool(proposal.primary_metric),
        "has_guardrails": len(proposal.guardrail_metrics) > 0,
        "has_stopping_rule": bool(proposal.stopping_rule),
        "has_decision_rule": bool(proposal.decision_rule),
        "has_rollback_plan": bool(proposal.rollback_plan),
    }
    return {
        "proposal": proposal.model_dump(),
        "governance_checks": checks,
        "ready_for_registration": all(checks.values()),
        "launch_requires_approval": True,
    }


@app.post("/v1/actions/{action_name}/control")
def control_action(action_name: str):
    approval_required = action_name in HIGH_IMPACT_ACTIONS
    return {
        "action": action_name,
        "approval_required": approval_required,
        "policy": "human_in_the_loop" if approval_required else "autonomous_with_audit",
    }
