import unittest
from pathlib import Path

from src.portfolio_api.p06_process_audit import ProcessAuditAI, ProcessAuditInput


ROOT = Path(__file__).parents[1]


def complete_case(ai, **overrides):
    criteria = [{"criterion_id": c["id"], "applicable": True, "ai_suggested_rating": 4, "auditor_rating": 4, "evidence_references": ["EV-DOC", "EV-LOG"], "override_reason": ""} for c in ai.config["criteria"]]
    data = {
        "audit_id": "AUD-SYN-001", "period": "2026-Q3", "division": "Synthetic Finance Division", "unit": "Synthetic Operations",
        "process_id": "PROC-SYN-001", "process_name": "Synthetic controlled process", "process_version": "2.0", "process_approved_at": "2026-07-01",
        "process_owner_role": "PROCESS_OWNER", "auditor_role": "AUDITOR", "lead_auditor_role": "LEAD_AUDITOR",
        "audit_scope": "Conformance, control, effectiveness and improvement", "criteria_version": "1.0.0",
        "documented_steps": ["Receive", "Validate", "Approve", "Close"], "actual_steps": ["Receive", "Validate", "Approve", "Close"],
        "criteria_results": criteria,
        "evidence_items": [{"reference":"EV-DOC","type":"controlled_document","source":"Synthetic repository","hash":"sha256:doc"},{"reference":"EV-LOG","type":"log","source":"Synthetic system","hash":"sha256:log"}],
        "transaction_samples": [{"sample_id":"TX-SYN-001","sequence_matches":True,"controls_operated":True,"authorized_approvals":True,"inputs_outputs_match":True,"roles_match":True,"timestamps_valid":True,"cross_unit_consistent":True,"workaround_detected":False,"evidence_references":["EV-LOG"]}],
        "sampling_plan_reference": "SAMPLE-PLAN-001", "evidence_plan_reference": "EVIDENCE-PLAN-001",
        "finding_review_reference": "FINDING-REVIEW-001", "human_approval_reference": "AUDITOR-DECISION-001", "assumptions": ["Synthetic evidence only"]
    }
    data.update(overrides)
    return ProcessAuditInput(**data)


class ProcessAuditAITests(unittest.TestCase):
    def setUp(self):
        self.ai = ProcessAuditAI(ROOT / "products/process-audit-ai/config/process-audit.v1.json")

    def test_fifteen_domains_and_bilingual_labels(self):
        self.assertEqual(len(self.ai.config["domains"]), 15)
        self.assertTrue(all(x["en"] and x["ar"] for x in self.ai.config["domains"]))

    def test_controlled_rating_scale(self):
        self.assertEqual(set(self.ai.config["rating_scale"]), {"0", "1", "2", "3", "4", "5"})

    def test_weighted_score_is_deterministic(self):
        result = self.ai.audit(complete_case(self.ai))
        self.assertEqual(result.overall_score_percent, 80.0)

    def test_unanswered_and_na_are_excluded(self):
        rows = complete_case(self.ai).criteria_results
        rows[0]["auditor_rating"] = None
        rows[1]["applicable"] = False
        result = self.ai.audit(complete_case(self.ai, criteria_results=rows))
        reasons = {x["reason"] for x in result.excluded_criteria}
        self.assertIn("auditor_rating_required", reasons)
        self.assertIn("not_applicable", reasons)

    def test_insufficient_evidence_not_scored(self):
        rows = complete_case(self.ai).criteria_results
        rows[0]["evidence_references"] = ["EV-DOC"]
        result = self.ai.audit(complete_case(self.ai, criteria_results=rows))
        self.assertTrue(any(x["reason"] == "insufficient_evidence_triangulation" for x in result.excluded_criteria))

    def test_auditor_override_requires_reason(self):
        rows = complete_case(self.ai).criteria_results
        rows[0]["auditor_rating"] = 3
        with self.assertRaises(ValueError):
            self.ai.audit(complete_case(self.ai, criteria_results=rows))

    def test_segregation_of_duties(self):
        with self.assertRaises(PermissionError):
            self.ai.audit(complete_case(self.ai, auditor_role="PROCESS_OWNER"))

    def test_documented_vs_actual_deviation(self):
        result = self.ai.audit(complete_case(self.ai, actual_steps=["Receive", "Manual workaround", "Close"]))
        self.assertIn("Validate", result.documented_vs_actual["missing_in_execution"])
        self.assertIn("Manual workaround", result.documented_vs_actual["unapproved_or_undocumented_steps"])

    def test_transaction_conformance(self):
        result = self.ai.audit(complete_case(self.ai))
        self.assertEqual(result.conformance_percent, 100.0)

    def test_low_critical_rating_recommends_major_draft(self):
        rows = complete_case(self.ai).criteria_results
        rows[0].update({"ai_suggested_rating": 2, "auditor_rating": 2})
        result = self.ai.audit(complete_case(self.ai, criteria_results=rows))
        finding = next(x for x in result.findings if x["criterion_id"] == "A01")
        self.assertEqual(finding["severity_recommendation"], "Major")
        self.assertEqual(finding["status"], "DRAFT_FOR_AUDITOR_REVIEW")

    def test_gate_never_auto_approves(self):
        result = self.ai.audit(complete_case(self.ai))
        self.assertEqual(result.gate_evaluation["status"], "READY_FOR_RECORDED_HUMAN_DECISION")
        self.assertFalse(result.gate_evaluation["autonomous_approval_permitted"])

    def test_capa_requires_independent_verifier(self):
        with self.assertRaises(PermissionError):
            self.ai.verify_capa("F-1", "ACTION_OWNER", "ACTION_OWNER", ["EV-1"], True, "APR-1")

    def test_capa_effectiveness_gate(self):
        result = self.ai.verify_capa("F-1", "ACTION_OWNER", "VERIFIER", [], False, None)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["close_finding_permitted"])

    def test_division_dashboard_aggregates(self):
        dash = self.ai.division_dashboard([{"division":"A","overall_score_percent":80,"major_findings":1,"minor_findings":2,"open_capa":2},{"division":"A","overall_score_percent":60,"major_findings":0,"minor_findings":1,"open_capa":1}])
        self.assertEqual(dash["divisions"][0]["average_assurance_score"], 70.0)
        self.assertFalse(dash["ai_calculation_permitted"])

    def test_no_autonomous_opinion_or_certification(self):
        for action in ["issue formal audit opinion", "certify iso 9001", "declare dgep compliance", "close finding"]:
            self.assertFalse(self.ai.check_action(action)["permitted"])
        result = self.ai.audit(complete_case(self.ai))
        self.assertIn("not an ISO certification", result.management_assurance_report["conclusion"])
        self.assertEqual(len(result.audit_digest), 64)


if __name__ == "__main__":
    unittest.main()
