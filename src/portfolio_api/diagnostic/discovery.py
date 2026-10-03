from __future__ import annotations
from dataclasses import dataclass,asdict
import re

DOMAINS=("Processes","Performance","Governance")
QUESTION_LIBRARY=[
 {"id":"PROC-OWN-01","domain":"Processes","dimension":"ownership","priority":100,"prompt":"Do your major end-to-end processes have formally assigned accountable owners?","options":["Yes, for most","For some","No","I don't know"],"critical":True},
 {"id":"PROC-DOC-01","domain":"Processes","dimension":"documentation","priority":90,"prompt":"Approximately how much of your major process landscape is documented?","options":["Most","About half","A small number","None","I don't know"],"critical":True},
 {"id":"PROC-PERF-01","domain":"Processes","dimension":"performance","priority":80,"prompt":"Do you measure process performance such as cycle time, volume, backlog or SLA achievement?","options":["Yes, consistently","For some processes","Rarely","No","I don't know"],"critical":False},
 {"id":"PERF-KPI-01","domain":"Performance","dimension":"kpis","priority":100,"prompt":"Are organizational KPIs formally defined with targets and accountable owners?","options":["Yes, for most","For some","No","I don't know"],"critical":True},
 {"id":"PERF-ACT-01","domain":"Performance","dimension":"corrective_action","priority":90,"prompt":"When a KPI is below target, is a corrective action formally assigned and tracked?","options":["Usually","Sometimes","Rarely","No","I don't know"],"critical":True},
 {"id":"PERF-DATA-01","domain":"Performance","dimension":"data","priority":80,"prompt":"How are KPI results primarily populated?","options":["Automatically from source systems","Combination of automated and manual","Mostly manual","I don't know"],"critical":False},
 {"id":"GOV-DOA-01","domain":"Governance","dimension":"delegation","priority":100,"prompt":"Is there a current approved delegation-of-authority or decision-rights framework?","options":["Yes","Partially / outdated","No","I don't know"],"critical":True},
 {"id":"GOV-RISK-01","domain":"Governance","dimension":"risk_controls","priority":90,"prompt":"Are major organizational risks linked to named controls and accountable owners?","options":["Yes, for most","For some","No","I don't know"],"critical":True},
 {"id":"GOV-ESC-01","domain":"Governance","dimension":"escalation","priority":80,"prompt":"Are materiality and escalation thresholds formally defined for significant issues?","options":["Yes","Partially","No","I don't know"],"critical":False},
]
PRECISION={"exact":.90,"approximate":.75,"range":.70,"qualitative":.55,"unknown":0.0}
DOC_HINTS={
 "Processes":{"ownership":("process owner","accountable owner"),"documentation":("process","procedure","workflow"),"performance":("cycle time","sla","backlog","volume")},
 "Performance":{"kpis":("kpi","key performance indicator","target"),"corrective_action":("corrective action","performance action"),"data":("data source","dashboard","automated")},
 "Governance":{"delegation":("delegation","authority","decision rights"),"risk_controls":("risk","control","risk owner"),"escalation":("materiality","escalation threshold","escalation")},
}
class AdaptiveDiscovery:
 def matrix(self,texts,normalized,answers,domains):
  domains=[d for d in domains if d in DOMAINS] or list(DOMAINS);answered={a["question_id"]:a for a in answers};rows=[]
  for q in QUESTION_LIBRARY:
   if q["domain"] not in domains:continue
   corpus="\n".join(texts.values()).lower();hints=DOC_HINTS[q["domain"]][q["dimension"]]
   doc_hits=sum(1 for h in hints if h in corpus)
   canonical={"Processes":len(normalized.get("processes",[])),"Performance":len(normalized.get("kpis",[])),"Governance":len(normalized.get("grc",[]))}[q["domain"]]
   a=answered.get(q["id"])
   if canonical>0: status="confirmed";confidence=.95;source="structured_evidence"
   elif doc_hits>=2: status="partial";confidence=.65;source="uploaded_evidence"
   elif a and a.get("precision")!="unknown": status="confirmed" if a.get("precision")=="exact" else "partial";confidence=PRECISION.get(a.get("precision","qualitative"),.55);source="client_answer"
   elif a: status="unknown";confidence=0;source="client_answer"
   else: status="unknown";confidence=0;source="none"
   rows.append({"domain":q["domain"],"dimension":q["dimension"],"question_id":q["id"],"status":status,"confidence":confidence,"source":source,"critical":q["critical"]})
  return rows
 def next_questions(self,matrix,answers,limit=3):
  answered={a["question_id"] for a in answers};byid={q["id"]:q for q in QUESTION_LIBRARY};c=[]
  for m in matrix:
   q=byid[m["question_id"]]
   if m["status"]=="confirmed" or q["id"] in answered:continue
   score=q["priority"]+(25 if m["critical"] else 0)+(15 if m["status"]=="unknown" else 0)
   c.append((score,q))
  return [dict(q,reason_asked=f"{q['dimension'].replace('_',' ')} evidence is {next(m['status'] for m in matrix if m['question_id']==q['id'])}") for _,q in sorted(c,key=lambda x:-x[0])[:limit]]
 def readiness(self,matrix,questions):
  critical=[m for m in matrix if m["critical"]];known=[m for m in critical if m["status"] in {"confirmed","partial"}]
  ratio=len(known)/len(critical) if critical else 1
  if ratio>=.80:return "sufficient"
  unanswered_critical=any(m["critical"] and m["status"]=="unknown" and m["question_id"] in {q["id"] for q in questions} for m in matrix)
  if not unanswered_critical:return "limited" if ratio>=.50 else "insufficient"
  return "questions_required"
 def answer(self,question_id,value,precision="qualitative",note=None):
  if question_id not in {q["id"] for q in QUESTION_LIBRARY}:raise KeyError(question_id)
  if precision not in PRECISION:raise ValueError("precision must be exact, approximate, range, qualitative, or unknown")
  return {"question_id":question_id,"answer":value,"precision":precision,"confidence":PRECISION[precision],"note":note}
