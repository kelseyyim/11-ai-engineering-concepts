# 11 AI Engineering Concepts

## Introduction

This repository helps developers learn the core concepts behind AI engineering and build reliable applications with language models. Use it as a guide for further study.

[Build one useful app: the practical AI engineering roadmap](ROADMAP.md)

[AI engineering concepts: practical learning resources](LEARNING-RESOURCES.md)

## Community

Contributions are welcome. Submit a pull request with a useful article, YouTube tutorial, or correction. If you would like to translate this list into your language, you are welcome to contribute a translation.

---

## Table of Contents

### Foundations

1. **[LLM foundations](#1-llm-foundations)**
2. **[Prompts and context](#2-prompts-and-context)**
3. **[Structured outputs](#3-structured-outputs)**

### Building applications

4. **[Running models: Ollama and Bedrock](#4-running-models-ollama-and-bedrock)**
5. **[Retrieval-augmented generation](#5-retrieval-augmented-generation)**
6. **[Tools and MCP](#6-tools-and-mcp)**
7. **[Workflows and agents](#7-workflows-and-agents)**

### Production

8. **[Evaluation](#8-evaluation)**
9. **[Security and privacy](#9-security-and-privacy)**
10. **[Reliability and observability](#10-reliability-and-observability)**
11. **[Deployment and efficiency](#11-deployment-and-efficiency)**

---

# Foundations

## 1. LLM foundations

### Articles

- 📜 [Text generation - Hugging Face](https://huggingface.co/docs/transformers/llm_tutorial)
- 📜 [Byte-pair encoding - Hugging Face](https://huggingface.co/learn/llm-course/en/chapter6/5)
- 📜 [The Illustrated GPT-2 - Jay Alammar](https://jalammar.github.io/illustrated-gpt2/)
  — Visual explanation of decoder-only transformers, masked attention, and next-token prediction through GPT-2.

### Videos

- 🎥 [(1hr Talk) Intro to Large Language Models - Andrej Karpathy](https://www.youtube.com/watch?v=zjkBMFhNj_g)

**[⬆ Back to Top](#table-of-contents)**

## 2. Prompts and context

### Articles

- 📜 [Prompting best practices - Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- 📜 [Context engineering - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- 📜 [Chat templates - Hugging Face](https://huggingface.co/docs/transformers/en/chat_templating)
- 📜 [Context Rot - Kelly Hong, Anton Troynikov, and Jeff Huber](https://www.trychroma.com/research/context-rot)
  — Controlled experiments on context length and distractors, with reproducible code; findings depend on the tested models and tasks.
- 📜 [Context Engineering for AI Agents - Yichao 'Peak' Ji](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
  — Firsthand Manus lessons on stable prompt prefixes, tool availability, and retaining error context for recovery.

### Videos

- 🎥 [Prompting 101 | Code w/ Claude - Anthropic](https://www.youtube.com/watch?v=ysPbXH0LpIE)

**[⬆ Back to Top](#table-of-contents)**

## 3. Structured outputs

### Articles

- 📜 [Structured model outputs - OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs)
- 📜 [Object validation - JSON Schema](https://json-schema.org/understanding-json-schema/reference/object)
- 📜 [Coding for Structured Generation with LLMs - Will Kurt](https://blog.dottxt.ai/coding-for-structured-generation.html)
  — Worked loop for designing regex constraints, validating examples, and inspecting generated data; uses an older Outlines API.

### Videos

- 🎥 [OpenAI DevDay 2024 | Structured outputs for reliable applications - OpenAI](https://www.youtube.com/watch?v=kE4BkATIl9c)

**[⬆ Back to Top](#table-of-contents)**

# Building applications

## 4. Running models: Ollama and Bedrock

### Articles

- 📜 [Local model commands - Ollama](https://docs.ollama.com/cli)
- 📜 [Chat API - Ollama](https://docs.ollama.com/api/chat)
- 📜 [Streaming responses - Ollama](https://docs.ollama.com/api/streaming)
- 📜 [Converse API tutorial - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- 📜 [Running Llama 3.3 70B locally with Ollama - Simon Willison](https://simonwillison.net/2024/Dec/9/llama-33-70b/)
  — His local-model experiment shows Ollama setup, memory pressure on a 64 GB Mac, and checks of model behavior.
- 📜 [A developer's guide to Bedrock's Converse API - Dennis Traub](https://builder.aws.com/content/2dtauBCeDa703x7fDS9Q30MJoBA/amazon-bedrock-converse-api-developer-guide)
  — Worked JavaScript SDK request and response handling; check current model availability and access requirements before using the sample.

### Videos

- 🎥 [4. The Ollama Course - Using the CLI - Matt Williams](https://www.youtube.com/watch?v=luH9j_eOEi4)
- 🎥 [Amazon Bedrock for Beginners - From First Prompt to AI Agent (Full Tutorial) - AWS Developers](https://www.youtube.com/watch?v=FAgmR9VV0GQ)

**[⬆ Back to Top](#table-of-contents)**

## 5. Retrieval-augmented generation

### Articles

- 📜 [Semantic search - Sentence Transformers](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)
- 📜 [Chunking strategies - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html)
- 📜 [Retrieve and rerank - Sentence Transformers](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)
- 📜 [Grounded answers and citations - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html)
- 📜 [How to Build an Open-Domain Question Answering System? - Lilian Weng](https://lilianweng.github.io/posts/2020-10-29-odqa/)
  — Research overview of sparse/dense retrieval and retriever-reader versus retriever-generator designs, including the original RAG formulation.

### Videos

- 🎥 [RAG From Scratch: Part 1 (Overview) - LangChain](https://www.youtube.com/watch?v=wd7TZ4w1mSw)

**[⬆ Back to Top](#table-of-contents)**

## 6. Tools and MCP

### Articles

- 📜 [Writing effective tools - Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- 📜 [Tool-use round trip - Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- 📜 [Build an MCP server - Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server)
- 📜 [MCP security - Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- 📜 [Your MCP Doesn't Need 30 Tools: It Needs Code - Armin Ronacher](https://lucumr.pocoo.org/2025/8/18/code-mcps/)
  — LLDB debugger case study in tool composition, session state, and context overhead; presents the author's design tradeoffs.

### Videos

- 🎥 [MCP 201 | Code w/ Claude - Anthropic](https://www.youtube.com/watch?v=HNzH5Us1Rvg)

**[⬆ Back to Top](#table-of-contents)**

## 7. Workflows and agents

### Articles

- 📜 [Building effective agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- 📜 [Graph API - LangGraph](https://docs.langchain.com/oss/python/langgraph/graph-api)
- 📜 [Human approval and resume - LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts)
- 📜 [How to Build an Agent - Thorsten Ball](https://ampcode.com/notes/how-to-build-an-agent)
  — Educational Go walkthrough of a conversation loop, tool dispatch, and file operations.
- 📜 [LLM Powered Autonomous Agents - Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/)
  — Research map of planning, memory, tool use, and failure modes; examples reflect the 2023 agent landscape.

### Videos

- 🎥 [Building Effective Agents with LangGraph - LangChain](https://www.youtube.com/watch?v=aHCDrAbH_go)

**[⬆ Back to Top](#table-of-contents)**

# Production

## 8. Evaluation

### Articles

- 📜 [Demystifying evals for AI agents - Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- 📜 [Your AI Product Needs Evals - Hamel Husain](https://hamel.dev/blog/posts/evals/index.html)
  — Real-estate assistant case study connecting scoped tests, trace inspection, human review, and model grading.

### Videos

- 🎥 [Error Analysis: The Highest ROI Technique In AI Engineering - Hamel Husain](https://www.youtube.com/watch?v=e2i6JbU2R-s)

**[⬆ Back to Top](#table-of-contents)**

## 9. Security and privacy

### Articles

- 📜 [Prompt-injection prevention - OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- 📜 [Authorization - OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- 📜 [Model data retention - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)
- 📜 [The lethal trifecta for AI agents - Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
  — Threat model and attack examples for agents combining private data, untrusted content, and external communication.

### Videos

- 🎥 [Prompt Injection, explained - Simon Willison](https://www.youtube.com/watch?v=FgxwCaL6UTA)

**[⬆ Back to Top](#table-of-contents)**

## 10. Reliability and observability

### Articles

- 📜 [Timeouts, retries, backoff, and jitter - AWS Builders’ Library (PDF)](https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf)
- 📜 [Distributed traces - OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/traces/)
- 📜 [Model invocation logging - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
- 📜 [Improving LLMs in Production With Observability - Phillip Carter](https://www.honeycomb.io/blog/improving-llms-production-observability)
  — Firsthand Query Assistant case study using traces, errors, token counts, latency, and user feedback to diagnose production behavior.

### Videos

- 🎥 [Getting Started with LangSmith (1/8): Tracing - LangChain](https://www.youtube.com/watch?v=fA9b4D8IsPQ)

**[⬆ Back to Top](#table-of-contents)**

## 11. Deployment and efficiency

### Articles

- 📜 [Model lifecycle - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html)
- 📜 [Prompt caching - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- 📜 [Batch inference jobs - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-create.html)
- 📜 [vLLM and PagedAttention - Woosuk Kwon and Zhuohan Li](https://vllm.ai/blog/2023-06-20-vllm)
  — Explains KV-cache paging, memory sharing, and batching in a serving system; performance results describe the original benchmark setup.

### Videos

- 🎥 [OpenAI DevDay 2024 | Balancing accuracy, latency, and cost at scale - OpenAI](https://www.youtube.com/watch?v=Bx6sUDRMx-8)

**[⬆ Back to Top](#table-of-contents)**

## Contributors

| [<img src="https://avatars.githubusercontent.com/u/32113193?v=4" width="100" alt="Kelsey Yim"/><br /><sub><b>Kelsey Yim</b></sub>](https://github.com/kelseyyim) |
| :---: |
