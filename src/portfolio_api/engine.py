from __future__ import annotations

import hashlib
import json
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TERMINAL_STATUSES = {"approved", "rejected", "closed"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


@dataclass
class AuditEvent:
    event_id: str
    event_type: str
    actor_role: str
    timestamp: str
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str


@dataclass
class ProductCase:
    case_id: str
    product_id: str
    title: str
    owner_role: str
    status: str = "draft"
    risk_level: str = "low"
    inputs: dict[str, Any] = field(default_factory=dict)
    calculations: dict[str, float] = field(default_factory=dict)
    findings: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    approvals: list[dict[str, Any]] = field(default_factory=list)
    audit_log: list[AuditEvent] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProductCase":
        copy = dict(data)
        copy["audit_log"] = [AuditEvent(**event) for event in copy.get("audit_log", [])]
        return cls(**copy)


class JsonCaseStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._lock = threading.RLock()

    def _read(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, cases: dict[str, dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".tmp")
        temp.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")
        temp.replace(self.path)

    def save(self, case: ProductCase) -> None:
        with self._lock:
            cases = self._read()
            cases[case.case_id] = case.to_dict()
            self._write(cases)

    def get(self, case_id: str) -> ProductCase:
        with self._lock:
            data = self._read().get(case_id)
        if data is None:
            raise KeyError(case_id)
        return ProductCase.from_dict(data)

    def list(self, product_id: str | None = None) -> list[ProductCase]:
        with self._lock:
            values = list(self._read().values())
        cases = [ProductCase.from_dict(value) for value in values]
        if product_id:
            cases = [case for case in cases if case.product_id == product_id]
        return sorted(cases, key=lambda item: item.updated_at, reverse=True)


class PortfolioEngine:
    def __init__(self, workflow_path: str | Path, store: JsonCaseStore):
        self.workflow_path = Path(workflow_path)
        self.store = store
        self.workflows = self._load_workflows()

    def _load_workflows(self) -> dict[str, dict[str, Any]]:
        data = json.loads(self.workflow_path.read_text(encoding="utf-8"))
        return {item["product_id"]: item for item in data["workflows"]}

    def _workflow(self, product_id: str) -> dict[str, Any]:
        try:
            return self.workflows[product_id]
        except KeyError as exc:
            raise ValueError(f"Unknown product: {product_id}") from exc

    def _event(self, case: ProductCase, event_type: str, actor_role: str, payload: dict[str, Any]) -> None:
        previous_hash = case.audit_log[-1].event_hash if case.audit_log else "GENESIS"
        body = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "actor_role": actor_role,
            "timestamp": utc_now(),
            "payload": payload,
            "previous_hash": previous_hash,
        }
        case.audit_log.append(AuditEvent(**body, event_hash=stable_hash(body)))
        case.updated_at = body["timestamp"]

    def create_case(self, product_id: str, title: str, owner_role: str, inputs: dict[str, Any]) -> ProductCase:
        workflow = self._workflow(product_id)
        missing = [field for field in workflow["required_inputs"] if inputs.get(field) in (None, "")]
        if missing:
            raise ValueError(f"Missing required inputs: {', '.join(missing)}")
        case = ProductCase(case_id=str(uuid.uuid4()), product_id=product_id, title=title, owner_role=owner_role, inputs=inputs)
        self._event(case, "case.created", owner_role, {"workflow_version": workflow["version"]})
        self.store.save(case)
        return case

    def add_evidence(self, case_id: str, actor_role: str, evidence: dict[str, Any]) -> ProductCase:
        case = self.store.get(case_id)
        if case.status in TERMINAL_STATUSES:
            raise ValueError("Cannot change a terminal case")
        required = {"evidence_id", "source_id", "source_version", "content_hash", "classification"}
        missing = sorted(required - set(evidence))
        if missing:
            raise ValueError(f"Evidence missing fields: {', '.join(missing)}")
        case.evidence.append(evidence)
        self._event(case, "evidence.added", actor_role, {"evidence_id": evidence["evidence_id"]})
        self.store.save(case)
        return case

    @staticmethod
    def _pfm_calculations(inputs: dict[str, Any]) -> dict[str, float]:
        numeric = {key: float(inputs.get(key, 0) or 0) for key in ("budget", "actual", "commitments")}
        budget, actual, commitments = numeric["budget"], numeric["actual"], numeric["commitments"]
        return {
            "variance": actual - budget,
            "utilization": actual / budget if budget else 0.0,
            "available_balance": budget - actual - commitments,
            "commitment_pressure": commitments / budget if budget else 0.0,
        }

    def evaluate(self, case_id: str, actor_role: str = "AI_ANALYST") -> ProductCase:
        case = self.store.get(case_id)
        workflow = self._workflow(case.product_id)
        if case.status in TERMINAL_STATUSES:
            raise ValueError("Cannot evaluate a terminal case")

        calculations: dict[str, float] = {}
        if workflow["calculation_profile"] == "pfm_execution":
            calculations = self._pfm_calculations(case.inputs)
        elif workflow["calculation_profile"] == "weighted_score":
            value = float(case.inputs.get("value_score", 0))
            feasibility = float(case.inputs.get("feasibility_score", 0))
            calculations = {"weighted_score": round(value * 0.6 + feasibility * 0.4, 4)}

        findings: list[dict[str, Any]] = []
        if calculations.get("available_balance", 0) < 0:
            findings.append({"code": "NEGATIVE_AVAILABLE_BALANCE", "risk": "critical", "material": True})
        if calculations.get("utilization", 0) > workflow["thresholds"].get("high_utilization", 1.0):
            findings.append({"code": "HIGH_UTILIZATION", "risk": "high", "material": True})
        if calculations.get("commitment_pressure", 0) > workflow["thresholds"].get("commitment_pressure", 1.0):
            findings.append({"code": "COMMITMENT_PRESSURE", "risk": "medium", "material": True})
        if "weighted_score" in calculations and calculations["weighted_score"] < workflow["thresholds"].get("minimum_score", 0):
            findings.append({"code": "BELOW_MINIMUM_SCORE", "risk": "medium", "material": True})

        evidence_required = workflow.get("evidence_required_for_material_findings", True)
        if any(item["material"] for item in findings) and evidence_required and not case.evidence:
            findings.append({"code": "MISSING_MATERIAL_EVIDENCE", "risk": "high", "material": True})

        risk_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        case.risk_level = max((item["risk"] for item in findings), key=risk_order.get, default="low")
        case.calculations = calculations
        case.findings = findings
        case.recommendations = [
            {
                "recommendation_id": str(uuid.uuid4()),
                "type": "review",
                "text": "Review findings, supporting evidence and control implications before decision.",
                "decision_authority": workflow["approval_role"],
            }
        ]
        case.status = "paused_critical" if case.risk_level == "critical" else "analysed"
        self._event(case, "case.evaluated", actor_role, {"risk_level": case.risk_level, "finding_count": len(findings)})
        self.store.save(case)
        return case

    def submit_for_approval(self, case_id: str, actor_role: str) -> ProductCase:
        case = self.store.get(case_id)
        workflow = self._workflow(case.product_id)
        if case.status not in {"analysed", "paused_critical"}:
            raise ValueError("Case must be analysed before submission")
        if any(item.get("material") for item in case.findings) and not case.evidence:
            raise ValueError("Material findings require evidence before submission")
        approval = {
            "approval_id": str(uuid.uuid4()),
            "gate": workflow["approval_gate"],
            "required_role": workflow["approval_role"],
            "status": "pending",
            "requested_at": utc_now(),
        }
        case.approvals.append(approval)
        case.status = "pending_approval"
        self._event(case, "approval.requested", actor_role, {"approval_id": approval["approval_id"]})
        self.store.save(case)
        return case

    def decide(self, case_id: str, approver_role: str, decision: str, reason: str) -> ProductCase:
        case = self.store.get(case_id)
        if case.status != "pending_approval" or not case.approvals:
            raise ValueError("Case has no pending approval")
        pending = case.approvals[-1]
        if pending["required_role"] != approver_role:
            raise PermissionError(f"Approval requires role {pending['required_role']}")
        if decision not in {"approved", "rejected", "returned"}:
            raise ValueError("Invalid decision")
        pending.update({"status": decision, "decided_at": utc_now(), "decided_by_role": approver_role, "reason": reason})
        case.status = decision
        self._event(case, f"approval.{decision}", approver_role, {"approval_id": pending["approval_id"], "reason": reason})
        self.store.save(case)
        return case

    @staticmethod
    def verify_audit_chain(case: ProductCase) -> bool:
        previous = "GENESIS"
        for event in case.audit_log:
            body = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "actor_role": event.actor_role,
                "timestamp": event.timestamp,
                "payload": event.payload,
                "previous_hash": event.previous_hash,
            }
            if event.previous_hash != previous or event.event_hash != stable_hash(body):
                return False
            previous = event.event_hash
        return True
