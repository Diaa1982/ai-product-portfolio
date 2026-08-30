from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .config import get_settings
from .schemas import UseCaseRequest
from .workflow_langgraph import EnterpriseLangGraphWorkflow


app = FastAPI(title="Enterprise Agentic AI", version="0.1.0")


class UseCasePayload(BaseModel):
    title: str
    challenge: str
    objective: str = ""
    business_area: str = "enterprise"
    use_case_type: str = "ai_transformation"
    users: list[str] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    image_paths: list[str] = Field(default_factory=list)
    expected_outcomes: list[str] = Field(default_factory=list)
    authorized_to_execute: bool = False


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(payload: UseCasePayload) -> dict:
    request = UseCaseRequest(**payload.model_dump())
    result = EnterpriseLangGraphWorkflow(get_settings()).run(request)
    return result.to_dict()

