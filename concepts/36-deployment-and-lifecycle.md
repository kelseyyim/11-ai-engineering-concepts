# 36. Deployment and model lifecycle

The deployable unit is more than a model name. It includes prompts, schemas, tools, retrieval indexes, policies, SDKs, routing rules, and evaluator versions.

## Why it matters

A prompt-only edit can change product behavior as much as a code release. An embedding upgrade can invalidate an index. A model retirement can break an otherwise untouched service. Versioning the full bundle makes failures diagnosable and rollback realistic.

## Build it

1. Create a release manifest covering model/artifact, prompt, tool schemas, policy, index/embedding version, dependency versions, and evaluation report.
2. Run offline tests, authorized integration checks, and a representative evaluation before rollout.
3. Use shadow or canary traffic only with approved data flows and spend limits. Compare outcomes and operating metrics.
4. Define stop conditions, rollback ownership, and what happens to in-flight tasks.
5. Track provider deprecations and license changes. Rehearse migration to an eligible replacement before the deadline.
6. Treat changes to persisted state and index schemas as migrations, including backward compatibility.

## Watch out

An unpinned latest tag is not a reproducible release. Rollback may require the old prompt and index, not just the old container image. Provider retirement dates can differ between direct APIs and managed platforms; verify the actual service you use. A green unit-test suite is necessary evidence, but it is not a production model-quality evaluation.

## Learn more

- [Bedrock model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html) — Check retirement policy for the exact model, including launch-date-dependent policies.
- [OpenAI evaluation design principles](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Task-specific cases, scoring, and continuous evaluation; check the page's Evals-platform deprecation notice before adopting its service APIs.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
