# 13. Context engineering

Context engineering is the process that chooses what a model sees on each call. It includes instructions, examples, history, tool descriptions, retrieved evidence, and tool results.

## Why it matters

These sources have different trust levels, freshness, and purposes. Adding all available text can bury critical facts, duplicate stale instructions, and expose unnecessary data. A context builder should make selection and omission deliberate, observable, and testable.

## Build it

1. Represent each candidate item with its origin, owner, timestamp, trust class, token estimate, and source identifier.
2. Apply access checks before selection. Rank by the current task, remove duplication, and reserve an output budget.
3. Keep application policy separate from untrusted source material. Preserve citations through summarization.
4. Log item IDs and exclusion reasons instead of raw sensitive text.
5. Test conflicting documents, stale facts, irrelevant long passages, and a malicious instruction inside a retrieved page. Compare the answer against a smaller curated context.

## Watch out

A summary is a lossy derived artifact, not a new authority. Keep links to source evidence and preserve unresolved uncertainty. Tool output should not overwrite trusted instructions. Context compaction can remove a constraint that matters later; test long multi-turn tasks, not only single questions.

## Learn more

- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Study context selection and compaction as explicit engineering choices.
- [LangGraph memory overview](https://docs.langchain.com/oss/python/concepts/memory) — Compare thread-scoped state with longer-lived application memory.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
