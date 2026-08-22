from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class PFMArchitectureInput:
    assessment_id: str
    jurisdiction_profile: str
    as_of_date: str
    target_horizon: str
    public_value_outcomes: list[str]
    mandates: list[dict[str, Any]]
    capabilities: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    assumptions: list[str]


@dataclass
class PFMArchitectureResult:
    assessment_id: str
    assessment_status: str
    coverage: dict[str, Any]
    value_chain: dict[str, Any]
    capability_heatmap: list[dict[str, Any]]
    alignment: dict[str, Any]
    exceptions: list[dict[str, str]]
    roadmap: list[dict[str, Any]]
    decision_package: dict[str, Any]
    audit_digest: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PFMBusinessArchitecture:
    """Deterministic, evidence-led PFM business-architecture assessment."""

    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))

    def analyze(self, case: PFMArchitectureInput) -> PFMArchitectureResult:
        if not case.assessment_id.strip():
            raise ValueError("assessment_id is required")
        if not case.public_value_outcomes:
            raise ValueError("at least one public_value_outcome is required")

        evidence_ids = {e.get("evidence_id") for e in case.evidence if e.get("evidence_id")}
        mandate_ids = {m.get("mandate_id") for m in case.mandates if m.get("mandate_id")}
        exceptions: list[dict[str, str]] = []
        capability_ids = [c.get("capability_id") for c in case.capabilities]
        for duplicate in sorted({x for x in capability_ids if x and capability_ids.count(x) > 1}):
            exceptions.append({"capability_id": duplicate, "exception": "duplicate_capability_id"})

        required_links = self.config["required_links"]
        total_links = 0
        completed_links = 0
        stage_counts = {stage["id"]: 0 for stage in self.config["value_chain"]}
        heatmap: list[dict[str, Any]] = []

        for capability in case.capabilities:
            cid = capability.get("capability_id", "UNKNOWN")
            stage = capability.get("value_chain_stage")
            if stage not in stage_counts:
                exceptions.append({"capability_id": cid, "exception": "invalid_value_chain_stage"})
            else:
                stage_counts[stage] += 1

            for field in required_links:
                total_links += 1
                value = capability.get(field)
                if value:
                    completed_links += 1
                else:
                    exceptions.append({"capability_id": cid, "exception": f"missing_link_{field}"})

            unknown_mandates = sorted(set(capability.get("mandate_refs", [])) - mandate_ids)
            if unknown_mandates:
                exceptions.append({"capability_id": cid, "exception": "unknown_mandate_reference"})

            refs = capability.get("evidence_refs", [])
            unknown_evidence = sorted(set(refs) - evidence_ids)
            if unknown_evidence:
                exceptions.append({"capability_id": cid, "exception": "unknown_evidence_reference"})

            current = capability.get("current_maturity")
            target = capability.get("target_maturity")
            evidenced = bool(refs) and not unknown_evidence and current in range(1, 6)
            if target not in range(1, 6):
                exceptions.append({"capability_id": cid, "exception": "invalid_target_maturity"})
                target = None
            if current not in range(1, 6):
                exceptions.append({"capability_id": cid, "exception": "invalid_current_maturity"})
                current = None
                evidenced = False

            gap = max(target - current, 0) if evidenced and target else None
            criticality = capability.get("criticality", 1)
            if criticality not in range(1, 6):
                criticality = 1
                exceptions.append({"capability_id": cid, "exception": "invalid_criticality"})
            priority = criticality * gap if gap is not None else None
            heatmap.append({
                "capability_id": cid,
                "name": capability.get("name", ""),
                "domain": capability.get("domain", ""),
                "owner_role": capability.get("owner_role", ""),
                "current_maturity": current if evidenced else None,
                "target_maturity": target,
                "gap": gap,
                "criticality": criticality,
                "priority_score": priority,
                "evidence_status": "EVIDENCED" if evidenced else "INSUFFICIENT_EVIDENCE",
            })

        coverage_percent = round(completed_links / total_links * 100, 2) if total_links else 0.0
        evidenced_rows = [x for x in heatmap if x["evidence_status"] == "EVIDENCED"]
        average_maturity = round(sum(x["current_maturity"] for x in evidenced_rows) / len(evidenced_rows), 2) if evidenced_rows else None
        missing_stages = [stage for stage, count in stage_counts.items() if count == 0]
        if missing_stages:
            for stage in missing_stages:
                exceptions.append({"capability_id": "PORTFOLIO", "exception": f"unmapped_value_chain_stage:{stage}"})

        roadmap = self._roadmap(heatmap)
        pefa_refs = sorted({r for c in case.capabilities for r in c.get("pefa_refs", [])})
        ipsas_refs = sorted({r for c in case.capabilities for r in c.get("ipsas_refs", [])})
        payload = {"case": asdict(case), "exceptions": exceptions, "roadmap": roadmap}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()

        return PFMArchitectureResult(
            assessment_id=case.assessment_id,
            assessment_status="TRACEABLE_DRAFT" if not exceptions else "EXCEPTIONS_FOUND",
            coverage={
                "required_links_assessed": total_links,
                "completed_links": completed_links,
                "coverage_percent": coverage_percent,
                "evidenced_capabilities": len(evidenced_rows),
                "capability_count": len(case.capabilities),
                "average_evidenced_maturity": average_maturity,
                "formal_maturity_rating": False,
            },
            value_chain={"stage_counts": stage_counts, "missing_stages": missing_stages},
            capability_heatmap=sorted(heatmap, key=lambda x: (-(x["priority_score"] or -1), x["capability_id"])),
            alignment={
                "pefa": {"mode": "informed", "references": pefa_refs, "compliance_conclusion": False},
                "ipsas": {"mode": "oriented", "references": ipsas_refs, "compliance_conclusion": False},
            },
            exceptions=exceptions,
            roadmap=roadmap,
            decision_package={
                "status": "DRAFT_FOR_DESIGN_AUTHORITY",
                "human_approval_required": True,
                "required_approvals": self.config["required_approvals"],
                "autonomous_operating_model_change_permitted": False,
            },
            audit_digest=digest,
            limitations=[
                "Synthetic-only technical deployment candidate; no production repository or system connection is represented.",
                "PEFA references are informative and IPSAS references are orientation metadata; neither is a certification or compliance conclusion.",
                "Maturity is reported only where referenced evidence exists; benchmark and target-state claims require independent validation.",
                "AI may map, validate and recommend, but accountable officials approve mandates, ownership, target states, investments and operating-model changes.",
            ],
        )

    @staticmethod
    def _roadmap(heatmap: list[dict[str, Any]]) -> list[dict[str, Any]]:
        candidates = [x for x in heatmap if x["priority_score"] and x["priority_score"] > 0]
        rows = []
        for item in sorted(candidates, key=lambda x: (-x["priority_score"], x["capability_id"])):
            score = item["priority_score"]
            wave = "W1_FOUNDATION" if score >= 12 else "W2_INTEGRATE" if score >= 6 else "W3_OPTIMIZE"
            rows.append({
                "capability_id": item["capability_id"],
                "wave": wave,
                "priority_score": score,
                "recommendation": "Close the evidenced capability gap through an owner-approved initiative and measurable outcome.",
                "status": "DRAFT",
            })
        return rows

    def check_action(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower().replace(" ", "_")
        protected = normalized in self.config["protected_actions"]
        return {
            "action": normalized,
            "permitted": not protected,
            "human_authority_required": protected,
            "reason": "Authorized public-finance or design authority approval required" if protected else "Analytical support permitted with evidence citations and audit logging",
        }
