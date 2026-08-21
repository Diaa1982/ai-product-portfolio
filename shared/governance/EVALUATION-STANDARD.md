# AI Evaluation Standard

Every product must define measurable acceptance thresholds before pilot or production.

## Evaluation dimensions

- Factual and calculation accuracy.
- Evidence citation coverage and source validity.
- Completeness against required fields and controls.
- Hallucination and unsupported-claim rate.
- Classification precision, recall and calibration.
- Bias, fairness and accessibility where applicable.
- Prompt-injection and data-exfiltration resistance.
- Privacy and sensitive-data leakage.
- Human-review effectiveness and escalation accuracy.
- Latency, availability, cost and operational resilience.

## Test-set controls

- Use synthetic or explicitly approved data.
- Separate development, validation and holdout cases.
- Include normal, edge, conflicting, incomplete and adversarial cases.
- Version datasets, prompts, models, rules and expected outputs.
- Require expert approval for financial, IPSAS, audit, risk and legal evaluation cases.

## Release decision

A passing aggregate score cannot override a failed critical control. Security, privacy, unsupported consequential advice, missing provenance or approval-bypass failures block release.
