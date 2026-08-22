# Product Requirements

## Outcome

Improve financial-data integrity and reporting-package quality by providing traceable, repeatable exception analysis to public-sector accounting and assurance teams without replacing professional judgement.

## MVP requirements

1. Support journal quality, reconciliation and disclosure checklist reviews.
2. Require entity, period, source, evidence, approved policy reference and cited requirement reference.
3. Identify missing, contradictory, cut-off, approval, SoD, balance, aging, disclosure and comparative-information issues.
4. Return `INSUFFICIENT_INFORMATION` below configured confidence or without authoritative evidence/references.
5. Require accounting-manager or equivalent review for material/reporting-impact exceptions.
6. Never issue a formal compliance conclusion or execute accounting/financial/audit actions.
7. Preserve facts, calculations, exceptions, assumptions, recommendations, evidence, configuration version and audit digest.
8. Provide API, workbench, synthetic scenarios, tests and container deployment.

## Acceptance targets

Process 100% of supported synthetic samples; all automated control tests pass; production evaluation design must target at least 90% key-field/test-set agreement against expert ground truth before pilot approval. Autonomous final approval remains out of scope.
