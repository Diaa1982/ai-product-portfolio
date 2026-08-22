# Deployment

```bash
cp products/pfm-brain/deploy/.env.example products/pfm-brain/deploy/.env
docker compose -f products/pfm-brain/deploy/docker-compose.yml up --build -d
curl http://localhost:8080/health
```

Open `http://localhost:8080/p02`. This deployment is a synthetic technical candidate.

Before production, approve hosting and environment segregation; pin/sign/scan images and dependencies; implement TLS, SSO/RBAC/SoD, secrets, persistent canonical/evidence/audit stores, owner-approved system adapters, monitoring, backups, disaster recovery and rollback; complete security/privacy/legal/PFM/accounting/control assurance and limited pilot approval.
