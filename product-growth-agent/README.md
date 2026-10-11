# Product Growth Agent — Deployment Pack

## Purpose
The Product Growth Agent (PGA) is an enterprise growth decision and orchestration agent focused on sustainable customer acquisition, activation, retention, monetization, and revenue optimization.

It is designed to operate as part of a multi-agent environment and collaborate with Product, Marketing, Sales, Data, Finance, CRM, and Experimentation agents/tools.

## Operating objective
Maximize sustainable, measurable growth subject to:
1. customer experience guardrails,
2. unit-economics guardrails,
3. privacy and consent controls,
4. experiment integrity,
5. approval thresholds,
6. product and brand constraints.

The agent must not optimize a single metric in isolation when doing so may damage retention, contribution margin, customer trust, or long-term enterprise value.

## Core growth loop
OBSERVE → DIAGNOSE → PRIORITIZE → DESIGN → APPROVE → EXECUTE → MEASURE → LEARN → SCALE / STOP

## Primary capabilities
- Growth strategy and growth-model decomposition
- Market / segment / behavior analysis
- Acquisition funnel analysis and channel optimization
- Activation and onboarding optimization
- Cohort and retention analysis
- Churn / risk segmentation
- Monetization, ARPU/ARPA, expansion and revenue optimization
- CAC, LTV/CLV, payback and unit economics
- Experiment hypothesis generation
- A/B test design and experiment governance
- Campaign and landing-page optimization
- Growth anomaly detection
- Growth forecasting and scenario analysis
- Cross-agent orchestration
- Executive growth reporting

## Default metric framework
North-star metric + metric tree:
- Acquisition: traffic, reach, qualified users/leads, CAC/CPA/CPL
- Activation: signup-to-activation, time-to-value, onboarding completion
- Engagement: DAU/WAU/MAU, frequency, depth, feature adoption
- Retention: D1/D7/D30, cohort retention, churn, reactivation
- Monetization: conversion-to-paid, ARPU/ARPA, AOV, expansion, NRR/GRR
- Referral: invites, referral conversion, viral coefficient where relevant
- Efficiency: LTV:CAC, CAC payback, contribution margin, ROAS/ROMI
- Experience guardrails: complaints, unsubscribes, refunds, latency, NPS/CSAT where available

## Decision policy
The agent may:
- read analytics and business data;
- produce analyses, diagnoses and recommendations;
- propose experiments;
- calculate sample-size inputs and evaluation plans;
- request work from other agents;
- create drafts for campaigns, growth briefs and product changes.

The agent requires approval before:
- changing production pricing, packaging, discounts, entitlements or billing;
- launching or stopping paid campaigns;
- changing campaign budgets or bid strategies;
- sending external customer communications;
- enabling experiments in production;
- changing targeting rules using sensitive or protected attributes;
- making irreversible product, CRM or revenue-system changes.

Approval thresholds are configurable in `policies/guardrails.yaml`.

## Multi-agent collaboration
The agent communicates through the envelope in `schemas/a2a_message.schema.json`.

Standard collaborators:
- Product Agent: roadmap, onboarding, activation, UX changes, feature experiments
- Marketing Agent: media, campaign creative, lifecycle campaigns, SEO/content
- Sales Agent: pipeline, conversion, lead quality, objections, enterprise expansion
- Data Agent: metric definitions, datasets, causal analysis, forecasting, data quality
- Finance Agent: unit economics, contribution margin, pricing economics, budget limits
- CRM / Lifecycle Agent: segmentation, journeys, reactivation, communication execution

## Analytics integrations
### Google Analytics 4
Use a read-only integration by default. The agent expects access to GA4 reporting through the Google Analytics Data API and configuration metadata through the Admin API.

Recommended adapter methods:
- `ga4.run_report`
- `ga4.run_realtime_report`
- `ga4.run_funnel_report` (treat as preview capability if used)
- `ga4.get_metadata`
- `ga4.list_audiences`
- `ga4.get_property_config`

### Mixpanel
Use service-account credentials for server-to-server access where supported.

Recommended adapter methods:
- `mixpanel.query_insights`
- `mixpanel.query_funnel`
- `mixpanel.query_retention`
- `mixpanel.list_cohorts`
- `mixpanel.export_events`
- `mixpanel.query_profiles`

## Deployment
1. Copy `.env.example` to `.env`.
2. Configure secrets in a secret manager; never commit them.
3. Configure tool adapter URLs or SDK implementations.
4. Validate `config/metrics.yaml` against your product's actual event taxonomy.
5. Validate guardrails and approval roles.
6. Build: `docker build -t product-growth-agent .`
7. Run: `docker run --env-file .env -p 8080:8080 product-growth-agent`
8. Health check: `GET /health`
9. Submit a growth task: `POST /v1/tasks`
10. Send inter-agent messages: `POST /v1/a2a/messages`

## Production hardening checklist
- SSO / workload identity
- secrets manager
- read/write scopes separated
- API gateway and rate limits
- immutable audit log
- PII redaction/tokenization
- approval workflow integration
- metric catalog / semantic layer
- experiment registry integration
- feature flag integration
- data-quality checks
- alerting and observability
- prompt/version registry
- offline and online evaluations
- incident / rollback procedure

## Reference implementation status
This pack contains the deployable control plane and contracts. Environment-specific connectors (GA4, Mixpanel, CRM, ad platforms, billing, warehouse, feature flags) must be configured with your credentials and endpoint/SDK implementations before production write actions are enabled.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Operating Model](docs/OPERATING-MODEL.md)
- [Integration Guide](docs/INTEGRATIONS.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Go-Live Checklist](docs/GO-LIVE-CHECKLIST.md)

## Reference-package status
This repository package is a governed deployment candidate and reference implementation. It is **not production-authorized**. Production use requires organization-specific data and metric validation, IAM and least-privilege access, security/privacy review, approved integrations, persistent audit and memory services, business UAT, pilot evidence, residual-risk acceptance, and formal go-live approval.
