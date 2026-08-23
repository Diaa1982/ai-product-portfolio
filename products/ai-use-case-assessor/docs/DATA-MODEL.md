# Data Model

## Assessment input

Identity and mode; business problem/outcome/owner; process trigger and closure; AI task; success criteria; prohibited automated decisions; low-confidence behavior; data sources; evidence references; value, feasibility and risk scores; assumptions.

Each data source includes `name`, `owner`, `classification` and `quality_status`. Allowed classifications are Public, Internal, Confidential and Restricted.

## Assessment result

Generated assessment ID and time; lifecycle stage; completeness and missing information; weighted value, feasibility, priority and risk scores; risk tier; portfolio class; recommendation; required gate and approver; copied evidence references and assumptions.

## Approval record

Approval ID, assessment ID, protected action, approver role, decision, reason and timestamp. Production storage must also capture authenticated subject ID, configuration version, content hash and audit-event linkage.

## Retention and lineage

The repository stores synthetic examples only. A production data owner must approve field-level collection, lawful purpose, retention/deletion schedule, residency, access, lineage and evidence integrity before real data is onboarded.
