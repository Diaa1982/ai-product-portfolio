from __future__ import annotations

import hashlib
import json
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class CycleTimeBenchmarkInput:
    assessment_id: str
    as_of_date: str
    jurisdiction_profile: str
    processes: list[dict[str, Any]]
    benchmark_register: list[dict[str, Any]]
    source_library: list[dict[str, Any]]
    assumptions: list[str]


@dataclass
class CycleTimeBenchmarkResult:
    assessment_id: str
    assessment_status: str
    portfolio_summary: dict[str, Any]
    process_results: list[dict[str, Any]]
    source_qa: list[dict[str, str]]
    unbenchmarked_queue: list[dict[str, str]]
    methodology_qa: list[dict[str, str]]
    decision_package: dict[str, Any]
    audit_digest: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PFMCycleTimeBenchmark:
    def __init__(self, config_path: str | Path):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))

    def analyze(self, case: CycleTimeBenchmarkInput) -> CycleTimeBenchmarkResult:
        if not case.assessment_id.strip():
            raise ValueError("assessment_id is required")
        source_ids = {x.get("source_id") for x in case.source_library if x.get("source_id")}
        benchmarks = {x.get("process_id"): x for x in case.benchmark_register if x.get("process_id")}
        source_qa: list[dict[str, str]] = []
        method_qa: list[dict[str, str]] = []
        queue: list[dict[str, str]] = []
        results: list[dict[str, Any]] = []

        duplicate_benchmark_ids = [pid for pid in benchmarks if sum(1 for x in case.benchmark_register if x.get("process_id") == pid) > 1]
        for pid in sorted(duplicate_benchmark_ids):
            method_qa.append({"process_id": pid, "issue": "duplicate_benchmark_record"})

        for process in case.processes:
            pid = process.get("process_id", "UNKNOWN")
            samples = process.get("actual_cycle_times", [])
            valid_samples = [float(x) for x in samples if isinstance(x, (int, float)) and x >= 0]
            if len(valid_samples) != len(samples):
                method_qa.append({"process_id": pid, "issue": "invalid_actual_sample"})
            actual_median = round(statistics.median(valid_samples), 2) if valid_samples else None
            actual_average = round(statistics.mean(valid_samples), 2) if valid_samples else None
            if len(valid_samples) < self.config["minimum_internal_sample"]:
                method_qa.append({"process_id": pid, "issue": "small_internal_sample"})

            benchmark = benchmarks.get(pid)
            if not benchmark:
                queue.append({"process_id": pid, "reason": "no_benchmark_record"})
                results.append(self._no_benchmark(process, actual_median, actual_average, len(valid_samples), "NO_BENCHMARK"))
                continue

            reliability = benchmark.get("reliability_class", "D")
            match_type = benchmark.get("match_type", "no_data")
            benchmark_type = benchmark.get("benchmark_type")
            source_id = benchmark.get("source_id")
            value = benchmark.get("benchmark_value")
            unit_match = benchmark.get("unit") == process.get("unit")
            start_match = benchmark.get("start_point") == process.get("start_point")
            end_match = benchmark.get("end_point") == process.get("end_point")
            scope_match = benchmark.get("scope_profile") == process.get("scope_profile")
            valid_type = benchmark_type in self.config["benchmark_types"]
            valid_reliability = reliability in self.config["reliability_classes"]
            valid_match = match_type in self.config["match_types"]

            if not valid_type: method_qa.append({"process_id": pid, "issue": "invalid_benchmark_type"})
            if not valid_reliability: method_qa.append({"process_id": pid, "issue": "invalid_reliability_class"})
            if not valid_match: method_qa.append({"process_id": pid, "issue": "invalid_match_type"})
            if source_id not in source_ids:
                source_qa.append({"process_id": pid, "issue": "missing_or_unknown_source"})
            if not benchmark.get("source_url"):
                source_qa.append({"process_id": pid, "issue": "missing_source_link"})
            if not benchmark.get("evidence_note"):
                source_qa.append({"process_id": pid, "issue": "missing_evidence_note"})
            if match_type in {"nearest", "proxy"} and not benchmark.get("match_rationale"):
                method_qa.append({"process_id": pid, "issue": "missing_match_rationale"})

            comparability = round(sum([unit_match, start_match, end_match, scope_match]) / 4, 2)
            source_valid = source_id in source_ids and bool(benchmark.get("source_url")) and bool(benchmark.get("evidence_note"))
            value_allowed = source_valid and reliability != "D" and match_type != "no_data" and isinstance(value, (int, float)) and value >= 0
            if value is not None and not value_allowed:
                source_qa.append({"process_id": pid, "issue": "benchmark_value_suppressed"})
                value = None

            aggregation = process.get("aggregation_method")
            if aggregation not in self.config["aggregation_methods"]:
                method_qa.append({"process_id": pid, "issue": "invalid_aggregation_method"})
            if aggregation == "sequential_sum" and not process.get("steps_consecutive", False):
                method_qa.append({"process_id": pid, "issue": "nonconsecutive_steps_cannot_be_summed"})
            if aggregation == "volume_weighted_average" and not process.get("volume_weights"):
                method_qa.append({"process_id": pid, "issue": "missing_volume_weights"})

            reliability_weight = self.config["reliability_classes"].get(reliability, {}).get("weight", 0)
            match_weight = self.config["match_weights"].get(match_type, 0)
            sample_weight = min(len(valid_samples) / self.config["confidence_sample_cap"], 1)
            confidence = round((reliability_weight * .45 + match_weight * .25 + comparability * .2 + sample_weight * .1), 2)
            directional_only = reliability == "C" or match_type == "proxy"
            eligible = value is not None and not directional_only and comparability >= self.config["minimum_comparability"]

            gap = round(actual_median - value, 2) if eligible and actual_median is not None else None
            gap_percent = round(gap / value * 100, 2) if gap is not None and value else None
            interpretation = self._interpretation(benchmark_type, gap)
            if value is None:
                queue.append({"process_id": pid, "reason": "no_reliable_cited_value"})
            elif directional_only:
                queue.append({"process_id": pid, "reason": "proxy_directional_only"})
            elif comparability < self.config["minimum_comparability"]:
                queue.append({"process_id": pid, "reason": "insufficient_comparability"})

            results.append({
                "process_id": pid, "process_name": process.get("process_name", ""),
                "l1_domain": process.get("l1_domain", ""), "sample_count": len(valid_samples),
                "actual_median": actual_median, "actual_average": actual_average, "unit": process.get("unit"),
                "waiting_time": process.get("waiting_time"), "rework_rate": process.get("rework_rate"),
                "benchmark_value": value, "benchmark_type": benchmark_type, "reliability_class": reliability,
                "match_type": match_type, "comparability_score": comparability, "confidence_score": confidence,
                "comparison_eligible": eligible, "directional_only": directional_only,
                "gap": gap, "gap_percent": gap_percent, "interpretation": interpretation,
                "recommended_target": value if eligible else None, "target_status": "DRAFT_FOR_OWNER_VALIDATION" if eligible else "NOT_PROPOSED",
                "source_id": source_id, "source_url": benchmark.get("source_url"),
            })

        eligible_results = [x for x in results if x["comparison_eligible"]]
        above = [x for x in eligible_results if x["gap"] is not None and x["gap"] > 0]
        payload = {"case": asdict(case), "results": results, "source_qa": source_qa, "methodology_qa": method_qa}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        status = "VALIDATED_SYNTHETIC_ANALYSIS" if not source_qa and not method_qa else "QA_EXCEPTIONS_FOUND"
        return CycleTimeBenchmarkResult(
            case.assessment_id, status,
            {"process_count": len(case.processes), "eligible_comparisons": len(eligible_results), "above_reference_count": len(above), "unbenchmarked_count": len(queue), "official_target_count": 0},
            results, source_qa, queue, method_qa,
            {"status": "DRAFT_FOR_PROCESS_PERFORMANCE_AUTHORITY", "human_approval_required": True, "autonomous_sla_or_staffing_decision_permitted": False, "required_approvals": self.config["required_approvals"]},
            digest,
            [
                "Synthetic-only technical deployment candidate; no production process-mining or operational data connection is represented.",
                "Benchmark references are diagnostic inputs, not mandatory SLAs, staffing norms or official standards.",
                "PEFA thresholds are retained as PFM performance thresholds and are not transaction-processing benchmarks unless the cited methodology explicitly says so.",
                "A recommended target remains a draft requiring owner validation against statutory deadlines, risk appetite, control requirements, complexity and service criticality.",
            ],
        )

    @staticmethod
    def _no_benchmark(process: dict[str, Any], median: float | None, average: float | None, count: int, reason: str) -> dict[str, Any]:
        return {"process_id": process.get("process_id", "UNKNOWN"), "process_name": process.get("process_name", ""), "l1_domain": process.get("l1_domain", ""), "sample_count": count, "actual_median": median, "actual_average": average, "unit": process.get("unit"), "benchmark_value": None, "comparison_eligible": False, "directional_only": False, "gap": None, "gap_percent": None, "interpretation": reason, "recommended_target": None, "target_status": "NOT_PROPOSED", "source_id": None, "source_url": None}

    @staticmethod
    def _interpretation(benchmark_type: str | None, gap: float | None) -> str:
        if gap is None: return "NO_NUMERIC_COMPARISON"
        if benchmark_type in {"statutory_deadline", "target_sla", "pfm_performance_threshold"}:
            return "WITHIN_THRESHOLD" if gap <= 0 else "ABOVE_THRESHOLD"
        return "AT_OR_FASTER_THAN_REFERENCE" if gap <= 0 else "SLOWER_THAN_REFERENCE"

    def check_action(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower().replace(" ", "_")
        protected = normalized in self.config["protected_actions"]
        return {"action": normalized, "permitted": not protected, "human_authority_required": protected, "reason": "Process-performance authority approval required" if protected else "Analytical support permitted with source citations and audit logging"}
