# Deployment Guide

Prerequisites: business owner, KPI dictionary, source-system inventory, process ownership, data-access model, approval matrix, target environment and secret management.

Steps:
1. Copy `.env.example` to `.env`.
2. Configure secrets outside source control.
3. Confirm KPI definitions in `config/kpis.yaml`.
4. Configure source adapters.
5. Validate data-quality rules.
6. Configure approval routes.
7. Build: `docker build -t service-excellence-agent .`
8. Run: `docker run --env-file .env -p 8080:8080 service-excellence-agent`
9. Test `/health`, KPI review and issue-analysis endpoints.
10. Perform business UAT, security/privacy review and formal go-live approval.

Production hardening includes SSO, least privilege, secrets manager, API gateway, observability, persistent audit/action registers, certified KPI semantic layer, data-quality monitoring, approvals and rollback procedures.
