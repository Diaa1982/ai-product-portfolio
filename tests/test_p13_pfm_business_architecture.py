import unittest
from pathlib import Path

from src.portfolio_api.p13_pfm_business_architecture import PFMBusinessArchitecture, PFMArchitectureInput

ROOT = Path(__file__).parents[1]


def capability(i, stage, **overrides):
    row = {
        "capability_id": f"CAP-{i:02d}", "name": f"Capability {i}", "domain": "budget_management",
        "owner_role": "CAPABILITY_OWNER", "mandate_refs": ["MAN-1"], "value_chain_stage": stage,
        "process_refs": [f"PROC-{i}"], "service_refs": [f"SVC-{i}"], "information_objects": ["Budget"],
        "system_refs": ["REFERENCE-GRP"], "kpi_refs": [f"KPI-{i}"], "risk_refs": [f"RISK-{i}"],
        "control_refs": [f"CTRL-{i}"], "evidence_refs": [f"EV-{i}"], "pefa_refs": ["budget_reliability"],
        "ipsas_refs": [], "current_maturity": 2, "target_maturity": 4, "criticality": 4,
    }
    row.update(overrides)
    return row


def complete(**overrides):
    capabilities = [capability(i, f"VC{i:02d}") for i in range(1, 12)]
    data = {
        "assessment_id": "P13-SYN-001", "jurisdiction_profile": "Synthetic local public-finance entity",
        "as_of_date": "2026-08-22", "target_horizon": "2029", "public_value_outcomes": ["Fiscal sustainability"],
        "mandates": [{"mandate_id": "MAN-1", "title": "Synthetic mandate", "status": "DRAFT"}],
        "capabilities": capabilities,
        "evidence": [{"evidence_id": f"EV-{i}", "type": "approved_record", "source": "synthetic"} for i in range(1, 12)],
        "assumptions": ["All records are synthetic"],
    }
    data.update(overrides)
    return PFMArchitectureInput(**data)


class Tests(unittest.TestCase):
    def setUp(self):
        self.engine = PFMBusinessArchitecture(ROOT / "products/pfm-business-architecture/config/pfm-architecture.v1.json")

    def test_config_has_eleven_stages(self): self.assertEqual(len(self.engine.config["value_chain"]), 11)
    def test_config_has_fifteen_domains(self): self.assertEqual(len(self.engine.config["l1_capability_domains"]), 15)
    def test_complete_traceability(self): self.assertEqual(self.engine.analyze(complete()).coverage["coverage_percent"], 100)
    def test_complete_value_chain(self): self.assertFalse(self.engine.analyze(complete()).value_chain["missing_stages"])
    def test_duplicate_capability(self):
        c = complete(); c.capabilities[1]["capability_id"] = "CAP-01"
        self.assertIn("duplicate_capability_id", {x["exception"] for x in self.engine.analyze(c).exceptions})
    def test_invalid_stage(self):
        c = complete(); c.capabilities[0]["value_chain_stage"] = "VC99"
        self.assertIn("invalid_value_chain_stage", {x["exception"] for x in self.engine.analyze(c).exceptions})
    def test_missing_link_reduces_coverage(self):
        c = complete(); c.capabilities[0]["control_refs"] = []
        self.assertLess(self.engine.analyze(c).coverage["coverage_percent"], 100)
    def test_unknown_mandate(self):
        c = complete(); c.capabilities[0]["mandate_refs"] = ["UNKNOWN"]
        self.assertIn("unknown_mandate_reference", {x["exception"] for x in self.engine.analyze(c).exceptions})
    def test_unknown_evidence_excludes_maturity(self):
        c = complete(); c.capabilities[0]["evidence_refs"] = ["UNKNOWN"]
        row = next(x for x in self.engine.analyze(c).capability_heatmap if x["capability_id"] == "CAP-01")
        self.assertEqual(row["evidence_status"], "INSUFFICIENT_EVIDENCE")
    def test_invalid_maturity(self):
        c = complete(); c.capabilities[0]["current_maturity"] = 6
        self.assertIn("invalid_current_maturity", {x["exception"] for x in self.engine.analyze(c).exceptions})
    def test_priority_is_transparent(self):
        row = next(x for x in self.engine.analyze(complete()).capability_heatmap if x["capability_id"] == "CAP-01")
        self.assertEqual(row["priority_score"], 8)
    def test_roadmap_is_draft(self): self.assertTrue(all(x["status"] == "DRAFT" for x in self.engine.analyze(complete()).roadmap))
    def test_alignment_not_compliance(self):
        result = self.engine.analyze(complete())
        self.assertFalse(result.alignment["pefa"]["compliance_conclusion"]); self.assertFalse(result.alignment["ipsas"]["compliance_conclusion"])
    def test_protected_action(self): self.assertFalse(self.engine.check_action("approve operating model")["permitted"])
    def test_digest_is_deterministic(self):
        self.assertEqual(self.engine.analyze(complete()).audit_digest, self.engine.analyze(complete()).audit_digest)


if __name__ == "__main__": unittest.main()
