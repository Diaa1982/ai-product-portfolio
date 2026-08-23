import unittest
from pathlib import Path

from src.portfolio_api.p07_partnership import PartnershipInput, PartnershipManagementCopilot


ROOT = Path(__file__).parents[1]


def complete_case(**overrides):
    data = {
        "case_id":"PART-SYN-001","partner_id":"PARTNER-SYN-001","partnership_id":"PSHIP-SYN-001","partner_name":"Synthetic Partner","entity_name":"Synthetic Entity","responsible_person":"Synthetic Contact","contact":"+971-00-0000000","email":"synthetic@example.invalid","start_date":"2026-01-01","end_date":"2026-12-31","partnership_status":"ACTIVE","strategic_classification":"Strategic","geographic_classification":"Local","initiative":"Synthetic collaboration","innovation":"Shared evidence register","expected_value":"Improve governed collaboration","objectives":["Deliver two evidence-backed outputs"],"notes":"Synthetic only","partnership_owner_role":"PARTNERSHIP_OWNER","agreement_source_id":"AGR-SYN-001","agreement_version":"1.0",
        "agreement_items":[{"item_id":"ITEM-001","item_type":"benefit","deliverable":"Two joint outputs","milestone":"Quarterly review","owner_role":"PARTNERSHIP_OWNER","counterparty_role":"PARTNER_OWNER","beneficiary":"Government units","due_date":"2026-06-30","recurrence":"quarterly","kpi":"outputs_delivered","target":2,"quantity_or_value":2,"expected_result":"Two outputs","evidence_type":"report","dependencies":["Approved plan"],"clause_citation":"Clause 4.2"}],
        "claims":[{"item_id":"ITEM-001","claimed_status":"Realized","actual_quantity_or_value":2,"evidence_references":["EV-001"]}],
        "evidence_items":[{"evidence_id":"EV-001","file_type":"report","submission_status":"ACCEPTED","relevance_score":0.95,"source_link":"sharepoint://synthetic/EV-001","language":"en"}],
        "evaluation_cycle":"2026-Q3","as_of_date":"2026-08-22","response_requested_at":"2026-08-10","owner_responded":True,"reminders_recorded":0,"assumptions":["Synthetic agreement only"]
    }
    data.update(overrides)
    return PartnershipInput(**data)


class PartnershipCopilotTests(unittest.TestCase):
    def setUp(self):
        self.ai = PartnershipManagementCopilot(ROOT / "products/partnership-management-copilot/config/partnership.v1.json")

    def test_four_bilingual_partnership_statuses(self):
        statuses = self.ai.config["partnership_statuses"]
        self.assertEqual([x["code"] for x in statuses], ["ACTIVE","TEMPORARY","PERMANENT","COMPLETED"])
        self.assertEqual(statuses[-1]["ar"], "تم الانتهاء منها")

    def test_first_build_has_no_orchestrator_or_background_trigger(self):
        controls = self.ai.config["architecture_constraints"]
        self.assertFalse(controls["custom_orchestrator"])
        self.assertFalse(controls["background_triggers"])
        self.assertEqual(controls["interaction_mode"], "user_initiated")

    def test_register_has_linking_ids(self):
        result = self.ai.analyze(complete_case())
        self.assertEqual(result.register_record["Partner_ID"], "PARTNER-SYN-001")
        self.assertEqual(result.register_record["Partnership_ID"], "PSHIP-SYN-001")

    def test_extracted_items_remain_draft(self):
        result = self.ai.analyze(complete_case())
        self.assertEqual(result.extracted_items[0]["confirmation_status"], "DRAFT_PENDING_AUTHORIZED_CONFIRMATION")

    def test_missing_owner_and_clause_are_flagged(self):
        item = dict(complete_case().agreement_items[0], owner_role="", clause_citation="")
        result = self.ai.analyze(complete_case(agreement_items=[item]))
        fields = {x["field"] for x in result.extraction_exceptions}
        self.assertIn("owner_role", fields)
        self.assertIn("clause_citation", fields)

    def test_ambiguous_date_is_flagged(self):
        item = dict(complete_case().agreement_items[0], due_date="Q2 2026")
        result = self.ai.analyze(complete_case(agreement_items=[item]))
        self.assertTrue(any(x["exception"] == "ambiguous_or_missing_date" for x in result.extraction_exceptions))

    def test_submission_is_not_acceptance(self):
        evidence = [dict(complete_case().evidence_items[0], submission_status="SUBMITTED")]
        result = self.ai.analyze(complete_case(evidence_items=evidence))
        self.assertEqual(result.claim_evidence_assessments[0]["assessed_status"], "Insufficient Evidence")
        self.assertFalse(result.claim_evidence_assessments[0]["evidence_submission_is_acceptance"])

    def test_weak_evidence_is_insufficient(self):
        evidence = [dict(complete_case().evidence_items[0], relevance_score=0.2)]
        result = self.ai.analyze(complete_case(evidence_items=evidence))
        self.assertEqual(result.claim_evidence_assessments[0]["assessed_status"], "Insufficient Evidence")

    def test_realized_and_utilization_calculation(self):
        result = self.ai.analyze(complete_case())
        self.assertEqual(result.claim_evidence_assessments[0]["assessed_status"], "Realized")
        self.assertEqual(result.utilization["utilization_percent"], 100.0)

    def test_partial_realization(self):
        claim = dict(complete_case().claims[0], actual_quantity_or_value=1, claimed_status="Partially Realized")
        result = self.ai.analyze(complete_case(claims=[claim]))
        self.assertEqual(result.claim_evidence_assessments[0]["assessed_status"], "Partially Realized")
        self.assertEqual(result.utilization["utilization_percent"], 50.0)

    def test_expiry_threshold(self):
        result = self.ai.analyze(complete_case(end_date="2026-09-10"))
        self.assertEqual(result.expiry_monitoring["status"], "DUE_WITHIN_30_DAYS")

    def test_reminder_is_draft_only(self):
        result = self.ai.analyze(complete_case(owner_responded=False, reminders_recorded=1))
        self.assertEqual(result.notification_draft["status"], "DRAFT_REMINDER")
        self.assertFalse(result.notification_draft["send_permitted"])

    def test_three_reminders_then_draft_escalation(self):
        result = self.ai.analyze(complete_case(owner_responded=False, reminders_recorded=3))
        self.assertEqual(result.notification_draft["status"], "DRAFT_ESCALATION")
        self.assertEqual(result.notification_draft["recipient_role"], "SECTOR_DIRECTOR")

    def test_two_stage_change_review_and_override(self):
        approved = self.ai.review_change("P-1","modify","DIVISION_USER","STRATEGY_EMPLOYEE_1","approved","STRATEGY_EMPLOYEE_2","approved","","CHG-1")
        self.assertEqual(approved["status"], "APPROVED_FOR_REGISTER_UPDATE")
        self.assertFalse(approved["autonomous_update_permitted"])
        with self.assertRaises(ValueError):
            self.ai.review_change("P-1","delete","DIVISION_USER","STRATEGY_EMPLOYEE_1","rejected","STRATEGY_EMPLOYEE_2","approved","","CHG-2")

    def test_protected_legal_actions_and_bilingual_report(self):
        for action in ["sign agreement", "terminate agreement", "issue legal opinion", "send external message", "accept evidence"]:
            self.assertFalse(self.ai.check_action(action)["permitted"])
        result = self.ai.analyze(complete_case())
        self.assertTrue(result.bilingual_report["title_en"])
        self.assertTrue(result.bilingual_report["title_ar"])
        self.assertEqual(len(result.audit_digest), 64)


if __name__ == "__main__":
    unittest.main()
