# Reference Architecture

## Logical layers

1. **Experience layer:** executive dashboard, analyst workspace, reviewer queue and API clients.
2. **Workflow layer:** product-specific orchestration, case states, approvals, segregation of duties and escalation.
3. **Intelligence layer:** retrieval, rules, classification, forecasting, anomaly detection and language-model services.
4. **Evidence layer:** approved source registry, document ingestion, metadata, provenance, citations and version control.
5. **PFM and enterprise data layer:** synthetic canonical models for planning, budget, execution, treasury, revenue, accounting, performance, risk, process, service and architecture.
6. **Control layer:** identity, authorization, privacy, security, model governance, audit logging, monitoring and retention.
7. **Integration layer:** API gateway, event interfaces and approved adapters to source systems.

## Mandatory design constraints

- Agents may recommend, analyse and draft; they do not approve budgets, post transactions, issue financial statements, close audit findings, or change official records without authorized human action.
- Every material conclusion must preserve source provenance and calculation lineage.
- High-impact, low-confidence, conflicting, or unsupported outputs must be escalated.
- Production environments must be separated from development and testing.
- Logs must not expose sensitive prompts, documents or credentials.
- Models and prompts require controlled versioning, evaluation and rollback.
