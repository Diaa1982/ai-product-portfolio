# Go-live evidence

## Technical candidate

- Config: `config/enterprise-architecture.v1.json`.
- Engine: `src/portfolio_api/p15_enterprise_architecture.py`.
- Tests: `tests/test_p15_enterprise_architecture.py` — 15 focused tests.
- Fixture: `synthetic/connected-enterprise-model.json`.
- Routes: `/p15`, `/p15/config`, `/p15/analyze`, `/p15/changes/classify`, `/p15/actions/check`.
- Container: `deploy/Dockerfile` and `deploy/docker-compose.yml`.

## GitHub Actions

Passed on implementation commit `a941afe1f1af4bad64c865858234b7f8d09a0fa8`: 232 tests; registry validation and compilation; P15 image build; health, UI, traceability/impact/ADR and protected-action smoke checks.\n\nCI evidence: https://github.com/Diaa1982/ai-product-portfolio/actions/runs/32616612607

Approved metamodel/conventions, production repository/data, adapters, IAM/security/privacy, migration proof, UAT, operations, residual risk and formal go-live remain outstanding.
