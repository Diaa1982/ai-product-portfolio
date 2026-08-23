# Operations Runbook

## Health and monitoring

Check `/health`, endpoint latency/error rate, blocked/ready handoffs, high-risk interruptions, missing evidence, invalid transitions, configuration version, approval failures and audit persistence. Alert on any attempted protected action and repeated validation bypass attempt.

## Incident response

1. Pause affected workflow/integration; preserve logs and evidence.
2. Notify product, PFM process, security/privacy and relevant financial/control owners.
3. Prevent downstream execution; revert to the approved manual process.
4. Classify impact, investigate source/config/code/model changes, and document decisions.
5. Remediate, independently verify, obtain change approval and restore gradually.

## Rollback

Redeploy the last approved image/config pair, verify protected-action checks and synthetic smoke tests, then re-enable traffic. Never replay financial actions from application logs; reconcile with authoritative systems and responsible officials.
