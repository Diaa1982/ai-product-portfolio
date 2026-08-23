from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class ITManagementInput:
    assessment_id: str
    as_of_date: str
    operating_scope: str
    services: list[dict[str, Any]]
    work_items: list[dict[str, Any]]
    configuration_items: list[dict[str, Any]]
    portfolio_items: list[dict[str, Any]]
    risks_controls: list[dict[str, Any]]
    evidence_register: list[dict[str, Any]]
    proposed_action: dict[str, Any]
    assumptions: list[str]


@dataclass
class ITManagementResult:
    assessment_id: str
    assessment_status: str
    integrated_health: dict[str, Any]
    service_management: dict[str, Any]
    change_management: dict[str, Any]
    configuration_quality: dict[str, Any]
    portfolio_alignment: dict[str, Any]
    risk_control_readiness: dict[str, Any]
    exceptions: list[dict[str, str]]
    recommendations: list[dict[str, Any]]
    decision_package: dict[str, Any]
    audit_digest: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class IntegratedITManagementAI:
    def __init__(self, path: str | Path):
        self.config = json.loads(Path(path).read_text(encoding="utf-8"))

    @staticmethod
    def _percent(part: int | float, total: int | float) -> float:
        return round(part / total * 100, 2) if total else 0.0

    def analyze(self, case: ITManagementInput) -> ITManagementResult:
        valid_evidence = {e.get("evidence_id") for e in case.evidence_register if e.get("valid") is True}
        exceptions: list[dict[str, str]] = []

        collections = {
            "service": (case.services, "service_id"),
            "work_item": (case.work_items, "work_item_id"),
            "configuration_item": (case.configuration_items, "ci_id"),
            "portfolio_item": (case.portfolio_items, "portfolio_item_id"),
            "risk_control": (case.risks_controls, "record_id"),
        }
        for kind, (items, id_field) in collections.items():
            ids = [x.get(id_field) for x in items if x.get(id_field)]
            for duplicate in sorted({x for x in ids if ids.count(x) > 1}):
                exceptions.append({"record_id": duplicate, "exception": f"duplicate_{kind}_id"})
            for item in items:
                rid = item.get(id_field, "UNKNOWN")
                for field in (id_field, "owner_role", "status"):
                    if not item.get(field):
                        exceptions.append({"record_id": rid, "exception": f"missing_{field}"})
                refs = item.get("evidence_refs", [])
                if not refs or any(ref not in valid_evidence for ref in refs):
                    exceptions.append({"record_id": rid, "exception": "missing_or_invalid_evidence"})

        service_ids = {x.get("service_id") for x in case.services}
        ci_ids = {x.get("ci_id") for x in case.configuration_items}
        for item in case.work_items:
            if item.get("service_id") not in service_ids:
                exceptions.append({"record_id": item.get("work_item_id", "UNKNOWN"), "exception": "unknown_service_link"})
            if item.get("type") not in self.config["work_item_types"]:
                exceptions.append({"record_id": item.get("work_item_id", "UNKNOWN"), "exception": "invalid_work_item_type"})
        for ci in case.configuration_items:
            for dependency in ci.get("depends_on", []):
                if dependency not in ci_ids:
                    exceptions.append({"record_id": ci.get("ci_id", "UNKNOWN"), "exception": "orphan_ci_dependency"})

        incidents = [x for x in case.work_items if x.get("type") == "incident"]
        closed_incidents = [x for x in incidents if x.get("status") == "closed"]
        sla_met = [x for x in closed_incidents if x.get("resolution_minutes", 10**9) <= x.get("sla_minutes", 0)]
        mtta_values = [x["acknowledgement_minutes"] for x in incidents if isinstance(x.get("acknowledgement_minutes"), (int, float))]
        mttr_values = [x["resolution_minutes"] for x in closed_incidents if isinstance(x.get("resolution_minutes"), (int, float))]
        service_management = {
            "service_count": len(case.services),
            "incident_count": len(incidents),
            "open_incidents": len(incidents) - len(closed_incidents),
            "sla_attainment_percent": self._percent(len(sla_met), len(closed_incidents)),
            "mtta_minutes": round(sum(mtta_values) / len(mtta_values), 2) if mtta_values else None,
            "mttr_minutes": round(sum(mttr_values) / len(mttr_values), 2) if mttr_values else None,
            "human_incident_closure_required": True,
        }

        changes = [x for x in case.work_items if x.get("type") == "change"]
        implemented = [x for x in changes if x.get("status") in {"implemented", "closed"}]
        successful = [x for x in implemented if x.get("outcome") == "successful"]
        emergency = [x for x in changes if x.get("change_type") == "emergency"]
        change_management = {
            "change_count": len(changes),
            "implemented_count": len(implemented),
            "success_percent": self._percent(len(successful), len(implemented)),
            "emergency_percent": self._percent(len(emergency), len(changes)),
            "approval_status": "DRAFT_FOR_CHANGE_AUTHORITY",
            "autonomous_production_change_permitted": False,
        }

        linked_cis = [x for x in case.configuration_items if x.get("service_id") in service_ids]
        controlled_cis = [x for x in case.configuration_items if x.get("control_refs")]
        configuration_quality = {
            "ci_count": len(case.configuration_items),
            "service_link_coverage_percent": self._percent(len(linked_cis), len(case.configuration_items)),
            "control_link_coverage_percent": self._percent(len(controlled_cis), len(case.configuration_items)),
            "orphan_count": len(case.configuration_items) - len(linked_cis),
        }

        aligned = [x for x in case.portfolio_items if x.get("strategy_refs")]
        benefit_evidenced = [x for x in case.portfolio_items if x.get("benefit_evidence_refs") and all(r in valid_evidence for r in x.get("benefit_evidence_refs", []))]
        at_risk = [x for x in case.portfolio_items if x.get("delivery_risk", 0) >= self.config["thresholds"]["high_delivery_risk"]]
        portfolio_alignment = {
            "item_count": len(case.portfolio_items),
            "strategy_alignment_percent": self._percent(len(aligned), len(case.portfolio_items)),
            "benefit_evidence_percent": self._percent(len(benefit_evidenced), len(case.portfolio_items)),
            "high_delivery_risk_count": len(at_risk),
            "investment_recommendations_are_drafts": True,
        }

        controls = [x for x in case.risks_controls if x.get("record_type") == "control"]
        risks = [x for x in case.risks_controls if x.get("record_type") == "risk"]
        effective = [x for x in controls if x.get("effectiveness") == "effective"]
        evidenced = [x for x in controls if x.get("evidence_refs") and all(r in valid_evidence for r in x["evidence_refs"])]
        high_risks = [x for x in risks if x.get("residual_score", 0) >= self.config["thresholds"]["high_residual_risk"]]
        risk_control_readiness = {
            "risk_count": len(risks),
            "control_count": len(controls),
            "effective_control_percent": self._percent(len(effective), len(controls)),
            "evidence_coverage_percent": self._percent(len(evidenced), len(controls)),
            "high_residual_risk_count": len(high_risks),
            "formal_risk_acceptance_recorded": False,
        }

        component_scores = {
            "service": service_management["sla_attainment_percent"],
            "change": change_management["success_percent"],
            "configuration": configuration_quality["service_link_coverage_percent"],
            "portfolio": portfolio_alignment["strategy_alignment_percent"],
            "control": risk_control_readiness["evidence_coverage_percent"],
        }
        weights = self.config["health_weights"]
        included = {k: v for k, v in component_scores.items() if v is not None}
        denominator = sum(weights[k] for k in included)
        score = round(sum(included[k] * weights[k] for k in included) / denominator, 2) if denominator else 0.0
        integrated_health = {"score_percent": score, "component_scores": component_scores, "weights": weights, "status": "DRAFT_MANAGEMENT_VIEW", "human_validation_required": True}

        recommendations = []
        if exceptions:
            recommendations.append({"priority": "HIGH", "recommendation": "Resolve data, linkage and evidence exceptions before relying on the integrated view.", "status": "DRAFT"})
        if high_risks:
            recommendations.append({"priority": "HIGH", "recommendation": "Route high residual technology risks to accountable risk owners.", "status": "DRAFT"})
        if at_risk:
            recommendations.append({"priority": "MEDIUM", "recommendation": "Review delivery recovery options and benefit assumptions with the portfolio authority.", "status": "DRAFT"})

        action_check = self.check_action(case.proposed_action.get("action", "analyze_it_management"))
        decision_package = {
            "action": case.proposed_action,
            "action_check": action_check,
            "status": "HUMAN_DECISION_REQUIRED" if action_check["human_authority_required"] else "ANALYSIS_ONLY",
            "required_roles": self.config["decision_roles"],
            "approval_recorded": False,
        }
        payload = {"case": asdict(case), "exceptions": exceptions, "health": integrated_health, "decision": decision_package}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        limitations = [
            "Synthetic-only technical deployment candidate; no live ITSM, GRC, PMO, audit, ITOM, CMDB, ERP or identity integration is represented.",
            "ITIL 4, COBIT, ISO, TOGAF and PMBOK are alignment references; this product does not claim certification or replace those frameworks.",
            "Indicators are deterministic management aids and depend on approved definitions, complete source data, valid timestamps and evidence.",
            "Authorized humans approve production changes, incident closure, risk acceptance, budgets, contracts, service commitments, retirement and go-live.",
        ]
        return ITManagementResult(case.assessment_id, "EXCEPTIONS_FOUND" if exceptions else "VALID", integrated_health, service_management, change_management, configuration_quality, portfolio_alignment, risk_control_readiness, exceptions, recommendations, decision_package, digest, limitations)

    def check_action(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower().replace(" ", "_")
        protected = normalized in self.config["protected_actions"]
        return {"action": normalized, "permitted": not protected, "human_authority_required": protected, "reason": "Named accountable authority approval required" if protected else "Evidence-led analysis permitted with audit logging"}
