# 18. State and memory

Context is what a model sees now. Workflow state records where a task is. Long-term memory stores selected facts or preferences across tasks. These need different lifetimes, schemas, and permissions.

## Why it matters

Persisting every transcript makes future requests slower and increases privacy exposure. Persisting nothing makes resumable work unreliable. Explicit state lets the application answer whether a step is pending, completed, failed, or waiting for approval without asking a model to reconstruct it.

## Build it

1. Define a task-state schema with a run ID, revision, status, approved scope, and completed operation IDs.
2. Keep user-specific memory in a separate tenant-scoped store with source, timestamp, retention, and correction behavior.
3. Revalidate permissions when old facts or artifacts are read back.
4. Decide what can be summarized and what must remain exact, such as an approval scope or external receipt ID.
5. Test resume after a crash, a user correction, deletion of a remembered fact, and two concurrent tasks changing state.

## Watch out

Model-generated memory can be wrong or poisoned by untrusted content. Treat additions as proposed data with provenance. Checkpoints are not automatically an exactly-once guarantee for external effects. A saved summary of an approval does not authorize a new action with different recipients, amounts, or inputs.

## Learn more

- [LangGraph memory overview](https://docs.langchain.com/oss/python/concepts/memory) — Compare thread-scoped state with longer-lived application memory.
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Study context selection and compaction as explicit engineering choices.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
