# Operations Runbook

## Normal checks

Confirm `/health` is 200, expected configuration version is active, latency/error metrics are within approved thresholds, audit writes succeed, storage has capacity and no restricted data appears in logs.

## Incident priorities

- P1: unauthorized decision, evidence/audit loss, sensitive-data exposure or widespread outage—disable affected route, preserve evidence and activate security/incident command.
- P2: scoring/config error or material degradation—freeze approvals, revert config/image and notify product/control owners.
- P3: minor UI or single-case issue—log, triage and resolve through normal release control.

## Recovery

Fail closed for approval if identity or audit systems fail. Use the last approved image/config, verify hashes, restore the approved backup, run health and synthetic checks, reconcile queued decisions, and obtain service-owner authorization before reopening.

## Routine ownership

Product owner manages scope and backlog; platform owner operates service; data owner governs sources; security/privacy/control owners monitor compliance; CEO performs protected final decisions. Names, contacts, SLAs, RTO and RPO are target-organization fields still requiring approval.
