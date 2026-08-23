# Test Plan

Automated tests cover weight integrity, verified change priority routing, unknown-source block, exact-citation block, prohibited manual creation, no-change suppression, conflict review, high-impact approval and role enforcement.

Production assurance adds connector/RSS/API/PDF/OCR contracts; version-diff accuracy; citation coverage; precision/recall and missed-change corpus; conflict/corroboration accuracy; authorization; content injection/SSRF; performance/capacity; accessibility; backup/restore; failover/rollback; container/security scans; and business/PFM UAT.

Run `python -m unittest discover -s tests -v` and `python -m compileall -q src tests`.
