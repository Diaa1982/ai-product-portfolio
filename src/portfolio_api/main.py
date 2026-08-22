import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .engine import JsonCaseStore, PortfolioEngine
from .p01_pfm_agentic import PFMCaseInput, PFMAgenticOrchestrator
from .p02_pfm_brain import FiscalSnapshotInput, PFMBrain
from .p11_ipsas_compliance import IPSASComplianceReviewer, IPSASReviewInput
from .p12_revenue_reconciliation import RevenueReconciler, RevenueReconciliationInput
from .p03_radar import SignalInput, StrategicRadar
from .p04_detector import DetectionInput, SignalDetector
from .p05_service_design import ServiceDesignAI, ServiceDesignInput
from .p06_process_audit import ProcessAuditAI, ProcessAuditInput
from .p07_partnership import PartnershipInput, PartnershipManagementCopilot
from .p10_process_intelligence import EnterpriseProcessIntelligence, ProcessPortfolioInput
from .p13_pfm_business_architecture import PFMBusinessArchitecture, PFMArchitectureInput
from .p08_assessor import AssessmentInput, UseCaseAssessor
from .p14_control_tower import AIGovernanceControlTower, UseCaseProfile
from .p09_performance import CorporatePerformanceReview, KPIReviewInput


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
P09_DASHBOARD_PATH = Path(os.getenv("P09_DASHBOARD_PATH", Path(__file__).parent / "static" / "p09.html"))
P09_CONFIG_PATH = Path(os.getenv("P09_CONFIG_PATH", REPO_ROOT / "products" / "corporate-performance-review-ai" / "config" / "performance.v1.json"))
P01_DASHBOARD_PATH = Path(os.getenv("P01_DASHBOARD_PATH", Path(__file__).parent / "static" / "p01.html"))
P01_CONFIG_PATH = Path(os.getenv("P01_CONFIG_PATH", REPO_ROOT / "products" / "pfm-agentic-ai" / "config" / "pfm-agents.v1.json"))
P02_DASHBOARD_PATH = Path(os.getenv("P02_DASHBOARD_PATH", Path(__file__).parent / "static" / "p02.html"))
P02_CONFIG_PATH = Path(os.getenv("P02_CONFIG_PATH", REPO_ROOT / "products" / "pfm-brain" / "config" / "pfm-brain.v1.json"))
P11_DASHBOARD_PATH = Path(os.getenv("P11_DASHBOARD_PATH", Path(__file__).parent / "static" / "p11.html"))
P11_CONFIG_PATH = Path(os.getenv("P11_CONFIG_PATH", REPO_ROOT / "products" / "ipsas-compliance-ai" / "config" / "ipsas-review.v1.json"))
P12_DASHBOARD_PATH = Path(os.getenv("P12_DASHBOARD_PATH", Path(__file__).parent / "static" / "p12.html"))
P12_CONFIG_PATH = Path(os.getenv("P12_CONFIG_PATH", REPO_ROOT / "products" / "revenue-reconciliation-ai" / "config" / "reconciliation.v1.json"))
P05_DASHBOARD_PATH = Path(os.getenv("P05_DASHBOARD_PATH", Path(__file__).parent / "static" / "p05.html"))
P05_CONFIG_PATH = Path(os.getenv("P05_CONFIG_PATH", REPO_ROOT / "products" / "service-design-ai" / "config" / "service-design.v1.json"))
P06_DASHBOARD_PATH = Path(os.getenv("P06_DASHBOARD_PATH", Path(__file__).parent / "static" / "p06.html"))
P06_CONFIG_PATH = Path(os.getenv("P06_CONFIG_PATH", REPO_ROOT / "products" / "process-audit-ai" / "config" / "process-audit.v1.json"))
P07_DASHBOARD_PATH = Path(os.getenv("P07_DASHBOARD_PATH", Path(__file__).parent / "static" / "p07.html"))
P07_CONFIG_PATH = Path(os.getenv("P07_CONFIG_PATH", REPO_ROOT / "products" / "partnership-management-copilot" / "config" / "partnership.v1.json"))
P10_DASHBOARD_PATH = Path(os.getenv("P10_DASHBOARD_PATH", Path(__file__).parent / "static" / "p10.html"))
P10_CONFIG_PATH = Path(os.getenv("P10_CONFIG_PATH", REPO_ROOT / "products" / "enterprise-process-intelligence" / "config" / "process-intelligence.v1.json"))
P13_DASHBOARD_PATH = Path(os.getenv("P13_DASHBOARD_PATH", Path(__file__).parent / "static" / "p13.html"))
P13_CONFIG_PATH = Path(os.getenv("P13_CONFIG_PATH", REPO_ROOT / "products" / "pfm-business-architecture" / "config" / "pfm-architecture.v1.json"))

store = JsonCaseStore(CASE_STORE_PATH)
engine = PortfolioEngine(WORKFLOW_PATH, store)
p08_assessor = UseCaseAssessor(P08_CONFIG_PATH)
p03_radar = StrategicRadar(P03_CONFIG_PATH)
p04_detector = SignalDetector(P04_CONFIG_PATH)
p14_control_tower = AIGovernanceControlTower(P14_CONFIG_PATH)
p09_performance = CorporatePerformanceReview(P09_CONFIG_PATH)
p01_orchestrator = PFMAgenticOrchestrator(P01_CONFIG_PATH)
p02_brain = PFMBrain(P02_CONFIG_PATH)
p11_reviewer = IPSASComplianceReviewer(P11_CONFIG_PATH)
p12_reconciler = RevenueReconciler(P12_CONFIG_PATH)
p05_service_design = ServiceDesignAI(P05_CONFIG_PATH)
p06_process_audit = ProcessAuditAI(P06_CONFIG_PATH)
p07_partnership = PartnershipManagementCopilot(P07_CONFIG_PATH)
p10_process_intelligence = EnterpriseProcessIntelligence(P10_CONFIG_PATH)
p13_pfm_architecture = PFMBusinessArchitecture(P13_CONFIG_PATH)

app = FastAPI(
    title="Governed AI Product Portfolio",
    version="0.4.0",
    description="Shared governed platform with controlled, evidence-led AI product workflows.",
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


class P09ReviewRequest(BaseModel):
    kpi_master: dict[str, Any]
    result: dict[str, Any]
    source_row_hash: str
    data_cutoff: str
    prior_actual: float | None = None
    owner_explanation: str
    inference: str
    recommendation: str
    corrective_actions: list[dict[str, Any]] = Field(default_factory=list)
    target_treatment: str
    proposed_target: float | None = None
    review_due_at: str
    submitted_at: str
    executive_briefing: bool = False


class P09ApprovalRequest(BaseModel):
    review_id: str
    action: str
    approver_role: str
    decision: str
    reason: str = Field(min_length=3, max_length=1000)


class P01AnalysisRequest(BaseModel):
    case_id: str = Field(min_length=3, max_length=100)
    workflow_type: str
    current_agent: str
    next_agent: str
    business_outcome: str
    payload: dict[str, Any]
    success_criteria: list[str]
    evidence_references: list[str]
    assumptions: list[str] = Field(default_factory=list)
    approved_budget: float = Field(ge=0)
    revised_budget: float = Field(ge=0)
    period_plan: float = Field(ge=0)
    actuals: float = Field(ge=0)
    commitments: float = Field(ge=0)
    cash_available: float = Field(ge=0)
    obligations_due: float = Field(ge=0)
    due_date: str
    validation_passed: bool
    high_risk: bool = False
    human_approval_reference: str | None = None


class P01ActionRequest(BaseModel):
    action: str = Field(min_length=3, max_length=200)


class P01ApprovalRequest(BaseModel):
    case_id: str
    approver_role: str
    decision: str
    reason: str = Field(min_length=3, max_length=1000)


class P02AnalysisRequest(BaseModel):
    case_id: str = Field(min_length=3, max_length=100)
    reporting_period: str
    currency: str
    division_id: str
    cost_center: str
    account_code: str
    source_record_id: str
    source_system: str
    evidence_references: list[str]
    assumptions: list[str] = Field(default_factory=list)
    organization_master_loaded: bool
    chart_of_accounts_loaded: bool
    approved_budget_loaded: bool
    original_budget: float = Field(ge=0)
    supplementary_budget: float = Field(ge=0)
    transfer_amount: float
    period_plan: float = Field(ge=0)
    actual_expenditure: float = Field(ge=0)
    commitments: float = Field(ge=0)
    revenue_target: float = Field(ge=0)
    revenue_actual: float = Field(ge=0)
    opening_cash: float = Field(ge=0)
    cash_inflow: float = Field(ge=0)
    cash_outflow: float = Field(ge=0)
    minimum_cash_buffer: float = Field(ge=0)
    kpi_direction: str
    kpi_target: float
    kpi_actual: float
    kpi_attention_tolerance_percent: float = Field(ge=0, le=100)
    inherent_risk_score: float = Field(ge=0, le=100)
    control_effectiveness_percent: float = Field(ge=0, le=100)
    requester_role: str
    approver_role: str
    proposed_action_amount: float = Field(ge=0)
    maximum_authority_amount: float = Field(ge=0)
    action_type: str
    duplicate_transaction: bool = False
    expected_revised_budget: float | None = None
    expected_closing_cash: float | None = None
    human_approval_reference: str | None = None


class P02DatasetReadinessRequest(BaseModel):
    loaded_domains: list[str]


class P11ReviewRequest(BaseModel):
    case_id: str = Field(min_length=3, max_length=100)
    review_type: str
    reporting_period: str
    entity_id: str
    source_system: str
    evidence_references: list[str]
    applicable_policy_reference: str
    requirement_reference: str
    assumptions: list[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0, le=1)
    materiality_threshold: float = Field(ge=0)
    reporting_impact: bool = False
    human_approval_reference: str | None = None
    journal_id: str | None = None
    debit_total: float | None = None
    credit_total: float | None = None
    entry_date: str | None = None
    period_start: str | None = None
    period_end: str | None = None
    account_code_valid: bool | None = None
    supporting_document_present: bool | None = None
    approval_status: str | None = None
    preparer_role: str | None = None
    approver_role: str | None = None
    ledger_balance: float | None = None
    external_balance: float | None = None
    unreconciled_items: list[dict[str, Any]] = Field(default_factory=list)
    disclosure_items: list[dict[str, Any]] = Field(default_factory=list)
    comparative_current: str | None = None
    comparative_prior: str | None = None
    comparative_required: bool = False


class P11ActionRequest(BaseModel):
    action: str = Field(min_length=3, max_length=200)


class P12ReconciliationRequest(BaseModel):
    case_id: str = Field(min_length=3, max_length=100)
    form_id: str
    reporting_period: str
    currency: str
    service_provider: str
    receiving_bank_account: str
    settlement_bank_account: str
    responsible_employee_role: str
    source_system: str
    evidence_references: list[str]
    assumptions: list[str] = Field(default_factory=list)
    received_amount: float = Field(ge=0)
    refund_amount: float = Field(ge=0)
    fraud_transactions: float = Field(ge=0)
    commission_type: str
    commission_rate_percent: float = Field(ge=0, le=100)
    vat_type: str
    vat_rate_percent: float = Field(ge=0, le=100)
    internal_reference: str
    bank_reference: str
    internal_amount: float = Field(ge=0)
    bank_amount: float = Field(ge=0)
    duplicate_internal: bool = False
    duplicate_bank: bool = False
    preparer_role: str
    approver_role: str
    materiality_threshold: float = Field(ge=0)
    expected_settlement: float | None = None
    expected_net_transfer: float | None = None
    human_approval_reference: str | None = None


class P12ActionRequest(BaseModel):
    action: str = Field(min_length=3, max_length=200)


class P05DesignRequest(BaseModel):
    case_id: str = Field(min_length=3, max_length=100)
    service_id: str
    service_name: str
    explicit_request: bool
    customer_type: str
    direct_individual_service: bool = False
    service_owner_role: str
    provider_roles: list[str]
    beneficiary_groups: list[str]
    legal_mandate_reference: str
    evidence_references: list[str]
    trigger: str
    objective: str
    channels: list[str]
    inputs: list[str]
    outputs: list[str]
    dependencies: list[str]
    escalation_path: str
    process_id: str
    sla_target: str
    kpis: list[str]
    stages: list[dict[str, Any]]
    proactive_trigger: str
    data_reuse: str
    inclusivity_considerations: list[str]
    current_state_summary: str
    desired_outcome: str
    evidence_items: list[dict[str, str]]
    selected_methods: list[str]
    gate: str = "G1"
    human_approval_reference: str | None = None
    improvement_options: list[str] = Field(default_factory=list)
    prototype_test_evidence: list[str] = Field(default_factory=list)
    risk_controls: list[str] = Field(default_factory=list)
    operating_raci: dict[str, str] = Field(default_factory=dict)
    benefits_baseline: list[str] = Field(default_factory=list)
    monitoring_evidence: list[str] = Field(default_factory=list)
    improvement_decision: str = ""


class P05ActionRequest(BaseModel):
    action: str = Field(min_length=3, max_length=200)


class P06AuditRequest(BaseModel):
    audit_id: str = Field(min_length=3, max_length=100)
    period: str
    division: str
    unit: str
    process_id: str
    process_name: str
    process_version: str
    process_approved_at: str
    process_owner_role: str
    auditor_role: str
    lead_auditor_role: str
    audit_scope: str
    criteria_version: str
    documented_steps: list[str]
    actual_steps: list[str]
    criteria_results: list[dict[str, Any]]
    evidence_items: list[dict[str, str]]
    transaction_samples: list[dict[str, Any]]
    sampling_plan_reference: str
    evidence_plan_reference: str
    finding_review_reference: str | None = None
    human_approval_reference: str | None = None
    assumptions: list[str] = Field(default_factory=list)


class P06CAPAVerificationRequest(BaseModel):
    finding_id: str
    action_owner_role: str
    verifier_role: str
    closure_evidence: list[str]
    effectiveness_passed: bool
    approval_reference: str | None = None


class P06DashboardRequest(BaseModel):
    audits: list[dict[str, Any]]


class P06ActionRequest(BaseModel):
    action: str = Field(min_length=3, max_length=200)


class P07AnalysisRequest(BaseModel):
    case_id: str = Field(min_length=3, max_length=100)
    partner_id: str
    partnership_id: str
    partner_name: str
    entity_name: str
    responsible_person: str
    contact: str
    email: str
    start_date: str
    end_date: str
    partnership_status: str
    strategic_classification: str
    geographic_classification: str
    initiative: str
    innovation: str
    expected_value: str
    objectives: list[str]
    notes: str
    partnership_owner_role: str
    agreement_source_id: str
    agreement_version: str
    agreement_items: list[dict[str, Any]]
    claims: list[dict[str, Any]]
    evidence_items: list[dict[str, Any]]
    evaluation_cycle: str
    as_of_date: str
    response_requested_at: str
    owner_responded: bool
    reminders_recorded: int = Field(ge=0)
    assumptions: list[str] = Field(default_factory=list)


class P07ChangeReviewRequest(BaseModel):
    partnership_id: str
    action: str
    requester_role: str
    first_reviewer_role: str
    first_decision: str
    final_approver_role: str
    final_decision: str
    override_reason: str = ""
    change_reference: str


class P07ActionRequest(BaseModel):
    action: str = Field(min_length=3, max_length=200)

class P10AnalysisRequest(BaseModel):
    assessment_id:str; as_of_date:str; repository_name:str; repository_version:str
    processes:list[dict[str,Any]]; maturity_evidence:list[dict[str,Any]]; migration_evidence:dict[str,str]
class P10ChangeRequest(BaseModel):
    structural:bool=False; legal:bool=False; cross_unit:bool=False; control:bool=False; metadata_only:bool=False
class P10ActionRequest(BaseModel): action:str=Field(min_length=3,max_length=200)

class P13AnalysisRequest(BaseModel):
    assessment_id: str = Field(min_length=3, max_length=100)
    jurisdiction_profile: str
    as_of_date: str
    target_horizon: str
    public_value_outcomes: list[str]
    mandates: list[dict[str, Any]]
    capabilities: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    assumptions: list[str] = Field(default_factory=list)

class P13ActionRequest(BaseModel):
    action: str = Field(min_length=3, max_length=200)


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


@app.get("/p09", include_in_schema=False)
def p09_dashboard() -> FileResponse:
    return FileResponse(P09_DASHBOARD_PATH)


@app.get("/p01", include_in_schema=False)
def p01_dashboard() -> FileResponse:
    return FileResponse(P01_DASHBOARD_PATH)


@app.get("/p02", include_in_schema=False)
def p02_dashboard() -> FileResponse:
    return FileResponse(P02_DASHBOARD_PATH)


@app.get("/p11", include_in_schema=False)
def p11_dashboard() -> FileResponse:
    return FileResponse(P11_DASHBOARD_PATH)


@app.get("/p12", include_in_schema=False)
def p12_dashboard() -> FileResponse:
    return FileResponse(P12_DASHBOARD_PATH)


@app.get("/p05", include_in_schema=False)
def p05_dashboard() -> FileResponse:
    return FileResponse(P05_DASHBOARD_PATH)


@app.get("/p06", include_in_schema=False)
def p06_dashboard() -> FileResponse:
    return FileResponse(P06_DASHBOARD_PATH)


@app.get("/p07", include_in_schema=False)
def p07_dashboard() -> FileResponse:
    return FileResponse(P07_DASHBOARD_PATH)

@app.get("/p10",include_in_schema=False)
def p10_dashboard()->FileResponse:return FileResponse(P10_DASHBOARD_PATH)

@app.get("/p13", include_in_schema=False)
def p13_dashboard() -> FileResponse: return FileResponse(P13_DASHBOARD_PATH)


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "version": app.version, "product_count": len(engine.workflows),
            "synthetic_data_only": True, "p08_config_version": p08_assessor.config["config_version"],
            "p03_config_version": p03_radar.config["config_version"],
            "p04_config_version": p04_detector.config["config_version"],
            "p14_config_version": p14_control_tower.config["config_version"],
            "p09_config_version": p09_performance.config["config_version"],
            "p01_config_version": p01_orchestrator.config["config_version"],
            "p02_config_version": p02_brain.config["config_version"],
            "p11_config_version": p11_reviewer.config["config_version"],
            "p12_config_version": p12_reconciler.config["config_version"],
            "p05_config_version": p05_service_design.config["config_version"],
            "p06_config_version": p06_process_audit.config["config_version"],
            "p07_config_version": p07_partnership.config["config_version"],"p10_config_version":p10_process_intelligence.config["config_version"],
            "p13_config_version": p13_pfm_architecture.config["config_version"]}

@app.get("/p13/config")
def p13_config() -> dict[str, Any]: return p13_pfm_architecture.config

@app.post("/p13/analyze")
def p13_analyze(request: P13AnalysisRequest) -> dict[str, Any]:
    try: return p13_pfm_architecture.analyze(PFMArchitectureInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc: raise as_http_error(exc) from exc

@app.post("/p13/actions/check")
def p13_check_action(request: P13ActionRequest) -> dict[str, Any]: return p13_pfm_architecture.check_action(request.action)

@app.get("/p10/config")
def p10_config():return p10_process_intelligence.config
@app.post("/p10/analyze")
def p10_analyze(request:P10AnalysisRequest):
    try:return p10_process_intelligence.analyze(ProcessPortfolioInput(**request.model_dump())).to_dict()
    except (ValueError,PermissionError,KeyError) as exc:raise as_http_error(exc) from exc
@app.post("/p10/changes/classify")
def p10_change(request:P10ChangeRequest):return p10_process_intelligence.classify_change(**request.model_dump())
@app.post("/p10/actions/check")
def p10_action(request:P10ActionRequest):return p10_process_intelligence.check_action(request.action)


@app.get("/p07/config")
def p07_config() -> dict[str, Any]:
    return p07_partnership.config


@app.post("/p07/analyze")
def p07_analyze(request: P07AnalysisRequest) -> dict[str, Any]:
    try:
        return p07_partnership.analyze(PartnershipInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p07/changes/review")
def p07_review_change(request: P07ChangeReviewRequest) -> dict[str, Any]:
    try:
        return p07_partnership.review_change(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p07/actions/check")
def p07_check_action(request: P07ActionRequest) -> dict[str, Any]:
    return p07_partnership.check_action(request.action)


@app.get("/p06/config")
def p06_config() -> dict[str, Any]:
    return p06_process_audit.config


@app.post("/p06/audit")
def p06_audit(request: P06AuditRequest) -> dict[str, Any]:
    try:
        return p06_process_audit.audit(ProcessAuditInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p06/capa/verify")
def p06_verify_capa(request: P06CAPAVerificationRequest) -> dict[str, Any]:
    try:
        return p06_process_audit.verify_capa(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p06/dashboard")
def p06_division_dashboard(request: P06DashboardRequest) -> dict[str, Any]:
    return p06_process_audit.division_dashboard(request.audits)


@app.post("/p06/actions/check")
def p06_check_action(request: P06ActionRequest) -> dict[str, Any]:
    return p06_process_audit.check_action(request.action)


@app.get("/p05/config")
def p05_config() -> dict[str, Any]:
    return p05_service_design.config


@app.post("/p05/design")
def p05_design(request: P05DesignRequest) -> dict[str, Any]:
    try:
        return p05_service_design.design(ServiceDesignInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p05/actions/check")
def p05_check_action(request: P05ActionRequest) -> dict[str, Any]:
    return p05_service_design.check_action(request.action)


@app.get("/p12/config")
def p12_config() -> dict[str, Any]:
    return p12_reconciler.config


@app.post("/p12/reconcile")
def p12_reconcile(request: P12ReconciliationRequest) -> dict[str, Any]:
    try:
        return p12_reconciler.reconcile(RevenueReconciliationInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p12/actions/check")
def p12_check_action(request: P12ActionRequest) -> dict[str, Any]:
    return p12_reconciler.check_action(request.action)


@app.get("/p11/config")
def p11_config() -> dict[str, Any]:
    return p11_reviewer.config


@app.post("/p11/review")
def p11_review(request: P11ReviewRequest) -> dict[str, Any]:
    try:
        return p11_reviewer.review(IPSASReviewInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p11/actions/check")
def p11_check_action(request: P11ActionRequest) -> dict[str, Any]:
    return p11_reviewer.check_action(request.action)


@app.get("/p02/config")
def p02_config() -> dict[str, Any]:
    return p02_brain.config


@app.post("/p02/analyze")
def p02_analyze(request: P02AnalysisRequest) -> dict[str, Any]:
    try:
        return p02_brain.analyze(FiscalSnapshotInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p02/dataset/readiness")
def p02_dataset_readiness(request: P02DatasetReadinessRequest) -> dict[str, Any]:
    return p02_brain.dataset_readiness(request.loaded_domains)


@app.get("/p01/config")
def p01_config() -> dict[str, Any]:
    return p01_orchestrator.config


@app.post("/p01/analyze")
def p01_analyze(request: P01AnalysisRequest) -> dict[str, Any]:
    try:
        return p01_orchestrator.analyze(PFMCaseInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p01/actions/check")
def p01_check_action(request: P01ActionRequest) -> dict[str, Any]:
    return p01_orchestrator.check_action(request.action)


@app.post("/p01/handoffs/approve")
def p01_approve_handoff(request: P01ApprovalRequest) -> dict[str, Any]:
    try:
        return p01_orchestrator.approve_handoff(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.get("/p09/config")
def p09_config() -> dict[str, Any]:
    return p09_performance.config


@app.post("/p09/review")
def p09_review(request: P09ReviewRequest) -> dict[str, Any]:
    try:
        return p09_performance.review(KPIReviewInput(**request.model_dump())).to_dict()
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


@app.post("/p09/approve")
def p09_approve(request: P09ApprovalRequest) -> dict[str, Any]:
    try:
        return p09_performance.approve(**request.model_dump())
    except (ValueError, PermissionError, KeyError) as exc:
        raise as_http_error(exc) from exc


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
