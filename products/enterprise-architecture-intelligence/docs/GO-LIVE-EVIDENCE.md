# Go-live evidence

## Technical candidate

- Config: `config/enterprise-architecture.v1.json`.
- Engine: `src/portfolio_api/p15_enterprise_architecture.py`.
- Tests: `tests/test_p15_enterprise_architecture.py` — 15 focused tests.
- Fixture: `synthetic/connected-enterprise-model.json`.
- Routes: `/p15`, `/p15/config`, `/p15/analyze`, `/p15/changes/classify`, `/p15/actions/check`.
- Container: `deploy/Dockerfile` and `deploy/docker-compose.yml`.

## GitHub Actions

Pending final branch run. Record commit, workflow URL, test count, image build and smoke result here.

Approved metamodel/conventions, production repository/data, adapters, IAM/security/privacy, migration proof, UAT, operations, residual risk and formal go-live remain outstanding.
