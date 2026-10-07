# 26. Retrieval and agent evaluation

A retrieval pipeline and an agent loop have several independently fallible stages. Evaluate each stage and the final user outcome so you know what to fix.

## Why it matters

For retrieval, ask whether relevant authorized evidence was found and ranked usefully. For agents, ask whether the task completed, whether actions were permitted, and whether the run stayed within its step, time, and spend limits. A convincing final message cannot substitute for a verified external result.

## Build it

1. Label relevant source IDs to compute retrieval recall@k. Inspect ranking metrics when ordering matters.
2. Evaluate answer correctness, evidence support, and citation validity separately.
3. For tools, record selected tool, argument validity, authorization result, execution status, and final state.
4. Compare the final outcome to a verified state or receipt. Permit multiple valid plans rather than requiring one exact transcript.
5. Track failure severity, cost per successful task, and repeated-run success. Add interruption, duplicate-call, and malicious-tool-output cases.

## Watch out

An exact string match is appropriate for a source ID, but often too rigid for prose. Conversely, vague similarity is unsafe for a bank amount or a permission decision. Do not let an evaluator execute tool calls from the transcript. Review judge errors and bias on a sample before using a score as a release gate.

## Learn more

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Distinguish tasks, trials, graders, transcripts, and outcomes.
- [Sentence Transformers retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — See why fast candidate retrieval and precise reranking are different stages.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
