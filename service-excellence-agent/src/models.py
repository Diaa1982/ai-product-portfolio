from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class KPIDefinition:
    name: str
    formula: str
    unit: str
    source: str
    owner: str
    direction: str
    target: Optional[float] = None

@dataclass
class CorrectiveAction:
    action_id: str
    problem: str
    action: str
    owner: str
    due_date: str
    closure_criteria: str
    status: str = "open"
    evidence_refs: List[str] = field(default_factory=list)
