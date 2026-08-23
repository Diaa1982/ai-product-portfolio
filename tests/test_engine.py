import json
import tempfile
import unittest
from pathlib import Path

from src.portfolio_api.engine import JsonCaseStore, PortfolioEngine


ROOT = Path(__file__).resolve().parents[1]


class PortfolioEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.store = JsonCaseStore(Path(self.temp.name) / "cases.json")
        self.engine = PortfolioEngine(ROOT / "products" / "workflows.json", self.store)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_every_product_has_a_workflow(self) -> None:
        self.assertEqual(len(self.engine.workflows), 18)
        self.assertEqual(set(self.engine.workflows), {f"P{i:02d}" for i in range(1, 19)})

    def test_pfm_calculations_and_critical_pause(self) -> None:
        case = self.engine.create_case(
            "P01",
            "Synthetic budget pressure",
            "BUDGET_ANALYST",
            {"business_outcome": "Protect fiscal discipline", "budget": 100, "actual": 95, "commitments": 10},
        )
        evaluated = self.engine.evaluate(case.case_id)
        self.assertEqual(evaluated.calculations["available_balance"], -5)
        self.assertEqual(evaluated.status, "paused_critical")
        self.assertTrue(self.engine.verify_audit_chain(evaluated))

    def test_material_finding_requires_evidence(self) -> None:
        case = self.engine.create_case(
            "P08",
            "Low readiness use case",
            "AI_PORTFOLIO_ANALYST",
            {"business_outcome": "Improve review efficiency", "value_score": 2, "feasibility_score": 2},
        )
        evaluated = self.engine.evaluate(case.case_id)
        with self.assertRaisesRegex(ValueError, "require evidence"):
            self.engine.submit_for_approval(evaluated.case_id, "AI_PORTFOLIO_ANALYST")

    def test_approval_enforces_role_and_preserves_chain(self) -> None:
        case = self.engine.create_case(
            "P08",
            "Qualified use case",
            "AI_PORTFOLIO_ANALYST",
            {"business_outcome": "Improve review efficiency", "value_score": 4.5, "feasibility_score": 4.0},
        )
        evaluated = self.engine.evaluate(case.case_id)
        submitted = self.engine.submit_for_approval(evaluated.case_id, "AI_PORTFOLIO_ANALYST")
        with self.assertRaises(PermissionError):
            self.engine.decide(submitted.case_id, "UNAUTHORIZED_ROLE", "approved", "No authority")
        decided = self.engine.decide(submitted.case_id, "AI_GOVERNANCE_BOARD", "approved", "Synthetic test passed")
        self.assertEqual(decided.status, "approved")
        self.assertTrue(self.engine.verify_audit_chain(decided))

    def test_store_round_trip(self) -> None:
        case = self.engine.create_case(
            "P05",
            "Institutional service",
            "SERVICE_DESIGNER",
            {"business_outcome": "Reduce service effort", "service_name": "Synthetic service", "customer_type": "G2G", "request_type": "explicit"},
        )
        loaded = self.store.get(case.case_id)
        self.assertEqual(json.loads(json.dumps(loaded.to_dict())), loaded.to_dict())


if __name__ == "__main__":
    unittest.main()
