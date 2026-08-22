# Go-live evidence

## Technical candidate

- Config: `config/cycle-time.v1.json`.
- Engine: `src/portfolio_api/p17_cycle_time_benchmark.py`.
- Tests: `tests/test_p17_cycle_time_benchmark.py` — 15 focused tests.
- Fixture: `synthetic/validated-benchmark-assessment.json`.
- Routes: `/p17`, `/p17/config`, `/p17/analyze`, `/p17/actions/check`.
- Container: `deploy/Dockerfile` and `deploy/docker-compose.yml`.

## GitHub Actions

Passed on implementation commit `101d7c52a63f3b304242550a65b26fe2d1226225`: 202 tests; registry validation and compilation; P17 image build; health, UI, cited threshold analysis and protected-action smoke checks.\n\nCI evidence: https://github.com/Diaa1982/ai-product-portfolio/actions/runs/32590679622

Production sources/licenses, event data, integrations, IAM/security/privacy, UAT, operations, residual risk and formal approvals remain outstanding.
