# Product Growth Agent — Integration Guide

## 1. Integration principles

1. Read access precedes write access.
2. Use service identities, not personal credentials.
3. Enforce least privilege at the source system and API gateway.
4. Keep authoritative data in systems of record; the agent stores references and derived decision evidence.
5. Separate analytical tools from transactional execution tools.
6. Every consequential write must be auditable, idempotent where possible, and rollback-capable.

## 2. GA4

Recommended read capabilities:

- standard reporting;
- realtime reporting;
- metadata discovery;
- funnel reporting where supported;
- audience/configuration metadata where required.

Expected adapter contract examples:

- `ga4.run_report`
- `ga4.run_realtime_report`
- `ga4.run_funnel_report`
- `ga4.get_metadata`
- `ga4.list_audiences`
- `ga4.get_property_config`

Required setup inputs:

- GA4 property ID;
- workload/service identity;
- approved scopes;
- canonical event and conversion dictionary;
- timezone and attribution conventions.

## 3. Mixpanel

Recommended capabilities:

- Insights;
- Funnels;
- Retention;
- Cohorts;
- governed raw-event export where justified;
- profile analysis.

Expected adapter contract examples:

- `mixpanel.query_insights`
- `mixpanel.query_funnel`
- `mixpanel.query_retention`
- `mixpanel.list_cohorts`
- `mixpanel.export_events`
- `mixpanel.query_profiles`

Required setup inputs:

- project ID;
- service-account credentials;
- event taxonomy;
- identity/alias rules;
- data residency and privacy requirements.

## 4. Data warehouse / lakehouse

Expose governed analytical views rather than unrestricted raw databases. At minimum provide:

- user/account dimension;
- acquisition attribution;
- product event facts;
- subscription/order/revenue facts;
- campaign spend;
- CRM opportunity/lead facts;
- customer support / experience signals;
- experiment assignments and exposures.

The warehouse semantic layer should own canonical metric definitions wherever possible.

## 5. CRM, billing and finance

CRM integration enables lead quality, pipeline, account conversion, churn reasons, and expansion analysis. Billing/revenue integration enables paid conversion, ARPU/ARPA, refunds, GRR/NRR, LTV, CAC payback, and contribution economics.

Pricing, discount, billing, entitlement, and refund write actions remain approval-gated.

## 6. Experimentation and feature flags

The experiment platform should support:

- experiment registration;
- hypothesis and metric metadata;
- randomization and allocation;
- exposure logging;
- feature flags;
- guardrail monitoring;
- stop/rollback;
- result persistence.

The PGA may create experiment drafts autonomously. Production launch or stop is approval-controlled by default.

## 7. Marketing and campaign platforms

Use separate read and write credentials. Reads may include spend, impressions, clicks, conversions, attribution, and campaign metadata. Campaign creation can remain in draft state until approved. Budget, bid, targeting, and launch actions require explicit authority.

## 8. Agent-to-agent integration

Use `schemas/a2a_message.schema.json` as the base envelope. Every handoff should carry:

- objective;
- context;
- evidence references;
- requested action;
- constraints;
- expected output;
- priority;
- correlation ID.

The receiving agent should return evidence and execution receipts using the same correlation chain so that the PGA can maintain an end-to-end audit trail.
