# Security and Privacy

Implemented baseline: typed validation, official/approved/active source checks, domain allowlisting, required provenance/hash, deterministic routing, protected human approval boundary, no external model call, synthetic-only data, unprivileged container and no embedded secrets.

Production requires SSO/OIDC and server-side RBAC; source-admin/analyst/approver segregation; TLS and encryption; secrets manager; WAF/rate limits; outbound proxy/egress allowlist; immutable evidence/audit stores; malware/content scanning; SSRF protection; secure OCR; dependency/container/SBOM/signing; privacy and legal review; monitoring and incident response.

Threats include malicious or compromised sources, redirect/domain takeover, prompt/content injection, evidence substitution, stale versions, role spoofing, fabricated citations and sensitive information leakage. Evidence verification and delivery must fail closed.
