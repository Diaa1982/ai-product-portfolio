# P08 Container Package

Run from the repository root with `docker compose -f products/ai-use-case-assessor/deploy/docker-compose.yml up --build`. The image uses an unprivileged user; Compose drops Linux capabilities, prevents privilege escalation and makes the root filesystem read-only except for the named runtime volume.

This is a technical deployment candidate, not evidence of production approval. Follow [the deployment guide](../docs/DEPLOYMENT.md) and complete [the go-live checklist](../GO-LIVE-CHECKLIST.md).
