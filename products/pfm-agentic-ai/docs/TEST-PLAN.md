# Test Plan

Automated unit tests verify nine-agent configuration; core calculations; strict threshold boundaries; zero-plan specialized review; validation/evidence/transition blocking; high-risk approval interruption; protected-action denial; analysis-only behavior; audit payload preservation; and approval-role enforcement.

CI must run all portfolio tests, compile Python, validate registry/configuration, scan for obvious committed secrets, build the P01 container, start it, check health/config, submit a synthetic analysis, verify metrics, and confirm payment authorization is denied.

Before production add contract tests for every source system, RBAC/segregation tests, audit immutability, load/recovery/security/privacy tests, reconciliation to authoritative calculations, accessibility testing and independent control-owner UAT.
