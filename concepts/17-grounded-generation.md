# 17. Grounded generation and citations

Retrieval-augmented generation (RAG) supplies evidence to a model at inference time. Grounding means the resulting claims are supported by that evidence, not merely accompanied by links.

## Why it matters

An answer can contain real citations that do not support its conclusion. Separate three questions: Was useful evidence retrieved? Does it support the claims? Does the final response answer the user’s actual question? This makes debugging far more precise than grading prose alone.

## Build it

1. Give each retrieved passage a stable source ID and preserve its revision and location.
2. Ask for a response that distinguishes supported claims from missing evidence. Provide an explicit abstention path.
3. Validate citation IDs against the authorized retrieved set. For important claims, check support manually or with a calibrated evaluator.
4. Test contradictory versions of a policy, an empty retrieval result, and a page containing an instruction to ignore the user.
5. Run the [offline orchestration lab](../labs/03-orchestration-and-evals.md) to see citation membership and abstention checks. Its fixtures demonstrate contracts, not real model quality.

## Watch out

RAG does not eliminate hallucination or prompt injection. Retrieving confidential content and deciding not to display it later is already too late if it reached an unapproved model. Do not fine-tune on frequently changing facts when a versioned lookup can supply them directly.

## Learn more

- [Bedrock RetrieveAndGenerate](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html) — Inspect a concrete retrieval, generation, and citation API.
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Distinguish tasks, trials, graders, transcripts, and outcomes.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
