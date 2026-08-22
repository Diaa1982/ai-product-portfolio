import json
import unittest
from pathlib import Path

from src.portfolio_api.p05_service_design import ServiceDesignAI, ServiceDesignInput


ROOT = Path(__file__).parents[1]


def complete_case(**overrides):
    stages = [{"stage": name, "touchpoints": ["Institutional portal"], "steps": ["Submit and validate"], "entities": ["Government entity", "DOF"], "systems": ["Synthetic service platform"], "pain_points": [], "evidence": [f"EV-{i:02d}"]} for i, name in enumerate(["Awareness & Reach", "Engagement & Access", "Service Delivery", "Post-Service", "Continuous Experience"], 1)]
    data = {
        "case_id": "SD-SYN-001", "service_id": "SVC-SYN-001", "service_name": "Synthetic institutional request",
        "explicit_request": True, "customer_type": "government_entity", "direct_individual_service": False,
        "service_owner_role": "SERVICE_OWNER", "provider_roles": ["SERVICE_TEAM"], "beneficiary_groups": ["Government entities"],
        "legal_mandate_reference": "LAW-SYN-001", "evidence_references": ["EV-SYN-001"], "trigger": "Authorized request received",
        "objective": "Provide a traceable institutional outcome", "channels": ["Institutional portal"], "inputs": ["Authorized request"],
        "outputs": ["Validated response"], "dependencies": ["Identity and records"], "escalation_path": "SERVICE_OWNER",
        "process_id": "PROC-SYN-001", "sla_target": "5 working days (proposal)", "kpis": ["cycle_time", "first_time_right"],
        "stages": stages, "proactive_trigger": "Mandate event", "data_reuse": "Approved institutional master data",
        "inclusivity_considerations": ["Accessible institutional channel"], "current_state_summary": "Synthetic AS-IS validated for test.",
        "desired_outcome": "Reduce avoidable handoffs with human accountability.",
        "evidence_items": [{"claim": "The synthetic service has an approved owner.", "classification": "fact", "reference": "EV-SYN-001"}, {"claim": "A unified intake may reduce handoffs.", "classification": "ai_inference", "reference": ""}],
        "selected_methods": ["three_round_brainstorming", "six_thinking_hats", "five_whys", "journey_mapping", "service_blueprinting"],
        "gate": "G1", "human_approval_reference": "APR-SYN-G1", "improvement_options": ["Unified intake"],
        "prototype_test_evidence": ["TEST-SYN-001"], "risk_controls": ["Human validation"],
        "operating_raci": {"accountable": "SERVICE_OWNER"}, "benefits_baseline": ["10 handoffs"],
        "monitoring_evidence": ["MON-SYN-001"], "improvement_decision": "Continue pilot"
    }
    data.update(overrides)
    return ServiceDesignInput(**data)


class ServiceDesignAITests(unittest.TestCase):
    def setUp(self):
        self.ai = ServiceDesignAI(ROOT / "products/service-design-ai/config/service-design.v1.json")

    def test_controlled_counts(self):
        self.assertEqual(len(self.ai.config["deliverables"]), 54)
        self.assertEqual(len(self.ai.config["registers"]), 8)
        self.assertEqual(len(self.ai.config["gates"]), 6)

    def test_public_benefit_classification(self):
        self.assertEqual(self.ai.classify_service(False, "institutional_public"), "PUBLIC_BENEFIT")

    def test_g2g_classification(self):
        self.assertEqual(self.ai.classify_service(True, "government_entity"), "G2G")

    def test_g2b_classification(self):
        self.assertEqual(self.ai.classify_service(True, "financial_institution"), "G2B")

    def test_direct_individual_service_is_out_of_profile(self):
        with self.assertRaises(ValueError):
            self.ai.design(complete_case(direct_individual_service=True))

    def test_missing_inputs_are_coached(self):
        result = self.ai.design(complete_case(legal_mandate_reference="", evidence_references=[]))
        self.assertEqual(result.completeness_status, "insufficient_information")
        self.assertIn("legal_mandate_reference", result.missing_information)
        self.assertTrue(any(x["field"] == "evidence_references" for x in result.missing_input_coaching))

    def test_five_stages_are_required(self):
        result = self.ai.design(complete_case(stages=[]))
        self.assertEqual(sum(x.startswith("journey_stage:") for x in result.missing_information), 5)

    def test_evidence_classifications_are_preserved(self):
        result = self.ai.design(complete_case())
        self.assertEqual(len(result.evidence_by_classification["fact"]), 1)
        self.assertEqual(len(result.evidence_by_classification["ai_inference"]), 1)

    def test_brainstorming_executes_three_rounds(self):
        result = self.ai.design(complete_case())
        self.assertEqual(len(result.method_workspace["three_round_brainstorming"]), 3)

    def test_six_hats_all_present(self):
        hats = self.ai.design(complete_case()).method_workspace["six_thinking_hats"]
        self.assertEqual(set(hats), {"white", "red", "black", "yellow", "green", "blue"})

    def test_service_card_journey_blueprint(self):
        result = self.ai.design(complete_case())
        self.assertEqual(result.service_card["classification"], "G2G")
        self.assertEqual(len(result.journey), 5)
        self.assertEqual(len(result.blueprint), 6)

    def test_g1_can_be_ready_for_recorded_decision(self):
        result = self.ai.design(complete_case())
        self.assertEqual(result.gate_evaluation["status"], "READY_FOR_RECORDED_DECISION")
        self.assertFalse(result.gate_evaluation["autonomous_approval_permitted"])

    def test_gate_blocks_without_approval(self):
        result = self.ai.design(complete_case(gate="G4", human_approval_reference=None, prototype_test_evidence=[]))
        self.assertEqual(result.gate_evaluation["status"], "BLOCKED")
        self.assertIn("human_approval_reference", result.gate_evaluation["missing_requirements"])

    def test_protected_actions_are_denied(self):
        check = self.ai.check_action("launch service")
        self.assertFalse(check["permitted"])
        self.assertTrue(check["human_approval_required"])

    def test_report_has_audit_digest_and_no_certification(self):
        result = self.ai.design(complete_case())
        self.assertEqual(len(result.audit_digest), 64)
        self.assertIn("alignment assumptions", " ".join(result.limitations).lower())
        self.assertEqual(result.deliverable_control["controlled_total"], 54)


if __name__ == "__main__":
    unittest.main()
