from pathlib import Path

from enterprise_ai.governance import GovernanceEngine
from enterprise_ai.rag import EnterpriseRAG
from enterprise_ai.schemas import UseCaseRequest
from enterprise_ai.tools import EnterpriseToolRegistry


def test_governance_requires_approval_for_sensitive_scope():
    request = UseCaseRequest(
        title="Employee decision agent",
        challenge="Automated decision using employee personal data",
    )
    decision = GovernanceEngine().assess(request)
    assert decision.approval_required
    assert decision.risk_score >= 70


def test_rag_offline_retrieval(tmp_path: Path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "policy.md").write_text(
        "High-impact AI decisions require human oversight and audit logs.",
        encoding="utf-8",
    )
    rag = EnterpriseRAG(knowledge, tmp_path / "vectors")
    rag._try_build_chroma = lambda: None
    rag.ingest()
    results = rag.search("human oversight", k=1)
    assert results
    assert "human oversight" in results[0].content


def test_value_estimation(tmp_path: Path):
    rag = EnterpriseRAG(tmp_path, tmp_path / "vectors")
    tools = EnterpriseToolRegistry(rag, tmp_path / "execution.jsonl")
    result = tools.estimate_value(1200, 15, 200)
    assert result["annual_hours_released"] == 300
    assert result["indicative_annual_value"] == 60000

