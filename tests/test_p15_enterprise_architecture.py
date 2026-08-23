import unittest
from pathlib import Path
from src.portfolio_api.p15_enterprise_architecture import EnterpriseArchitectureIntelligence,EnterpriseArchitectureInput
ROOT=Path(__file__).parents[1]
def el(i,t,**o):
 d={"element_id":i,"name":i,"element_type":t,"owner_role":"OWNER","lifecycle_status":"ACTIVE","criticality":3,"evidence_refs":["EV-1"]};d.update(o);return d
def rel(i,a,b,t="supports"):return {"relationship_id":i,"from_id":a,"to_id":b,"relationship_type":t,"evidence_refs":["EV-1"]}
def complete(**o):
 es=[el("S1","strategy_outcome"),el("C1","capability"),el("P1","process"),el("SV1","service"),el("K1","kpi"),el("R1","risk"),el("CT1","control"),el("A1","application",business_fit=4,technical_health=4),el("I1","interface",security_control_refs=["SC1"]),el("D1","data_object",data_classification="INTERNAL"),el("DB1","database"),el("T1","technology",support_status="supported")]
 rs=[rel("L1","C1","S1"),rel("L2","C1","P1"),rel("L3","P1","SV1"),rel("L4","P1","A1"),rel("L5","P1","K1","measures"),rel("L6","P1","R1"),rel("L7","P1","CT1"),rel("L8","SV1","A1"),rel("L9","A1","I1"),rel("L10","A1","D1"),rel("L11","A1","T1"),rel("L12","D1","DB1")]
 d={"assessment_id":"P15-SYN-001","repository_name":"Synthetic EA","repository_version":"1","as_of_date":"2026-08-23","elements":es,"relationships":rs,"evidence_register":[{"evidence_id":"EV-1","valid":True}],"impact_targets":["A1"],"proposed_change":{"adr_id":"ADR-1","title":"Synthetic change","cross_layer":True,"alternatives":["A","B"],"principle_refs":["INTEROPERABILITY"],"risk_refs":["R1"],"evidence_refs":["EV-1"]},"assumptions":["Synthetic only"]};d.update(o);return EnterpriseArchitectureInput(**d)
class Tests(unittest.TestCase):
 def setUp(self):self.e=EnterpriseArchitectureIntelligence(ROOT/"products/enterprise-architecture-intelligence/config/enterprise-architecture.v1.json")
 def test_valid_repository(self):self.assertEqual(self.e.analyze(complete()).repository_status,"VALID")
 def test_full_traceability(self):self.assertEqual(self.e.analyze(complete()).traceability["coverage_percent"],100)
 def test_duplicate_id(self):
  c=complete();c.elements.append(el("A1","application"));self.assertIn("duplicate_element_id",{x["exception"] for x in self.e.analyze(c).quality_exceptions})
 def test_orphan_relationship(self):
  c=complete();c.relationships.append(rel("X","A1","NO"));self.assertIn("orphan_relationship",{x["exception"] for x in self.e.analyze(c).quality_exceptions})
 def test_self_relationship(self):
  c=complete();c.relationships.append(rel("X","A1","A1"));self.assertIn("self_relationship",{x["exception"] for x in self.e.analyze(c).quality_exceptions})
 def test_invalid_evidence(self):
  c=complete();c.elements[0]["evidence_refs"]=["NO"];self.assertIn("missing_or_invalid_evidence",{x["exception"] for x in self.e.analyze(c).quality_exceptions})
 def test_impact_transitive(self):self.assertGreater(len(self.e.analyze(complete()).impact_analysis[0]["affected"]),3)
 def test_unknown_impact_target(self):
  c=complete(impact_targets=["NO"]);self.assertEqual(self.e.analyze(c).impact_analysis[0]["status"],"UNKNOWN_TARGET")
 def test_application_tolerate(self):self.assertEqual(self.e.analyze(complete()).application_portfolio[0]["recommendation"],"TOLERATE")
 def test_application_modernize(self):
  c=complete();a=next(x for x in c.elements if x["element_id"]=="A1");a.update(criticality=5,technical_health=1);self.assertEqual(self.e.analyze(c).application_portfolio[0]["recommendation"],"MODERNIZE")
 def test_duplicate_app_investigation(self):
  c=complete();a=next(x for x in c.elements if x["element_id"]=="A1");a["duplicate_group"]="G";c.elements.append(el("A2","application",duplicate_group="G"));self.assertEqual(self.e.analyze(c).application_portfolio[0]["recommendation"],"INVESTIGATE_DUPLICATION")
 def test_unsupported_technology_debt(self):
  c=complete();next(x for x in c.elements if x["element_id"]=="T1")["support_status"]="unsupported";self.assertGreater(self.e.analyze(c).architecture_debt["item_count"],0)
 def test_adr_draft(self):self.assertEqual(self.e.analyze(complete()).decision_record["status"],"DRAFT_FOR_DESIGN_AUTHORITY")
 def test_change_classification(self):self.assertEqual(self.e.classify_change(False,True,False,False,False)["classification"],"major")
 def test_protected_action_and_digest(self):self.assertFalse(self.e.check_action("decommission application")["permitted"]);self.assertEqual(len(self.e.analyze(complete()).audit_digest),64)
if __name__=="__main__":unittest.main()
