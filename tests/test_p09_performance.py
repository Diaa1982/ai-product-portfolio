import unittest
from pathlib import Path
from src.portfolio_api.p09_performance import CorporatePerformanceReview, KPIReviewInput

ROOT=Path(__file__).resolve().parents[1]
def review_input(**overrides):
    master={"KPI_ID":"KPI-001","KPI_Name":"Synthetic service performance","Organization_Level":"Enterprise","Frequency":"Quarterly","Direction":"Higher","Unit":"%","Target":95,"Weight":10,"Aggregation_Method":"Average","KPI_Owner":"PERFORMANCE_OWNER","Data_Owner":"DATA_OWNER","Data_Source":"Synthetic KPI register","Tolerance":0}
    result={"KPI_ID":"KPI-001","Period":"2026-Q2","Actual":100,"Target":95,"Forecast":98,"Evidence_Reference":"EV-SYN-1","Owner_Comment":"Validated","Root_Cause":"Synthetic","Existing_Action":"Monitor","Data_Status":"Official","Approval_Date":"2026-07-10"}
    data={"kpi_master":master,"result":result,"source_row_hash":"a"*64,"data_cutoff":"2026-07-01","prior_actual":94,"owner_explanation":"Owner confirmed improvement.","inference":"Performance is above target.","recommendation":"Retain controls and monitor.","corrective_actions":[],"target_treatment":"Retain","proposed_target":None,"review_due_at":"2026-07-15T00:00:00Z","submitted_at":"2026-07-10T00:00:00Z","executive_briefing":False};data.update(overrides);return KPIReviewInput(**data)

class PerformanceReviewTests(unittest.TestCase):
    def setUp(self):self.engine=CorporatePerformanceReview(ROOT/"products/corporate-performance-review-ai/config/performance.v1.json")
    def test_higher_direction_exceeded(self):
        r=self.engine.review(review_input());self.assertEqual(r.performance_status,"Exceeded");self.assertEqual(r.review_calendar_status,"On Time")
    def test_lower_direction(self):
        x=review_input();x.kpi_master["Direction"]="Lower";x.result["Target"]=10;x.result["Actual"]=8;r=self.engine.review(x);self.assertEqual(r.performance_status,"Exceeded")
    def test_official_result_requires_evidence(self):
        x=review_input();x.result["Evidence_Reference"]="";r=self.engine.review(x);self.assertEqual(r.data_quality_status,"Invalid");self.assertIn("official_result_missing_evidence",r.data_issues)
    def test_zero_target_requires_specialized_review(self):
        x=review_input();x.result["Target"]=0;r=self.engine.review(x);self.assertEqual(r.performance_score,None);self.assertEqual(r.performance_status,"Specialized Review")
    def test_exact_within_tolerance(self):
        x=review_input();x.kpi_master["Direction"]="Exact";x.kpi_master["Tolerance"]=1;x.result["Target"]=10;x.result["Actual"]=10.5;r=self.engine.review(x);self.assertEqual(r.performance_status,"Achieved")
    def test_late_submission(self):
        r=self.engine.review(review_input(submitted_at="2026-07-20T00:00:00Z"));self.assertEqual(r.review_calendar_status,"Late")
    def test_incomplete_corrective_action_invalid(self):
        r=self.engine.review(review_input(corrective_actions=[{"action":"Fix"}]));self.assertEqual(r.data_quality_status,"Invalid")
    def test_proposed_target_not_approved(self):
        r=self.engine.review(review_input(target_treatment="Stretch",proposed_target=98));self.assertEqual(r.proposed_target_status,"NOT APPROVED");self.assertTrue(r.approval_required)
    def test_output_layers_remain_separate(self):
        r=self.engine.review(review_input());self.assertIn("actual is",r.fact);self.assertIn("variance",r.calculation);self.assertNotEqual(r.owner_explanation,r.inference)
    def test_executive_approval_role(self):
        with self.assertRaises(PermissionError):self.engine.approve("R1","executive_briefing","PERFORMANCE_OWNER","approved","Valid")
        r=self.engine.approve("R1","executive_briefing","EXECUTIVE_APPROVER","approved","Evidence accepted");self.assertEqual(r["decision"],"approved")

if __name__=="__main__":unittest.main()
