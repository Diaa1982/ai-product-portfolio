from __future__ import annotations

import uuid
from dataclasses import asdict
from typing import Any, TypedDict

from .agents import SpecialistAgent, synthesize_findings
from .audit import append_event
from .config import Settings
from .governance import GovernanceEngine
from .llm import ModelGateway
from .multimodal import MultimodalAnalyzer
from .rag import EnterpriseRAG
from .schemas import AgentFinding, Evidence, UseCaseRequest, WorkflowResult
from .tools import EnterpriseToolRegistry


class EnterpriseState(TypedDict, total=False):
    request_id: str
    request: UseCaseRequest
    evidence: list[Evidence]
    image_findings: list[str]
    findings: list[AgentFinding]
    governance: Any
    executive_summary: str
    action_plan: list[dict[str, Any]]
    execution_receipts: list[dict[str, Any]]
    status: str


class EnterpriseLangGraphWorkflow:
    """Stateful enterprise AI transformation workflow with controlled execution."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.rag = EnterpriseRAG(settings.knowledge_dir, settings.vector_dir)
        self.gateway = ModelGateway(settings)
        self.multimodal = MultimodalAnalyzer(settings)
        self.governance_engine = GovernanceEngine()
        self.tools = EnterpriseToolRegistry(self.rag, settings.execution_log)
        self.graph = self._build()

    def _build(self):
        try:
            from langgraph.graph import END, START, StateGraph
        except ImportError as exc:
            raise RuntimeError("Install project dependencies to use LangGraph") from exc

        builder = StateGraph(EnterpriseState)
        builder.add_node("intake", self._intake)
        builder.add_node("retrieve", self._retrieve)
        builder.add_node("multimodal", self._multimodal)
        builder.add_node("specialists", self._specialists)
        builder.add_node("govern", self._govern)
        builder.add_node("synthesize", self._synthesize)
        builder.add_node("execute", self._execute)
        builder.add_node("hold", self._hold)
        builder.add_edge(START, "intake")
        builder.add_edge("intake", "retrieve")
        builder.add_edge("retrieve", "multimodal")
        builder.add_edge("multimodal", "specialists")
        builder.add_edge("specialists", "govern")
        builder.add_edge("govern", "synthesize")
        builder.add_conditional_edges(
            "synthesize",
            self._route,
            {"execute": "execute", "hold": "hold"},
        )
        builder.add_edge("execute", END)
        builder.add_edge("hold", END)
        return builder.compile()

    def _intake(self, state: EnterpriseState) -> EnterpriseState:
        request_id = state.get("request_id") or str(uuid.uuid4())
        append_event(self.settings.audit_log, "workflow_started", {"request_id": request_id})
        return {"request_id": request_id, "status": "intake_complete"}

    def _retrieve(self, state: EnterpriseState) -> EnterpriseState:
        request = state["request"]
        query = f"{request.title} {request.challenge} {request.objective}"
        return {"evidence": self.rag.search(query, k=5), "status": "evidence_retrieved"}

    def _multimodal(self, state: EnterpriseState) -> EnterpriseState:
        request = state["request"]
        findings = [
            self.multimodal.analyze(path, f"Identify enterprise-relevant facts for: {request.challenge}")
            for path in request.image_paths
        ]
        return {"image_findings": findings, "status": "multimodal_complete"}

    def _specialists(self, state: EnterpriseState) -> EnterpriseState:
        request = state["request"]
        use_cases = self.settings.load_use_cases()
        config = use_cases.get(request.use_case_type, use_cases["ai_transformation"])
        evidence = list(state.get("evidence", []))
        evidence.extend(
            Evidence(source=f"image:{i}", content=text, score=1.0)
            for i, text in enumerate(state.get("image_findings", []), start=1)
        )
        roles = [role for role in config["required_agents"] if role not in {"retrieval", "synthesizer"}]
        findings = [SpecialistAgent(role, self.gateway).analyze(request, evidence) for role in roles]
        return {"findings": findings, "status": "specialist_analysis_complete"}

    def _govern(self, state: EnterpriseState) -> EnterpriseState:
        decision = self.governance_engine.assess(
            state["request"], self.settings.high_risk_threshold
        )
        return {"governance": decision, "status": "governance_assessed"}

    def _synthesize(self, state: EnterpriseState) -> EnterpriseState:
        summary = synthesize_findings(self.gateway, state.get("findings", []))
        plan = self.tools.create_action_plan(state["request"].title)["phases"]
        return {"executive_summary": summary, "action_plan": plan, "status": "recommendation_ready"}

    @staticmethod
    def _route(state: EnterpriseState) -> str:
        request = state["request"]
        governance = state["governance"]
        return "execute" if request.authorized_to_execute and governance.approved else "hold"

    def _execute(self, state: EnterpriseState) -> EnterpriseState:
        receipt = self.tools.call(
            "create_action_plan", title=state["request"].title, owner="Approved owner"
        )
        return {"execution_receipts": [receipt], "status": "executed"}

    @staticmethod
    def _hold(state: EnterpriseState) -> EnterpriseState:
        reason = "human_approval_required" if state["governance"].approval_required else "advisory_only"
        return {"execution_receipts": [{"status": "held", "reason": reason}], "status": "held"}

    def run(self, request: UseCaseRequest) -> WorkflowResult:
        state = self.graph.invoke({"request": request})
        result = WorkflowResult(
            request_id=state["request_id"],
            status=state["status"],
            executive_summary=state["executive_summary"],
            findings=state.get("findings", []),
            action_plan=state.get("action_plan", []),
            governance=state["governance"],
            citations=sorted({e.source for f in state.get("findings", []) for e in f.evidence}),
            execution_receipts=state.get("execution_receipts", []),
        )
        append_event(self.settings.audit_log, "workflow_completed", result.to_dict())
        return result

