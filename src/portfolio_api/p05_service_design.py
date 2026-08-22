from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ServiceDesignInput:
    case_id: str
    service_id: str
    service_name: str
    explicit_request: bool
    customer_type: str
    direct_individual_service: bool
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
    improvement_options: list[str] = field(default_factory=list)
    prototype_test_evidence: list[str] = field(default_factory=list)
    risk_controls: list[str] = field(default_factory=list)
    operating_raci: dict[str, str] = field(default_factory=dict)
    benefits_baseline: list[str] = field(default_factory=list)
    monitoring_evidence: list[str] = field(default_factory=list)
    improvement_decision: str = ""


@dataclass
class ServiceDesignResult:
    case_id: str
    service_classification: str
    completeness_status: str
    missing_information: list[str]
    missing_input_coaching: list[dict[str, str]]
    evidence_register: list[dict[str, str]]
    evidence_by_classification: dict[str, list[dict[str, str]]]
    service_card: dict[str, Any]
    journey: list[dict[str, Any]]
    blueprint: dict[str, list[dict[str, Any]]]
    method_workspace: dict[str, Any]
    deliverable_control: dict[str, Any]
    gate_evaluation: dict[str, Any]
    end_to_end_report: dict[str, Any]
    audit_digest: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ServiceDesignAI:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))

    def classify_service(self, explicit_request: bool, customer_type: str) -> str:
        if not explicit_request:
            return "PUBLIC_BENEFIT"
        if customer_type == "government_entity":
            return "G2G"
        if customer_type in {"private_company", "financial_institution"}:
            return "G2B"
        raise ValueError("The institutional profile cannot classify this explicit-request customer type")

    def _validate(self, case: ServiceDesignInput) -> list[str]:
        missing: list[str] = []
        checks = {
            "service_owner_role": case.service_owner_role,
            "legal_mandate_reference": case.legal_mandate_reference,
            "objective": case.objective,
            "beneficiary_groups": case.beneficiary_groups,
            "inputs": case.inputs,
            "outputs": case.outputs,
            "evidence_references": case.evidence_references,
            "current_state_summary": case.current_state_summary,
            "desired_outcome": case.desired_outcome,
            "sla_target": case.sla_target,
            "kpis": case.kpis,
        }
        missing.extend(key for key, value in checks.items() if not value)
        supplied = {stage.get("stage") for stage in case.stages}
        for stage in self.config["journey_stages"]:
            if stage not in supplied:
                missing.append(f"journey_stage:{stage}")
        if not case.evidence_items:
            missing.append("classified_evidence_items")
        for index, item in enumerate(case.evidence_items):
            if item.get("classification") not in self.config["evidence_classifications"]:
                missing.append(f"evidence_items[{index}].classification")
            if not item.get("claim"):
                missing.append(f"evidence_items[{index}].claim")
            if item.get("classification") == "fact" and not item.get("reference"):
                missing.append(f"evidence_items[{index}].reference")
        return list(dict.fromkeys(missing))

    @staticmethod
    def _coaching(missing: list[str]) -> list[dict[str, str]]:
        prompts = {
            "service_owner_role": "Name the accountable role that can validate the service boundary and decisions.",
            "legal_mandate_reference": "Provide the law, decree, policy or approved mandate reference; do not infer it.",
            "objective": "State the measurable public or institutional value the service must produce.",
            "evidence_references": "Attach approved evidence IDs with source owner, version and date.",
            "classified_evidence_items": "Record each material statement as fact, assumption, AI inference or decision.",
            "sla_target": "Propose an SLA for owner validation; the AI cannot approve it.",
            "kpis": "Define service, experience, efficiency and outcome measures with owners.",
        }
        output = []
        for item in missing:
            base = item.split(":", 1)[0].split("[", 1)[0]
            output.append({"field": item, "prompt": prompts.get(base, "Supply owner-validated information and its evidence reference before advancing the gate.")})
        return output

    def _journey(self, case: ServiceDesignInput) -> list[dict[str, Any]]:
        supplied = {item.get("stage"): item for item in case.stages}
        return [{"stage": name, **supplied.get(name, {}), "status": "evidenced" if supplied.get(name, {}).get("evidence") else "needs_evidence"} for name in self.config["journey_stages"]]

    @staticmethod
    def _blueprint(case: ServiceDesignInput) -> dict[str, list[dict[str, Any]]]:
        layers = {"customer_or_stakeholder": [], "frontstage": [], "backstage": [], "support_process": [], "systems_and_data": [], "evidence_and_controls": []}
        for stage in case.stages:
            name = stage.get("stage", "Unspecified")
            layers["customer_or_stakeholder"].append({"stage": name, "touchpoints": stage.get("touchpoints", [])})
            layers["frontstage"].append({"stage": name, "steps": stage.get("steps", [])})
            layers["backstage"].append({"stage": name, "entities": stage.get("entities", [])})
            layers["support_process"].append({"stage": name, "dependencies": case.dependencies})
            layers["systems_and_data"].append({"stage": name, "systems": stage.get("systems", []), "data_reuse": case.data_reuse})
            layers["evidence_and_controls"].append({"stage": name, "evidence": stage.get("evidence", []), "pain_points": stage.get("pain_points", [])})
        return layers

    def _method_workspace(self, case: ServiceDesignInput) -> dict[str, Any]:
        workspace: dict[str, Any] = {}
        if "three_round_brainstorming" in case.selected_methods:
            workspace["three_round_brainstorming"] = [
                {"round": 1, "purpose": "frame", "prompt": f"What evidence defines the service problem for {case.service_name}?"},
                {"round": 2, "purpose": "diverge", "prompt": "Generate options against the validated constraints; label assumptions and AI inferences."},
                {"round": 3, "purpose": "converge", "prompt": "Group, test and shortlist options using owner-approved criteria."},
            ]
        if "six_thinking_hats" in case.selected_methods:
            workspace["six_thinking_hats"] = {
                "white": "List facts and missing evidence.", "red": "Capture stakeholder concerns without presenting them as facts.",
                "black": "Identify risks, constraints and control gaps.", "yellow": "Identify potential public value and benefits.",
                "green": "Develop alternatives for appraisal.", "blue": "Define the decision, owner, method and next gate."
            }
        if "five_whys" in case.selected_methods:
            workspace["five_whys"] = [{"why": i, "prompt": "Ask why, record evidence, and stop when the answer is unsupported."} for i in range(1, 6)]
        for method in case.selected_methods:
            if method in self.config["methods"] and method not in workspace:
                workspace[method] = {"status": "ready_for_facilitation", "instruction": "Execute with participants, evidence and recorded validation; do not auto-decide."}
        return workspace

    def _gate(self, case: ServiceDesignInput, missing: list[str]) -> dict[str, Any]:
        if case.gate not in self.config["gates"]:
            raise ValueError("Unknown service-design gate")
        requirement_map = {
            "service_owner_role": bool(case.service_owner_role), "legal_mandate_reference": bool(case.legal_mandate_reference),
            "objective": bool(case.objective), "classification_evidence": bool(case.evidence_references),
            "beneficiary_groups": bool(case.beneficiary_groups), "inputs": bool(case.inputs), "outputs": bool(case.outputs),
            "evidence_references": bool(case.evidence_references), "current_state_summary": bool(case.current_state_summary),
            "journey_complete": not any(x.startswith("journey_stage:") for x in missing), "blueprint_complete": bool(case.stages),
            "desired_outcome": bool(case.desired_outcome), "improvement_options": bool(case.improvement_options),
            "prototype_test_evidence": bool(case.prototype_test_evidence), "sla_target": bool(case.sla_target), "kpis": bool(case.kpis),
            "risk_controls": bool(case.risk_controls), "operating_raci": bool(case.operating_raci),
            "benefits_baseline": bool(case.benefits_baseline), "monitoring_evidence": bool(case.monitoring_evidence),
            "improvement_decision": bool(case.improvement_decision),
        }
        required = self.config["gates"][case.gate]["required"]
        missing_gate = [item for item in required if not requirement_map.get(item, False)]
        if not case.human_approval_reference:
            missing_gate.append("human_approval_reference")
        return {"gate": case.gate, "name": self.config["gates"][case.gate]["name"], "status": "READY_FOR_RECORDED_DECISION" if not missing_gate else "BLOCKED", "missing_requirements": missing_gate, "human_decision_required": True, "autonomous_approval_permitted": False}

    def design(self, case: ServiceDesignInput) -> ServiceDesignResult:
        if case.direct_individual_service and not self.config["direct_individual_services_permitted"]:
            raise ValueError("Direct individual service is outside the configured DOF institutional service profile")
        classification = self.classify_service(case.explicit_request, case.customer_type)
        missing = self._validate(case)
        evidence_by = {kind: [] for kind in self.config["evidence_classifications"]}
        for item in case.evidence_items:
            kind = item.get("classification")
            if kind in evidence_by:
                evidence_by[kind].append(dict(item))
        journey = self._journey(case)
        blueprint = self._blueprint(case)
        gate = self._gate(case, missing)
        card = {"service_id": case.service_id, "service_name": case.service_name, "classification": classification, "owner": case.service_owner_role, "providers": case.provider_roles, "beneficiaries": case.beneficiary_groups, "trigger": case.trigger, "inputs": case.inputs, "outputs": case.outputs, "channels": case.channels, "sla_target": case.sla_target, "dependencies": case.dependencies, "escalation_path": case.escalation_path, "expected_value": case.objective}
        ready_count = sum(bool(value) for value in [case.legal_mandate_reference, case.service_owner_role, case.evidence_references, case.stages, case.sla_target, case.kpis, case.desired_outcome])
        deliverables = {"controlled_total": len(self.config["deliverables"]), "available_as_drafts": ready_count, "status": "drafts_require_human_validation", "catalog": self.config["deliverables"]}
        report = {"title": f"End-to-end service report — {case.service_name}", "lifecycle": self.config["lifecycle_phases"], "classification": classification, "current_state": case.current_state_summary, "desired_outcome": case.desired_outcome, "gate": gate, "evidence_summary": {k: len(v) for k, v in evidence_by.items()}, "decision_note": "All service, cost, SLA, launch and stop decisions remain with accountable authorities."}
        payload = {"case": asdict(case), "classification": classification, "missing": missing, "gate": gate}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        return ServiceDesignResult(case.case_id, classification, "complete" if not missing else "insufficient_information", missing, self._coaching(missing), [dict(x) for x in case.evidence_items], evidence_by, card, journey, blueprint, self._method_workspace(case), deliverables, gate, report, digest, ["Synthetic-data technical candidate; no production data is authorized.", "Dubai Services 360, IDCXS and ALMAS references are alignment assumptions requiring local validation, not certification.", "AI outputs are drafts and cannot approve classification, design, costing, SLAs, launch, publication or cessation."])

    def check_action(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower().replace(" ", "_")
        protected = set(self.config["protected_actions"])
        return {"action": normalized, "permitted": normalized not in protected, "human_approval_required": normalized in protected, "reason": "Accountable human authority required" if normalized in protected else "Drafting or analytical support is permitted with audit logging"}
