import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .engine import JsonCaseStore, PortfolioEngine


REPO_ROOT = Path(__file__).resolve().parents[2]
PRODUCT_REGISTRY = Path(os.getenv("PRODUCT_REGISTRY_PATH", REPO_ROOT / "products" / "registry.json"))
WORKFLOW_PATH = Path(os.getenv("WORKFLOW_PATH", REPO_ROOT / "products" / "workflows.json"))
CASE_STORE_PATH = Path(os.getenv("CASE_STORE_PATH", REPO_ROOT / "data" / "runtime" / "cases.json"))
DASHBOARD_PATH = Path(os.getenv("DASHBOARD_PATH", Path(__file__).parent / "static" / "index.html"))

store = JsonCaseStore(CASE_STORE_PATH)
engine = PortfolioEngine(WORKFLOW_PATH, store)

app = FastAPI(
    title="Governed AI Product Portfolio",
    version="0.2.0",
    description="Shared case, evidence, analysis and approval platform for 18 AI products.",
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


def as_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, KeyError):
        return HTTPException(status_code=404, detail="Case not found")
    if isinstance(exc, PermissionError):
        return HTTPException(status_code=403, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(DASHBOARD_PATH)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "version": app.version,
        "product_count": len(engine.workflows),
        "synthetic_data_only": True,
    }


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
