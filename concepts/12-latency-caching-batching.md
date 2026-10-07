# 12. Latency, caching, and batching

Latency is a pipeline property. Queueing, retrieval, prompt processing, generation, tool calls, and retries all contribute. Optimize the slow stage you measured.

## Why it matters

For interactive work, track time to first useful output and total completion time separately. For background jobs, throughput and deadline compliance can matter more. Prompt-prefix caching reuses inference work; application-response caching reuses an answer. They require different correctness checks.

## Build it

1. Trace each stage and compare cold versus warm runs under realistic concurrency. Report percentiles, not only the mean.
2. Reduce unnecessary output and repeated context before adding infrastructure.
3. For response caches, include tenant, permissions, model/prompt version, source revision, and relevant parameters in the key. Set explicit expiry and invalidation behavior.
4. For provider prompt caching, check eligibility, cache-write/read costs, actual usage fields, and privacy policy.
5. Move independent, delay-tolerant jobs to an approved batch API only after checking its model support, completion window, and storage requirements.

## Watch out

A cache miss is not a correctness failure; a cross-tenant cache hit is. Semantic caches can return a plausible answer to a materially different question. Batch processing does not imply prompt-cache support or interactive latency. Avoid printing a cached answer after the user’s access to its sources was revoked.

## Learn more

- [Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) — Review explicit and implicit caching, eligibility, and usage accounting.
- [Bedrock batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html) — Understand the separate asynchronous workload model.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
