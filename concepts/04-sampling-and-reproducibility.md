# 4. Sampling and reproducibility

Decoding decides how the next token is selected from the model’s distribution. Temperature, top-p, top-k, output limits, and stop sequences influence that process when the selected model and API support them.

## Why it matters

Reducing randomness may stabilize outputs, but it cannot make an incorrect premise true. Reproducibility also depends on weights, tokenizer, chat template, runtime, hardware, provider behavior, and input ordering. A fixed seed is useful experimental metadata, not a universal promise of identical responses.

## Build it

1. Freeze a prompt, model version, and input set.
2. Repeat each case several times with a small set of supported decoding configurations. Change one parameter at a time.
3. Measure task success and variation, including format errors and truncation. Do not compare only a favorite example.
4. Record the configuration with the evaluation result. Keep strict assertions for deterministic application code; use justified thresholds and repeated trials for model behavior.

## Watch out

Parameter names and accepted ranges differ across providers. Some reasoning models restrict sampling controls. Do not send unsupported defaults through a universal adapter. Higher temperature is not a reliable synonym for creativity or quality, and zero temperature does not establish correctness. Retrying until a test passes conceals instability.

## Learn more

- [Transformers generation strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies) — Compare greedy decoding and sampling; use the version matching your installation.
- [Transformers text generation](https://huggingface.co/docs/transformers/llm_tutorial) — Follow the inference path from tokenization to generated tokens.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
