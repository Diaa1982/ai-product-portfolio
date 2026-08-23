# Deployment

The supplied container is a technical baseline: non-root user, read-only filesystem, dropped capabilities, no-new-privileges, health check and dedicated runtime volume. Validate locally with the synthetic fixture and full test suite.

Production requires separate build/test/stage/prod environments; signed/scanned artifacts; protected branches and approvals; managed identity/secrets; TLS; data stores; approved adapters; observability/SIEM; capacity and performance testing; backup/restore; continuity; rollback; regional/residency review; runbooks; support ownership; and formal release/go-live records. This repository does not provision production infrastructure.
