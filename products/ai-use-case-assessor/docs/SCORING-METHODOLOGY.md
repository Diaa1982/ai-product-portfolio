# Scoring Methodology

## Calculation

Each criterion is scored 0–5 and multiplied by its configured weight. Value and feasibility are separately weighted, then priority is calculated as `0.60 × value + 0.40 × feasibility`. The 60/40 split is a configurable baseline, not an immutable policy.

Value criteria cover strategic alignment, public/business value, service/operational impact and risk/control improvement. Feasibility covers data readiness, technical feasibility, process/organizational readiness and delivery sustainability. Risk covers decision impact, data/privacy, legal/compliance and model/operational risk.

## Portfolio classes

At the default 3.5 threshold: high value/high feasibility is Quick Win; high value/low feasibility is Strategic Bet; low value/high feasibility is Fill-In; low value/low feasibility is Question Mark.

## Decision rules

- Incomplete required information always returns to Discover.
- Risk ≥3.75 requires independent risk review and CEO decision.
- Complete, non-high-risk cases with priority ≥3.5 proceed to prioritization/business case.
- Lower-priority cases remain in the backlog for stronger evidence or redesign.

## Governance and calibration

Scores are advisory. Every score needs evidence and an owner. Before production, governance must approve the configuration version and complete inter-rater reliability, threshold sensitivity, edge-case and disparate-impact testing. Changes require versioning, review, rollback and renewed calibration.
