# Product Growth Agent — Go-Live Checklist

The reference package is **not production-authorized** until all applicable gates below are completed and evidenced.

## G1 — Business and growth governance
- [ ] Executive sponsor and product-growth owner assigned.
- [ ] North Star Metric approved.
- [ ] Metric tree and business definitions approved.
- [ ] Growth objectives, horizons, and constraints approved.
- [ ] Decision rights and approval thresholds approved.
- [ ] Product, Marketing, Sales, Data, Finance, and CRM responsibilities confirmed.

## G2 — Data and analytics
- [ ] GA4 event/conversion taxonomy validated.
- [ ] Mixpanel event and identity taxonomy validated.
- [ ] CRM and billing semantics validated.
- [ ] Warehouse/semantic-layer definitions approved.
- [ ] Historical data quality assessed.
- [ ] Timezone, attribution, identity, deduplication, and consent rules documented.
- [ ] Production access follows least privilege.

## G3 — Experimentation
- [ ] Experiment platform integrated.
- [ ] Randomization/exposure logging validated.
- [ ] Sample-ratio and guardrail monitoring available.
- [ ] Experiment registry and result ledger available.
- [ ] Stop/rollback procedures tested.
- [ ] Production experiment launch requires authorized approval.

## G4 — Security, privacy and legal
- [ ] Workload identity / SSO architecture approved.
- [ ] Secrets stored outside source control.
- [ ] PII minimization and masking controls implemented.
- [ ] Sensitive/protected-attribute targeting controls implemented.
- [ ] Consent and data-use basis validated.
- [ ] Data retention and deletion rules implemented.
- [ ] Security testing completed.
- [ ] Audit logging is tamper-evident and retained per policy.

## G5 — Model and agent assurance
- [ ] Prompt and policy versions controlled.
- [ ] Offline evaluation dataset approved.
- [ ] Growth-analysis accuracy benchmarked.
- [ ] Hallucination / unsupported-claim tests passed.
- [ ] Tool-routing and permission tests passed.
- [ ] Adversarial and prompt-injection tests completed.
- [ ] Human override available.
- [ ] Failure/degraded-mode behavior tested.

## G6 — Integration and operations
- [ ] GA4 adapter tested.
- [ ] Mixpanel adapter tested.
- [ ] Warehouse adapter tested.
- [ ] CRM adapter tested.
- [ ] Billing/revenue adapter tested.
- [ ] A2A handoffs tested end-to-end.
- [ ] Approval service tested.
- [ ] Monitoring, alerting, incident management, and runbooks available.
- [ ] Backup / continuity requirements addressed.

## G7 — Pilot and production authorization
- [ ] Shadow-mode results reviewed by domain experts.
- [ ] Pilot scope and success criteria approved.
- [ ] Pilot completed without unresolved critical findings.
- [ ] Residual risks accepted by accountable owners.
- [ ] Production write permissions explicitly authorized.
- [ ] Formal go-live decision recorded.

## Current reference-package status

The package provides architecture, schemas, policies, workflow, prompt, API skeleton, Docker configuration, and sample task. Environment-specific production connectors, enterprise identity, production data, approval integration, persistent memory/audit services, and formal authorization remain outside the reference baseline.
