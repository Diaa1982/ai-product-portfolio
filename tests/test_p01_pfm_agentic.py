import unittest
from dataclasses import replace
from pathlib import Path

from src.portfolio_api.p01_pfm_agentic import PFMCaseInput, PFMAgenticOrchestrator


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "products" / "pfm-agentic-ai" / "config" / "pfm-agents.v1.json"


class PFMAgenticTests(unittest.TestCase):
    def setUp(self):
        self.engine = PFMAgenticOrchestrator(CONFIG)
        self.case = PFMCaseInput(
            case_id="PFM-SYN-001", workflow_type="budget_variance_review",
            current_agent="budget_execution_commitments", next_agent="treasury_cash",
            business_outcome="Identify execution and liquidity exceptions for human review.",
            payload={"period": "SYNTHETIC-Q2"}, success_criteria=["validated balances", "documented alert"],
            evidence_references=["synthetic://budget-ledger-v1"],
            assumptions=["All values are synthetic and currency-neutral."],
            approved_budget=1000, revised_budget=1200, period_plan=500,
            actuals=450, commitments=300, cash_available=400, obligations_due=350,
            due_date="2030-06-30", validation_passed=True,
        )

    def test_defines_nine_functional_agents(self):
        self.assertEqual(len(self.engine.agents), 9)

    def test_calculates_core_pfm_metrics(self):
        result = self.engine.analyze(self.case)
        self.assertEqual(result.available_balance, 450)
        self.assertEqual(result.utilization_percent, 37.5)
        self.assertEqual(result.commitment_pressure_percent, 25)
        self.assertEqual(result.variance_percent, 10)
        self.assertEqual(result.liquidity_gap, 50)
        self.assertEqual(result.handoff_status, "READY")

    def test_thresholds_are_strictly_greater_than(self):
        variance_result = self.engine.analyze(
            replace(self.case, period_plan=100, actuals=120, revised_budget=200, commitments=0)
        )
        utilization_result = self.engine.analyze(
            replace(self.case, period_plan=95, actuals=95, revised_budget=100, commitments=0)
        )
        self.assertNotIn("VARIANCE_ABOVE_THRESHOLD", variance_result.alerts)
        self.assertNotIn("UTILIZATION_ABOVE_THRESHOLD", utilization_result.alerts)

    def test_zero_period_plan_routes_specialized_review(self):
        result = self.engine.analyze(replace(self.case, period_plan=0))
        self.assertIsNone(result.variance_percent)
        self.assertIn("ZERO_PERIOD_PLAN_SPECIALIZED_REVIEW", result.alerts)

    def test_invalid_source_validation_blocks_handoff(self):
        result = self.engine.analyze(replace(self.case, validation_passed=False))
        self.assertEqual(result.handoff_status, "BLOCKED")
        self.assertIn("source_validation_failed", result.validation_issues)

    def test_missing_evidence_blocks_handoff(self):
        result = self.engine.analyze(replace(self.case, evidence_references=[]))
        self.assertEqual(result.handoff_status, "BLOCKED")
        self.assertIn("missing_evidence_references", result.validation_issues)

    def test_invalid_transition_blocks_downstream_agent(self):
        item = replace(self.case, next_agent="revenue_management")
        result = self.engine.analyze(item)
        self.assertIn("invalid_agent_transition", result.validation_issues)
        self.assertEqual(result.failure_route, "DATA_AND_CONTROL_REMEDIATION_QUEUE")

    def test_high_risk_requires_human_approval(self):
        item = replace(self.case, actuals=1100, commitments=300, cash_available=100, obligations_due=400)
        result = self.engine.analyze(item)
        self.assertEqual(result.risk_rating, "High")
        self.assertTrue(result.approval_interruption)
        self.assertEqual(result.handoff_status, "BLOCKED")
        approved = self.engine.analyze(replace(item, human_approval_reference="APR-SYN-1"))
        self.assertFalse(approved.approval_interruption)
        self.assertEqual(approved.handoff_status, "READY")

    def test_protected_financial_action_is_denied(self):
        result = self.engine.check_action("authorize payment")
        self.assertFalse(result["permitted_for_ai"])
        self.assertTrue(result["human_authority_required"])

    def test_analysis_action_is_allowed_only_as_analysis(self):
        result = self.engine.check_action("prepare cash forecast")
        self.assertTrue(result["permitted_for_ai"])
        self.assertEqual(result["decision"], "ANALYSIS_ONLY_ALLOWED")

    def test_evidence_assumptions_and_audit_payload_are_preserved(self):
        result = self.engine.analyze(self.case)
        self.assertEqual(result.evidence_references, self.case.evidence_references)
        self.assertEqual(result.assumptions, self.case.assumptions)
        self.assertEqual(result.audit_event["input"], self.case.payload)
        self.assertEqual(result.audit_event["success_criteria"], self.case.success_criteria)

    def test_approval_roles_are_enforced(self):
        with self.assertRaises(PermissionError):
            self.engine.approve_handoff("PFM-SYN-1", "AI_AGENT", "approved", "Not authorized")
        decision = self.engine.approve_handoff(
            "PFM-SYN-1", "PFM_PROCESS_OWNER", "approved", "Synthetic UAT approval"
        )
        self.assertEqual(decision["decision"], "approved")


if __name__ == "__main__":
    unittest.main()
