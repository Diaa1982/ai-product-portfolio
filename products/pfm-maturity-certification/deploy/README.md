# P18 deployment

Run `docker compose -f products/pfm-maturity-certification/deploy/docker-compose.yml up --build` from the repository root. The profile is synthetic-only, non-root and read-only with dropped capabilities. Production scheme governance, assessor identities, evidence repository, IAM, security, resilience and approvals remain separate gates.
