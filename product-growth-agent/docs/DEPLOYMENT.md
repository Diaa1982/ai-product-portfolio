# Product Growth Agent — Deployment Guide

## 1. Reference runtime

The package provides a FastAPI control-plane reference implementation and Docker configuration. It is a deployment candidate, not production authorization.

## 2. Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

Health endpoint: `GET /health`

Task endpoint: `POST /v1/tasks`

Agent-to-agent endpoint: `POST /v1/a2a/messages`

Experiment proposal endpoint: `POST /v1/experiments/propose`

## 3. Container deployment

```bash
docker build -t product-growth-agent .
docker run --env-file .env -p 8080:8080 product-growth-agent
```

## 4. Environment configuration

Copy `.env.example` to the environment-specific secret/configuration mechanism. Do not commit populated `.env` files.

Required production configuration includes:

- model provider and approved model;
- model secret/reference;
- GA4 property and service identity;
- Mixpanel project and service identity;
- warehouse connection;
- CRM integration;
- billing/revenue integration;
- experimentation platform;
- campaign platform;
- approval service;
- audit-log sink.

## 5. Deployment stages

### Stage 0 — Documentation and design
Approve scope, metrics, decision rights, privacy, and integration architecture.

### Stage 1 — Read-only analytical sandbox
Connect synthetic or approved non-production data. Validate calculations, prompts, tools, and outputs.

### Stage 2 — Shadow mode
Run against approved production reads without allowing production writes. Compare recommendations with human experts.

### Stage 3 — Controlled pilot
Enable a narrow set of approved draft/write actions with explicit approvals, rollback, monitoring, and named owners.

### Stage 4 — Production
Authorize only after security, privacy, model, data, operational, business, and control gates are evidenced and approved.

## 6. Observability

Capture at minimum:

- task/correlation ID;
- model and prompt version;
- tool calls and tool latency;
- source/evidence references;
- decisions and confidence;
- approval requests/responses;
- write receipts;
- experiment ID/version;
- errors and retries;
- model/token cost where applicable.

## 7. Rollback

Every write-enabled adapter must define a rollback or compensating action. If a tool has no safe rollback, the action should remain human-executed or use a stronger approval threshold.
