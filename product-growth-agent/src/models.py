"""Shared domain objects for the Product Growth Agent."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MetricDefinition:
    name: str
    business_definition: str
    formula: str
    grain: str
    source: str
    owner: str
    guardrail: bool = False


@dataclass
class GrowthOpportunity:
    name: str
    funnel_stage: str
    target_segment: str
    evidence: List[str]
    expected_impact: Optional[float] = None
    confidence: float = 0.0
    effort: float = 0.0
    strategic_fit: float = 0.0
    reversibility: float = 0.0


@dataclass
class ValidatedLearning:
    statement: str
    status: str  # validated | rejected | inconclusive
    evidence_refs: List[str] = field(default_factory=list)
    scope: Dict[str, Any] = field(default_factory=dict)
