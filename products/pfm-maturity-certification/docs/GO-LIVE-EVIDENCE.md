# Go-live evidence

## Technical candidate

- Config: `config/maturity.v1.json`.
- Engine: `src/portfolio_api/p18_maturity_certification.py`.
- Tests: `tests/test_p18_maturity_certification.py` — 15 focused tests.
- Fixture: `synthetic/moderation-ready-assessment.json`.
- Routes: `/p18`, `/p18/config`, `/p18/assess`, `/p18/actions/check`.
- Container: `deploy/Dockerfile` and `deploy/docker-compose.yml`.

## GitHub Actions

Passed on implementation commit `99114ba82c74be76f5814cfbfe5aa4840fe808ae`: 217 tests; registry validation and compilation; P18 image build; health, UI, evidenced-maturity/moderation and certificate-denial smoke checks.\n\nCI evidence: https://github.com/Diaa1982/ai-product-portfolio/actions/runs/32616063656

Adopted scheme, legal authority, competent assessors, evidence repository, calibration, IAM/security/privacy, UAT, operations, residual risk and formal production approval remain outstanding.
