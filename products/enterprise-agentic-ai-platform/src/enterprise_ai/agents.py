from __future__ import annotations

import json
from dataclasses import asdict

from .llm import ModelGateway
from .schemas import AgentFinding, Evidence, UseCaseRequest


AGENT_PROMPTS = {
    "strategy": "Assess strategic alignment, operating-model impact, stakeholders, and transformation roadmap.",
    "process": "Assess process scope, bottlenecks, controls, handoffs, standardization, and automation potential.",
    "pfm": "Assess budget credibility, fiscal risk, revenue, expenditure, cash, controls, reporting, and public value.",
    "architecture": "Design data, application, integration, model, security, observability, and deployment architecture.",
    "risk": "Assess legal, privacy, security, fairness, explainability, model, operational, and vendor risks.",
    "value": "Define benefits, costs, baselines, KPIs, targets, dependencies, and value-realization controls.",
    "synthesizer": "Reconcile all findings into an executive recommendation, roadmap, and decision requests.",
}


class SpecialistAgent:
    def __init__(self, role: str, gateway: ModelGateway):
        if role not in AGENT_PROMPTS:
            raise ValueError(f"Unsupported agent role: {role}")
        self.role = role
        self.gateway = gateway

    def analyze(self, request: UseCaseRequest, evidence: list[Evidence]) -> AgentFinding:
        system = (
            f"You are the enterprise {self.role} agent. {AGENT_PROMPTS[self.role]} "
            "Use only supplied evidence. Separate facts, assumptions, and recommendations. "
            "Return JSON with summary, recommendations, risks, and confidence."
        )
        user = json.dumps(
            {
                "request": asdict(request),
                "evidence": [asdict(item) for item in evidence],
            },
            ensure_ascii=False,
            default=str,
        )
        data = self.gateway.invoke_json(system, user)
        return AgentFinding(
            agent=self.role,
            summary=str(data.get("summary", "")),
            recommendations=[str(x) for x in data.get("recommendations", [])],
            risks=[str(x) for x in data.get("risks", [])],
            evidence=evidence,
            confidence=float(data.get("confidence", 0.6)),
        )


def synthesize_findings(gateway: ModelGateway, findings: list[AgentFinding]) -> str:
    payload = [asdict(finding) for finding in findings]
    return gateway.invoke(
        "You are an executive AI transformation lead. Reconcile specialist findings into a concise decision brief. Include outcome, rationale, dependencies, risks, controls, and next decision.",
        json.dumps(payload, ensure_ascii=False, default=str),
    )

