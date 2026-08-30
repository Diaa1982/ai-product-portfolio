from __future__ import annotations

from dataclasses import asdict

from fastmcp import FastMCP

from enterprise_ai.config import get_settings
from enterprise_ai.governance import GovernanceEngine
from enterprise_ai.rag import EnterpriseRAG
from enterprise_ai.schemas import UseCaseRequest
from enterprise_ai.tools import EnterpriseToolRegistry


settings = get_settings()
rag = EnterpriseRAG(settings.knowledge_dir, settings.vector_dir)
registry = EnterpriseToolRegistry(rag, settings.execution_log)
governance = GovernanceEngine()
mcp = FastMCP("Enterprise-Agentic-AI")


@mcp.resource("enterprise://operating-principles")
def operating_principles() -> str:
    path = settings.knowledge_dir / "enterprise_ai_principles.md"
    return path.read_text(encoding="utf-8")


@mcp.tool()
def search_enterprise_knowledge(query: str, k: int = 5) -> dict:
    """Retrieve evidence from approved enterprise knowledge sources."""
    return registry.search_knowledge(query, k)


@mcp.tool()
def assess_enterprise_use_case(request: dict) -> dict:
    """Assess completeness and governance risk of an enterprise AI use case."""
    item = UseCaseRequest(**request)
    return {
        "completeness": registry.assess_use_case(request),
        "governance": asdict(governance.assess(item, settings.high_risk_threshold)),
    }


@mcp.tool()
def estimate_enterprise_value(
    annual_volume: float, minutes_saved: float, hourly_cost: float
) -> dict:
    """Estimate annual capacity released and indicative financial value."""
    return registry.estimate_value(annual_volume, minutes_saved, hourly_cost)


@mcp.tool()
def create_enterprise_action_plan(title: str, owner: str = "TBD") -> dict:
    """Create a gated enterprise AI implementation plan."""
    return registry.call("create_action_plan", title=title, owner=owner)


if __name__ == "__main__":
    mcp.run()
