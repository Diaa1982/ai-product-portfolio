import unittest
from pathlib import Path
from src.portfolio_api.p14_control_tower import AIGovernanceControlTower, UseCaseProfile

ROOT=Path(__file__).resolve().parents[1]
def profile(**overrides):
    data={"use_case_id":"UC-SYN-001","title":"Synthetic advisory","purpose":"Draft an analysis","owner_role":"PRODUCT_OWNER","data_owner_role":"DATA_OWNER","data_classification":"Internal","external_autonomous_action":False,"consequential_decision":False,"prohibited_financial_action":False,"sensitive_personal_data":False,"decision_support_at_scale":False,"public_facing":False,"human_reviewed_output":False,"agentic_autonomy_level":1,"evidence_references":["EV-1"]};data.update(overrides);return UseCaseProfile(**data)

class ControlTowerTests(unittest.TestCase):
    def setUp(self):self.tower=AIGovernanceControlTower(ROOT/"products/ai-governance-control-tower/config/governance.v1.json")
    def test_low_risk(self):self.assertEqual(self.tower.classify_risk(profile()).risk_tier,"Low")
    def test_moderate_risk(self):self.assertEqual(self.tower.classify_risk(profile(human_reviewed_output=True)).risk_tier,"Moderate")
    def test_high_risk(self):self.assertEqual(self.tower.classify_risk(profile(decision_support_at_scale=True)).risk_tier,"High")
    def test_critical_risk_and_financial_block(self):
        r=self.tower.classify_risk(profile(prohibited_financial_action=True));self.assertEqual(r.risk_tier,"Critical");self.assertTrue(r.deployment_blocked)
    def test_gate_missing_controls_blocks(self):
        r=self.tower.evaluate_gate(profile(),"G0",{},[],False,False);self.assertEqual(r.status,"blocked");self.assertIn("CTRL-OWNER",r.missing_controls)
    def test_g4_requires_qa_and_prior_approvals(self):
        ev={"CTRL-CONTINUOUS-MONITORING":"EV-1","CTRL-ROLLBACK":"EV-2"}
        r=self.tower.evaluate_gate(profile(),"G4",ev,[],False,False);self.assertIn("mandatory_qa_not_passed",r.missing_conditions);self.assertEqual(r.status,"blocked")
    def test_high_risk_g3_requires_independent_testing(self):
        p=profile(decision_support_at_scale=True);ev={"CTRL-EVALUATION":"E1","CTRL-AUDIT":"E2","CTRL-INDEPENDENT-TEST":"E3","CTRL-RED-TEAM":"E4"}
        r=self.tower.evaluate_gate(p,"G3",ev,[],True,False);self.assertIn("independent_testing_not_passed",r.missing_conditions)
    def test_only_ceo_approves_g4(self):
        with self.assertRaises(PermissionError):self.tower.approve_gate("UC1","G4","DESIGN_AUTHORITY","approved","Valid","ready_for_human_decision")
        r=self.tower.approve_gate("UC1","G4","CEO","approved","Controls accepted","ready_for_human_decision");self.assertEqual(r["decision"],"approved")
    def test_blocked_gate_cannot_be_approved(self):
        with self.assertRaises(PermissionError):self.tower.approve_gate("UC1","G1","AI_GOVERNANCE_COUNCIL","approved","Valid","blocked")
    def test_critical_monitoring_requires_safe_shutdown(self):
        r=self.tower.monitor("UC1",{"security_breach":True,"drift_score":.1});self.assertEqual(r["severity"],"Critical");self.assertEqual(r["required_action"],"safe_shutdown_and_incident_command")
    def test_high_drift_pauses(self):
        r=self.tower.monitor("UC1",{"drift_score":.4});self.assertEqual(r["severity"],"High");self.assertTrue(r["pause_required"])

if __name__=="__main__":unittest.main()
