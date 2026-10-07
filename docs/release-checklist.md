# Release checklist

Use this as a review aid, not proof that a system is secure or legally compliant.

## This learning repository

- [ ] Owner has selected a license and approved public visibility, if a public release is intended
- [ ] All 36 concept IDs, headings, local links, and generated README indexes validate
- [ ] Resource review dates reflect actual review, especially Ollama, Bedrock, MCP, and security sources
- [ ] Offline tests and synthetic evaluation fixtures pass
- [ ] Any claimed live tests include runtime, model, environment, date, and result
- [ ] No private information, credentials, unlicensed copied content, or false endorsements
- [ ] CI runs for the exact published commit have been inspected

## An application built from these concepts

- [ ] A real user task and acceptance rubric are defined; a simpler baseline has been compared
- [ ] Model/provider capabilities, license, approved data destinations, and retention are verified
- [ ] Request, output, tool, and domain constraints are enforced in code
- [ ] Retrieval is permission-aware and deletion/freshness are tested
- [ ] Prompt-injection cases and unauthorized-action attempts are in the evaluation set
- [ ] Side effects use trusted approvals where needed, durable operation IDs, and reconciliation
- [ ] Timeouts, run limits, retry budgets, quotas, and spend controls are configured
- [ ] Logs and traces minimize sensitive content and have access/retention controls
- [ ] Human escalation, cancellation, partial-result, and unknown-outcome experiences are designed
- [ ] Model, prompt, schema, index, SDK, and evaluation versions are recorded together
- [ ] Canary criteria, rollback procedure, operational owner, and retirement/migration plan are defined
