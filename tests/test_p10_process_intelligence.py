import unittest
from pathlib import Path
from src.portfolio_api.p10_process_intelligence import EnterpriseProcessIntelligence,ProcessPortfolioInput
ROOT=Path(__file__).parents[1]
def process(pid,guid,level,parent,notation="VAC",**o):
 d={"process_id":pid,"process_guid":guid,"name":pid,"level":level,"parent_id":parent,"owner_role":"PROCESS_OWNER","status":"ACTIVE","version":"1.0","notation":notation,"objective":"Outcome","trigger":"Need","outputs":["Output"],"policies":["POL-1"],"services":["SVC-1"],"systems":["SYS-1"],"kpis":["KPI-1"],"risks":["R-1"],"controls":["C-1"],"last_review_date":"2026-01-01","review_triggers":[]};d.update(o);return d
def complete(**o):
 rows=[process("L1-1","G1","L1",None),process("L2-1","G2","L2","L1-1"),process("L3-1","G3","L3","L2-1","BPMN_2_0"),process("L4-1","G4","L4","L3-1","BPMN_2_0"),process("L5-1","G5","L5","L4-1","BPMN_2_0")]
 controls=["security_clearance","complete_export","guid_preservation","hierarchy_preservation","model_conversion_poc","ea_link_preservation","workflow_validation","attachment_export","audit_history_export","identity_rbac","uae_approved_residency","encryption_keys","siem_logs","dr_rto_rpo","exit_rights","sbom_secure_sdlc","no_critical_findings"]
 d={"assessment_id":"EPI-SYN-1","as_of_date":"2026-08-22","repository_name":"Synthetic","repository_version":"1","processes":rows,"maturity_evidence":[{"domain":"governance","score":3,"evidence_references":["EV-1"]}],"migration_evidence":{x:"EV-"+x for x in controls}};d.update(o);return ProcessPortfolioInput(**d)
class Tests(unittest.TestCase):
 def setUp(self):self.ai=EnterpriseProcessIntelligence(ROOT/"products/enterprise-process-intelligence/config/process-intelligence.v1.json")
 def test_hierarchy(self):self.assertEqual(list(self.ai.config["hierarchy"]),["L1","L2","L3","L4","L5"])
 def test_notation(self):self.assertEqual(self.ai.analyze(complete()).validation_status,"VALID")
 def test_duplicate_id(self):
  c=complete();c.processes[1]["process_id"]="L1-1";self.assertIn("duplicate_process_id",{x["exception"] for x in self.ai.analyze(c).exceptions})
 def test_duplicate_guid(self):
  c=complete();c.processes[1]["process_guid"]="G1";self.assertIn("duplicate_process_guid",{x["exception"] for x in self.ai.analyze(c).exceptions})
 def test_orphan(self):
  c=complete();c.processes[2]["parent_id"]="X";self.assertIn("orphan_process",{x["exception"] for x in self.ai.analyze(c).exceptions})
 def test_wrong_notation(self):
  c=complete();c.processes[2]["notation"]="VAC";self.assertIn("notation_mismatch",{x["exception"] for x in self.ai.analyze(c).exceptions})
 def test_traceability(self):self.assertEqual(self.ai.analyze(complete()).traceability["coverage_percent"],100)
 def test_missing_link(self):
  c=complete();c.processes[2]["risks"]=[];self.assertLess(self.ai.analyze(c).traceability["coverage_percent"],100)
 def test_annual_review(self):
  c=complete();c.processes[0]["last_review_date"]="2024-01-01";self.assertTrue(self.ai.analyze(c).review_due)
 def test_trigger_review(self):
  c=complete();c.processes[0]["review_triggers"]=["audit"];self.assertIn("trigger:audit",{x["reason"] for x in self.ai.analyze(c).review_due})
 def test_maturity_requires_evidence(self):self.assertIsNone(self.ai.analyze(complete(maturity_evidence=[{"domain":"x","score":4,"evidence_references":[]}])).maturity["average"])
 def test_migration_ready(self):self.assertEqual(self.ai.analyze(complete()).migration_readiness["status"],"READY_FOR_CONTROLLED_POC")
 def test_migration_blocked(self):self.assertEqual(self.ai.analyze(complete(migration_evidence={})).migration_readiness["status"],"BLOCKED")
 def test_change_routes(self):
  self.assertEqual(self.ai.classify_change(False,False,False,False,True)["classification"],"minor");self.assertEqual(self.ai.classify_change(True,False,False,False,False)["classification"],"major")
 def test_protected_actions(self):
  self.assertFalse(self.ai.check_action("publish process")["permitted"]);self.assertFalse(self.ai.check_action("approve vendor")["permitted"]);self.assertEqual(len(self.ai.analyze(complete()).audit_digest),64)
if __name__=="__main__":unittest.main()
