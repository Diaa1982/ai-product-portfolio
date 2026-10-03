from __future__ import annotations
import re
from .contracts import Finding

DOMAIN_TERMS={
"Processes":["process","procedure","workflow","handoff","owner","raci","cycle time","bottleneck","sop"],
"Performance":["kpi","target","actual","performance","indicator","variance","trend","initiative"],
"Governance":["risk","control","policy","delegation","authority","committee","audit","governance","approval"]
}
class EvidenceQualityAgent:
    name="Evidence & Quality Agent"
    def run(self,engagement_id,records,texts):
        findings=[];usable=[]
        for r in records:
            text=texts.get(r.evidence_id,"");issues=[]
            if not text.strip():issues.append("No extractable text")
            if r.size<=0:issues.append("Empty source")
            if issues:
                findings.append(Finding.create(engagement_id,self.name,"Evidence","Evidence requires attention",f"{r.filename}: "+", ".join(issues),[r.evidence_id],severity="high",confidence=.99,recommendation="Replace, clarify or manually validate this source before relying on it."))
            else:usable.append(r.evidence_id)
        return {"usable_evidence_ids":usable,"findings":[x.to_dict() for x in findings],"ready":bool(usable),"limitations":["Quality checks validate technical usability and traceability; they do not establish factual truth."]}

class SpecialistAgent:
    def __init__(self,domain):self.domain=domain;self.name={"Processes":"Process Intelligence Agent","Performance":"Performance Intelligence Agent","Governance":"Governance, Risk & Control Agent"}[domain]
    def run(self,engagement_id,texts,approved_ids):
        corpus="\n".join(texts.get(x,"") for x in approved_ids);low=corpus.lower();terms=DOMAIN_TERMS[self.domain]
        hits=[t for t in terms if t in low];findings=[]
        if not approved_ids:return []
        if len(hits)<3:
            findings.append(Finding.create(engagement_id,self.name,self.domain,f"Insufficient {self.domain.lower()} evidence",f"Current evidence contains limited {self.domain.lower()} signals ({', '.join(hits) or 'none'}).",[ *approved_ids],severity="medium",confidence=.85,recommendation=f"Provide authoritative {self.domain.lower()} records before material conclusions are approved.",limitations=["Automated diagnostic is evidence-limited."]))
        else:
            findings.append(Finding.create(engagement_id,self.name,self.domain,f"{self.domain} evidence available for diagnostic review",f"Evidence contains multiple relevant signals: {', '.join(hits[:6])}. Detailed assertions require source-level validation.",approved_ids,severity="low",confidence=.65,recommendation=f"Run the domain-specific {self.domain.lower()} engine against normalized structured records.",limitations=["Keyword-level routing is not a substitute for domain calculation or expert interpretation."]))
        return [x.to_dict() for x in findings]

class ExecutiveSynthesisAgent:
    name="Executive Synthesis Agent"
    def run(self,engagement_id,findings):
        active=[f for f in findings if f.get("status")!="rejected"];domains=sorted(set(f["domain"] for f in active if f["domain"]!="Evidence"))
        evidence=sorted(set(e for f in active for e in f.get("evidence_ids",[])))
        return Finding.create(engagement_id,self.name,"Cross-domain","Executive diagnostic synthesis",f"{len(active)} draft finding(s) span {', '.join(domains) or 'no validated specialist domains'}. This synthesis remains provisional until human review.",evidence,severity="medium" if active else "low",confidence=.6 if active else .3,recommendation="Review cross-domain dependencies, approve or modify each material finding, then publish the controlled diagnostic report.",limitations=["Synthesis does not override specialist evidence or human decision authority."]).to_dict()
