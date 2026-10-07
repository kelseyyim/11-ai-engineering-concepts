# 11 AI Engineering Concepts

## Introduction

This repository helps developers learn the core concepts behind AI engineering and build reliable applications with language models. Use it as a guide for further study.

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

### Videos

- 🎥 [(1hr Talk) Intro to Large Language Models - Andrej Karpathy](https://www.youtube.com/watch?v=zjkBMFhNj_g)

**[⬆ Back to Top](#table-of-contents)**

## 2. Prompts and context

### Articles

- 📜 [Prompting best practices - Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- 📜 [Context engineering - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- 📜 [Chat templates - Hugging Face](https://huggingface.co/docs/transformers/en/chat_templating)

### Videos

- 🎥 [Prompting 101 | Code w/ Claude - Anthropic](https://www.youtube.com/watch?v=ysPbXH0LpIE)

**[⬆ Back to Top](#table-of-contents)**

## 3. Structured outputs

### Articles

- 📜 [Structured model outputs - OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs)
- 📜 [Object validation - JSON Schema](https://json-schema.org/understanding-json-schema/reference/object)

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

### Videos

- 🎥 [RAG From Scratch: Part 1 (Overview) - LangChain](https://www.youtube.com/watch?v=wd7TZ4w1mSw)

**[⬆ Back to Top](#table-of-contents)**

## 6. Tools and MCP

### Articles

- 📜 [Writing effective tools - Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- 📜 [Tool-use round trip - Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- 📜 [Build an MCP server - Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server)
- 📜 [MCP security - Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

### Videos

- 🎥 [MCP 201 | Code w/ Claude - Anthropic](https://www.youtube.com/watch?v=HNzH5Us1Rvg)

**[⬆ Back to Top](#table-of-contents)**

## 7. Workflows and agents

### Articles

- 📜 [Building effective agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- 📜 [Graph API - LangGraph](https://docs.langchain.com/oss/python/langgraph/graph-api)
- 📜 [Human approval and resume - LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts)

### Videos

- 🎥 [Building Effective Agents with LangGraph - LangChain](https://www.youtube.com/watch?v=aHCDrAbH_go)

**[⬆ Back to Top](#table-of-contents)**

# Production

## 8. Evaluation

### Articles

- 📜 [Demystifying evals for AI agents - Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### Videos

- 🎥 [Error Analysis: The Highest ROI Technique In AI Engineering - Hamel Husain](https://www.youtube.com/watch?v=e2i6JbU2R-s)

**[⬆ Back to Top](#table-of-contents)**

## 9. Security and privacy

### Articles

- 📜 [Prompt-injection prevention - OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- 📜 [Authorization - OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- 📜 [Model data retention - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)

### Videos

- 🎥 [Prompt Injection, explained - Simon Willison](https://www.youtube.com/watch?v=FgxwCaL6UTA)

**[⬆ Back to Top](#table-of-contents)**

## 10. Reliability and observability

### Articles

- 📜 [Timeouts, retries, backoff, and jitter - AWS Builders’ Library (PDF)](https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf)
- 📜 [Distributed traces - OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/traces/)
- 📜 [Model invocation logging - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)

### Videos

- 🎥 [Getting Started with LangSmith (1/8): Tracing - LangChain](https://www.youtube.com/watch?v=fA9b4D8IsPQ)

**[⬆ Back to Top](#table-of-contents)**

## 11. Deployment and efficiency

### Articles

- 📜 [Model lifecycle - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html)
- 📜 [Prompt caching - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- 📜 [Batch inference jobs - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-create.html)

### Videos

- 🎥 [OpenAI DevDay 2024 | Balancing accuracy, latency, and cost at scale - OpenAI](https://www.youtube.com/watch?v=Bx6sUDRMx-8)

**[⬆ Back to Top](#table-of-contents)**

## Contributors

| [<img src="https://avatars.githubusercontent.com/u/32113193?v=4" width="100" alt="Kelsey Yim"/><br /><sub><b>Kelsey Yim</b></sub>](https://github.com/kelseyyim) |
| :---: |
