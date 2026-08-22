# Security and privacy

The container runs non-root with a read-only filesystem and dropped capabilities. Production requires SSO/MFA, role/attribute access, segregation of duties, encryption, managed secrets/keys, residency, DLP, tamper-evident audit, SBOM/dependency scanning, threat modeling, vulnerability tests and incident response.

Viewer, architect, capability-owner, evidence-steward, reviewer and approver duties must be separated. Application access alone never grants approval authority.
