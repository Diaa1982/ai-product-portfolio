import unittest
from pathlib import Path
from src.portfolio_api.p18_maturity_certification import PFMMaturityCertification,PFMMaturityInput
ROOT=Path(__file__).parents[1]
def complete(**o):
 domains=["strategy_governance","business_architecture","financial_operations","government_financial_digital_twin","data","applications_integration","technology","cybersecurity_resilience","ai_human_oversight","risk_compliance_assurance","performance_public_value"]
 criteria=[{"criterion_id":f"CR-{i:02d}","domain":d,"weight":1,"mandatory":True,"proposed_level":3,"evidence_refs":[f"EV-{i:02d}"],"assessor_id":"A1","reviewer_id":"A2"} for i,d in enumerate(domains,1)]
 evidence=[{"evidence_id":f"EV-{i:02d}","evidence_type":"architecture_process_review","valid":True,"independently_verified":False} for i in range(1,12)]
 data={"assessment_id":"P18-SYN-001","entity_profile":"Synthetic public-finance entity","as_of_date":"2026-08-23","assessment_mode":"independent_assessment","scope_statement":"Synthetic entity-wide PFM assessment","criteria_results":criteria,"evidence_register":evidence,"assessors":[{"assessor_id":"A1","role":"LEAD_ASSESSOR"},{"assessor_id":"A2","role":"INDEPENDENT_REVIEWER"}],"performance_history":{"sustained_quarters":4},"external_comparisons":[],"moderation":{"independent_reviewer_confirmed":True,"conflicts_disclosed":True,"appeal_status":"NOT_OPEN","mandatory_principles":{"public_value":True,"human_accountability":True,"canonical_financial_events":True,"interoperability":True,"security_resilience":True,"continuous_assurance":True}},"assumptions":["Synthetic only"]};data.update(o);return PFMMaturityInput(**data)
class Tests(unittest.TestCase):
 def setUp(self):self.e=PFMMaturityCertification(ROOT/"products/pfm-maturity-certification/config/maturity.v1.json")
 def test_six_levels(self):self.assertEqual(len(self.e.config["maturity_levels"]),6)
 def test_eleven_domains(self):self.assertEqual(len(self.e.config["domains"]),11)
 def test_evidenced_level(self):self.assertEqual(self.e.assess(complete()).overall_maturity["evidenced_level"],3)
 def test_all_domains(self):self.assertEqual(len(self.e.assess(complete()).domain_results),11)
 def test_never_formal_rating(self):self.assertFalse(self.e.assess(complete()).overall_maturity["formal_rating"])
 def test_never_issues_certificate(self):self.assertFalse(self.e.assess(complete()).recognition["certificate_issued"])
 def test_candidate_class_only(self):self.assertEqual(self.e.assess(complete()).recognition["candidate_class"],"Gold candidate")
 def test_self_assessment_not_moderation_ready(self):
  r=self.e.assess(complete(assessment_mode="self_assessment"));self.assertEqual(r.assessment_status,"SELF_ASSESSMENT_ONLY");self.assertIsNone(r.recognition["candidate_class"])
 def test_missing_evidence_caps(self):
  c=complete();c.criteria_results[0]["evidence_refs"]=["UNKNOWN"];r=self.e.assess(c);self.assertEqual(r.domain_results[0]["level"],1)
 def test_level_four_requires_outcome_evidence(self):
  c=complete();c.criteria_results[0]["proposed_level"]=4;r=self.e.assess(c);self.assertIn("level_4_evidence_not_met",{x["issue"] for x in r.evidence_qa})
 def test_level_five_requires_independent_sustained_external_audited(self):
  c=complete();c.criteria_results[0]["proposed_level"]=5;r=self.e.assess(c);self.assertIn("level_5_evidence_not_met",{x["issue"] for x in r.evidence_qa})
 def test_conflict_blocks_moderation(self):
  c=complete();c.criteria_results[0]["reviewer_id"]="A1";self.assertFalse(self.e.assess(c).moderation["ready"])
 def test_missing_principle_blocks(self):
  c=complete();c.moderation["mandatory_principles"]["public_value"]=False;self.assertFalse(self.e.assess(c).conformance["mandatory_principles_passed"])
 def test_surveillance_dates(self):self.assertEqual(self.e.assess(complete()).surveillance["annual_reassessment_due"],"2027-08-23")
 def test_protected_action_and_digest(self):
  self.assertFalse(self.e.check_action("issue certificate")["permitted"]);self.assertEqual(len(self.e.assess(complete()).audit_digest),64)
if __name__=="__main__":unittest.main()
