import unittest
from pathlib import Path

from src.portfolio_api.p03_radar import SignalInput, StrategicRadar


ROOT = Path(__file__).resolve().parents[1]
HASH = "a" * 64


def signal(**overrides):
    data = {
        "title": "Synthetic fiscal signal", "audience": "government",
        "industry": "Financial Services/Fintech", "jurisdiction": "UAE",
        "pfm_category": "Fiscal sustainability", "signal_statement": "A material rule changed",
        "fact": "The synthetic source version changed.",
        "interpretation": "The change may affect medium-term fiscal assumptions.",
        "recommendation": "Validate the impact with the accountable policy owner.",
        "source_id": "SYN-OFFICIAL-001", "source_url": "https://official.example/rule/1",
        "source_version": "v2", "published_at": "2026-08-20T00:00:00Z",
        "retrieved_at": "2026-08-21T00:00:00Z", "evidence_hash": HASH,
        "change_summary": "Threshold changed from synthetic A to B.",
        "materiality_scores": {"jurisdictional_scope": .9, "industry_breadth": .8,
            "time_sensitivity": .9, "evidence_strength": .9, "novelty": .8,
            "stakeholder_relevance": .9},
        "confidence_score": .9,
    }
    data.update(overrides)
    return SignalInput(**data)


class StrategicRadarTests(unittest.TestCase):
    def setUp(self):
        self.radar = StrategicRadar(ROOT / "products/strategic-radar/config/radar.v1.json")

    def test_weights_total_one(self):
        self.assertEqual(sum(x["weight"] for x in self.radar.config["materiality_criteria"]), 1.0)

    def test_verified_high_materiality_signal(self):
        result = self.radar.assess_signal(signal())
        self.assertEqual(result.evidence_status, "verified")
        self.assertEqual(result.materiality_route, "auto_alert_eligible")
        self.assertEqual(result.output_status, "eligible_for_delivery")

    def test_unapproved_source_is_blocked(self):
        result = self.radar.assess_signal(signal(source_id="UNKNOWN"))
        self.assertEqual(result.output_status, "blocked_evidence")
        self.assertIn("source_not_registered", result.approval_reasons)

    def test_wrong_domain_is_blocked(self):
        result = self.radar.assess_signal(signal(source_url="https://example.com/item"))
        self.assertEqual(result.evidence_status, "blocked")

    def test_null_score_routes_to_analyst(self):
        scores = signal().materiality_scores | {"novelty": None}
        result = self.radar.assess_signal(signal(materiality_scores=scores))
        self.assertIsNone(result.materiality_score)
        self.assertEqual(result.output_status, "pending_analyst_review")

    def test_high_impact_requires_human_approval(self):
        result = self.radar.assess_signal(signal(high_impact=True))
        self.assertEqual(result.output_status, "pending_human_approval")
        self.assertIn("high_impact_external_alert", result.approval_reasons)

    def test_low_confidence_executive_delivery_is_protected(self):
        result = self.radar.assess_signal(signal(executive_delivery=True, confidence_score=.5))
        self.assertIn("low_confidence_executive_sharing", result.approval_reasons)

    def test_only_authority_can_approve(self):
        with self.assertRaises(PermissionError):
            self.radar.approve("S-1", "executive_delivery", "ANALYST", "approved", "Valid")
        result = self.radar.approve("S-1", "executive_delivery", "STRATEGY_RISK_AUTHORITY", "approved", "Evidence accepted")
        self.assertEqual(result["decision"], "approved")


if __name__ == "__main__":
    unittest.main()
