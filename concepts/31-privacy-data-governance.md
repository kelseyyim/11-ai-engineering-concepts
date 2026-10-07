# 31. Privacy and data governance

An AI data-flow map should include the client, application, model provider, retrieval store, tools, caches, logs, evaluation datasets, and backups. Each is a potential destination for user information.

## Why it matters

Local inference can still use cloud-backed models or external tools. Managed inference can still write your prompts to your own logs. Privacy depends on the exact path, configuration, and agreements, not a label such as local or enterprise.

## Build it

1. Classify the data required for the task and remove unnecessary fields before model calls.
2. Document approved destinations, region requirements, retention, training use, access controls, and deletion behavior for each component. Verify current service-specific terms with the responsible owner.
3. Scope retrieval and caches to the authenticated user or tenant. Recheck access when reading stored results.
4. Use synthetic examples for tutorials and development. Keep secrets outside prompts and source control.
5. Test deletion end to end: source records, derived chunks, vectors, memory, cache entries, and governed logs.

## Watch out

Embeddings and summaries are derived data, not automatic anonymization. Sending a private document to an evaluator is also data sharing. A global or cross-region inference route may differ from a regional endpoint. Do not make compliance promises based on this learning guide; use your organization’s approved policies and current provider documentation.

## Learn more

- [Bedrock data protection](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html) — Review service-specific responsibilities and linked retention details.
- [Bedrock invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) — Account for optional prompt/response copies in your own observability infrastructure.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
