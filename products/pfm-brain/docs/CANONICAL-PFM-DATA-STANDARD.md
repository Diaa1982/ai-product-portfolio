# Canonical PFM Data Standard

## Dataset baseline

Version 1.0; FY2026; AED; synthetic; eight divisions; 60 accounts; 1,500 transactions; 20 acceptance cases; no personal or confidential data; not for statutory reporting.

## Required load sequence

1. Organization Master
2. Chart of Accounts
3. Approved Budget
4. Budget Execution
5. Revenue
6. Cash
7. KPI
8. Risk and Control
9. Authority Matrix

## Minimum record controls

Every analytical record requires a unique source record ID, source system, fiscal period, currency/unit, division, cost centre, account, evidence reference, load/version timestamp, data owner, quality status and lineage to transformations. Master identifiers must exist before transactions are accepted. Approved budget precedes execution. Status values must be from controlled lists.

## Production extensions

Define entity/fund/program/project/activity/economic classifications, budget version, accounting basis, consolidation, cut-off, commitment stage, revenue type, bank/cash account, KPI formula, risk/control ownership, delegation validity dates, classification, retention and privacy/security handling. Local owners must approve mappings; no identifier or rule may be inferred.
