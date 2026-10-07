# 14. Embeddings and similarity

An embedding maps content to a numeric representation useful for tasks such as semantic retrieval. Similarity compares those representations; it does not verify factual agreement or access rights.

## Why it matters

Queries and documents must be encoded with compatible models and preprocessing. A query about revoking a token may resemble a page about creating one. Exact identifiers, dates, and rare terms often benefit from lexical search alongside embeddings.

## Build it

1. Assemble a small corpus and labeled query-to-document matches. Include paraphrases and exact identifiers.
2. Choose an embedding model appropriate for the corpus language and query/document task. Follow its required prefixes, normalization, and input limits.
3. Store model version, dimensions, preprocessing version, and source ID with each vector.
4. Compare cosine or the model’s recommended scoring function against a lexical baseline.
5. Change the embedding model only with a re-embedding/migration plan; matching dimensions alone do not make two vector spaces compatible.

## Watch out

An embedding is derived from private content and can still be sensitive. Do not treat it as anonymization. Vector similarity values are model- and distribution-dependent; an arbitrary universal threshold will fail. Approximate-nearest-neighbor indexing trades speed against recall and needs its own measurement.

## Learn more

- [Sentence Transformers semantic search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) — Compare query/document encoding and symmetric versus asymmetric retrieval.
- [Sentence Transformers retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — See why fast candidate retrieval and precise reranking are different stages.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
