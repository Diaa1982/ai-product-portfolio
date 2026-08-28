# Enterprise Agentic AI Platform — Go-Live Checklist

This repository package is a technical reference implementation. It is not production-authorized and must use synthetic or explicitly approved data until every applicable gate below is complete.

## 1. Accountable ownership

- [ ] Executive sponsor, product owner, risk owner, data owner, security owner, and service owner are named.
- [ ] Decision rights distinguish advisory output, human approval, and authorized execution.
- [ ] Business scope, intended users, prohibited uses, and success measures are approved.

## 2. Data, RAG, and multimodal evidence

- [ ] Approved source register, retention rules, classification, and access permissions are documented.
- [ ] Retrieval permissions are enforced before indexing and again at query time.
- [ ] Ground-truth evaluation covers retrieval relevance, citations, freshness, and access isolation.
- [ ] Image/document processing has privacy, consent, malware, OCR, and content-safety controls.
- [ ] Production data is excluded until its onboarding and privacy assessment are approved.

## 3. Models and agents

- [ ] Model/provider, region, data-processing terms, and fallback behavior are approved.
- [ ] Agent roles, prompts, tools, memory boundaries, stop conditions, and escalation paths are versioned.
- [ ] LangGraph and CrewAI paths pass representative end-to-end tests.
- [ ] Hallucination, prompt-injection, data-leakage, tool-misuse, and unsafe-action evaluations meet approved thresholds.
- [ ] Multi-agent conflicts and incomplete evidence route to a human rather than silent resolution.

## 4. MCP and tool execution

- [ ] MCP servers and clients use authenticated, encrypted, allow-listed connections.
- [ ] Tool schemas, scopes, timeouts, retries, idempotency, and compensating actions are approved.
- [ ] Read-only and write-capable tools are separated; least privilege is enforced.
- [ ] Consequential actions require explicit authorization and human approval.
- [ ] Tool outputs and execution receipts are retained in the audit trail.

## 5. Security and operations

- [ ] Enterprise SSO, RBAC/ABAC, segregation of duties, secrets management, and environment isolation are implemented.
- [ ] Threat modeling, dependency scanning, penetration testing, and incident response are complete.
- [ ] Persistent state, audit storage, observability, alerting, backup, recovery, and safe shutdown are tested.
- [ ] Performance, concurrency, resilience, cost, and capacity targets are validated.
- [ ] Runbooks, support ownership, change control, rollback, and model/tool versioning are operational.

## 6. Assurance and release

- [ ] Business, accessibility, security, privacy, legal, compliance, and operational UAT are approved.
- [ ] Evaluation evidence and residual risks receive independent review.
- [ ] A limited pilot is completed with monitored users and reversible actions.
- [ ] Production authorization is recorded by the accountable decision makers.
- [ ] Post-launch monitoring, periodic review, and decommissioning criteria are scheduled.

## Current status

Technical starter kit only. Synthetic/reference content is included; no live enterprise integration or autonomous consequential action is authorized.
