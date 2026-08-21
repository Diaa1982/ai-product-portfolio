import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .engine import JsonCaseStore, PortfolioEngine
from .p03_radar import SignalInput, StrategicRadar
from .p04_detector import DetectionInput, SignalDetector
from .p08_assessor import AssessmentInput, UseCaseAssessor
from .p14_control_tower import AIGovernanceControlTower, UseCaseProfile


REPO_ROOT = Path(__file__).resolve().parents[2]
PRODUCT_REGISTRY = Path(os.getenv("PRODUCT_REGISTRY_PATH", REPO_ROOT / "products" / "registry.json"))
WORKFLOW_PATH = Path(os.getenv("WORKFLOW_PATH", REPO_ROOT / "products" / "workflows.json"))
CASE_STORE_PATH = Path(os.getenv("CASE_STORE_PATH", REPO_ROOT / "data" / "runtime" / "cases.json"))
DASHBOARD_PATH = Path(os.getenv("DASHBOARD_PATH", Path(__file__).parent / "static" / "index.html"))
P08_DASHBOARD_PATH = Path(os.getenv("P08_DASHBOARD_PATH", Path(__file__).parent / "static" / "p08.html"))
P08_CONFIG_PATH = Path(os.getenv("P08_CONFIG_PATH", REPO_ROOT / "products" / "ai-use-case-assessor" / "config" / "scoring.v1.json"))
P03_DASHBOARD_PATH = Path(os.getenv("P03_DASHBOARD_PATH", Path(__file__).parent / "static" / "p03.html"))
P03_CONFIG_PATH = Path(os.getenv("P03_CONFIG_PATH", REPO_ROOT / "products" / "strategic-radar" / "config" / "radar.v1.json"))
P04_DASHBOARD_PATH = Path(os.getenv("P04_DASHBOARD_PATH", Path(__file__).parent / "static" / "p04.html"))
P04_CONFIG_PATH = Path(os.getenv("P04_CONFIG_PATH", REPO_ROOT / "products" / "signal-detection-agent" / "config" / "detection.v1.json"))
P14_DASHBOARD_PATH = Path(os.getenv("P14_DASHBOARD_PATH", Path(__file__).parent / "static" / "p14.html"))
P14_CONFIG_PATH = Path(os.getenv("P14_CONFIG_PATH", REPO_ROOT / "products" / "ai-governance-control-tower" / "config" / "governance.v1.json"))

store = JsonCaseStore(CASE_STORE_PATH)
engine = PortfolioEngine(WORKFLOW_PATH, store)
p08_assessor = UseCaseAssessor(P08_CONFIG_PATH)
p03_radar = StrategicRadar(P03_CONFIG_PATH)
p04_detector = SignalDetector(P04_CONFIG_PATH)
p14_control_tower = AIGovernanceControlTower(P14_CONFIG_PATH)

app = FastAPI(
    title="Governed AI Product Portfolio",
    version="0.3.0",
    description="Shared governed platform plus a deployment-candidate AI Use Case Assessor.",
)


class CaseCreate(BaseModel):
    product_id: str = Field(pattern=r"^P[0-9]{2}$")
    title: str = Field(min_length=3, max_length=200)
    owner_role: str = Field(min_length=2, max_length=100)
    inputs: dict[str, Any]


class EvidenceCreate(BaseModel):
    actor_role: str
    evidence: dict[str, Any]


class ActorAction(BaseModel):
    actor_role: str


class ApprovalDecision(BaseModel):
    approver_role: str
    decision: str
    reason: str = Field(min_length=3, max_length=1000)


class P08AssessmentRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    assessment_mode: str
    business_problem: str
    desired_outcome: str
    business_owner: str
    process_trigger: str
    process_closure: str
    ai_task: str
    success_criteria: list[str]
    prohibited_automated_decisions: list[str]
    low_confidence_behavior: str
    data_sources: list[dict[str, Any]]
    evidence_references: list[str]
    value_scores: dict[str, float]
    feasibility_scores: dict[str, float]
    risk_scores: dict[str, float]
    assumptions: list[str] = Field(default_factory=list)


class P08ApprovalRequest(BaseModel):
    assessment_id: str
    action: str
    approver_role: str
    decision: str
    reason: str = Field(min_length=3, max_length=1000)


class P03SignalRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    audience: str
    industry: str
    jurisdiction: str
    pfm_category: str
    signal_statement: str
    fact: str
    interpretation: str
    recommendation: str
    source_id: str
    source_url: str
    source_version: str
    published_at: str
    retrieved_at: str
    evidence_hash: str
    change_summary: str
    materiality_scores: dict[str, float | None]
    confidence_score: float = Field(ge=0, le=1)
    high_impact: bool = False
    normative_policy_advice: bool = False
    sensitive_jurisdiction: bool = False
    executive_delivery: bool = False
    promote_to_memory: bool = False


class P03ApprovalRequest(BaseModel):
    signal_id: str
    action: str
    approver_role: str
    decision: str
    reason: str = Field(min_length=3, max_length=1000)


class P04DetectionRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    creation_mode: str
    audience: str
    signal_category: str
    pfm_focus: str
    affected_entities: list[str]
    effective_date: str
    source_id: str
    source_url: str
    current_version: str
    current_hash: str
    prior_version: str
    prior_hash: str
    snapshot_path: str
    fetched_at: str
    published_at: str
    issuing_authority: str
    provenance_token: str
    citations: list[dict[str, Any]]
    change_summary: str
    evidence_quality: str
    materiality_scores: dict[str, float | None]
    confidence_scores: dict[str, float | None]
    fact: str
    interpretation: str
    recommendation: str
    opportunity: str
    risk: str
    scenario: str
    kpi_hypothesis: str
    high_impact: bool = False


class P04ApprovalRequest(BaseModel):
    signal_id: str
    action: str
    approver_role: str
    decision: str
    reason: str = Field(min_length=3, max_length=1000)


class P14UseCaseRequest(BaseModel):
    use_case_id: str
    title: str
    purpose: str
    owner_role: str
    data_owner_role: str
    data_classification: str
    external_autonomous_action: bool = False
    consequential_decision: bool = False
    prohibited_financial_action: bool = False
    sensitive_personal_data: bool = False
    decision_support_at_scale: bool = False
    public_facing: bool = False
    human_reviewed_output: bool = False
    agentic_autonomy_level: int = Field(ge=0, le=4)
    evidence_references: list[str]


class P14GateRequest(BaseModel):
    profile: P14UseCaseRequest
    gate: str
    control_evidence: dict[str, str]
    prior_approvals: list[str] = Field(default_factory=list)
    qa_passed: bool = False
    independent_testing_passed: bool = False


class P14GateApprovalRequest(BaseModel):
    use_case_id: str
    gate: str
    approver_role: str
    decision: str
    reason: str = Field(min_length=3, max_length=1000)
    gate_status: str


class P14MonitoringRequest(BaseModel):
    use_case_id: str
    metrics: dict[str, Any]


def as_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, KeyError):
        return HTTPException(status_code=404, detail="Case not found")
    if isinstance(exc, PermissionError):
        return HTTPException(status_code=403, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(DASHBOARD_PATH)


@app.get("/p08", include_in_schema=False)
def p08_dashboard() -> FileResponse:
    return FileResponse(P08_DASHBOARD_PATH)


@app.get("/p03", include_in_schema=False)
def p03_dashboard() -> FileResponse:
    return FileResponse(P03_DASHBOARD_PATH)


@app.get("/p04", include_in_schema=False)
def p04_dashboard() -> FileResponse:
    return FileResponse(P04_DASHBOARD_PATH)


@app.get("/p14", include_in_schema=False)
def p14_dashboard() -> FileResponse:
    return FileResponse(P14_DASHBOARD_PATH)


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "version": app.version, "product_count": len(engine.workflows),
            "synthetic_data_only": True, "p08_config_version": p08_assessor.config["config_version"],
            "p03_config_version": p03_radar.config["config_version"],
            "p04_config_version": p04_detector.config["config_version"],
            "p14_config_version": p14_control_tower.config["config_version"]}


@app.get("/p14/config")
def p14_config() -> dict[str, Any]:
    return p14_control_tower.config


@app.post("/p14/risk/classify")
def p14_classify(request: P14UseCaseRequest) -> dict[str, Any]:
    try:
        return p14_control_tower.classify_risk(UseCaseProfile(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p14/gates/evaluate")
def p14_evaluate_gate(request: P14GateRequest) -> dict[str, Any]:
    try:
        return p14_control_tower.evaluate_gate(
            UseCaseProfile(**request.profile.model_dump()), request.gate,
            request.control_evidence, request.prior_approvals,
            request.qa_passed, request.independent_testing_passed,
        ).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p14/gates/approve")
def p14_approve_gate(request: P14GateApprovalRequest) -> dict[str, Any]:
    try:
        return p14_control_tower.approve_gate(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p14/monitor")
def p14_monitor(request: P14MonitoringRequest) -> dict[str, Any]:
    try:
        return p14_control_tower.monitor(request.use_case_id, request.metrics)
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.get("/p04/config")
def p04_config() -> dict[str, Any]:
    return p04_detector.config


@app.get("/p04/sources")
def p04_sources() -> dict[str, Any]:
    return {"sources": list(p04_detector.sources.values()), "synthetic_only": True}


@app.post("/p04/detect")
def p04_detect(request: P04DetectionRequest) -> dict[str, Any]:
    try:
        return p04_detector.detect(DetectionInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p04/approve")
def p04_approve(request: P04ApprovalRequest) -> dict[str, Any]:
    try:
        return p04_detector.approve(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.get("/p03/config")
def p03_config() -> dict[str, Any]:
    return p03_radar.config


@app.get("/p03/sources")
def p03_sources() -> dict[str, Any]:
    return {"sources": list(p03_radar.sources.values()), "synthetic_only": True}


@app.post("/p03/signals/assess")
def p03_assess_signal(request: P03SignalRequest) -> dict[str, Any]:
    try:
        return p03_radar.assess_signal(SignalInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p03/approve")
def p03_approve(request: P03ApprovalRequest) -> dict[str, Any]:
    try:
        return p03_radar.approve(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.get("/p08/config")
def p08_config() -> dict[str, Any]:
    return p08_assessor.config


@app.post("/p08/assess")
def p08_assess(request: P08AssessmentRequest) -> dict[str, Any]:
    try:
        return p08_assessor.assess(AssessmentInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p08/approve")
def p08_approve(request: P08ApprovalRequest) -> dict[str, Any]:
    try:
        return p08_assessor.approve(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.get("/products")
def list_products() -> dict[str, Any]:
    return json.loads(PRODUCT_REGISTRY.read_text(encoding="utf-8"))


@app.get("/workflows")
def list_workflows() -> dict[str, Any]:
    return {"workflows": list(engine.workflows.values())}


@app.get("/cases")
def list_cases(product_id: str | None = None) -> dict[str, Any]:
    return {"cases": [case.to_dict() for case in store.list(product_id)]}


@app.post("/cases", status_code=201)
def create_case(request: CaseCreate) -> dict[str, Any]:
    try:
        return engine.create_case(request.product_id, request.title, request.owner_role, request.inputs).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.get("/cases/{case_id}")
def get_case(case_id: str) -> dict[str, Any]:
    try:
        return store.get(case_id).to_dict()
    except KeyError as exc:
        raise as_http_error(exc) from exc


@app.post("/cases/{case_id}/evidence")
def add_evidence(case_id: str, request: EvidenceCreate) -> dict[str, Any]:
    try:
        return engine.add_evidence(case_id, request.actor_role, request.evidence).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/cases/{case_id}/evaluate")
def evaluate(case_id: str, request: ActorAction) -> dict[str, Any]:
    try:
        return engine.evaluate(case_id, request.actor_role).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/cases/{case_id}/submit")
def submit(case_id: str, request: ActorAction) -> dict[str, Any]:
    try:
        return engine.submit_for_approval(case_id, request.actor_role).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/cases/{case_id}/decision")
def decide(case_id: str, request: ApprovalDecision) -> dict[str, Any]:
    try:
        return engine.decide(case_id, request.approver_role, request.decision, request.reason).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.get("/cases/{case_id}/audit/verify")
def verify_audit(case_id: str) -> dict[str, Any]:
    try:
        case = store.get(case_id)
    except KeyError as exc:
        raise as_http_error(exc) from exc
    return {"case_id": case_id, "valid": engine.verify_audit_chain(case), "event_count": len(case.audit_log)}
