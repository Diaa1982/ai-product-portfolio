from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .audit import append_event
from .rag import EnterpriseRAG
from .schemas import UseCaseRequest


ToolFunction = Callable[..., dict[str, Any]]


class EnterpriseToolRegistry:
    def __init__(self, rag: EnterpriseRAG, execution_log: Path):
        self.rag = rag
        self.execution_log = execution_log
        self._tools: dict[str, ToolFunction] = {
            "search_knowledge": self.search_knowledge,
            "assess_use_case": self.assess_use_case,
            "estimate_value": self.estimate_value,
            "create_action_plan": self.create_action_plan,
        }

    def names(self) -> list[str]:
        return sorted(self._tools)

    def call(self, name: str, **arguments: Any) -> dict[str, Any]:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        append_event(self.execution_log, "tool_call", {"tool": name, "arguments": arguments})
        result = self._tools[name](**arguments)
        append_event(self.execution_log, "tool_result", {"tool": name, "result": result})
        return result

    def search_knowledge(self, query: str, k: int = 5) -> dict[str, Any]:
        return {"query": query, "results": [asdict(e) for e in self.rag.search(query, k)]}

    @staticmethod
    def assess_use_case(request: dict[str, Any]) -> dict[str, Any]:
        item = UseCaseRequest(**request)
        completeness = sum(
            bool(value)
            for value in [item.challenge, item.objective, item.users, item.data_sources, item.expected_outcomes]
        ) / 5
        return {
            "completeness": round(completeness, 2),
            "ready_for_design": completeness >= 0.8,
            "missing": [
                name
                for name, value in {
                    "objective": item.objective,
                    "users": item.users,
                    "data_sources": item.data_sources,
                    "expected_outcomes": item.expected_outcomes,
                }.items()
                if not value
            ],
        }

    @staticmethod
    def estimate_value(annual_volume: float, minutes_saved: float, hourly_cost: float) -> dict[str, Any]:
        hours = annual_volume * minutes_saved / 60
        return {
            "annual_hours_released": round(hours, 2),
            "indicative_annual_value": round(hours * hourly_cost, 2),
            "assumptions": {
                "annual_volume": annual_volume,
                "minutes_saved": minutes_saved,
                "hourly_cost": hourly_cost,
            },
        }

    @staticmethod
    def create_action_plan(title: str, owner: str = "TBD") -> dict[str, Any]:
        phases = ["Discover", "Assess", "Design", "Approve", "Pilot", "Scale", "Monitor"]
        return {
            "title": title,
            "owner": owner,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "phases": [
                {"phase": phase, "status": "pending", "decision_gate": index in {1, 3, 4}}
                for index, phase in enumerate(phases)
            ],
        }

