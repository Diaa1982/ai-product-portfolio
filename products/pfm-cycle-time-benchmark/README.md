# PFM Cycle-Time Benchmark

**Product ID:** P17 · **Stage:** Technical deployment candidate · **Data:** Synthetic only · **Production ready:** No

P17 compares PFM and shared-service process cycle times only when the source, boundary, unit, scope and match are traceable. It distinguishes observed averages/medians, target SLAs, statutory deadlines, PFM performance thresholds, best-practice references and expert estimates.

## Executable scope

- A–D reliability, exact/nearest/proxy/no-data match and source-license metadata.
- Median/average, gap, threshold interpretation, comparability and confidence calculation.
- Citation enforcement: missing/unknown sources suppress benchmark values.
- Sequential-sum, critical-path and volume-weighted aggregation controls.
- Unbenchmarked queue, source QA, methodology QA and draft target package.
- API/UI, synthetic fixture, 15 focused tests and hardened container.

Run `python -m unittest tests.test_p17_cycle_time_benchmark -v`, start the API and open `/p17`.

Benchmarks are diagnostic references. Practitioner ranges are not official tables; PEFA thresholds are not transaction benchmarks unless explicitly defined as such. Owners validate targets against law, controls, risk, complexity and criticality.

See the [checklist](GO-LIVE-CHECKLIST.md), [methodology](docs/BENCHMARK-METHODOLOGY.md), [comparability rules](docs/COMPARABILITY-STANDARD.md), [source standard](docs/SOURCE-AND-LICENSING-STANDARD.md), [scoring](docs/SCORING-METHODOLOGY.md), [API](docs/API.md) and [evidence](docs/GO-LIVE-EVIDENCE.md).
