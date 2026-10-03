import json,time,requests,sys
BASE="https://transformation-intelligence-web-staging.onrender.com"
eid="TI-SMOKE-"+str(int(time.time()))
def check(name,r,expect=(200,)):
 print(json.dumps({"step":name,"status":r.status_code,"message":r.text[:500] if "application/json" in r.headers.get("content-type","") else r.reason}))
 if r.status_code not in expect: raise SystemExit(f"BLOCKER {name}: HTTP {r.status_code} {r.text[:500]}")
check("Assessment page",requests.get(BASE+"/assessments/transformation-readiness",timeout=60))
eng={"id":eid,"organization":"Synthetic Smoke Test Org","objective":"Validate process, performance and governance diagnostic","priorities":["Processes","Performance","Governance"]}
check("Engagement creation",requests.post(BASE+"/api/diagnostics",json=eng,timeout=60))
files={
"processes.csv":"process_id,process_name,level,owner_role,status,version,notation,objective,trigger,outputs,policies,services,systems,kpis,risks,controls,last_review_date\nP1,Invoice Processing,L3,Finance Manager,ACTIVE,1.0,BPMN_2_0,Pay valid invoices,Invoice received,Payment,AP Policy,Payments,ERP,KPI-1,R1,C1,2025-01-01\nP2,Access Provisioning,L3,,ACTIVE,1.0,BPMN_2_0,Provision access,Approved request,Access,Access Policy,IT Service,ServiceDesk,KPI-2,R2,,2024-01-01\n",
"kpis.csv":"kpi_id,kpi_name,organization_level,frequency,direction,unit,target,weight,aggregation_method,kpi_owner,data_owner,data_source,period,actual,data_status,approval_date\nKPI-1,Invoice Cycle Time,Enterprise,Monthly,Lower,days,7,1,Manual,Finance Manager,Finance Analyst,ERP,2026-09,12.4,Draft,\nKPI-2,Access Within SLA,Enterprise,Monthly,Higher,%,95,1,Manual,IT Manager,IT Analyst,ServiceDesk,2026-09,72,Draft,\n",
"grc.csv":"risk_id,risk,control_id,control,owner,policy,status\nR1,Duplicate or delayed supplier payment,C1,Three-way match,Finance Manager,AP Policy,Partially effective\nR2,Unauthorized access,,,IT Manager,Access Policy,Open\nR3,Delegated authority exceeded,C3,,Finance Director,Delegation Framework,Open\n"}
for fn,body in files.items():
 r=requests.post(BASE+f"/api/diagnostics/{eid}/evidence",files={"file":(fn,body,"text/csv")},data={"classification":"Internal"},timeout=60);check("Evidence upload "+fn,r)
r=requests.post(BASE+f"/api/diagnostics/{eid}/execute",json={"domains":["Processes","Performance","Governance"]},timeout=120);check("Diagnostic execution",r)
case=r.json();print(json.dumps({"finding_count":len(case.get("findings",[])),"normalized_counts":case.get("normalized_counts"),"engine_outputs":list(case.get("engine_outputs",{}))}))
if not case.get("findings"):raise SystemExit("BLOCKER Diagnostic execution: zero findings")
f=case["findings"][0]
r=requests.post(BASE+f"/api/diagnostics/{eid}/findings/{f['finding_id']}/decision",json={"decision":"approved","reviewer_role":"DIAGNOSTIC_REVIEWER","reason":"Automated staging smoke approval"},timeout=60);check("Human approval",r)
r=requests.get(BASE+f"/api/diagnostics/{eid}/report?format=html",timeout=60);check("HTML report",r)
if "Human-approved findings" not in r.text:raise SystemExit("BLOCKER HTML report: approved findings section missing")
r=requests.get(BASE+f"/api/diagnostics/{eid}/report?format=pdf",timeout=60);check("PDF report",r)
if not r.content.startswith(b"%PDF"):raise SystemExit("BLOCKER PDF report: response is not PDF")
print(json.dumps({"SMOKE":"PASS","engagement":eid}))
