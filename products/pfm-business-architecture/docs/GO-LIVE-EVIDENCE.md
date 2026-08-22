# Go-live evidence

## Technical-candidate evidence

- Config: `config/pfm-architecture.v1.json`.
- Engine: `src/portfolio_api/p13_pfm_business_architecture.py`.
- Tests: `tests/test_p13_pfm_business_architecture.py` — 15 focused tests.
- Fixture: `synthetic/complete-pfm-architecture.json`.
- Routes: `/p13`, `/p13/config`, `/p13/analyze`, `/p13/actions/check`.
- Container: `deploy/Dockerfile` and `deploy/docker-compose.yml`.

## GitHub Actions

Passed on implementation commit `8c5230333cb5bebff9f11ac3f124e7268e0ef2c1`: 187 tests; registry validation and compilation; P13 image build; `/health`, `/p13`, analysis and protected-action smoke checks.\n\nCI evidence: https://github.com/Diaa1982/ai-product-portfolio/actions/runs/32586199017

All organizational, data, legal, security, integration, UAT, operations, resilience, residual-risk and formal go-live approvals remain outstanding.
