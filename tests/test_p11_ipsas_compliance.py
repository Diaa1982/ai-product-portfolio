import unittest
from dataclasses import replace
from pathlib import Path

from src.portfolio_api.p11_ipsas_compliance import IPSASComplianceReviewer, IPSASReviewInput


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "products" / "ipsas-compliance-ai" / "config" / "ipsas-review.v1.json"


class IPSASComplianceTests(unittest.TestCase):
    def setUp(self):
        self.reviewer = IPSASComplianceReviewer(CONFIG)
        self.journal = IPSASReviewInput(
            case_id="IPS-SYN-001", review_type="journal_quality", reporting_period="FY2026",
            entity_id="ENTITY-SYN-01", source_system="SYNTHETIC_LEDGER",
            evidence_references=["synthetic://journal/J-001"],
            applicable_policy_reference="SYNTHETIC-ACCOUNTING-POLICY-01",
            requirement_reference="SYNTHETIC-REQUIREMENT-REF-01",
            assumptions=["Synthetic review; no formal IPSAS conclusion."], confidence_score=0.95,
            materiality_threshold=1000, reporting_impact=False, human_approval_reference=None,
            journal_id="J-SYN-001", debit_total=100, credit_total=100,
            entry_date="2026-06-30", period_start="2026-01-01", period_end="2026-12-31",
            account_code_valid=True, supporting_document_present=True, approval_status="Approved",
            preparer_role="ACCOUNTANT", approver_role="ACCOUNTING_REVIEWER",
            ledger_balance=None, external_balance=None, unreconciled_items=[], disclosure_items=[],
            comparative_current=None, comparative_prior=None, comparative_required=False,
        )

    def test_configuration_disables_formal_compliance_determination(self):
        self.assertFalse(self.reviewer.config["formal_compliance_determination_allowed"])
        self.assertEqual(len(self.reviewer.config["review_types"]), 3)

    def test_clean_journal_is_review_ready_not_formally_compliant(self):
        result = self.reviewer.review(self.journal)
        self.assertEqual(result.review_status, "REVIEW_READY")
        self.assertEqual(result.calculations["debit_credit_difference"], 0)
        self.assertEqual(result.exceptions, [])
        self.assertIn("formal compliance determination not performed", result.compliance_conclusion)
        self.assertTrue(result.human_review_required)

    def test_unbalanced_journal_is_high_severity(self):
        result = self.reviewer.review(replace(self.journal, credit_total=90))
        self.assertTrue(any(e["code"] == "UNBALANCED_JOURNAL" and e["severity"] == "High" for e in result.exceptions))
        self.assertEqual(result.review_status, "HUMAN_REVIEW_REQUIRED")

    def test_period_cutoff_exception(self):
        result = self.reviewer.review(replace(self.journal, entry_date="2027-01-01"))
        self.assertTrue(any(e["code"] == "PERIOD_CUTOFF_EXCEPTION" for e in result.exceptions))

    def test_journal_evidence_approval_and_sod_controls(self):
        result = self.reviewer.review(replace(
            self.journal, supporting_document_present=False, approval_status="Submitted",
            approver_role="ACCOUNTANT",
        ))
        codes = {e["code"] for e in result.exceptions}
        self.assertTrue({"MISSING_SUPPORT", "JOURNAL_NOT_APPROVED", "SEGREGATION_OF_DUTIES_CONFLICT"}.issubset(codes))

    def test_material_reporting_impact_requires_human_reference(self):
        result = self.reviewer.review(replace(self.journal, reporting_impact=True))
        self.assertEqual(result.review_status, "HUMAN_REVIEW_REQUIRED")
        approved = self.reviewer.review(replace(self.journal, reporting_impact=True, human_approval_reference="APR-SYN"))
        self.assertEqual(approved.review_status, "HUMAN_DECISION_RECORDED")

    def test_low_confidence_returns_insufficient_information(self):
        result = self.reviewer.review(replace(self.journal, confidence_score=0.6))
        self.assertEqual(result.review_status, "INSUFFICIENT_INFORMATION")
        self.assertEqual(result.evidence_strength, "Insufficient")

    def test_missing_policy_or_requirement_returns_insufficient_information(self):
        result = self.reviewer.review(replace(
            self.journal, applicable_policy_reference="", requirement_reference=""
        ))
        codes = {e["code"] for e in result.exceptions}
        self.assertTrue({"MISSING_POLICY_REFERENCE", "MISSING_REQUIREMENT_REFERENCE"}.issubset(codes))
        self.assertEqual(result.review_status, "INSUFFICIENT_INFORMATION")

    def test_reconciliation_difference_and_aging(self):
        item = replace(
            self.journal, review_type="reconciliation", journal_id=None, debit_total=None,
            credit_total=None, entry_date=None, period_start=None, period_end=None,
            account_code_valid=None, supporting_document_present=None, approval_status=None,
            preparer_role=None, approver_role=None, ledger_balance=1000, external_balance=900,
            unreconciled_items=[{"item_id":"R-1","amount":100,"age_days":45,"evidence_reference":"synthetic://recon/R-1"}],
        )
        result = self.reviewer.review(item)
        self.assertEqual(result.calculations["reconciliation_difference"], 100)
        codes = {e["code"] for e in result.exceptions}
        self.assertTrue({"UNRECONCILED_BALANCE", "AGED_UNRECONCILED_ITEMS"}.issubset(codes))

    def test_unsupported_reconciliation_item_is_high_severity(self):
        item = replace(
            self.journal, review_type="reconciliation", ledger_balance=100, external_balance=100,
            unreconciled_items=[{"item_id":"R-2","amount":5,"age_days":2,"evidence_reference":""}],
        )
        result = self.reviewer.review(item)
        self.assertTrue(any(e["code"] == "UNSUPPORTED_RECONCILIATION_ITEMS" for e in result.exceptions))

    def test_disclosure_gaps_and_comparatives(self):
        item = replace(
            self.journal, review_type="disclosure_checklist",
            disclosure_items=[
                {"item_id":"D-1","status":"Missing","evidence_reference":"","policy_reference":"SYN-POL"},
                {"item_id":"D-2","status":"Partial","evidence_reference":"synthetic://D-2","policy_reference":"SYN-POL"}
            ], comparative_required=True, comparative_current="FY2026", comparative_prior=None,
        )
        result = self.reviewer.review(item)
        codes = {e["code"] for e in result.exceptions}
        self.assertTrue({"DISCLOSURE_GAPS", "PARTIAL_DISCLOSURES", "UNSUPPORTED_DISCLOSURES", "MISSING_COMPARATIVE_INFORMATION"}.issubset(codes))

    def test_empty_disclosure_checklist_blocks(self):
        result = self.reviewer.review(replace(self.journal, review_type="disclosure_checklist"))
        self.assertTrue(any(e["code"] == "MISSING_DISCLOSURE_CHECKLIST" for e in result.exceptions))

    def test_protected_accounting_actions_are_denied(self):
        for action in ("post journal", "close accounting period", "publish financial statements"):
            result = self.reviewer.check_action(action)
            self.assertEqual(result["decision"], "DENY_AUTONOMOUS_EXECUTION")
            self.assertFalse(result["permitted_for_ai"])

    def test_review_support_action_is_not_execution(self):
        result = self.reviewer.check_action("draft disclosure gap checklist")
        self.assertEqual(result["decision"], "REVIEW_SUPPORT_ONLY")
        self.assertTrue(result["permitted_for_ai"])

    def test_output_preserves_layers_and_audit_digest(self):
        result = self.reviewer.review(self.journal)
        self.assertEqual(result.facts["policy_reference"], "SYNTHETIC-ACCOUNTING-POLICY-01")
        self.assertEqual(result.assumptions, self.journal.assumptions)
        self.assertEqual(result.evidence_references, self.journal.evidence_references)
        self.assertEqual(len(result.audit_record["calculation_digest"]), 64)


if __name__ == "__main__":
    unittest.main()
