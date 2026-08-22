import unittest
from pathlib import Path
from src.portfolio_api.p17_cycle_time_benchmark import PFMCycleTimeBenchmark, CycleTimeBenchmarkInput

ROOT=Path(__file__).parents[1]
def complete(**o):
    p={"process_id":"P-BUD-01","process_name":"Budget circular response","l1_domain":"budget","start_point":"Circular received","end_point":"Detailed estimates completed","scope_profile":"Standard entity","unit":"days","actual_cycle_times":[35,36,38,40,41],"waiting_time":8,"rework_rate":.05,"aggregation_method":"single_process","steps_consecutive":False,"volume_weights":[]}
    b={"process_id":"P-BUD-01","matched_process":"Budget circular response","match_type":"exact","match_rationale":"Exact boundary and scope","benchmark_type":"pfm_performance_threshold","reliability_class":"B","benchmark_value":42,"unit":"days","start_point":"Circular received","end_point":"Detailed estimates completed","scope_profile":"Standard entity","source_id":"SRC-PEFA-SYN","source_url":"https://example.invalid/synthetic-pefa-reference","evidence_note":"Synthetic representation of a six-week performance threshold; not a transaction benchmark"}
    d={"assessment_id":"P17-SYN-001","as_of_date":"2026-08-22","jurisdiction_profile":"Synthetic public-finance entity","processes":[p],"benchmark_register":[b],"source_library":[{"source_id":"SRC-PEFA-SYN","publisher":"Synthetic authoritative source","version":"synthetic","license_status":"review_required"}],"assumptions":["Synthetic only"]};d.update(o);return CycleTimeBenchmarkInput(**d)
class Tests(unittest.TestCase):
 def setUp(self):self.e=PFMCycleTimeBenchmark(ROOT/"products/pfm-cycle-time-benchmark/config/cycle-time.v1.json")
 def test_median_and_average(self):
  r=self.e.analyze(complete()).process_results[0];self.assertEqual(r["actual_median"],38);self.assertEqual(r["actual_average"],38)
 def test_exact_comparison(self):self.assertTrue(self.e.analyze(complete()).process_results[0]["comparison_eligible"])
 def test_threshold_interpretation(self):self.assertEqual(self.e.analyze(complete()).process_results[0]["interpretation"],"WITHIN_THRESHOLD")
 def test_gap(self):self.assertEqual(self.e.analyze(complete()).process_results[0]["gap"],-4)
 def test_missing_source_suppresses_value(self):
  c=complete(source_library=[]);r=self.e.analyze(c);self.assertIsNone(r.process_results[0]["benchmark_value"]);self.assertTrue(r.source_qa)
 def test_missing_url_suppresses_value(self):
  c=complete();c.benchmark_register[0]["source_url"]="";self.assertIsNone(self.e.analyze(c).process_results[0]["benchmark_value"])
 def test_proxy_is_directional(self):
  c=complete();c.benchmark_register[0].update(match_type="proxy",reliability_class="C");r=self.e.analyze(c).process_results[0];self.assertTrue(r["directional_only"]);self.assertIsNone(r["gap"])
 def test_d_class_suppresses_value(self):
  c=complete();c.benchmark_register[0].update(reliability_class="D",match_type="no_data");self.assertIsNone(self.e.analyze(c).process_results[0]["benchmark_value"])
 def test_boundary_mismatch_blocks_comparison(self):
  c=complete();c.benchmark_register[0]["start_point"]="Different";c.benchmark_register[0]["end_point"]="Different";self.assertFalse(self.e.analyze(c).process_results[0]["comparison_eligible"])
 def test_nearest_requires_rationale(self):
  c=complete();c.benchmark_register[0].update(match_type="nearest",match_rationale="");self.assertIn("missing_match_rationale",{x["issue"] for x in self.e.analyze(c).methodology_qa})
 def test_small_sample_flag(self):
  c=complete();c.processes[0]["actual_cycle_times"]=[1,2];self.assertIn("small_internal_sample",{x["issue"] for x in self.e.analyze(c).methodology_qa})
 def test_parallel_requires_critical_path(self):
  c=complete();c.processes[0].update(aggregation_method="sequential_sum",steps_consecutive=False);self.assertIn("nonconsecutive_steps_cannot_be_summed",{x["issue"] for x in self.e.analyze(c).methodology_qa})
 def test_mixed_volume_requires_weights(self):
  c=complete();c.processes[0]["aggregation_method"]="volume_weighted_average";self.assertIn("missing_volume_weights",{x["issue"] for x in self.e.analyze(c).methodology_qa})
 def test_no_benchmark_queue(self):
  r=self.e.analyze(complete(benchmark_register=[]));self.assertEqual(r.unbenchmarked_queue[0]["reason"],"no_benchmark_record")
 def test_protected_actions_and_digest(self):
  self.assertFalse(self.e.check_action("approve SLA")["permitted"]);self.assertEqual(len(self.e.analyze(complete()).audit_digest),64)
if __name__=="__main__":unittest.main()
