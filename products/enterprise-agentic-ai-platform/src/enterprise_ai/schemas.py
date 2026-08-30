from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal


RiskLevel = Literal["low", "medium", "high", "critical"]


@dataclass
class Evidence:
    source: str
    content: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class UseCaseRequest:
    title: str
    challenge: str
    objective: str = ""
    business_area: str = "enterprise"
    use_case_type: str = "ai_transformation"
    users: list[str] = field(default_factory=list)
    data_sources: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    image_paths: list[str] = field(default_factory=list)
    expected_outcomes: list[str] = field(default_factory=list)
    authorized_to_execute: bool = False


@dataclass
class AgentFinding:
    agent: str
    summary: str
    recommendations: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class GovernanceDecision:
    risk_score: int
    risk_level: RiskLevel
    approval_required: bool
    approved: bool
    reasons: list[str] = field(default_factory=list)
    controls: list[str] = field(default_factory=list)


@dataclass
class WorkflowResult:
    request_id: str
    status: str
    executive_summary: str
    findings: list[AgentFinding]
    action_plan: list[dict[str, Any]]
    governance: GovernanceDecision
    citations: list[str] = field(default_factory=list)
    execution_receipts: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

