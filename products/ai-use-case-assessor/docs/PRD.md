# Product Requirements Document

## Outcome

Help leaders discover, evaluate and prioritize AI opportunities based on verified business need—not solution enthusiasm—while preserving accountable human decisions.

## Users

- Business sponsor: states the problem, target outcome and success criteria.
- Assessor/advisory team: performs discovery, challenges assumptions and scores evidence.
- Data and control owners: validate sources, classifications, feasibility and risk.
- CEO: approves protected final actions and unresolved escalations.

## Supported journeys

1. Client-led: assess a use case already proposed by a sponsor.
2. Diagnostic-led: study goals, operating model, processes, pain points and cost drivers to discover opportunities.
3. Hybrid: combine a proposed use case with diagnostic challenge and alternatives.

## Functional requirements

- Capture business problem, outcome, trigger-to-closure process, users/owners, AI task, success criteria, prohibited decisions, low-confidence behavior, data dependencies and evidence.
- Score configurable value, feasibility and risk criteria on a 0–5 scale.
- Calculate traceable weighted results and portfolio classification.
- Route incomplete cases back to discovery and high-risk cases to independent review and CEO decision.
- Record versioned configuration and immutable decision evidence in the production implementation.
- Expose an API and usable web interface.

## Out of scope for v1

- Autonomous funding, procurement, risk acceptance or deployment decisions.
- Production connectors, enterprise SSO and organization-specific policy interpretation.
- Storage of personal, confidential or restricted data in the repository demo.

## Acceptance criteria

- All configured weights total 1.0 and scores outside 0–5 are rejected.
- All four portfolio classes are reproducible.
- Missing evidence results in `insufficient_information`.
- High risk never routes directly to development or deployment.
- A non-CEO role cannot approve protected final actions.
- Container starts, `/health` returns 200 and `/p08` is usable.
