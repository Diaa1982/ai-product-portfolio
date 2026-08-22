import unittest
from dataclasses import replace
from pathlib import Path

from src.portfolio_api.p02_pfm_brain import FiscalSnapshotInput, PFMBrain


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "products" / "pfm-brain" / "config" / "pfm-brain.v1.json"


class PFMBrainTests(unittest.TestCase):
    def setUp(self):
        self.brain = PFMBrain(CONFIG)
        self.item = FiscalSnapshotInput(
            case_id="PFB-SYN-001", reporting_period="FY2026", currency="AED",
            division_id="DIV-SYN-01", cost_center="CC-SYN-001", account_code="ACC-SYN-100",
            source_record_id="TXN-SYN-0001", source_system="SYNTHETIC_PFM_PACK",
            evidence_references=["synthetic://pfm-brain/txn-0001"],
            assumptions=["All records are synthetic and not suitable for statutory reporting."],
            organization_master_loaded=True, chart_of_accounts_loaded=True,
            approved_budget_loaded=True, original_budget=100, supplementary_budget=10,
            transfer_amount=-5, period_plan=60, actual_expenditure=60, commitments=20,
            revenue_target=100, revenue_actual=110, opening_cash=50, cash_inflow=100,
            cash_outflow=80, minimum_cash_buffer=20, kpi_direction="Higher",
            kpi_target=100, kpi_actual=102, kpi_attention_tolerance_percent=10,
            inherent_risk_score=60, control_effectiveness_percent=80,
            requester_role="PFM_ANALYST", approver_role="PFM_REVIEWER",
            proposed_action_amount=10, maximum_authority_amount=20,
            action_type="prepare fiscal analysis", expected_revised_budget=105,
            expected_closing_cash=70,
        )

    def test_retains_approved_synthetic_profile_and_twenty_cases(self):
        p = self.brain.config["synthetic_dataset_profile"]
        self.assertEqual((p["division_count"], p["account_count"], p["transaction_count"]), (8, 60, 1500))
        self.assertEqual(len(self.brain.config["acceptance_cases"]), 20)
        self.assertFalse(p["statutory_reporting_allowed"])

    def test_required_dataset_load_order(self):
        order = self.brain.config["load_order"]
        ready = self.brain.dataset_readiness(order)
        self.assertTrue(ready["ready_for_analysis"])
        invalid = self.brain.dataset_readiness(["approved_budget", "organization_master"])
        self.assertFalse(invalid["sequence_valid"])

    def test_reconciles_core_budget_cash_and_risk_calculations(self):
        result = self.brain.analyze(self.item)
        self.assertEqual(result.calculations["revised_budget"], 105)
        self.assertEqual(result.calculations["available_budget"], 25)
        self.assertEqual(result.calculations["closing_cash"], 70)
        self.assertEqual(result.calculations["residual_risk_score"], 12)
        self.assertEqual(result.reconciliation_status, "Reconciled")
        self.assertEqual(result.decision_status, "ANALYSIS_READY_FOR_HUMAN_USE")

    def test_master_data_and_approved_budget_are_prerequisites(self):
        result = self.brain.analyze(replace(
            self.item, organization_master_loaded=False, chart_of_accounts_loaded=False,
            approved_budget_loaded=False,
        ))
        self.assertIn("organization_master_not_loaded", result.validation_issues)
        self.assertIn("chart_of_accounts_not_loaded", result.validation_issues)
        self.assertIn("approved_budget_not_loaded", result.validation_issues)
        self.assertEqual(result.decision_status, "BLOCKED")

    def test_currency_period_and_identifiers_are_validated(self):
        result = self.brain.analyze(replace(
            self.item, currency="USD", reporting_period="FY2025", account_code="", cost_center=""
        ))
        self.assertIn("invalid_currency", result.validation_issues)
        self.assertIn("invalid_reporting_period", result.validation_issues)
        self.assertIn("missing_account_code", result.validation_issues)
        self.assertIn("missing_cost_center", result.validation_issues)

    def test_duplicate_and_missing_evidence_block_analysis(self):
        result = self.brain.analyze(replace(self.item, duplicate_transaction=True, evidence_references=[]))
        self.assertIn("duplicate_transaction", result.validation_issues)
        self.assertIn("missing_evidence", result.validation_issues)
        self.assertEqual(result.confidence, "Low")

    def test_kpi_direction_statuses(self):
        self.assertEqual(self.brain.analyze(replace(self.item, kpi_actual=95)).calculations["kpi_status"], "Attention")
        self.assertEqual(self.brain.analyze(replace(self.item, kpi_actual=80)).calculations["kpi_status"], "Off Target")
        lower = replace(self.item, kpi_direction="Lower", kpi_target=100, kpi_actual=105)
        self.assertEqual(self.brain.analyze(lower).calculations["kpi_status"], "Attention")
        self.assertEqual(self.brain.analyze(replace(lower, kpi_actual=90)).calculations["kpi_status"], "On Target")

    def test_control_results_use_configured_thresholds(self):
        self.assertEqual(self.brain.analyze(self.item).calculations["control_result"], "Effective")
        self.assertEqual(self.brain.analyze(replace(self.item, control_effectiveness_percent=60)).calculations["control_result"], "Partially Effective")
        failed = self.brain.analyze(replace(self.item, control_effectiveness_percent=20, human_approval_reference="APR-SYN"))
        self.assertEqual(failed.calculations["control_result"], "Failed")
        self.assertTrue(any(x["risk"] == "control_failed" for x in failed.risks))

    def test_financial_exceptions_are_exposed_as_risks(self):
        item = replace(
            self.item, actual_expenditure=100, commitments=20,
            revenue_actual=70, cash_outflow=140, human_approval_reference="APR-SYN",
        )
        result = self.brain.analyze(item)
        names = {risk["risk"] for risk in result.risks}
        self.assertTrue({"budget_exceeded", "revenue_shortfall", "cash_buffer_breach"}.issubset(names))

    def test_segregation_of_duties_conflict_blocks(self):
        result = self.brain.analyze(replace(self.item, approver_role="PFM_ANALYST"))
        self.assertIn("segregation_of_duties_conflict", result.validation_issues)

    def test_authority_limit_never_becomes_automatic_approval(self):
        within = self.brain.analyze(self.item)
        self.assertEqual(within.authority_status, "WITHIN_LIMIT_HUMAN_APPROVAL_REQUIRED")
        above = self.brain.analyze(replace(self.item, proposed_action_amount=30))
        self.assertEqual(above.authority_status, "EXCEEDS_AUTHORITY_ESCALATE")
        self.assertEqual(above.decision_status, "BLOCKED")

    def test_protected_action_is_blocked_without_human_reference(self):
        result = self.brain.analyze(replace(self.item, action_type="authorize payment"))
        self.assertEqual(result.authority_status, "PROTECTED_ACTION_HUMAN_AUTHORITY_REQUIRED")
        self.assertIn("human_approval_required", result.validation_issues)

    def test_aed_420m_rephase_is_critical_and_requires_human_approval(self):
        result = self.brain.analyze(replace(
            self.item, action_type="rephase budget", proposed_action_amount=420_000_000,
            maximum_authority_amount=500_000_000,
        ))
        self.assertTrue(any(x["risk"] == "critical_value_action" for x in result.risks))
        self.assertEqual(result.decision_status, "BLOCKED")

    def test_reconciliation_mismatch_blocks_reporting_use(self):
        result = self.brain.analyze(replace(self.item, expected_revised_budget=999))
        self.assertEqual(result.reconciliation_status, "Mismatch")
        self.assertIn("revised_budget_mismatch", result.validation_issues)

    def test_output_separates_facts_assumptions_risks_and_recommendations(self):
        result = self.brain.analyze(self.item)
        self.assertEqual(result.facts["source_record_id"], "TXN-SYN-0001")
        self.assertEqual(result.assumptions, self.item.assumptions)
        self.assertTrue(result.recommendations)
        self.assertEqual(len(result.audit_record["calculation_digest"]), 64)
        self.assertEqual(result.evidence_references, self.item.evidence_references)


if __name__ == "__main__":
    unittest.main()
