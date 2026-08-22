# Data Model

## Input domains

- Context: case, FY2026 period, AED currency, division, cost centre and account.
- Lineage: source record, source system, evidence references and assumptions.
- Prerequisites: Organization Master, Chart of Accounts and Approved Budget loaded.
- Budget/execution: original, supplementary, transfer, plan, actual and commitments.
- Revenue/cash: target/actual; opening, inflow, outflow and minimum buffer.
- Performance/control: KPI direction/target/actual/tolerance; inherent risk and control effectiveness.
- Authority: requester/approver roles, action, proposed amount, maximum amount and human approval reference.
- Reconciliation: expected revised budget and expected closing cash.

## Output contract

Validation and reconciliation status; facts; deterministic calculations; classified risks; explicit assumptions; recommendations; evidence; confidence; authority and decision status; audit record with source, issues, configuration version, approval reference, timestamp and SHA-256 calculation digest.

Production normalization should separate these domains into versioned master, transaction, evidence, calculation, approval and audit entities with effective dates and immutable lineage.
