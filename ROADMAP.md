# AI engineering roadmap: build one useful app

Build one documentation assistant that answers from a small set of public docs and shows its evidence. Work through the 11 stages below; keep each improvement only when you can measure it.

This is a project plan, not a tested starter application. The linked 11-concept library supplies deeper articles and videos for each stage.

## What you need

- Basic JavaScript or Python, Git, and a small repository for your app.
- Five to ten public documentation pages you are allowed to reuse. Keep private files out of this learning project.
- One model runtime. Use existing access; choose your own spending limit before making paid API calls.
- A simple results sheet: question, expected evidence, answer, pass/fail, latency and usage.

## 1. LLM foundations

Run five questions through one model. Repeat them and note changed answers, missing knowledge and token usage.

**Checkpoint:** Keep a baseline of inputs, outputs and expected facts. Explain why a fluent answer can still be wrong.

[Study resources](README.md#1-llm-foundations)

## 2. Prompts and context

Write one task instruction with an explicit audience, output format and “not enough evidence” response. Compare it with your baseline using the same questions.

**Checkpoint:** Keep the simpler prompt unless the comparison shows an improvement. Treat retrieved text as evidence, never as instructions.

[Study resources](README.md#2-prompts-and-context)

## 3. Structured outputs

Request an object with answer, evidence IDs and an insufficient-evidence flag. Validate its shape in your application and handle refusal or incomplete output.

**Checkpoint:** Reject invalid results before using them. A valid schema does not prove that an answer or citation is correct.

[Study resources](README.md#3-structured-outputs)

## 4. Running models: Ollama and Bedrock

Choose one route: a local Ollama model that fits your machine, or Bedrock with an existing approved AWS account. Run the same baseline; record model/version, latency and usage.

**Checkpoint:** Make one request succeed and one failure understandable. Keep provider credentials on the server; do not buy capacity or add another provider just for this exercise.

[Study resources](README.md#4-running-models-ollama-and-bedrock)

## 5. Retrieval-augmented generation

Index a small set of public docs. Store document URL, section and chunk ID; retrieve passages before answering. Start with simple retrieval, then test chunking or reranking only when misses justify it.

**Checkpoint:** For each answer, open the cited passage and check it supports the claim. Include questions the docs cannot answer; the app should say so.

[Study resources](README.md#5-retrieval-augmented-generation)

## 6. Tools and MCP

Add one read-only tool that looks up an approved document by ID. Validate arguments and enforce an allowlist in code. Wrap it in MCP if you need a standard interface between clients and tools.

**Checkpoint:** Reject unknown IDs and unauthorized requests without calling the tool. Require explicit approval before any future write action; a model request is not permission.

[Study resources](README.md#6-tools-and-mcp)

## 7. Workflows and agents

Use a fixed sequence: retrieve, answer, validate. Add an agent loop only for a task that actually needs flexible tool choice. Bound tool calls, elapsed time and spending.

**Checkpoint:** Stop cleanly when the limit is reached. Show a useful partial result or failure rather than retrying forever.

[Study resources](README.md#7-workflows-and-agents)

## 8. Evaluation

Expand the baseline to 20 questions: ordinary, ambiguous, unanswerable and adversarial. Set aside a small held-out set before tuning. Track factual support, source accuracy and correct abstention separately.

**Checkpoint:** Compare each change against the same baseline. Inspect failures by category; do not hide a security failure inside an average score. Twenty cases are a learning starting point, not launch certification.

[Study resources](README.md#8-evaluation)

## 9. Security and privacy

Use public sample documents only. Test a passage that tells the assistant to reveal secrets or ignore instructions. Enforce authorization in the server before retrieval and tool execution; redact sensitive logs.

**Checkpoint:** Verify that denied requests return no private content. Prompt wording is one defense, not the access-control boundary.

[Study resources](README.md#9-security-and-privacy)

## 10. Reliability and observability

Add request IDs, timeouts and bounded retries with backoff for transient failures. Retry only when safe; prevent duplicate side effects. Record latency, failures, tool calls and token usage without storing full prompts by default.

**Checkpoint:** Simulate a timeout and rate limit. Confirm the request ends, the user gets a clear message and logs explain where it failed.

[Study resources](README.md#10-reliability-and-observability)

## 11. Deployment and efficiency

Deploy a small preview with server-side secrets, a usage cap and a pinned model/configuration. Re-run your held-out checks. Compare a cheaper model or caching only after quality is measured.

**Checkpoint:** Write down the quality target, p95 latency, usage/cost estimate and known failures. Release only when your chosen targets and all access-control checks pass.

[Study resources](README.md#11-deployment-and-efficiency)

## If you get stuck

- Wrong answers with good retrieval: inspect the prompt and cited claims. Missing evidence: fix retrieval before changing the model.
- Valid JSON but bad facts: schema validation and factual evaluation are separate checks.
- Too many tool calls: return to a fixed workflow and lower the step limit.
- High latency or cost: measure the slow or expensive step first, then test one smaller model, shorter context or cache change at a time.

## Primary references

- [OpenAI: structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Anthropic: building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Sentence Transformers: retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)
- [OWASP: prompt injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [Anthropic: demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

Reference review: October 8, 2026. Exercises are proposed learning tasks; no application implementation or benchmark results are claimed.
