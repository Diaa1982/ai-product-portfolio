from __future__ import annotations
import json
from pathlib import Path
from .agents import EvidenceQualityAgent,ExecutiveSynthesisAgent,SpecialistAgent
from .contracts import ReviewDecision
from .extraction import EvidenceExtractor
from .storage import EvidenceRepository

class DiagnosticRuntime:
    def __init__(self,root):
        self.root=Path(root);self.evidence=EvidenceRepository(self.root/"evidence");self.extractor=EvidenceExtractor();self.cases=self.root/"diagnostics.json"
    def _read(self):return json.loads(self.cases.read_text()) if self.cases.exists() else {}
    def _write(self,d):self.cases.parent.mkdir(parents=True,exist_ok=True);t=self.cases.with_suffix(".tmp");t.write_text(json.dumps(d,indent=2)+"\n");t.replace(self.cases)
    def create(self,engagement):
        d=self._read();eid=engagement["id"];d[eid]={"engagement":engagement,"findings":[],"decisions":[],"synthesis":None,"status":"evidence_collection"};self._write(d);return d[eid]
    def upload(self,eid,filename,media_type,data,classification="Internal"):
        r=self.evidence.store(eid,filename,media_type,data,classification);x=self.extractor.extract(filename,media_type,data);text_path=self.root/"extracted"/f"{r.evidence_id}.txt";text_path.parent.mkdir(parents=True,exist_ok=True);text_path.write_text(x["text"]);return self.evidence.update(r.evidence_id,extracted_text_path=str(text_path),extraction_status=x["status"])
    def _texts(self,eid):
        out={}
        for r in self.evidence.list(eid):
            if r.extracted_text_path and Path(r.extracted_text_path).exists():out[r.evidence_id]=Path(r.extracted_text_path).read_text()
        return out
    def execute(self,eid,domains):
        d=self._read();case=d[eid];records=self.evidence.list(eid);texts=self._texts(eid);quality=EvidenceQualityAgent().run(eid,records,texts)
        findings=list(quality["findings"])
        if quality["ready"]:
            for domain in domains:
                if domain in {"Processes","Performance","Governance"}:findings+=SpecialistAgent(domain).run(eid,texts,quality["usable_evidence_ids"])
        synthesis=ExecutiveSynthesisAgent().run(eid,findings);case.update({"findings":findings,"synthesis":synthesis,"status":"human_review","evidence_quality":quality});self._write(d);return case
    def decide(self,eid,finding_id,decision,reviewer_role,reason,modified_statement=None):
        d=self._read();case=d[eid];f=next(x for x in case["findings"] if x["finding_id"]==finding_id)
        if decision=="modified":
            if not modified_statement:raise ValueError("Modified decision requires replacement statement")
            f["statement"]=modified_statement
        f["status"]=decision;rd=ReviewDecision(finding_id,decision,reviewer_role,reason);case["decisions"].append(rd.__dict__);self._write(d);return case
    def report(self,eid):
        c=self._read()[eid];approved=[x for x in c["findings"] if x["status"] in {"approved","modified"}]
        return {"engagement":c["engagement"],"report_status":"reviewed" if approved else "draft","approved_findings":approved,"executive_synthesis":c["synthesis"],"evidence":[x.to_dict() for x in self.evidence.list(eid)],"decisions":c["decisions"],"notice":"Only human-approved or human-modified specialist findings are publishable conclusions."}
