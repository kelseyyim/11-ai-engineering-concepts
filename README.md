# AI Engineering Concepts

Curated resources for the core concepts behind building reliable applications with language models. Start with a topic below; notes, exercises, and hands-on labs are there when you want to go deeper.

## Table of contents

<!-- BEGIN TOC -->

- [LLM foundations and model selection](#llm-foundations-and-model-selection)
- [Prompting and context engineering](#prompting-and-context-engineering)
- [Model APIs and structured outputs](#model-apis-and-structured-outputs)
- [Local models with Ollama](#local-models-with-ollama)
- [Amazon Bedrock](#amazon-bedrock)
- [Retrieval-augmented generation (RAG)](#retrieval-augmented-generation-rag)
- [Tool calling and MCP](#tool-calling-and-mcp)
- [Workflows and agents](#workflows-and-agents)
- [Evaluation and testing](#evaluation-and-testing)
- [Security and privacy](#security-and-privacy)
- [Reliability and observability](#reliability-and-observability)
- [Deployment, performance, and cost](#deployment-performance-and-cost)

<!-- END TOC -->

<!-- BEGIN CONCEPTS -->

## LLM foundations and model selection

- [Hugging Face LLM course](https://huggingface.co/learn/llm-course/en/chapter1/1) — A guided foundation in language models, architectures, and limitations.
- [Hugging Face BPE tokenization](https://huggingface.co/learn/llm-course/en/chapter6/5) — See why tokens are not interchangeable with words.
- [Transformers generation strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies) — Compare greedy decoding and sampling; use the version matching your installation.
- [Hugging Face model cards](https://huggingface.co/docs/hub/model-cards) — Inspect intended uses, limitations, provenance, and licensing.

Notes and exercises: [LLM mental models](concepts/01-llm-mental-models.md) · [Tokens and context windows](concepts/02-tokens-and-context.md) · [Model selection and capability checks](concepts/03-model-selection.md) · [Sampling and reproducibility](concepts/04-sampling-and-reproducibility.md) · [Model artifacts and quantization](concepts/08-model-artifacts-quantization.md)

[⬆ Back to top](#table-of-contents)

## Prompting and context engineering

- [Claude prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — Start from success criteria and empirical prompt tests.
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Study context selection and compaction as explicit engineering choices.
- [Transformers chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating) — Understand how roles and message content become the model’s input tokens.
- [LangGraph memory overview](https://docs.langchain.com/oss/python/concepts/memory) — Compare thread-scoped state with longer-lived application memory.

Notes and exercises: [Prompting and instruction design](concepts/05-prompting-and-instructions.md) · [Context engineering](concepts/13-context-engineering.md) · [State and memory](concepts/18-state-and-memory.md)

[⬆ Back to top](#table-of-contents)

## Model APIs and structured outputs

- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — Compare JSON output and schema constraints, including refusal handling.
- [JSON Schema reference](https://json-schema.org/understanding-json-schema/reference) — Learn the underlying vocabulary independently of any model provider.
- [Ollama compatibility reference](https://docs.ollama.com/api/openai-compatibility): supported interfaces and compatibility boundaries.
- [Ollama streaming guide](https://docs.ollama.com/api/streaming): NDJSON framing and non-streaming requests.

Notes and exercises: [Structured outputs and validation](concepts/06-structured-outputs.md) · [Provider APIs and adapters](concepts/09-provider-apis.md) · [Streaming and cancellation](concepts/11-streaming-and-cancellation.md)

[⬆ Back to top](#table-of-contents)

## Local models with Ollama

- [Ollama FAQ](https://docs.ollama.com/faq): cloud-disable configuration, loopback binding, and memory inspection.
- [Ollama CLI reference](https://docs.ollama.com/cli): model inventory and running-model controls.
- [Chat API](https://docs.ollama.com/api/chat): the application-to-runtime request boundary.

Notes and exercises: [Local models with Ollama](concepts/07-local-models-ollama.md)

[⬆ Back to top](#table-of-contents)

## Amazon Bedrock

- [Converse API reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) — request structure, return fields, and invocation permission.
- [Models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html) — select a model and verify its current capabilities and Regions.
- [Inference-profile prerequisites](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html) — resource scoping for profile-based invocation.

Notes and exercises: [Amazon Bedrock and IAM](concepts/10-amazon-bedrock.md)

[⬆ Back to top](#table-of-contents)

## Retrieval-augmented generation (RAG)

- [Sentence Transformers semantic search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) — Compare query/document encoding and symmetric versus asymmetric retrieval.
- [Bedrock chunking strategies](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html) — Compare fixed-size, hierarchical, and semantic chunking in a managed implementation.
- [Sentence Transformers retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — See why fast candidate retrieval and precise reranking are different stages.
- [Bedrock RetrieveAndGenerate](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html) — Inspect a concrete retrieval, generation, and citation API.

Notes and exercises: [Embeddings and similarity](concepts/14-embeddings-and-similarity.md) · [Chunking and indexing](concepts/15-chunking-and-indexing.md) · [Retrieval and reranking](concepts/16-retrieval-and-reranking.md) · [Grounded generation and citations](concepts/17-grounded-generation.md)

[⬆ Back to top](#table-of-contents)

## Tool calling and MCP

- [Anthropic: Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents) — design clear interfaces and evaluate tool usability on realistic tasks.
- [Claude: Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — follow a provider-specific tool request/result cycle and understand execution responsibility.
- [MCP specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) — understand the protocol's roles, capabilities, and limits.
- [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) — study token misuse, confused-deputy risks, local-server compromise, and scope minimization.

Notes and exercises: [Tool calling and contracts](concepts/20-tool-calling.md) · [Model Context Protocol (MCP)](concepts/21-mcp.md)

[⬆ Back to top](#table-of-contents)

## Workflows and agents

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — distinguish predefined workflows from model-directed loops; read for architecture patterns, with the article's tooling-update notice in mind.
- [LangGraph: Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) — learn explicit state, nodes, conditional edges, and execution limits.
- [LangGraph: Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) — learn pause/resume behavior and why pre-interrupt side effects need care.
- [Temporal: Activity definition](https://docs.temporal.io/activity-definition) — understand retryable execution and idempotent Activities.

Notes and exercises: [Workflows versus agents](concepts/19-workflows-and-agents.md) · [Routing and fallbacks](concepts/22-routing-and-fallbacks.md) · [Durable execution and human approval](concepts/23-durable-execution.md) · [Multi-agent systems](concepts/24-multi-agent-systems.md)

[⬆ Back to top](#table-of-contents)

## Evaluation and testing

- [OpenAI evaluation design principles](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Task-specific cases, scoring, and continuous evaluation; check the page's Evals-platform deprecation notice before adopting its service APIs.
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Distinguish tasks, trials, graders, transcripts, and outcomes.

Notes and exercises: [Evaluations and golden datasets](concepts/25-evals-and-golden-datasets.md) · [Retrieval and agent evaluation](concepts/26-retrieval-and-agent-evaluation.md) · [Testing and CI for AI systems](concepts/27-testing-and-ci.md)

[⬆ Back to top](#table-of-contents)

## Security and privacy

- [OWASP: Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — study attack surfaces, layered defenses, and outcome-based tests.
- [OWASP: Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — implement least privilege, deny-by-default behavior, and per-request checks.
- [Bedrock data protection](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html) — Review service-specific responsibilities and linked retention details.

Notes and exercises: [Prompt injection and untrusted data](concepts/29-prompt-injection.md) · [Permissions and sandboxing](concepts/30-permissions-and-sandboxing.md) · [Privacy and data governance](concepts/31-privacy-data-governance.md)

[⬆ Back to top](#table-of-contents)

## Reliability and observability

- [AWS Builders’ Library: timeouts and retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — Study why retries require deadlines, jitter, and care around side effects.
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) — Learn spans, context propagation, and distributed request structure.
- [Bedrock invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) — Inspect what enabling content logging actually sends to CloudWatch and S3.

Notes and exercises: [Observability and tracing](concepts/28-observability.md) · [Reliability and error handling](concepts/32-reliability-and-error-handling.md)

[⬆ Back to top](#table-of-contents)

## Deployment, performance, and cost

- [Bedrock model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html) — Check retirement policy for the exact model, including launch-date-dependent policies.
- [Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) — Review explicit and implicit caching, eligibility, and usage accounting.
- [Bedrock batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html) — Understand the separate asynchronous workload model.
- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) — verify rates and billing modes for the chosen workload.
- [Amazon Bedrock quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) — check capacity constraints and token accounting.

Notes and exercises: [Latency, caching, and batching](concepts/12-latency-caching-batching.md) · [Cost, quotas, and capacity](concepts/33-cost-and-capacity.md) · [Deployment and model lifecycle](concepts/36-deployment-and-lifecycle.md)

[⬆ Back to top](#table-of-contents)

<!-- END CONCEPTS -->

## Further reading

Optional topics to explore when your project calls for them.

<!-- BEGIN MORE -->

- [Fine-tuning and adaptation](concepts/34-fine-tuning-and-adaptation.md)
- [AI-assisted software development](concepts/35-ai-assisted-development.md)

<!-- END MORE -->

## Hands-on labs

- [Local models with Ollama](labs/01-ollama.md): local-only setup, a bounded chat request, and output validation.
- [Amazon Bedrock](labs/02-bedrock.md): model and Region selection, IAM, Converse requests, and failure handling.
- [Orchestration and evaluations](labs/03-orchestration-and-evals.md): a bounded tool loop, authorization checks, and a synthetic evaluation harness.

The Python 3.11+ examples run offline by default. Live labs require explicit setup; Bedrock inference can incur charges. See [verification and limits](docs/verification.md) and the [release checklist](docs/release-checklist.md).

## Contributing

Suggest a useful resource, improve a note, or fix a broken link. Topics are selected for practical value and can be added, merged, or removed as the field changes. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [resource quality policy](docs/resource-policy.md).

## Credits

Inspired by the resource-first format of [36 GraphQL Concepts](https://github.com/Novvum/36-graphql-concepts), started by [@kelseyyim](https://github.com/kelseyyim). Linked resources belong to their authors. See [attribution and licensing status](docs/attribution.md) before reusing or publishing this private review draft.
