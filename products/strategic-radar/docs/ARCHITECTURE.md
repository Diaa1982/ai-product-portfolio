# Architecture

## Candidate

Browser/API → FastAPI → Strategic Radar engine → versioned source/materiality configuration. The deterministic evidence verifier precedes materiality and delivery routing and cannot be bypassed through the API.

## Target production architecture

Event-driven services orchestrate approved-source fetch, normalization/OCR, version comparison, classification, materiality, evidence verification, audience recommendation, human approval and delivery. Temporal-style durable orchestration, independent workers, immutable evidence/audit stores, RBAC, encrypted object/database storage, observability and network egress domain allowlisting are recommended. AWS, Azure or GCP may host the API-first design subject to organizational cloud policy.

## Failure rules

Unknown/inactive/unofficial sources, non-allowlisted domains, incomplete provenance or invalid hashes block output. Null materiality routes to analyst review. Identity, audit or evidence-storage failure must fail closed for delivery and approval.
