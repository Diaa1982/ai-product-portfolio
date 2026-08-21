# Deployment Guide

## Candidate deployment

From repository root:

```bash
docker compose -f products/ai-use-case-assessor/deploy/docker-compose.yml up --build -d
curl --fail http://localhost:8080/health
```

Open `/p08` for the interface and `/docs` for OpenAPI. Stop with the same compose command plus `down`.

## Configuration

The default scoring file is `config/scoring.v1.json`. Environment variables can override `P08_CONFIG_PATH`, `CASE_STORE_PATH`, `PRODUCT_REGISTRY_PATH`, `WORKFLOW_PATH`, `DASHBOARD_PATH` and `P08_DASHBOARD_PATH`. Configuration changes require a new semantic version and approval evidence.

## Production promotion

Build an immutable image from a reviewed commit; generate SBOM and vulnerability evidence; sign the image; deploy to test; run functional, security, performance and recovery tests; obtain UAT and control approvals; promote the same digest to production; smoke-test health/UI/API; monitor; record the release.

## Rollback

Keep the previous image digest and compatible configuration. On critical failure, stop traffic, preserve evidence/logs, restore the prior digest and config, verify health and a synthetic assessment, notify owners, and open an incident/postmortem. Database migrations must provide tested backward recovery before deployment.
