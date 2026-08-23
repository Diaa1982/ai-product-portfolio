# Data Model

Source records contain ID, name, official/approved/active status, environment, allowed domains and owner. Signal input contains title, audience, industry, jurisdiction, PFM category, signal, separated conclusion layers, provenance fields, version-change summary, six materiality criteria, confidence and protected-output flags.

Results contain signal ID/time, evidence status, weighted materiality/route, confidence, output status, approval reasons/role, separated conclusion layers, advisory disclaimer and immutable source reference.

Production extends this with raw evidence object ID/hash, normalized/OCR artifact, prior/current version relationship, citations/spans, authenticated actor, model/prompt/rule versions, approval event and delivery receipt. Retention and deletion must be approved by source/data owners.
