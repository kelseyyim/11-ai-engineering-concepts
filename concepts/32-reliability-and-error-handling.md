# 32. Reliability and error handling

Reliability means completing a permitted task or returning an honest, actionable failure within a bounded budget. It includes uncertainty about whether an external action already happened.

## Why it matters

A timeout does not prove the server did nothing. Retrying a read is different from retrying a payment, message, or deployment. Model calls can also succeed at the transport layer while returning a refusal, truncated answer, invalid schema, or unsupported tool proposal.

## Build it

1. Classify failures into invalid input, permission/configuration error, transient provider failure, invalid output, and unknown external outcome.
2. Set connect/read timeouts, a whole-run deadline, and a single retry budget across layers.
3. Use bounded exponential backoff with jitter for eligible transient failures; respect provider retry guidance.
4. For side effects, use server-supported idempotency keys or reconcile an operation ID before retrying.
5. Stop on policy rejection and permanent validation errors. Surface partial results and what is still unverified.
6. Test throttling, provider outage, deadline expiry, and a response lost after a successful tool action.

## Watch out

Nested retry loops multiply cost and load. Fallback to another provider can change data destination and model capabilities; it must already be permitted. A cancellation request may not stop server-side inference or charges immediately. An in-memory dictionary is useful for a toy duplicate-call test but is not a durable transaction system.

## Learn more

- [AWS SDK retry behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html) — Understand standard retry policy, backoff, and attempt configuration.
- [AWS Builders’ Library: timeouts and retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — Study why retries require deadlines, jitter, and care around side effects.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
