# Architecture

The technical candidate has four layers: FastAPI/dashboard presentation; deterministic management engine; versioned policy/configuration; and JSON evidence/case records. The engine normalizes canonical entities, validates ownership/evidence/links, calculates domain indicators, combines visible weighted scores and emits a draft decision package plus SHA-256 audit digest.

Production adapters are outside this baseline. Approved adapters should authenticate with least privilege, map source identifiers to canonical IDs, preserve source timestamps/version/hash, reject schema errors to quarantine, publish idempotent events and never bypass human approval systems. API gateway, identity provider, secrets manager, immutable audit store, monitoring, SIEM, backup and disaster recovery belong in the target deployment architecture.
