from pathlib import Path
from src.portfolio_api.diagnostic.runtime import DiagnosticRuntime
from src.portfolio_api.diagnostic.reporting import render_html,render_pdf

def test_diagnostic_vertical_slice(tmp_path:Path):
    r=DiagnosticRuntime(tmp_path)
    e={"id":"TI-DIAG-TEST","organization":"Test Org","objective":"Validate operating model","priorities":["Processes","Performance","Governance"]}
    r.create(e)
    csv=b"process_id,process_name,level,owner_role,status,version,notation,objective,trigger,outputs,policies,services,systems,kpis,risks,controls\nP1,Proc,L3,Owner,ACTIVE,1.0,BPMN_2_0,Objective,Request,Output,Policy,Service,System,K1,R1,C1"
    stored=r.upload(e["id"],"processes.csv","text/csv",csv)
    assert stored.extraction_status=="extracted"
    case=r.execute(e["id"],e["priorities"])
    assert case["status"]=="human_review"
    assert case["normalized_counts"]["processes"]==1
    assert "process" in case["engine_outputs"]
    first=case["findings"][0]
    r.decide(e["id"],first["finding_id"],"approved","DIAGNOSTIC_REVIEWER","Evidence checked")
    report=r.report(e["id"])
    assert report["report_status"]=="reviewed"
    assert all(x["status"] in {"approved","modified"} for x in report["approved_findings"])
    assert "Human-approved findings" in render_html(report)
    assert render_pdf(report).startswith(b"%PDF")
