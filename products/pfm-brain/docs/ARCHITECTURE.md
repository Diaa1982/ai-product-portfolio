# Architecture

## Logical layers

1. **Source and evidence:** owner-approved organization, COA, budget, execution, revenue, cash, KPI, risk/control and authority sources.
2. **Canonical PFM data:** versioned identifiers, periods, units, currency, lineage and validation state.
3. **Deterministic control engine:** approved formulas, reconciliation, exceptions, materiality and authority/SoD checks.
4. **Governed knowledge and reasoning:** future retrieval over approved policies/definitions with citations, confidence and evaluation controls.
5. **Workflow and human gates:** review queues, escalation, approval references and protected-action boundaries.
6. **Experience:** API, fiscal workbench, dashboards and approved reports.
7. **Assurance and operations:** tamper-evident audit, monitoring, versioning, incident response, rollback and safe shutdown.

The MVP implements layers 2–3, a basic layer 5 contract and layer 6 interface over synthetic data. Production APIs/adapters, enterprise identity, persistent stores and governed retrieval are not implemented.

## Routing principle

Requirements determine the analytical domain and owner. Parallel analysis may occur only over validated, period-consistent records. Missing, ambiguous or conflicting information routes to remediation; high-risk and protected actions interrupt for a human decision. A reported insight must trace to source record, evidence, formula, configuration version and approval state.
