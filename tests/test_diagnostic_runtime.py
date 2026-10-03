from pathlib import Path
from src.portfolio_api.diagnostic.runtime import DiagnosticRuntime

def test_diagnostic_vertical_slice(tmp_path: Path):
    r=DiagnosticRuntime(tmp_path)
    e={'id':'TI-DIAG-TEST','organization':'Test Org','priorities':['Processes','Performance','Governance']}
    r.create(e)
    stored=r.upload(e['id'],'evidence.txt','text/plain',b'process owner workflow KPI target actual risk control policy approval')
    assert stored.extraction_status=='extracted'
    case=r.execute(e['id'],e['priorities'])
    assert case['status']=='human_review'
    assert len(case['findings'])==3
    first=case['findings'][0]
    r.decide(e['id'],first['finding_id'],'approved','DIAGNOSTIC_REVIEWER','Evidence checked')
    report=r.report(e['id'])
    assert report['report_status']=='reviewed'
