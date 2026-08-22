# Security and Privacy

The repository uses synthetic data and contains no approved connection to live financial systems. The container runs non-root with a read-only filesystem, dropped capabilities and tmpfs runtime storage.

Production minimum controls include federated identity and MFA; least privilege and SoD; effective-dated authority mapping; encryption; managed secrets; network segmentation; field-level classification/minimization; privacy/legal assessment; immutable audit and evidence logs; dependency/image/SAST/DAST scanning; penetration testing; monitoring; backup/restore; incident response; and safe shutdown.

If governed retrieval or generative models are added, use only approved corpora, citation enforcement, prompt/tool allow-lists, injection/data-exfiltration defenses, versioned prompts/models, quality/safety evaluations, human review and rollback. Do not submit credentials, bank/payment data, taxpayer details, personal data or confidential fiscal records to this MVP.
