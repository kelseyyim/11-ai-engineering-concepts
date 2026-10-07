# 15. Chunking and indexing

Ingestion transforms source documents into searchable records. Chunking determines which pieces travel together; indexing determines how you can find and update them.

## Why it matters

The retrieval unit needs enough context to be interpretable. Splitting a table from its headers or a function from its signature can produce misleading evidence. A clean index also needs stable IDs, permission metadata, source revisions, and deletion handling.

## Build it

1. Parse a representative sample of your actual files, including tables, headings, lists, and code. Inspect the extracted text before tuning a vector database.
2. Start with document-aware boundaries and measured size limits. Use overlap only where it preserves meaning.
3. Attach document ID, chunk ID, source location, revision, tenant/access metadata, and ingestion version.
4. Make re-ingestion idempotent. Remove superseded chunks and propagate source deletion and permission changes.
5. Evaluate several chunking strategies on labeled questions; examine evidence lost at boundaries and duplicate results.

## Watch out

No universal chunk size works for every model and corpus. Token counts depend on the tokenizer. A correct answer from a stale policy document is still a product failure. OCR errors and broken parsing cannot be repaired simply by buying a more powerful generator. Keep raw source and derived-index lineage inspectable.

## Learn more

- [Bedrock chunking strategies](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html) — Compare fixed-size, hierarchical, and semantic chunking in a managed implementation.
- [Sentence Transformers semantic search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) — Compare query/document encoding and symmetric versus asymmetric retrieval.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
