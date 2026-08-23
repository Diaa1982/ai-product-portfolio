# Deployment

```bash
cp products/ipsas-compliance-ai/deploy/.env.example products/ipsas-compliance-ai/deploy/.env
docker compose -f products/ipsas-compliance-ai/deploy/docker-compose.yml up --build -d
curl http://localhost:8080/health
```

Open `http://localhost:8080/p11`. This is a synthetic technical candidate.

Production requires approved environments and network; signed/scanned images; SSO/RBAC/SoD; secure file intake; owner-approved ledger/reconciliation/reporting and knowledge interfaces; persistent evidence/audit/approval stores; monitoring, backup/DR and rollback; expert accounting validation, security/privacy/legal assurance and controlled pilot approval.
