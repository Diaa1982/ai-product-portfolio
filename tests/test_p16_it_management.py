import unittest
from pathlib import Path
from src.portfolio_api.p16_it_management import IntegratedITManagementAI, ITManagementInput

ROOT = Path(__file__).parents[1]

def complete(**overrides):
    data = {
        "assessment_id": "P16-SYN-001", "as_of_date": "2026-08-23", "operating_scope": "Synthetic IT",
        "services": [{"service_id": "S1", "owner_role": "SERVICE_OWNER", "status": "active", "evidence_refs": ["EV1"]}],
        "work_items": [
            {"work_item_id": "I1", "type": "incident", "service_id": "S1", "owner_role": "INCIDENT_MANAGER", "status": "closed", "acknowledgement_minutes": 5, "resolution_minutes": 40, "sla_minutes": 60, "evidence_refs": ["EV1"]},
            {"work_item_id": "CH1", "type": "change", "service_id": "S1", "owner_role": "CHANGE_MANAGER", "status": "implemented", "outcome": "successful", "change_type": "normal", "evidence_refs": ["EV1"]}
        ],
        "configuration_items": [{"ci_id": "CI1", "service_id": "S1", "owner_role": "ASSET_OWNER", "status": "active", "control_refs": ["C1"], "depends_on": [], "evidence_refs": ["EV1"]}],
        "portfolio_items": [{"portfolio_item_id": "P1", "owner_role": "SPONSOR", "status": "delivery", "strategy_refs": ["STR1"], "benefit_evidence_refs": ["EV1"], "delivery_risk": 2, "evidence_refs": ["EV1"]}],
        "risks_controls": [
            {"record_id": "R1", "record_type": "risk", "owner_role": "RISK_OWNER", "status": "open", "residual_score": 8, "evidence_refs": ["EV1"]},
            {"record_id": "C1", "record_type": "control", "owner_role": "CONTROL_OWNER", "status": "active", "effectiveness": "effective", "evidence_refs": ["EV1"]}
        ],
        "evidence_register": [{"evidence_id": "EV1", "valid": True}], "proposed_action": {"action": "approve_change", "reference": "CH1"}, "assumptions": ["Synthetic only"]
    }
    data.update(overrides)
    return ITManagementInput(**data)

class Tests(unittest.TestCase):
    def setUp(self): self.engine = IntegratedITManagementAI(ROOT / "products/integrated-it-management-ai/config/it-management.v1.json")
    def test_valid_integrated_assessment(self): self.assertEqual(self.engine.analyze(complete()).assessment_status, "VALID")
    def test_sla_and_mttr(self):
        r = self.engine.analyze(complete()); self.assertEqual(r.service_management["sla_attainment_percent"], 100); self.assertEqual(r.service_management["mttr_minutes"], 40)
    def test_change_success(self): self.assertEqual(self.engine.analyze(complete()).change_management["success_percent"], 100)
    def test_change_requires_authority(self): self.assertFalse(self.engine.analyze(complete()).change_management["autonomous_production_change_permitted"])
    def test_configuration_coverage(self): self.assertEqual(self.engine.analyze(complete()).configuration_quality["service_link_coverage_percent"], 100)
    def test_orphan_configuration(self):
        c=complete(); c.configuration_items[0]["service_id"]="NO"; self.assertEqual(self.engine.analyze(c).configuration_quality["orphan_count"],1)
    def test_orphan_dependency(self):
        c=complete(); c.configuration_items[0]["depends_on"]=["NO"]; self.assertIn("orphan_ci_dependency", {x["exception"] for x in self.engine.analyze(c).exceptions})
    def test_portfolio_alignment(self): self.assertEqual(self.engine.analyze(complete()).portfolio_alignment["strategy_alignment_percent"],100)
    def test_high_delivery_risk(self):
        c=complete(); c.portfolio_items[0]["delivery_risk"]=5; self.assertEqual(self.engine.analyze(c).portfolio_alignment["high_delivery_risk_count"],1)
    def test_control_evidence(self): self.assertEqual(self.engine.analyze(complete()).risk_control_readiness["evidence_coverage_percent"],100)
    def test_high_residual_risk(self):
        c=complete(); c.risks_controls[0]["residual_score"]=18; self.assertEqual(self.engine.analyze(c).risk_control_readiness["high_residual_risk_count"],1)
    def test_invalid_evidence_exception(self):
        c=complete(); c.services[0]["evidence_refs"]=["NO"]; self.assertIn("missing_or_invalid_evidence", {x["exception"] for x in self.engine.analyze(c).exceptions})
    def test_unknown_service_link(self):
        c=complete(); c.work_items[0]["service_id"]="NO"; self.assertIn("unknown_service_link", {x["exception"] for x in self.engine.analyze(c).exceptions})
    def test_protected_action(self): self.assertFalse(self.engine.check_action("accept risk")["permitted"])
    def test_digest_and_draft_decision(self):
        r=self.engine.analyze(complete()); self.assertEqual(len(r.audit_digest),64); self.assertEqual(r.decision_package["status"],"HUMAN_DECISION_REQUIRED")

if __name__ == "__main__": unittest.main()
