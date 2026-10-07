# 32 Essential AI Engineering Resources

A focused reading list for building, evaluating, and operating LLM applications.

## LLM foundations

1. [Text generation — Hugging Face](https://huggingface.co/docs/transformers/llm_tutorial) — Follow tokenization, generation, decoding settings, and common inference mistakes.
2. [Byte-pair encoding — Hugging Face](https://huggingface.co/learn/llm-course/en/chapter6/5) — Work through tokenization with a complete, small Python implementation.

## Prompts and context

3. [Prompting best practices — Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — Learn instruction design, examples, and output constraints; check the model-specific guidance.
4. [Context engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Choose, retrieve, and compact the information supplied to an agent.
5. [Chat templates — Hugging Face](https://huggingface.co/docs/transformers/en/chat_templating) — Understand how message roles become model-specific token sequences.

## Structured outputs

6. [Structured model outputs — OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs) — Use schemas and typed SDK outputs, including refusals and schema limitations.
7. [Object validation — JSON Schema](https://json-schema.org/understanding-json-schema/reference/object) — Learn properties, required fields, and extra-field validation through worked examples.

## Running models: Ollama and Bedrock

8. [Local model commands — Ollama](https://docs.ollama.com/cli) — Download, run, inspect, and stop models from the command line.
9. [Chat API — Ollama](https://docs.ollama.com/api/chat) — Make a local chat request and understand its messages, options, and response fields.
10. [Streaming responses — Ollama](https://docs.ollama.com/api/streaming) — Read newline-delimited output and choose streaming or complete responses.
11. [Converse API tutorial — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) — Build managed model calls, preserve conversation context, and read streaming responses.

## Retrieval-augmented generation

12. [Semantic search — Sentence Transformers](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) — Implement query/document embeddings and similarity search.
13. [Chunking strategies — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html) — Compare fixed-size, hierarchical, and semantic document splitting.
14. [Retrieve and rerank — Sentence Transformers](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — Combine fast candidate retrieval with a cross-encoder reranker.
15. [Grounded answers and citations — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html) — Connect retrieved passages to generated answers and inspect their source references.

## Tools and MCP

16. [Writing effective tools — Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents) — Design clear tool interfaces and evaluate them on realistic tasks.
17. [Tool-use round trip — Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — Implement the model request, application execution, and tool-result cycle.
18. [Build an MCP server — Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server) — Implement, connect, and test a tool server using the documented SDK version.
19. [MCP security — Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) — Understand token misuse, confused deputies, and server trust boundaries.

## Workflows and agents

20. [Building effective agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents) — Compare routing, chaining, and agent loops; focus on patterns rather than its older tooling examples.
21. [Graph API — LangGraph](https://docs.langchain.com/oss/python/langgraph/graph-api) — Build stateful workflows with nodes, edges, reducers, and execution limits.
22. [Human approval and resume — LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts) — Pause and resume workflows while handling persistence and repeated side effects.

## Evaluation

23. [Demystifying evals for AI agents — Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Design datasets, graders, trials, and outcome-based regression evaluations.

## Security and privacy

24. [Prompt-injection prevention — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — Study attacks, layered defenses, and security tests; filters alone are insufficient.
25. [Authorization — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — Enforce least privilege, deny-by-default behavior, and per-request permissions.
26. [Model data retention — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html) — Understand model-dependent retention and configuration before sending data.

## Reliability and observability

27. [Timeouts, retries, backoff, and jitter — AWS Builders’ Library (PDF)](https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf) — Learn retry budgets, idempotence, and how retries can amplify failures.
28. [Distributed traces — OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/traces/) — Understand spans, parent-child relationships, and context propagation.
29. [Model invocation logging — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) — Configure request logging and understand the prompt/response data it can capture.

## Deployment and efficiency

30. [Model lifecycle — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html) — Plan for model retirement and migration using the applicable lifecycle policy.
31. [Prompt caching — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) — Learn cache eligibility, prefix matching, expiration, and usage accounting.
32. [Batch inference jobs — Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-create.html) — Prepare asynchronous inference jobs with S3 inputs, outputs, and bounded execution.

Content and links reviewed on **2026-10-07**. Match code examples to the documented versions.

Inspired by [36 GraphQL Concepts](https://github.com/Novvum/36-graphql-concepts). [Contributing and source policy](CONTRIBUTING.md).
