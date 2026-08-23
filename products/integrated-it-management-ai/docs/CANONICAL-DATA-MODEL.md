# Canonical Data Model

| Entity | Identifier | Mandatory governance fields |
|---|---|---|
| Service | `service_id` | owner, status, evidence |
| Work item | `work_item_id` | type, service, owner, status, evidence |
| Configuration item | `ci_id` | service, owner, status, dependencies, controls, evidence |
| Portfolio item | `portfolio_item_id` | sponsor/owner, status, strategy, benefits, risk, evidence |
| Risk/control | `record_id` | type, owner, status, score/effectiveness, evidence |
| Evidence | `evidence_id` | validity plus production provenance fields |
| Decision | action/reference | authority, decision, reason, timestamp, evidence |

Production mappings must also capture source system, source record ID, event time, ingestion time, version/hash, classification, retention class and reconciliation status. Master-data owners approve identity matching and mapping changes.
