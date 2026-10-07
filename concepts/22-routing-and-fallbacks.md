# 22. Routing and fallbacks

Routing selects a path before execution. A fallback selects an acceptable alternative after a problem. A retry repeats an attempt. Keeping these separate prevents a reliability feature from quietly changing your product's behavior.

## Why it matters

A small model may handle routine classification while a stronger model handles ambiguous cases. During an outage, a cached answer or explicit “try later” response may be safer than switching providers. The right choice depends on quality requirements, deadlines, data permissions, and the consequence of an incorrect answer.

## Build it

1. Define route eligibility in code: input types, tools, region, data-handling constraints, and cost. Classify only among eligible routes.
2. Evaluate routing with labeled tasks, including ambiguous requests. Keep an abstain or escalation path instead of forcing every input into a category.
3. Classify failures. Retry transient transport failures within a bounded budget; fix invalid inputs rather than replaying them. Treat authorization denials as a stop condition.
4. Use a request-level deadline, exponential backoff with jitter, and a circuit breaker for failing dependencies. Include SDK retries in the total budget.
5. Test each fallback against the same output contract and safety requirements as the primary path. Log the selected route, fallback reason, latency, and outcome without unnecessary sensitive content.

When live retrieval fails, an approved fallback might return a cited cached passage with its age. Do not silently replace missing evidence with generated claims.

## Watch out

A model's stated confidence is not calibrated routing evidence. Sending a request to another provider may change privacy obligations and must remain within approved destinations. Never use fallback to bypass an access denial, required approval, or safety refusal. An ambiguous timeout on a write requires reconciliation or idempotency before retrying elsewhere.

## Learn more

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — see when routing into specialized paths is useful.
- [AWS: Retry with backoff](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html) — distinguish transient failures, retry budgets, and idempotency.
- [Microsoft: Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) — understand when to stop calling an unhealthy dependency and how to probe recovery.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
