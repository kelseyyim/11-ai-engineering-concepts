# 36 AI Engineering Concepts Every Developer Should Know

📜 A practical, curated guide to building reliable applications with language models.

Start with the fundamentals. Run a model locally with Ollama. Use managed inference with Amazon Bedrock. Then connect context, tools, workflows, evaluations, and production controls into a system you can explain and maintain.

## Introduction

This is a study map for software engineers who can already work with APIs, tests, and version control. You do not need to train a foundation model or adopt an agent framework to begin.

The focus is **engineering applications with LLMs**. [AI-assisted software development](concepts/35-ai-assisted-development.md) gets its own chapter because using a coding assistant and building an AI product are related but different skills.

There are exactly **36 concepts in six groups**. Each has an original explanation, a concrete exercise, failure modes, and a short list of primary resources. The README is the browsable resource index; the linked notes go deeper. Treat this as a learning path, not a hiring checklist or a claim that every project needs every technique.

Inspired by [36 GraphQL Concepts](https://github.com/Novvum/36-graphql-concepts), whose README credits [@kelseyyim](https://github.com/kelseyyim) for getting it started. This guide follows the categorized concepts-and-resources format with newly written content.

## Start here

- **Learn the basics:** concepts 1–6, then [Lab 1: Ollama](labs/01-ollama.md).
- **Build a useful prototype:** concepts 13–20, then [Lab 3: orchestration and evaluation](labs/03-orchestration-and-evals.md).
- **Work in AWS:** concepts 9–12 and 30–33, then [Lab 2: Amazon Bedrock](labs/02-bedrock.md).
- **Prepare to ship:** concepts 25–36 and the [release checklist](docs/release-checklist.md).

The small examples use Python 3.11+ so the transport and control flow are easy to inspect. The concepts apply equally to TypeScript, Java, Go, or your existing stack.

### Try it without a model or cloud account

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_content.py
python3 scripts/check_links.py
python3 examples/ollama_chat.py
python3 examples/bedrock_chat.py
python3 examples/bounded_agent.py --eval
```

The first two provider examples print offline previews by default. The orchestration example uses scripted responses and synthetic data. Nothing here needs credentials, installs a model, provisions AWS, or calls an inference API unless you deliberately follow a live lab. Live Bedrock calls can incur charges and may have model-access or agreement requirements.

### What is verified?

Offline tests cover request construction, response validation, failures, tool authorization, replay handling, and evaluation checks. They do **not** establish live model quality, AWS account access, hardware compatibility, or production security. See [verification details](docs/verification.md).

Resources were reviewed against primary documentation on **2026-10-07**. APIs, model availability, pricing, and protocol revisions change. Use the source for your selected version and follow the [resource quality policy](docs/resource-policy.md).

## Table of contents

<!-- BEGIN TOC -->

### Foundations

1. [LLM mental models](#1-llm-mental-models)
2. [Tokens and context windows](#2-tokens-and-context-windows)
3. [Model selection and capability checks](#3-model-selection-and-capability-checks)
4. [Sampling and reproducibility](#4-sampling-and-reproducibility)
5. [Prompting and instruction design](#5-prompting-and-instruction-design)
6. [Structured outputs and validation](#6-structured-outputs-and-validation)
### Running models

7. [Local models with Ollama](#7-local-models-with-ollama)
8. [Model artifacts and quantization](#8-model-artifacts-and-quantization)
9. [Provider APIs and adapters](#9-provider-apis-and-adapters)
10. [Amazon Bedrock and IAM](#10-amazon-bedrock-and-iam)
11. [Streaming and cancellation](#11-streaming-and-cancellation)
12. [Latency, caching, and batching](#12-latency-caching-and-batching)
### Context and retrieval

13. [Context engineering](#13-context-engineering)
14. [Embeddings and similarity](#14-embeddings-and-similarity)
15. [Chunking and indexing](#15-chunking-and-indexing)
16. [Retrieval and reranking](#16-retrieval-and-reranking)
17. [Grounded generation and citations](#17-grounded-generation-and-citations)
18. [State and memory](#18-state-and-memory)
### Orchestration

19. [Workflows versus agents](#19-workflows-versus-agents)
20. [Tool calling and contracts](#20-tool-calling-and-contracts)
21. [Model Context Protocol (MCP)](#21-model-context-protocol-mcp)
22. [Routing and fallbacks](#22-routing-and-fallbacks)
23. [Durable execution and human approval](#23-durable-execution-and-human-approval)
24. [Multi-agent systems](#24-multi-agent-systems)
### Quality and safety

25. [Evaluations and golden datasets](#25-evaluations-and-golden-datasets)
26. [Retrieval and agent evaluation](#26-retrieval-and-agent-evaluation)
27. [Testing and CI for AI systems](#27-testing-and-ci-for-ai-systems)
28. [Observability and tracing](#28-observability-and-tracing)
29. [Prompt injection and untrusted data](#29-prompt-injection-and-untrusted-data)
30. [Permissions and sandboxing](#30-permissions-and-sandboxing)
### Shipping and operating

31. [Privacy and data governance](#31-privacy-and-data-governance)
32. [Reliability and error handling](#32-reliability-and-error-handling)
33. [Cost, quotas, and capacity](#33-cost-quotas-and-capacity)
34. [Fine-tuning and adaptation](#34-fine-tuning-and-adaptation)
35. [AI-assisted software development](#35-ai-assisted-software-development)
36. [Deployment and model lifecycle](#36-deployment-and-model-lifecycle)

<!-- END TOC -->

---

<!-- BEGIN CONCEPTS -->

# Foundations

## 1. LLM mental models

Separate the probabilistic model from the deterministic application around it.

[Explanation, exercise, and pitfalls](concepts/01-llm-mental-models.md)

### Resources

- [Hugging Face LLM course](https://huggingface.co/learn/llm-course/en/chapter1/1) — A guided foundation in language models, architectures, and limitations.
- [Transformers text generation](https://huggingface.co/docs/transformers/llm_tutorial) — Follow the inference path from tokenization to generated tokens.

[⬆ Back to top](#table-of-contents)

## 2. Tokens and context windows

Budget the entire request, reserve output space, and make truncation visible.

[Explanation, exercise, and pitfalls](concepts/02-tokens-and-context.md)

### Resources

- [Hugging Face BPE tokenization](https://huggingface.co/learn/llm-course/en/chapter6/5) — See why tokens are not interchangeable with words.
- [Transformers padding and truncation](https://huggingface.co/docs/transformers/main/en/pad_truncation) — Understand explicit length handling and truncation strategies.
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Study context selection and compaction as explicit engineering choices.

[⬆ Back to top](#table-of-contents)

## 3. Model selection and capability checks

Choose against a task-specific evaluation and explicit operating constraints.

[Explanation, exercise, and pitfalls](concepts/03-model-selection.md)

### Resources

- [Hugging Face model cards](https://huggingface.co/docs/hub/model-cards) — Inspect intended uses, limitations, provenance, and licensing.
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Study task-specific cases, scoring, and continuous evaluation; service APIs are provider-specific.

[⬆ Back to top](#table-of-contents)

## 4. Sampling and reproducibility

Understand decoding controls without mistaking a seed for a guarantee.

[Explanation, exercise, and pitfalls](concepts/04-sampling-and-reproducibility.md)

### Resources

- [Transformers generation strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies) — Compare greedy decoding and sampling; use the version matching your installation.
- [Transformers text generation](https://huggingface.co/docs/transformers/llm_tutorial) — Follow the inference path from tokenization to generated tokens.

[⬆ Back to top](#table-of-contents)

## 5. Prompting and instruction design

Turn a vague request into a testable input, output, and failure contract.

[Explanation, exercise, and pitfalls](concepts/05-prompting-and-instructions.md)

### Resources

- [Claude prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — Start from success criteria and empirical prompt tests.
- [Transformers chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating) — Understand how roles and message content become the model’s input tokens.

[⬆ Back to top](#table-of-contents)

## 6. Structured outputs and validation

Treat generated JSON as untrusted input that still needs semantic validation.

[Explanation, exercise, and pitfalls](concepts/06-structured-outputs.md)

### Resources

- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — Compare JSON output and schema constraints, including refusal handling.
- [JSON Schema reference](https://json-schema.org/understanding-json-schema/reference) — Learn the underlying vocabulary independently of any model provider.

[⬆ Back to top](#table-of-contents)

# Running models

## 7. Local models with Ollama

Run a local model deliberately, with an explicit network and resource boundary.

[Explanation, exercise, and pitfalls](concepts/07-local-models-ollama.md)

### Resources

- [Ollama FAQ](https://docs.ollama.com/faq): cloud-disable configuration, loopback binding, and memory inspection.
- [Ollama CLI reference](https://docs.ollama.com/cli): model inventory and running-model controls.
- [Chat API](https://docs.ollama.com/api/chat): the application-to-runtime request boundary.

[⬆ Back to top](#table-of-contents)

## 8. Model artifacts and quantization

Understand weights, tokenizers, templates, licenses, and memory tradeoffs.

[Explanation, exercise, and pitfalls](concepts/08-model-artifacts-quantization.md)

### Resources

- [Safetensors documentation](https://huggingface.co/docs/safetensors/index): tensor-format purpose and loading model.
- [Hugging Face GGUF guide](https://huggingface.co/docs/hub/gguf): metadata and quantized tensor representations.
- [Ollama model imports](https://docs.ollama.com/import): supported artifact import workflows.

[⬆ Back to top](#table-of-contents)

## 9. Provider APIs and adapters

Normalize only the capabilities you actually support and test.

[Explanation, exercise, and pitfalls](concepts/09-provider-apis.md)

### Resources

- [Ollama compatibility reference](https://docs.ollama.com/api/openai-compatibility): supported interfaces and compatibility boundaries.
- [Native chat endpoint](https://docs.ollama.com/api/chat): a concrete provider-specific request/response contract.
- [Ollama API errors](https://docs.ollama.com/api/errors): status codes and errors within streamed responses.

[⬆ Back to top](#table-of-contents)

## 10. Amazon Bedrock and IAM

Use managed inference with explicit model, Region, identity, and billing choices.

[Explanation, exercise, and pitfalls](concepts/10-amazon-bedrock.md)

### Resources

- [Converse API reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) — request structure, return fields, and invocation permission.
- [Models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html) — select a model and verify its current capabilities and Regions.
- [Inference-profile prerequisites](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html) — resource scoping for profile-based invocation.

[⬆ Back to top](#table-of-contents)

## 11. Streaming and cancellation

Handle partial output, terminal events, timeouts, and user cancellation.

[Explanation, exercise, and pitfalls](concepts/11-streaming-and-cancellation.md)

### Resources

- [Ollama streaming guide](https://docs.ollama.com/api/streaming): NDJSON framing and non-streaming requests.
- [Ollama error behavior](https://docs.ollama.com/api/errors): failures after a stream has started.
- [Python HTTP client documentation](https://docs.python.org/3.11/library/http.client.html): response reading and connection lifecycle.

[⬆ Back to top](#table-of-contents)

## 12. Latency, caching, and batching

Optimize a measured bottleneck without hiding stale or cross-tenant results.

[Explanation, exercise, and pitfalls](concepts/12-latency-caching-batching.md)

### Resources

- [Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) — Review explicit and implicit caching, eligibility, and usage accounting.
- [Bedrock batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html) — Understand the separate asynchronous workload model.

[⬆ Back to top](#table-of-contents)

# Context and retrieval

## 13. Context engineering

Build the smallest sufficient, trustworthy context for each model call.

[Explanation, exercise, and pitfalls](concepts/13-context-engineering.md)

### Resources

- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Study context selection and compaction as explicit engineering choices.
- [LangGraph memory overview](https://docs.langchain.com/oss/python/concepts/memory) — Compare thread-scoped state with longer-lived application memory.

[⬆ Back to top](#table-of-contents)

## 14. Embeddings and similarity

Choose representations and distance metrics for the retrieval task.

[Explanation, exercise, and pitfalls](concepts/14-embeddings-and-similarity.md)

### Resources

- [Sentence Transformers semantic search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) — Compare query/document encoding and symmetric versus asymmetric retrieval.
- [Sentence Transformers retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — See why fast candidate retrieval and precise reranking are different stages.

[⬆ Back to top](#table-of-contents)

## 15. Chunking and indexing

Preserve source identity, access rules, and freshness through ingestion.

[Explanation, exercise, and pitfalls](concepts/15-chunking-and-indexing.md)

### Resources

- [Bedrock chunking strategies](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html) — Compare fixed-size, hierarchical, and semantic chunking in a managed implementation.
- [Sentence Transformers semantic search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) — Compare query/document encoding and symmetric versus asymmetric retrieval.

[⬆ Back to top](#table-of-contents)

## 16. Retrieval and reranking

Measure candidate recall before asking a generator to answer.

[Explanation, exercise, and pitfalls](concepts/16-retrieval-and-reranking.md)

### Resources

- [Sentence Transformers retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — See why fast candidate retrieval and precise reranking are different stages.
- [Bedrock reranking](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html) — See a managed reranking interface and its model-dependent constraints.

[⬆ Back to top](#table-of-contents)

## 17. Grounded generation and citations

Connect every supported claim to evidence and make abstention useful.

[Explanation, exercise, and pitfalls](concepts/17-grounded-generation.md)

### Resources

- [Bedrock RetrieveAndGenerate](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html) — Inspect a concrete retrieval, generation, and citation API.
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Distinguish tasks, trials, graders, transcripts, and outcomes.

[⬆ Back to top](#table-of-contents)

## 18. State and memory

Separate request context, durable workflow state, and user-specific memory.

[Explanation, exercise, and pitfalls](concepts/18-state-and-memory.md)

### Resources

- [LangGraph memory overview](https://docs.langchain.com/oss/python/concepts/memory) — Compare thread-scoped state with longer-lived application memory.
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Study context selection and compaction as explicit engineering choices.

[⬆ Back to top](#table-of-contents)

# Orchestration

## 19. Workflows versus agents

Pick the simplest control flow that can complete the job reliably.

[Explanation, exercise, and pitfalls](concepts/19-workflows-and-agents.md)

### Resources

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — distinguish predefined workflows from model-directed loops and choose the simplest useful pattern.
- [LangGraph: Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) — learn explicit state, nodes, conditional edges, and execution limits.

[⬆ Back to top](#table-of-contents)

## 20. Tool calling and contracts

Validate model proposals before executing scoped application code.

[Explanation, exercise, and pitfalls](concepts/20-tool-calling.md)

### Resources

- [Anthropic: Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents) — design clear interfaces and evaluate tool usability on realistic tasks.
- [Claude: Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — follow a provider-specific tool request/result cycle and understand execution responsibility.

[⬆ Back to top](#table-of-contents)

## 21. Model Context Protocol (MCP)

Connect tools and resources through a protocol without confusing it with permission.

[Explanation, exercise, and pitfalls](concepts/21-mcp.md)

### Resources

- [MCP specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) — understand the protocol's roles, capabilities, and limits.
- [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) — study token misuse, confused-deputy risks, local-server compromise, and scope minimization.

[⬆ Back to top](#table-of-contents)

## 22. Routing and fallbacks

Make quality, cost, capability, and privacy constraints explicit at every route.

[Explanation, exercise, and pitfalls](concepts/22-routing-and-fallbacks.md)

### Resources

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — see when routing into specialized paths is useful.
- [AWS: Retry with backoff](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html) — distinguish transient failures, retry budgets, and idempotency.
- [Microsoft: Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) — understand when to stop calling an unhealthy dependency and how to probe recovery.

[⬆ Back to top](#table-of-contents)

## 23. Durable execution and human approval

Resume safely after failures and approvals without repeating side effects.

[Explanation, exercise, and pitfalls](concepts/23-durable-execution.md)

### Resources

- [LangGraph: Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers) — inspect persisted state and understand durability tradeoffs.
- [LangGraph: Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) — learn pause/resume behavior and why pre-interrupt side effects need care.
- [Temporal: Activity definition](https://docs.temporal.io/activity-definition) — understand retryable execution and idempotent Activities.

[⬆ Back to top](#table-of-contents)

## 24. Multi-agent systems

Justify delegation with measurable gains and bounded coordination costs.

[Explanation, exercise, and pitfalls](concepts/24-multi-agent-systems.md)

### Resources

- [Anthropic: Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — examine parallel research, delegation design, and coordination costs in a concrete deployment.
- [LangChain: Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent) — compare specialist subagents, handoffs, and other ways to divide context and control.

[⬆ Back to top](#table-of-contents)

# Quality and safety

## 25. Evaluations and golden datasets

Define success on representative cases before changing models or prompts.

[Explanation, exercise, and pitfalls](concepts/25-evals-and-golden-datasets.md)

### Resources

- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Study task-specific cases, scoring, and continuous evaluation; service APIs are provider-specific.
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Distinguish tasks, trials, graders, transcripts, and outcomes.

[⬆ Back to top](#table-of-contents)

## 26. Retrieval and agent evaluation

Score evidence retrieval, final outcomes, and unsafe actions separately.

[Explanation, exercise, and pitfalls](concepts/26-retrieval-and-agent-evaluation.md)

### Resources

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Distinguish tasks, trials, graders, transcripts, and outcomes.
- [Sentence Transformers retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — See why fast candidate retrieval and precise reranking are different stages.

[⬆ Back to top](#table-of-contents)

## 27. Testing and CI for AI systems

Keep deterministic contract tests separate from probabilistic model evaluations.

[Explanation, exercise, and pitfalls](concepts/27-testing-and-ci.md)

### Resources

- [Python unittest](https://docs.python.org/3/library/unittest.html) — Use a zero-dependency unit-test runner and deterministic fixtures.
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Study task-specific cases, scoring, and continuous evaluation; service APIs are provider-specific.

[⬆ Back to top](#table-of-contents)

## 28. Observability and tracing

Explain a failed run without turning telemetry into a sensitive-data dump.

[Explanation, exercise, and pitfalls](concepts/28-observability.md)

### Resources

- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) — Learn spans, context propagation, and distributed request structure.
- [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai) — Follow the current home of evolving model/tool telemetry conventions.
- [Bedrock invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) — Inspect what enabling content logging actually sends to CloudWatch and S3.

[⬆ Back to top](#table-of-contents)

## 29. Prompt injection and untrusted data

Keep retrieved content and tool output from becoming authority.

[Explanation, exercise, and pitfalls](concepts/29-prompt-injection.md)

### Resources

- [OWASP: Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — study attack surfaces, layered defenses, and outcome-based tests.
- [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) — understand information-flow controls and the limits of the paper's threat model.

[⬆ Back to top](#table-of-contents)

## 30. Permissions and sandboxing

Enforce least privilege outside the model, at the actual execution boundary.

[Explanation, exercise, and pitfalls](concepts/30-permissions-and-sandboxing.md)

### Resources

- [OWASP: Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — implement least privilege, deny-by-default behavior, and per-request checks.
- [Anthropic: Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) — examine a provider-specific implementation of combined filesystem and network boundaries; verify current product settings separately.

[⬆ Back to top](#table-of-contents)

# Shipping and operating

## 31. Privacy and data governance

Track where information travels, who can access it, and when it is deleted.

[Explanation, exercise, and pitfalls](concepts/31-privacy-data-governance.md)

### Resources

- [Bedrock data protection](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html) — Review service-specific responsibilities and linked retention details.
- [Bedrock invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) — Account for optional prompt/response copies in your own observability infrastructure.

[⬆ Back to top](#table-of-contents)

## 32. Reliability and error handling

Bound retries and distinguish failed work from an unknown outcome.

[Explanation, exercise, and pitfalls](concepts/32-reliability-and-error-handling.md)

### Resources

- [AWS SDK retry behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html) — Understand standard retry policy, backoff, and attempt configuration.
- [AWS Builders’ Library: timeouts and retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — Study why retries require deadlines, jitter, and care around side effects.

[⬆ Back to top](#table-of-contents)

## 33. Cost, quotas, and capacity

Budget complete workflows, including retries, tools, and operational overhead.

[Explanation, exercise, and pitfalls](concepts/33-cost-and-capacity.md)

### Resources

- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) — verify rates and billing modes for the chosen workload.
- [Amazon Bedrock quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) — check capacity constraints and token accounting.
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) — understand budget tracking and notification delays.

[⬆ Back to top](#table-of-contents)

## 34. Fine-tuning and adaptation

Change weights only when prompting and retrieval do not solve the measured problem.

[Explanation, exercise, and pitfalls](concepts/34-fine-tuning-and-adaptation.md)

### Resources

- [Hugging Face PEFT](https://huggingface.co/docs/peft/index) — Learn parameter-efficient adaptation and the relationship between adapters and base models.
- [TRL supervised fine-tuning](https://huggingface.co/docs/trl/sft_trainer) — Inspect a concrete training workflow, dataset formats, and configuration choices.

[⬆ Back to top](#table-of-contents)

## 35. AI-assisted software development

Use coding assistants with reviewable scope, independent tests, and clear authority.

[Explanation, exercise, and pitfalls](concepts/35-ai-assisted-development.md)

### Resources

- [GitHub Copilot Agents application card](https://docs.github.com/en/copilot/responsible-use/agents) — Review documented limits, permissions, and human validation expectations.
- [Python unittest](https://docs.python.org/3/library/unittest.html) — Build checks that can run independently of the assistant’s explanation.

[⬆ Back to top](#table-of-contents)

## 36. Deployment and model lifecycle

Version the whole system and rehearse both rollout and rollback.

[Explanation, exercise, and pitfalls](concepts/36-deployment-and-lifecycle.md)

### Resources

- [Bedrock model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html) — Check retirement policy for the exact model, including launch-date-dependent policies.
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Study task-specific cases, scoring, and continuous evaluation; service APIs are provider-specific.

[⬆ Back to top](#table-of-contents)

<!-- END CONCEPTS -->

## Hands-on labs

1. [Local, schema-validated chat with Ollama](labs/01-ollama.md): inspect an offline request, configure a local-only daemon, make one bounded request, and validate its output.
2. [Managed inference with Amazon Bedrock](labs/02-bedrock.md): understand identity, model and Region selection, Converse requests, usage, stop reasons, and failure handling.
3. [A bounded tool loop and an evaluation harness](labs/03-orchestration-and-evals.md): run offline fixtures, reject unauthorized actions, validate citations, and test the grader itself.

## Community and contributions

A good contribution helps a developer make a better engineering decision. Improve a confusing explanation, replace a stale resource, add a reproducible failure case, or suggest a stronger exercise. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Translations and carefully selected videos are welcome when they have a maintainer, a clear connection to a concept, and a review date. There are no claimed translations or contributor endorsements yet.

## Attribution and licensing

The linked resources belong to their respective authors and retain their own licenses. This repository links to them rather than redistributing their content. See [attribution and licensing status](docs/attribution.md) before reusing or publishing this private review draft.
