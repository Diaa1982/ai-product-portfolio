# Security and Privacy

## MVP posture

The repository contains synthetic examples only, runs as a non-root container user and keeps controls/configuration in version control. It is not hardened for live PFM data.

## Production minimum

- Federated identity, MFA and least-privilege role mapping to validated delegations.
- Segregation of preparer, reviewer, approver, administrator and auditor capabilities.
- Encryption in transit/at rest, managed secrets, network restrictions and dependency/image scanning.
- Field minimization, classification, privacy/legal basis, residency, retention and deletion controls.
- Immutable or tamper-evident case, evidence, configuration, approval and access logs.
- Prompt/input defense and strict tool allow-lists if probabilistic models are added.
- Independent threat model, privacy impact assessment, penetration test and incident exercise.

Never send credentials, payment instructions, bank details, taxpayer records or personal data to the demo endpoint.
