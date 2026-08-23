# Architecture

## Current deployment candidate

Browser → FastAPI `/p08/*` → deterministic `UseCaseAssessor` → versioned JSON scoring configuration.

The shared portfolio case engine remains available for evidence, stage and audit workflows. The P08 scorer is deliberately deterministic: no external model, prompt or client data is required for the baseline assessment.

## Trust boundaries

- Browser input is untrusted and validated by Pydantic and the scoring engine.
- Repository configuration is version-controlled but requires governance approval before production activation.
- The demo case store is file-based and synthetic-only.
- The CEO role check is application-level in the candidate; production must derive role claims from enterprise identity, not request text.

## Production target

Replace file persistence with an encrypted managed database; add SSO/OIDC, role mapping, immutable audit storage, secrets management, ingress TLS/WAF, centralized logs/metrics/traces, backup and recovery, and approved source connectors. Run separate development, test and production environments with controlled promotion.

## Failure behavior

Invalid scores return 400, unauthorized protected approval returns 403, incomplete intake returns a discovery result, and high risk returns an explicit CEO gate. The service must fail closed if identity, configuration, evidence storage or audit writing is unavailable.
