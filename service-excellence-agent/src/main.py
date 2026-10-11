from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal
import uuid
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Service Excellence Agent", version="1.0.0")

class ServiceTask(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    objective: str
    scope: Dict[str, Any] = Field(default_factory=dict)
    kpis: List[str] = Field(default_factory=list)
    regions: List[str] = Field(default_factory=list)
    functions: List[str] = Field(default_factory=list)
    time_period: Optional[str] = None
    available_sources: List[str] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)

class KPIReview(BaseModel):
    kpi_name: str
    actual: float
    target: Optional[float] = None
    prior_period: Optional[float] = None
    direction: Literal["higher_is_better","lower_is_better","context_dependent"]
    data_quality_status: Literal["good","limited","poor"] = "good"

class OperationalIssue(BaseModel):
    problem_statement: str
    business_impact: str
    severity: Literal["low","medium","high","critical"] = "medium"
    kpi_impact: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)

HIGH_IMPACT_ACTIONS = {"change_official_kpi_definition","change_official_kpi_target","publish_official_executive_results","write_salesforce_or_crm","change_customer_commitment","change_financial_record_or_forecast_of_record","change_supply_plan","change_manufacturing_execution_plan","close_critical_corrective_action","deploy_production_automation"}

@app.get("/health")
def health():
    return {"status":"ok","agent":"service-excellence-agent","timestamp":datetime.now(timezone.utc).isoformat()}

@app.post("/v1/tasks")
def task(t: ServiceTask):
    return {"task_id": t.task_id,"status": "needs_data" if not t.available_sources else "ready_for_agent_runtime","cycle": ["define","validate_data","measure","compare","diagnose","root_cause","prioritize","improve","control","track","standardize","report"]}

@app.post("/v1/kpi/review")
def review(r: KPIReview):
    gap = None if r.target is None else r.actual-r.target
    if r.target is None: status = "not_evaluated"
    elif r.direction == "higher_is_better": status = "on_or_above_target" if r.actual >= r.target else "below_target"
    elif r.direction == "lower_is_better": status = "on_or_below_target" if r.actual <= r.target else "above_target"
    else: status = "context_review_required"
    return {"kpi":r.kpi_name,"gap":gap,"status":status,"data_quality_status":r.data_quality_status}

@app.post("/v1/issues/analyze")
def issue(i: OperationalIssue):
    return {"issue":i.model_dump(),"next_steps":["validate_problem","baseline","stratify","map_process","validate_causes","countermeasures"],"critical_control": i.severity == "critical"}

@app.post("/v1/actions/{action_name}/control")
def control(action_name: str):
    return {"action":action_name,"approval_required":action_name in HIGH_IMPACT_ACTIONS}
