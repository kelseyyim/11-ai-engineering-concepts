# 16. Retrieval and reranking

Retrieval selects candidate evidence. Reranking spends more compute to order a smaller candidate set. The generator can only ground its answer in evidence that actually reaches it.

## Why it matters

If a relevant document is absent from the candidate set, a reranker cannot recover it. If the retrieved document belongs to another tenant, better ranking only makes the leak more likely. Quality and access enforcement must be measured independently.

## Build it

1. Establish a lexical baseline and a labeled query set with relevant source IDs.
2. Compare dense retrieval, keyword retrieval, or a hybrid for the actual corpus. Apply authorization constraints before exposing content to a model.
3. Choose candidate count by recall, latency, and cost. Rerank candidates only if it improves the task.
4. Deduplicate near-identical chunks and preserve useful adjacent context.
5. Measure recall@k and ranking quality separately from final-answer correctness. Add queries with no valid answer and documents with changed permissions.

## Watch out

More retrieved passages can introduce contradictions and bury the answer. Metadata filters are only as current and correct as the ingestion pipeline. A reranker score is not a calibrated probability that a statement is true. Inspect the complete retrieved text when diagnosing failures, using controlled access rather than indiscriminate logs.

## Learn more

- [Sentence Transformers retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — See why fast candidate retrieval and precise reranking are different stages.
- [Bedrock reranking](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html) — See a managed reranking interface and its model-dependent constraints.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
