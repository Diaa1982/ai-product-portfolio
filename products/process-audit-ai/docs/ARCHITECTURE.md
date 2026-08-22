# Architecture

`Process Register → Audit Programme → Controlled Criteria → Evidence Plan → Fieldwork/Sampling → Deterministic Assessment → Auditor Findings → CAPA → Independent Verification → Process Update → Monitoring`

FastAPI hosts the bilingual studio and APIs. `ProcessAuditAI` loads a versioned master-data criterion library, applies deterministic scoring/evidence rules, performs structured comparisons and generates an audit digest. Production persistence must be transactional and append-only for evidence, AI recommendations, auditor overrides, findings, CAPA and approvals.

Target adapters include the enterprise process repository/ARIS or BIC, DMS, ERP, performance and risk systems, Microsoft 365 and Power BI. Integration is not implemented by this technical candidate.
