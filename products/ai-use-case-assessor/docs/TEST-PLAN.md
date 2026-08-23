# Test Plan

## Automated baseline

Unit tests validate weight totals, weighted calculation, four portfolio classes, incomplete intake, valid data classification, high-risk routing and CEO-only protected approval. Existing portfolio tests cover shared case workflow, evidence, audit chain and API smoke behavior.

Run from repository root:

```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

## Required before formal go-live

- API contract, negative, boundary and concurrency tests.
- Inter-rater reliability and scoring sensitivity on an approved representative corpus.
- Authorization, role-spoofing, configuration/evidence tampering and penetration tests.
- Dependency/container scan and signed-image verification.
- Performance/load/capacity tests against approved SLOs.
- Backup/restore, failover and rollback exercises.
- Accessibility and supported-browser tests.
- Business UAT and independent assurance for high-impact use.

Results, defects, exceptions and approvers must be linked in [GO-LIVE-EVIDENCE.md](GO-LIVE-EVIDENCE.md).
