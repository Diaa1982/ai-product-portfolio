# Data Model

## PFM case input

Identity/workflow: `case_id`, `workflow_type`, `current_agent`, `next_agent`, `business_outcome`, `due_date`. Handoff: `payload`, `success_criteria`, `evidence_references`, `assumptions`, `validation_passed`, `high_risk`, `human_approval_reference`. Financial measures: `approved_budget`, `revised_budget`, `period_plan`, `actuals`, `commitments`, `cash_available`, `obligations_due`.

## Analysis output

Identity/state: `analysis_id`, agents, validation and handoff status. Measures: available balance, utilization, commitment pressure, variance and liquidity gap. Governance: alerts, risk, issues, interruption, escalation/failure route, recommendation, evidence and assumptions. Audit event: exact payload, calculated output, success criteria, approval context and UTC timestamp.

## Production data rules

Define authoritative source, owner, accounting/budget basis, currency/unit, entity/fund/program/chart dimensions, period, cut-off, version, lineage, quality status and retention. References should resolve to access-controlled immutable evidence. Do not place secrets or unnecessary personal data in payloads or logs.
