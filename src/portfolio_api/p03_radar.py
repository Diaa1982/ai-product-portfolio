from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PROTECTED_ACTIONS = {
    "high_impact_external_alert",
    "normative_policy_advice",
    "approved_action",
    "executive_delivery",
    "trusted_memory_promotion",
    "low_confidence_executive_sharing",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class SignalInput:
    title: str
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
    confidence_score: float
    high_impact: bool = False
    normative_policy_advice: bool = False
    sensitive_jurisdiction: bool = False
    executive_delivery: bool = False
    promote_to_memory: bool = False


@dataclass
class SignalResult:
    signal_id: str
    evidence_status: str
    materiality_score: float | None
    materiality_route: str
    confidence_score: float
    output_status: str
    approval_required: bool
    approval_reasons: list[str]
    required_approver_role: str
    fact: str
    interpretation: str
    recommendation: str
    advisory_disclaimer: str
    source_reference: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class StrategicRadar:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.sources = {item["source_id"]: item for item in self.config["source_registry"]}
        self._validate_config()

    def _validate_config(self) -> None:
        total = sum(item["weight"] for item in self.config["materiality_criteria"])
        if round(total, 8) != 1.0:
            raise ValueError("Materiality weights must total 1.0")
        thresholds = self.config["thresholds"]
        if not 0 <= thresholds["analyst_review"] < thresholds["auto_alert"] <= 1:
            raise ValueError("Materiality thresholds are invalid")

    @staticmethod
    def hash_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def verify_evidence(self, signal: SignalInput) -> tuple[str, list[str]]:
        errors: list[str] = []
        source = self.sources.get(signal.source_id)
        if not source:
            return "blocked", ["source_not_registered"]
        if not (source.get("approved") and source.get("active") and source.get("official")):
            errors.append("source_not_approved_official_active")
        hostname = (urlparse(signal.source_url).hostname or "").lower()
        allowed = [domain.lower() for domain in source.get("allowed_domains", [])]
        if not any(hostname == domain or hostname.endswith("." + domain) for domain in allowed):
            errors.append("source_domain_not_allowlisted")
        required = {
            "source_url": signal.source_url,
            "source_version": signal.source_version,
            "published_at": signal.published_at,
            "retrieved_at": signal.retrieved_at,
            "evidence_hash": signal.evidence_hash,
            "fact": signal.fact,
            "change_summary": signal.change_summary,
        }
        errors.extend(f"missing_{key}" for key, value in required.items() if not str(value).strip())
        if signal.evidence_hash and (len(signal.evidence_hash) != 64 or any(c not in "0123456789abcdef" for c in signal.evidence_hash.lower())):
            errors.append("invalid_evidence_hash")
        return ("verified" if not errors else "blocked"), errors

    def score_materiality(self, scores: dict[str, float | None]) -> tuple[float | None, str]:
        weighted = 0.0
        for criterion in self.config["materiality_criteria"]:
            value = scores.get(criterion["id"])
            if value is None:
                return None, "analyst_review"
            value = float(value)
            if not 0 <= value <= 1:
                raise ValueError(f"Score {criterion['id']} must be between 0 and 1")
            weighted += value * criterion["weight"]
        result = round(weighted, 4)
        if result >= self.config["thresholds"]["auto_alert"]:
            return result, "auto_alert_eligible"
        if result >= self.config["thresholds"]["analyst_review"]:
            return result, "analyst_review"
        return result, "low_priority"

    def assess_signal(self, signal: SignalInput) -> SignalResult:
        if signal.audience not in self.config["audiences"]:
            raise ValueError("Unsupported audience")
        if signal.industry not in self.config["approved_industries"]:
            raise ValueError("Industry is not in the approved POC catalog")
        if signal.jurisdiction not in self.config["onboarded_jurisdictions"]:
            raise ValueError("Jurisdiction is not onboarded")
        if signal.pfm_category not in self.config["pfm_categories"]:
            raise ValueError("Unsupported PFM category")
        if not 0 <= signal.confidence_score <= 1:
            raise ValueError("Confidence score must be between 0 and 1")

        evidence_status, evidence_errors = self.verify_evidence(signal)
        materiality, route = self.score_materiality(signal.materiality_scores)
        reasons: list[str] = []
        if signal.high_impact:
            reasons.append("high_impact_external_alert")
        if signal.normative_policy_advice:
            reasons.append("normative_policy_advice")
        if signal.sensitive_jurisdiction:
            reasons.append("sensitive_jurisdiction_output")
        if signal.executive_delivery:
            reasons.append("executive_delivery")
        if signal.promote_to_memory:
            reasons.append("trusted_memory_promotion")
        if signal.executive_delivery and signal.confidence_score < self.config["thresholds"]["executive_confidence"]:
            reasons.append("low_confidence_executive_sharing")

        if evidence_status == "blocked":
            output_status = "blocked_evidence"
            reasons = evidence_errors + reasons
        elif reasons:
            output_status = "pending_human_approval"
        elif route == "analyst_review":
            output_status = "pending_analyst_review"
        else:
            output_status = "eligible_for_delivery" if route == "auto_alert_eligible" else "retained_low_priority"

        source = self.sources.get(signal.source_id, {})
        return SignalResult(
            signal_id=str(uuid.uuid4()), evidence_status=evidence_status,
            materiality_score=materiality, materiality_route=route,
            confidence_score=signal.confidence_score, output_status=output_status,
            approval_required=bool(reasons), approval_reasons=sorted(set(reasons)),
            required_approver_role=self.config["human_approver_role"],
            fact=signal.fact, interpretation=signal.interpretation,
            recommendation=signal.recommendation,
            advisory_disclaimer=self.config["advisory_disclaimer"],
            source_reference={"source_id": signal.source_id, "source_name": source.get("name"),
                              "url": signal.source_url, "version": signal.source_version,
                              "published_at": signal.published_at, "retrieved_at": signal.retrieved_at,
                              "evidence_hash": signal.evidence_hash},
            created_at=utc_now(),
        )

    @staticmethod
    def approve(signal_id: str, action: str, approver_role: str, decision: str, reason: str) -> dict[str, Any]:
        if not signal_id.strip():
            raise ValueError("Signal ID is required")
        if action not in PROTECTED_ACTIONS:
            raise ValueError("Unsupported protected action")
        if approver_role != "STRATEGY_RISK_AUTHORITY":
            raise PermissionError("Protected output requires STRATEGY_RISK_AUTHORITY")
        if decision not in {"approved", "rejected", "returned"}:
            raise ValueError("Invalid decision")
        if len(reason.strip()) < 3:
            raise ValueError("Decision reason is required")
        return {"approval_id": str(uuid.uuid4()), "signal_id": signal_id, "action": action,
                "approver_role": approver_role, "decision": decision, "reason": reason,
                "decided_at": utc_now()}
