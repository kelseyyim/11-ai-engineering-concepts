# 2. Tokens and context windows

Tokens are the units a model consumes and produces. A context window limits the information available to an inference request; useful context can be much smaller than the advertised maximum.

## Why it matters

Your budget includes instructions, tool definitions, retrieved passages, message history, formatting overhead, and output allowances. Counting words or characters is only a rough heuristic. Different tokenizers handle source code, languages, punctuation, and identifiers differently. Some APIs account for reasoning tokens separately; inspect the selected model’s contract.

## Build it

1. Build a request-budget report with separate buckets for instructions, history, tools, evidence, and reserved output.
2. Use the provider’s token counting feature or the exact local tokenizer when possible. If only an estimate is available, label it and keep a margin.
3. Define what gets removed first when the budget is exceeded. Preserve the latest user request and mandatory policy.
4. Add a test where the relevant fact appears at the end of a long document. Check whether truncation drops it.

## Watch out

Do not silently clip arbitrary JSON, tool results, or code. Truncation can erase the very evidence required to answer. A larger window also consumes memory, money, and time; it does not guarantee accurate use of every included fact. Inspect stop reasons when output reaches its cap.

## Learn more

- [Hugging Face BPE tokenization](https://huggingface.co/learn/llm-course/en/chapter6/5) — See why tokens are not interchangeable with words.
- [Transformers padding and truncation](https://huggingface.co/docs/transformers/main/en/pad_truncation) — Understand explicit length handling and truncation strategies.
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Study context selection and compaction as explicit engineering choices.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
