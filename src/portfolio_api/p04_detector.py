from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PROTECTED_ACTIONS = {"high_impact_signal_publication", "executive_alert", "recommended_action"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class DetectionInput:
    title: str
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


@dataclass
class DetectionResult:
    signal_id: str
    detection_status: str
    evidence_status: str
    evidence_issues: list[str]
    materiality_score: float | None
    confidence_score: float | None
    review_route: str
    publication_status: str
    human_approval_required: bool
    required_approver_role: str
    fact: str
    interpretation: str
    recommendation: str
    opportunity: str
    risk: str
    scenario: str
    kpi_hypothesis: str
    evidence_reference: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SignalDetector:
    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self.sources = {x["source_id"]: x for x in self.config["source_registry"]}
        self._validate_config()

    def _validate_config(self) -> None:
        for name in ("materiality_criteria", "confidence_criteria"):
            if round(sum(x["weight"] for x in self.config[name]), 8) != 1.0:
                raise ValueError(f"{name} weights must total 1.0")

    @staticmethod
    def _score(criteria: list[dict[str, Any]], scores: dict[str, float | None]) -> float | None:
        total = 0.0
        for criterion in criteria:
            value = scores.get(criterion["id"])
            if value is None:
                return None
            value = float(value)
            if not 0 <= value <= 1:
                raise ValueError(f"Score {criterion['id']} must be between 0 and 1")
            total += value * criterion["weight"]
        return round(total, 4)

    def verify_evidence(self, item: DetectionInput) -> tuple[str, list[str]]:
        issues: list[str] = []
        source = self.sources.get(item.source_id)
        if not source:
            return "blocked", ["source_not_registered"]
        if not source.get("approved") or not source.get("active"):
            issues.append("source_not_approved_active")
        if source.get("source_class") not in self.config["allowed_source_classes"]:
            issues.append("source_class_prohibited")
        if source.get("source_class") != "official" and not source.get("official_lineage_required"):
            issues.append("controlled_exception_missing_official_lineage")
        host = (urlparse(item.source_url).hostname or "").lower()
        if not any(host == d or host.endswith("." + d) for d in source.get("allowed_domains", [])):
            issues.append("source_domain_not_allowlisted")
        required = {"current_version": item.current_version, "current_hash": item.current_hash,
                    "snapshot_path": item.snapshot_path, "fetched_at": item.fetched_at,
                    "published_at": item.published_at, "issuing_authority": item.issuing_authority,
                    "provenance_token": item.provenance_token, "change_summary": item.change_summary,
                    "fact": item.fact, "citations": item.citations}
        issues.extend(f"missing_{k}" for k, v in required.items() if v in (None, "", []))
        if item.current_hash and (len(item.current_hash) != 64 or any(c not in "0123456789abcdef" for c in item.current_hash.lower())):
            issues.append("invalid_current_hash")
        for citation in item.citations:
            if not citation.get("exact_span"):
                issues.append("citation_missing_exact_span")
            if not any(citation.get(k) not in (None, "") for k in ("page", "table", "section")):
                issues.append("citation_missing_locator")
        if item.creation_mode == "manual" or (item.creation_mode == "human_high_impact_review" and not item.high_impact):
            issues.append("manual_signal_creation_not_permitted")
        if item.creation_mode not in {"automated_version_change", "human_high_impact_review"}:
            issues.append("invalid_creation_mode")
        requested_quality = item.evidence_quality
        if requested_quality == "blocked" or issues:
            return "blocked", sorted(set(issues))
        if requested_quality in {"pending", "conflict", "partial"}:
            return requested_quality, []
        if requested_quality != "verified":
            return "blocked", ["invalid_evidence_quality"]
        return "verified", []

    def detect(self, item: DetectionInput) -> DetectionResult:
        if item.signal_category not in self.config["signal_categories"]:
            raise ValueError("Unsupported signal category")
        if item.pfm_focus not in self.config["pfm_focus"]:
            raise ValueError("Unsupported PFM focus")
        if item.audience not in self.config["audiences"]:
            raise ValueError("Unsupported audience")

        evidence_status, issues = self.verify_evidence(item)
        materiality = self._score(self.config["materiality_criteria"], item.materiality_scores)
        confidence = self._score(self.config["confidence_criteria"], item.confidence_scores)
        changed = item.current_hash != item.prior_hash or item.current_version != item.prior_version

        if not changed:
            detection_status, route = "no_material_change", "no_signal"
        elif evidence_status == "blocked":
            detection_status, route = "blocked", "evidence_remediation"
        elif materiality is None or confidence is None or evidence_status in {"pending", "conflict", "partial"}:
            detection_status, route = "candidate_signal", "analyst_evidence_review"
        elif materiality >= self.config["thresholds"]["priority_review"]:
            detection_status, route = "candidate_signal", "priority_analyst_review"
        elif materiality >= self.config["thresholds"]["standard_review"]:
            detection_status, route = "candidate_signal", "standard_review"
        else:
            detection_status, route = "candidate_signal", "evidence_enhancement_queue"

        approval_required = item.high_impact
        if detection_status in {"blocked", "no_material_change"}:
            publication = "blocked"
        elif approval_required:
            publication = "pending_human_approval"
        else:
            publication = "not_published_analyst_review_required"

        source = self.sources.get(item.source_id, {})
        return DetectionResult(
            signal_id=str(uuid.uuid4()), detection_status=detection_status,
            evidence_status=evidence_status, evidence_issues=issues,
            materiality_score=materiality, confidence_score=confidence, review_route=route,
            publication_status=publication, human_approval_required=approval_required,
            required_approver_role=self.config["human_approver_role"],
            fact=item.fact, interpretation=item.interpretation, recommendation=item.recommendation,
            opportunity=item.opportunity, risk=item.risk, scenario=item.scenario,
            kpi_hypothesis=item.kpi_hypothesis,
            evidence_reference={"source_id": item.source_id, "source_name": source.get("name"),
                "url": item.source_url, "current_version": item.current_version,
                "prior_version": item.prior_version, "current_hash": item.current_hash,
                "prior_hash": item.prior_hash, "snapshot_path": item.snapshot_path,
                "fetched_at": item.fetched_at, "published_at": item.published_at,
                "issuing_authority": item.issuing_authority,
                "provenance_token": item.provenance_token, "citations": item.citations},
            created_at=utc_now(),
        )

    @staticmethod
    def approve(signal_id: str, action: str, approver_role: str, decision: str, reason: str) -> dict[str, Any]:
        if action not in PROTECTED_ACTIONS:
            raise ValueError("Unsupported protected action")
        if approver_role != "STRATEGY_RISK_AUTHORITY":
            raise PermissionError("Protected publication requires STRATEGY_RISK_AUTHORITY")
        if decision not in {"approved", "rejected", "returned"}:
            raise ValueError("Invalid decision")
        if not signal_id.strip() or len(reason.strip()) < 3:
            raise ValueError("Signal ID and decision reason are required")
        return {"approval_id": str(uuid.uuid4()), "signal_id": signal_id, "action": action,
                "approver_role": approver_role, "decision": decision, "reason": reason,
                "decided_at": utc_now()}
