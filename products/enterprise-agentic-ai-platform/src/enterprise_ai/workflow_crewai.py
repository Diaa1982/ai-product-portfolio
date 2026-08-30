from __future__ import annotations

from dataclasses import asdict

from .config import Settings
from .schemas import UseCaseRequest


def build_crewai_crew(request: UseCaseRequest, settings: Settings):
    """Alternative collaborative workflow using CrewAI."""
    try:
        from crewai import Agent, Crew, Process, Task
    except ImportError as exc:
        raise RuntimeError("Install project dependencies to use CrewAI") from exc

    roles = {
        "strategist": "Translate the challenge into an AI transformation roadmap and operating model.",
        "architect": "Design the secure RAG, multimodal, agent, integration, and deployment architecture.",
        "risk_lead": "Assess governance, security, privacy, model, operational, and compliance risks.",
        "value_lead": "Define baselines, KPIs, costs, benefits, and value-realization controls.",
    }
    agents = {
        name: Agent(
            role=name.replace("_", " ").title(),
            goal=goal,
            backstory="Enterprise specialist who separates evidence, assumptions, and recommendations.",
            verbose=True,
            allow_delegation=True,
        )
        for name, goal in roles.items()
    }
    context = str(asdict(request))
    tasks = [
        Task(
            description=f"{goal}\nUse case: {context}",
            expected_output="A concise evidence-based analysis with risks, controls, KPIs, and decisions required.",
            agent=agents[name],
        )
        for name, goal in roles.items()
    ]
    return Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


def run_crewai(request: UseCaseRequest, settings: Settings) -> str:
    return str(build_crewai_crew(request, settings).kickoff())

