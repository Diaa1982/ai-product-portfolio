import unittest
from pathlib import Path

from src.portfolio_api.p08_assessor import AssessmentInput, UseCaseAssessor


ROOT = Path(__file__).resolve().parents[1]


def complete_input(**overrides):
    data = {
        "title": "Synthetic control review",
        "assessment_mode": "hybrid",
        "business_problem": "Manual review delays decisions",
        "desired_outcome": "Reduce effort while preserving accountability",
        "business_owner": "PROCESS_OWNER",
        "process_trigger": "Request received",
        "process_closure": "Approved response issued",
        "ai_task": "Analyse evidence and draft a recommendation",
        "success_criteria": ["30% effort reduction", "100% material evidence traceability"],
        "prohibited_automated_decisions": ["Final approval", "Risk acceptance"],
        "low_confidence_behavior": "Return insufficient information and escalate",
        "data_sources": [{"name": "Synthetic register", "owner": "DATA_OWNER", "classification": "Internal", "quality_status": "validated"}],
        "evidence_references": ["EV-SYN-001"],
        "value_scores": {"strategic_alignment": 4, "public_business_value": 4, "service_operational_impact": 4, "risk_control_improvement": 4},
        "feasibility_scores": {"data_readiness": 4, "technical_feasibility": 4, "process_organizational_readiness": 4, "delivery_sustainability": 4},
        "risk_scores": {"decision_impact": 2, "data_privacy": 2, "legal_compliance": 2, "model_operational": 2},
        "assumptions": ["Synthetic inputs only"],
    }
    data.update(overrides)
    return AssessmentInput(**data)


class UseCaseAssessorTests(unittest.TestCase):
    def setUp(self):
        self.assessor = UseCaseAssessor(ROOT / "products/ai-use-case-assessor/config/scoring.v1.json")

    def test_config_weights(self):
        self.assertEqual(self.assessor.config["dimension_weights"], {"value": 0.6, "feasibility": 0.4})

    def test_weighted_score_and_quick_win(self):
        result = self.assessor.assess(complete_input())
        self.assertEqual(result.priority_score, 4.0)
        self.assertEqual(result.portfolio_classification, "Quick Win")
        self.assertEqual(result.lifecycle_stage, "prioritize")

    def test_four_portfolio_classes(self):
        self.assertEqual(self.assessor.portfolio_class(4, 4, 3.5), "Quick Win")
        self.assertEqual(self.assessor.portfolio_class(4, 2, 3.5), "Strategic Bet")
        self.assertEqual(self.assessor.portfolio_class(2, 4, 3.5), "Fill-In")
        self.assertEqual(self.assessor.portfolio_class(2, 2, 3.5), "Question Mark")

    def test_missing_information_routes_to_discovery(self):
        result = self.assessor.assess(complete_input(evidence_references=[]))
        self.assertEqual(result.completeness_status, "insufficient_information")
        self.assertEqual(result.lifecycle_stage, "discover")

    def test_invalid_classification_is_incomplete(self):
        source = [{"name": "X", "owner": "Y", "classification": "Secret", "quality_status": "validated"}]
        result = self.assessor.assess(complete_input(data_sources=source))
        self.assertIn("data_sources.valid_classification", result.missing_information)

    def test_high_risk_requires_ceo_gate(self):
        scores = {"decision_impact": 5, "data_privacy": 5, "legal_compliance": 5, "model_operational": 5}
        result = self.assessor.assess(complete_input(risk_scores=scores))
        self.assertEqual(result.risk_tier, "high")
        self.assertEqual(result.required_gate, "HIGH_RISK_RECOMMENDATION")

    def test_only_ceo_can_approve_final_actions(self):
        with self.assertRaises(PermissionError):
            self.assessor.approve("A-1", "final_client_output", "REVIEWER", "approved", "Looks good")
        approval = self.assessor.approve("A-1", "final_client_output", "CEO", "approved", "Evidence accepted")
        self.assertEqual(approval["assessment_id"], "A-1")
        self.assertEqual(approval["decision"], "approved")


if __name__ == "__main__":
    unittest.main()
