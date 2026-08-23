# Process Audit AI

**Product ID:** P06  
**Product:** Enterprise Process Audit & Assurance Management System  
**Maturity:** Technical deployment candidate; not production or certification ready

P06 assesses whether enterprise processes are current, approved, executed as documented, controlled, measured and continually improved. It operates across `Plan → Audit → Evidence → Assess → Find → Correct → Verify → Update → Monitor → Improve` using four assurance lenses: conformance, control, effectiveness and improvement.

## Implemented

- Bilingual English/Arabic criterion library covering 15 domains A–O and ISO 9001/DGEP alignment metadata.
- Deterministic 0–5 weighted scoring; unanswered, N/A and insufficiently evidenced criteria are excluded.
- Documented-versus-actual comparison and transaction-sample conformance testing.
- Evidence triangulation, auditor/owner segregation, draft finding severity and CAPA effectiveness controls.
- Division dashboard aggregation and filters.
- Human-only final ratings, findings, formal opinions, CAPA closure, publication and certification/compliance declarations.
- `/p06` bilingual studio, API, 15 focused tests, synthetic fixture and hardened container.

P06 supports evidence-based management assurance. It does not certify ISO 9001, declare DGEP compliance or issue a formal audit opinion.

Run `uvicorn src.portfolio_api.main:app --host 0.0.0.0 --port 8080`, then open `/p06`.
