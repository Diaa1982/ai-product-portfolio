import unittest
from dataclasses import replace
from pathlib import Path

from src.portfolio_api.p12_revenue_reconciliation import RevenueReconciler, RevenueReconciliationInput


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "products" / "revenue-reconciliation-ai" / "config" / "reconciliation.v1.json"


class RevenueReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.engine = RevenueReconciler(CONFIG)
        self.item = RevenueReconciliationInput(
            case_id="REV-SYN-001", form_id="Frm.601.2025.01", reporting_period="FY2026",
            currency="AED", service_provider="SP-SYN-01",
            receiving_bank_account="BANK-SYN-RECEIVING", settlement_bank_account="BANK-SYN-SETTLEMENT",
            responsible_employee_role="REVENUE_RESPONSIBLE_EMPLOYEE", source_system="SYNTHETIC_EPAY_REPORT",
            evidence_references=["synthetic://epay/REV-001", "synthetic://bank/REV-001"],
            assumptions=["Dummy sample data; configured rules require owner validation before production."],
            received_amount=1000, refund_amount=100, fraud_transactions=50,
            commission_type="fixed_100_vat_5", commission_rate_percent=0,
            vat_type="fixed_100_vat_5", vat_rate_percent=5,
            internal_reference="REF-SYN-001", bank_reference="REF-SYN-001",
            internal_amount=745, bank_amount=745, duplicate_internal=False, duplicate_bank=False,
            preparer_role="REVENUE_ANALYST", approver_role="REVENUE_REVIEWER",
            materiality_threshold=100, expected_settlement=850, expected_net_transfer=745,
        )

    def test_config_preserves_three_forms_and_rules(self):
        self.assertEqual(len(self.engine.config["forms"]), 3)
        self.assertEqual(self.engine.config["fixed_commission_amount"], 100)
        self.assertEqual(self.engine.config["fixed_vat_rate_percent"], 5)

    def test_form_601_settlement_invoice_and_net(self):
        result = self.engine.reconcile(self.item)
        self.assertEqual(result.calculations["settlement_amount"], 850)
        self.assertEqual(result.calculations["commission_amount"], 100)
        self.assertEqual(result.calculations["vat_amount"], 5)
        self.assertEqual(result.calculations["total_invoice"], 105)
        self.assertEqual(result.calculations["net_transfer"], 745)
        self.assertEqual(result.decision_status, "RECONCILED_FOR_HUMAN_CONFIRMATION")

    def test_agreed_percentage_commission_and_vat(self):
        item = replace(
            self.item, received_amount=1000, refund_amount=0, fraud_transactions=0,
            commission_type="agreed_percentage", commission_rate_percent=2,
            vat_type="agreed_percentage", vat_rate_percent=5,
            internal_amount=979, bank_amount=979, expected_settlement=1000, expected_net_transfer=979,
        )
        result = self.engine.reconcile(item)
        self.assertEqual(result.calculations["commission_amount"], 20)
        self.assertEqual(result.calculations["vat_amount"], 1)
        self.assertEqual(result.calculations["net_transfer"], 979)

    def test_form_172_only_allows_agreed_percentage(self):
        invalid = self.engine.reconcile(replace(self.item, form_id="Frm.172.2024.02"))
        self.assertIn("form_172_requires_agreed_percentage", invalid.validation_issues)
        valid_item = replace(
            self.item, form_id="Frm.172.2024.02", commission_type="agreed_percentage",
            commission_rate_percent=1, vat_type="zero_percent", expected_net_transfer=841.5,
            internal_amount=841.5, bank_amount=841.5,
        )
        self.assertNotIn("form_172_requires_agreed_percentage", self.engine.reconcile(valid_item).validation_issues)

    def test_form_221_accepts_configured_types_for_record(self):
        for commission_type in self.engine.config["commission_types"]:
            item = replace(self.item, form_id="Frm.221.2018.01", commission_type=commission_type,
                           expected_net_transfer=None, internal_amount=745, bank_amount=745)
            self.assertNotIn("invalid_commission_type", self.engine.reconcile(item).validation_issues)

    def test_exact_reference_and_amount_match(self):
        result = self.engine.reconcile(self.item)
        self.assertEqual(result.match_status, "MATCHED")
        self.assertEqual(result.exceptions, [])

    def test_matched_discount_is_explained(self):
        result = self.engine.reconcile(replace(self.item, bank_amount=740))
        self.assertEqual(result.match_status, "MATCHED_WITH_DISCOUNT_VARIANCE")
        self.assertEqual(result.calculations["discount_amount"], 5)
        self.assertTrue(any(e["code"] == "DISCOUNTED_MATCH" for e in result.exceptions))
        self.assertEqual(result.decision_status, "EXCEPTION_REVIEW_READY")

    def test_unmatched_bank_reference_requires_human_approval(self):
        result = self.engine.reconcile(replace(self.item, bank_reference="OTHER"))
        self.assertEqual(result.match_status, "UNMATCHED_REFERENCE")
        self.assertIn("human_approval_required", result.validation_issues)
        self.assertEqual(result.decision_status, "BLOCKED")
        reviewed = self.engine.reconcile(replace(self.item, bank_reference="OTHER", human_approval_reference="APR-SYN"))
        self.assertEqual(reviewed.decision_status, "EXCEPTION_REVIEW_READY")

    def test_duplicates_and_missing_evidence_block(self):
        result = self.engine.reconcile(replace(
            self.item, duplicate_internal=True, duplicate_bank=True, evidence_references=[]
        ))
        self.assertIn("duplicate_internal_transaction", result.validation_issues)
        self.assertIn("duplicate_bank_transaction", result.validation_issues)
        self.assertIn("missing_evidence", result.validation_issues)

    def test_period_currency_and_bank_fields_are_validated(self):
        result = self.engine.reconcile(replace(
            self.item, reporting_period="FY2025", currency="USD", receiving_bank_account=""
        ))
        self.assertIn("invalid_reporting_period", result.validation_issues)
        self.assertIn("invalid_currency", result.validation_issues)
        self.assertIn("missing_receiving_bank_account", result.validation_issues)

    def test_segregation_of_duties_conflict_blocks(self):
        result = self.engine.reconcile(replace(self.item, approver_role="REVENUE_ANALYST"))
        self.assertIn("segregation_of_duties_conflict", result.validation_issues)

    def test_expected_result_mismatch_blocks(self):
        result = self.engine.reconcile(replace(self.item, expected_settlement=999, expected_net_transfer=999))
        self.assertIn("settlement_reconciliation_mismatch", result.validation_issues)
        self.assertIn("net_transfer_reconciliation_mismatch", result.validation_issues)

    def test_material_bank_variance_requires_review(self):
        result = self.engine.reconcile(replace(
            self.item, bank_amount=500, human_approval_reference=None
        ))
        self.assertTrue(any(e["code"] == "MATERIAL_BANK_VARIANCE" for e in result.exceptions))
        self.assertEqual(result.decision_status, "BLOCKED")

    def test_protected_financial_and_tax_actions_are_denied(self):
        for action in ("approve refund", "determine tax eligibility", "transfer funds", "adjust ledger"):
            result = self.engine.check_action(action)
            self.assertEqual(result["decision"], "DENY_AUTONOMOUS_EXECUTION")
            self.assertFalse(result["permitted_for_ai"])

    def test_output_separates_evidence_and_has_audit_digest(self):
        result = self.engine.reconcile(self.item)
        self.assertEqual(result.facts["service_provider"], "SP-SYN-01")
        self.assertEqual(result.assumptions, self.item.assumptions)
        self.assertEqual(result.evidence_references, self.item.evidence_references)
        self.assertEqual(len(result.audit_record["calculation_digest"]), 64)


if __name__ == "__main__":
    unittest.main()
