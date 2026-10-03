from __future__ import annotations
import hashlib,json
from pathlib import Path
from .agents import EvidenceQualityAgent,ExecutiveSynthesisAgent
from .contracts import Finding,ReviewDecision
from .extraction import EvidenceExtractor
from .storage import EvidenceRepository
from .normalization import EvidenceNormalizer
from .grc import EnterpriseGRCReview
from .discovery import AdaptiveDiscovery
from ..p10_process_intelligence import EnterpriseProcessIntelligence,ProcessPortfolioInput
from ..p09_performance import CorporatePerformanceReview,KPIReviewInput

ROOT=Path(__file__).resolve().parents[3]
class DiagnosticRuntime:
    def __init__(self,root):
        self.root=Path(root);self.evidence=EvidenceRepository(self.root/"evidence");self.extractor=EvidenceExtractor();self.normalizer=EvidenceNormalizer();self.cases=self.root/"diagnostics.json"
        self.process_engine=EnterpriseProcessIntelligence(ROOT/"products/enterprise-process-intelligence/config/process-intelligence.v1.json")
        self.performance_engine=CorporatePerformanceReview(ROOT/"products/corporate-performance-review-ai/config/performance.v1.json")
        self.grc_engine=EnterpriseGRCReview();self.discovery=AdaptiveDiscovery()
    def _read(self):return json.loads(self.cases.read_text()) if self.cases.exists() else {}
    def _write(self,d):self.cases.parent.mkdir(parents=True,exist_ok=True);t=self.cases.with_suffix(".tmp");t.write_text(json.dumps(d,indent=2,default=str)+"\n");t.replace(self.cases)
    def create(self,engagement):
        d=self._read();eid=engagement["id"]
        if eid in d:return d[eid]
        d[eid]={"engagement":engagement,"findings":[],"decisions":[],"synthesis":None,"status":"evidence_collection","discovery_answers":[],"discovery":None};self._write(d);return d[eid]
    def get(self,eid):return self._read()[eid]
    def upload(self,eid,filename,media_type,data,classification="Internal"):
        if eid not in self._read():raise KeyError(eid)
        x=self.extractor.extract(filename,media_type,data);r=self.evidence.store(eid,filename,media_type,data,classification);p=self.root/"extracted"/f"{r.evidence_id}.txt";p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x["text"]);return self.evidence.update(r.evidence_id,extracted_text_path=str(p),extraction_status=x["status"])
    def _texts(self,eid):
        out={}
        for r in self.evidence.list(eid):
            if r.extracted_text_path and Path(r.extracted_text_path).exists():out[r.evidence_id]=Path(r.extracted_text_path).read_text()
        return out
    def _process(self,eid,rows):
        if not rows:return [],{"status":"NO_CANONICAL_PROCESS_RECORDS"}
        result=self.process_engine.analyze(ProcessPortfolioInput(eid,"2026-10-03","Diagnostic evidence","1.0",rows,[],{})).to_dict();fs=[]
        for x in result["exceptions"][:20]:
            pid=x.get("process_id") or "repository";refs=sorted({r["evidence_id"] for r in rows if r["process_id"]==pid}) or sorted({r["evidence_id"] for r in rows})
            fs.append(Finding.create(eid,"Process Intelligence Agent","Processes",x["exception"].replace("_"," ").title(),f"{pid}: {x['exception']}",refs,severity="high" if "missing" in x["exception"] else "medium",confidence=.95,recommendation="Validate and correct the canonical process record before approval.").to_dict())
        return fs,result
    def _performance(self,eid,rows):
        fs=[];results=[]
        for x in rows:
            m=x["master"];r=x["result"]
            try:
                source_hash=hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
                item=KPIReviewInput(m,r,source_hash,"2026-10-03",None,"","","",[],"Retain",None,"2026-10-03T23:59:00+00:00","2026-10-03T12:00:00+00:00",False)
                out=self.performance_engine.review(item).to_dict();results.append(out)
                if out["data_issues"] or out["performance_status"] in {"Attention","Off Target","Data Invalid"}:
                    fs.append(Finding.create(eid,"Performance Intelligence Agent","Performance",f"KPI review: {m.get('KPI_Name') or m.get('KPI_ID')}",out["fact"]+" "+out["calculation"],[x["evidence_id"]],severity="high" if out["performance_status"] in {"Off Target","Data Invalid"} else "medium",confidence=.98,recommendation="Validate data quality, owner explanation and corrective action before management conclusion.").to_dict())
            except Exception as ex:
                fs.append(Finding.create(eid,"Performance Intelligence Agent","Performance","KPI record could not be deterministically evaluated",f"{m.get('KPI_ID')}: {ex}",[x["evidence_id"]],severity="high",confidence=.99,recommendation="Complete the controlled KPI master/result fields.").to_dict())
        return fs,results
    def discover(self,eid,domains):
        d=self._read();case=d[eid];texts=self._texts(eid);normalized=self.normalizer.normalize(texts);answers=case.get("discovery_answers",[])
        matrix=self.discovery.matrix(texts,normalized,answers,domains);questions=self.discovery.next_questions(matrix,answers);readiness=self.discovery.readiness(matrix,questions)
        summary={"readiness":readiness,"matrix":matrix,"questions":questions,"remaining_questions":len(questions),"normalized_counts":{k:len(v) for k,v in normalized.items() if isinstance(v,list)}}
        case["discovery"]=summary;case["status"]="guided_discovery" if readiness=="questions_required" else "ready_for_analysis";self._write(d);return case
    def answer_discovery(self,eid,question_id,answer,precision="qualitative",note=None):
        d=self._read();case=d[eid];item=self.discovery.answer(question_id,answer,precision,note);answers=case.setdefault("discovery_answers",[])
        answers=[a for a in answers if a["question_id"]!=question_id];answers.append(item);case["discovery_answers"]=answers;self._write(d)
        return self.discover(eid,case["engagement"].get("priorities") or ["Processes","Performance","Governance"])
    def execute(self,eid,domains):
        d=self._read();case=d[eid];records=self.evidence.list(eid);texts=self._texts(eid);quality=EvidenceQualityAgent().run(eid,records,texts);normalized=self.normalizer.normalize(texts)
        matrix=self.discovery.matrix(texts,normalized,case.get("discovery_answers",[]),domains);questions=self.discovery.next_questions(matrix,case.get("discovery_answers",[]));readiness=self.discovery.readiness(matrix,questions)
        case["discovery"]={"readiness":readiness,"matrix":matrix,"questions":questions,"remaining_questions":len(questions),"normalized_counts":{k:len(v) for k,v in normalized.items() if isinstance(v,list)}}
        if readiness=="questions_required":
            case["status"]="guided_discovery";self._write(d);return case
        findings=list(quality["findings"]);engine_outputs={}
        if quality["ready"] and "Processes" in domains:
            f,o=self._process(eid,normalized["processes"]);findings+=f;engine_outputs["process"]=o
        if quality["ready"] and "Performance" in domains:
            f,o=self._performance(eid,normalized["kpis"]);findings+=f;engine_outputs["performance"]=o
        if quality["ready"] and "Governance" in domains:
            o=self.grc_engine.review(normalized["grc"]);engine_outputs["grc"]=o
            for x in o["findings"]:findings.append(Finding.create(eid,"Governance, Risk & Control Agent","Governance",x["code"].replace("_"," ").title(),x["statement"],x["evidence_ids"],severity=x["severity"],confidence=.95,recommendation=x["recommendation"]).to_dict())
        for w in normalized["warnings"]:findings.append(Finding.create(eid,"Evidence & Quality Agent","Evidence","Evidence retained for qualitative review",w["warning"],[w["evidence_id"]],severity="low",confidence=.99,recommendation="Use a controlled structured template when deterministic specialist analysis is required.").to_dict())
        synthesis=ExecutiveSynthesisAgent().run(eid,findings);case.update({"findings":findings,"synthesis":synthesis,"status":"human_review","evidence_quality":quality,"normalized_counts":{k:len(v) for k,v in normalized.items() if isinstance(v,list)},"engine_outputs":engine_outputs});self._write(d);return case
    def decide(self,eid,finding_id,decision,reviewer_role,reason,modified_statement=None):
        d=self._read();case=d[eid];f=next((x for x in case["findings"] if x["finding_id"]==finding_id),None)
        if f is None:raise KeyError(finding_id)
        if decision=="modified":
            if not modified_statement:raise ValueError("Modified decision requires replacement statement")
            f["statement"]=modified_statement
        f["status"]=decision;case["decisions"].append(ReviewDecision(finding_id,decision,reviewer_role,reason).__dict__);self._write(d);return case
    def report(self,eid):
        c=self._read()[eid];approved=[x for x in c["findings"] if x["status"] in {"approved","modified"}]
        synthesis=ExecutiveSynthesisAgent().run(eid,approved) if approved else None
        return {"engagement":c["engagement"],"report_status":"reviewed" if approved else "draft","approved_findings":approved,"executive_synthesis":synthesis,"evidence":[x.to_dict() for x in self.evidence.list(eid)],"decisions":c["decisions"],"engine_outputs":c.get("engine_outputs",{}),"notice":"Only human-approved or human-modified specialist findings are publishable conclusions."}
