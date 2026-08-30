from __future__ import annotations

from .schemas import GovernanceDecision, UseCaseRequest


class GovernanceEngine:
    """Proportionate governance gate for enterprise agent execution."""

    SENSITIVE_TERMS = {
        "personal data",
        "health",
        "biometric",
        "credit",
        "payment",
        "employee",
        "citizen",
        "automated decision",
    }

    def assess(self, request: UseCaseRequest, high_risk_threshold: int = 70) -> GovernanceDecision:
        text = " ".join(
            [request.challenge, request.objective, *request.constraints, *request.data_sources]
        ).lower()
        reasons: list[str] = []
        score = 15
        hits = sorted(term for term in self.SENSITIVE_TERMS if term in text)
        if hits:
            score += min(45, len(hits) * 15)
            reasons.append(f"Sensitive or consequential scope detected: {', '.join(hits)}")
        if request.authorized_to_execute:
            score += 10
            reasons.append("Request includes execution authority and requires action controls.")
        if not request.data_sources:
            score += 15
            reasons.append("Data sources and ownership have not been confirmed.")
        if not request.expected_outcomes:
            score += 10
            reasons.append("Measurable outcomes have not been defined.")
        score = min(score, 100)
        level = "critical" if score >= 85 else "high" if score >= 70 else "medium" if score >= 40 else "low"
        approval_required = score >= high_risk_threshold or request.authorized_to_execute
        controls = [
            "Use approved and traceable data sources",
            "Log prompts, evidence, tool calls, and decisions",
            "Apply least-privilege access and separation of duties",
            "Require human review for high-impact outputs",
            "Define monitoring, incident, and rollback procedures",
        ]
        return GovernanceDecision(
            risk_score=score,
            risk_level=level,
            approval_required=approval_required,
            approved=(not approval_required) or (request.authorized_to_execute and score < 85),
            reasons=reasons or ["No elevated risk indicators detected."],
            controls=controls,
        )
