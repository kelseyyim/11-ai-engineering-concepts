# 28. Observability and tracing

A trace connects one user request to retrieval, model calls, tools, retries, and the final result. Metrics aggregate those traces; logs add selected diagnostic details.

## Why it matters

When an answer fails, you need to know which model and prompt were used, what evidence was selected, which tool failed, and where time and money went. You rarely need every raw prompt, completion, credential, or customer document in your logging platform.

## Build it

1. Generate a run ID and span IDs. Record stage, duration, model identifier, prompt version, token usage, tool name, attempt number, and terminal status.
2. Distinguish first-token latency from total latency and distinguish model refusal from transport failure.
3. Default to redacted metadata. Make any content capture opt-in, permissioned, access-controlled, and time-limited.
4. Alert on failure rate, unsafe-action attempts, latency tails, budget exhaustion, and retrieval-empty rates.
5. Pick one failed run and reconstruct it using IDs and controlled evidence access.

## Watch out

Observability can become a second sensitive database. Scrub tool arguments and exception messages as well as prompts. High-cardinality labels such as a full user question can cause both cost and privacy problems. GenAI telemetry conventions evolve; pin the version your instrumentation uses and plan migrations.

## Learn more

- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) — Learn spans, context propagation, and distributed request structure.
- [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai) — Follow the current home of evolving model/tool telemetry conventions.
- [Bedrock invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) — Inspect what enabling content logging actually sends to CloudWatch and S3.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
