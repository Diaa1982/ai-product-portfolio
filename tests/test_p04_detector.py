import unittest
from pathlib import Path

from src.portfolio_api.p04_detector import DetectionInput, SignalDetector

ROOT = Path(__file__).resolve().parents[1]

def candidate(**overrides):
    high={"jurisdictional_scope":.9,"industry_breadth":.8,"time_sensitivity":.9,"evidence_strength":.95,"novelty":.85,"stakeholder_relevance":.9}
    confidence={"evidence":.95,"classification":.9,"novelty":.85,"corroboration":.8,"extraction_quality":.9,"recommendation_coherence":.85}
    data={"title":"Synthetic revenue change","creation_mode":"automated_version_change","audience":"government","signal_category":"Trade, customs, tax, tariff, subsidy and market access","pfm_focus":"Systemic fiscal risk","affected_entities":["Synthetic entity"],"effective_date":"2026-09-01","source_id":"SYN-OFFICIAL-P04","source_url":"https://official.example/tax/1","current_version":"v2","current_hash":"b"*64,"prior_version":"v1","prior_hash":"a"*64,"snapshot_path":"synthetic/p04/current.json","fetched_at":"2026-08-21T00:00:00Z","published_at":"2026-08-20T00:00:00Z","issuing_authority":"Synthetic Authority","provenance_token":"PV-SYN-001","citations":[{"exact_span":"Synthetic rate changed.","page":1}],"change_summary":"Rate changed from A to B.","evidence_quality":"verified","materiality_scores":high,"confidence_scores":confidence,"fact":"The synthetic rate changed.","interpretation":"Revenue assumptions may require review.","recommendation":"Validate fiscal impact with the revenue owner.","opportunity":"Refresh the medium-term revenue scenario.","risk":"Forecast variance if assumptions remain unchanged.","scenario":"Test baseline and downside revenue paths.","kpi_hypothesis":"Revenue forecast variance may increase.","high_impact":False}
    data.update(overrides);return DetectionInput(**data)

class SignalDetectorTests(unittest.TestCase):
    def setUp(self): self.detector=SignalDetector(ROOT/"products/signal-detection-agent/config/detection.v1.json")
    def test_weights(self):
        self.assertEqual(sum(x["weight"] for x in self.detector.config["materiality_criteria"]),1.0)
        self.assertEqual(sum(x["weight"] for x in self.detector.config["confidence_criteria"]),1.0)
    def test_verified_change_routes_priority_review(self):
        r=self.detector.detect(candidate());self.assertEqual(r.evidence_status,"verified");self.assertEqual(r.review_route,"priority_analyst_review");self.assertEqual(r.publication_status,"not_published_analyst_review_required")
    def test_unknown_source_blocks(self):
        r=self.detector.detect(candidate(source_id="UNKNOWN"));self.assertEqual(r.detection_status,"blocked")
    def test_missing_exact_citation_blocks(self):
        r=self.detector.detect(candidate(citations=[{"page":1}]));self.assertIn("citation_missing_exact_span",r.evidence_issues)
    def test_manual_creation_blocks(self):
        r=self.detector.detect(candidate(creation_mode="manual"));self.assertEqual(r.evidence_status,"blocked")
    def test_no_change_creates_no_signal(self):
        r=self.detector.detect(candidate(current_hash="a"*64,current_version="v1"));self.assertEqual(r.detection_status,"no_material_change")
    def test_conflicting_evidence_routes_review(self):
        r=self.detector.detect(candidate(evidence_quality="conflict"));self.assertEqual(r.review_route,"analyst_evidence_review")
    def test_high_impact_requires_approval(self):
        r=self.detector.detect(candidate(high_impact=True));self.assertTrue(r.human_approval_required);self.assertEqual(r.publication_status,"pending_human_approval")
    def test_only_authority_approves(self):
        with self.assertRaises(PermissionError):self.detector.approve("S1","executive_alert","ANALYST","approved","Valid")
        r=self.detector.approve("S1","executive_alert","STRATEGY_RISK_AUTHORITY","approved","Evidence accepted");self.assertEqual(r["decision"],"approved")

if __name__=="__main__":unittest.main()
