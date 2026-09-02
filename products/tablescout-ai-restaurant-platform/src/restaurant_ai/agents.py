from __future__ import annotations

from dataclasses import dataclass

from .models import Evidence, Recommendation, UserPreferences
from .retrieval import MultimodalRetriever, SearchHit


@dataclass
class AgentTrace:
    agent: str
    output: str


class PreferenceAgent:
    name = "Preference Analyst"

    def run(self, prefs: UserPreferences) -> AgentTrace:
        constraints = [*(x.value for x in prefs.dietary), *(x.lower() for x in prefs.cuisines)]
        return AgentTrace(self.name, f"Intent: {prefs.query}; constraints: {', '.join(constraints) or 'none'}")


class RetrievalAgent:
    name = "Multimodal Retrieval Specialist"

    def __init__(self, retriever: MultimodalRetriever):
        self.retriever = retriever

    def run(self, prefs: UserPreferences, image_path: str | None, top_k: int) -> tuple[list[SearchHit], AgentTrace]:
        hits = self.retriever.search(prefs, image_path=image_path, top_k=top_k)
        return hits, AgentTrace(self.name, f"Retrieved {len(hits)} policy-compliant candidates")


class CriticAgent:
    name = "Evidence and Safety Critic"

    def run(self, hits: list[SearchHit], prefs: UserPreferences) -> AgentTrace:
        flags = []
        if prefs.dietary:
            flags.append("dietary claims restricted to structured evidence")
        if not hits:
            flags.append("no candidate satisfies all hard filters")
        return AgentTrace(self.name, "; ".join(flags) or "evidence coverage acceptable")


class SynthesisAgent:
    name = "Recommendation Synthesizer"

    def run(self, hits: list[SearchHit], prefs: UserPreferences) -> list[Recommendation]:
        output = []
        for hit in hits:
            r = hit.restaurant
            tradeoffs = []
            if r.price_band.value in {"$$$", "$$$$"}:
                tradeoffs.append(f"Higher price point ({r.price_band.value})")
            if not r.reviews:
                tradeoffs.append("Limited review evidence")
            rationale = f"Strong match for '{prefs.query}' with {', '.join(r.cuisines)} cuisine"
            if r.average_rating:
                rationale += f" and a {r.average_rating:.1f}/5 average rating"
            evidence = [Evidence(source="restaurant profile", excerpt=r.description[:220], score=hit.text_score)]
            if r.reviews:
                best = max(r.reviews, key=lambda x: x.rating)
                evidence.append(Evidence(source="customer review", excerpt=best.text[:220], score=best.rating / 5))
            output.append(Recommendation(
                restaurant_id=r.id, restaurant_name=r.name, score=round(hit.fused_score, 4),
                rationale=rationale + ".", tradeoffs=tradeoffs or ["No material tradeoff identified"],
                evidence=evidence, policy_checks=["active listing", "hard filters satisfied", "evidence-grounded claims"],
            ))
        return output


class RecommendationCrew:
    """Explicit sequential orchestration with inspectable hand-offs."""

    def __init__(self, retriever: MultimodalRetriever):
        self.preference = PreferenceAgent()
        self.retrieval = RetrievalAgent(retriever)
        self.critic = CriticAgent()
        self.synthesis = SynthesisAgent()

    def recommend(self, prefs: UserPreferences, image_path: str | None = None, top_k: int = 3):
        traces = [self.preference.run(prefs)]
        hits, trace = self.retrieval.run(prefs, image_path, top_k)
        traces.append(trace)
        traces.append(self.critic.run(hits, prefs))
        return self.synthesis.run(hits, prefs), traces

