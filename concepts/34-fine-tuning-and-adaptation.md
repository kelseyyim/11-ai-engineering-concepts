# 34. Fine-tuning and adaptation

Fine-tuning changes model parameters using task-specific training examples. It can improve a recurring behavior, format, or domain skill; it introduces a new artifact and a new evaluation obligation.

## Why it matters

If the model is missing current facts, retrieval or a tool often addresses the actual problem. If instructions are ambiguous, improve the specification first. Training on poor labels, sensitive data, or benchmark answers can produce expensive overfitting rather than a useful system.

## Build it

1. Establish a prompting/retrieval baseline and categorize its failures. Decide which failures training could plausibly address.
2. Confirm rights and consent for training data. Create train, development, and held-out splits that avoid near-duplicate leakage.
3. Compare a small adaptation experiment against the baseline on quality, safety, latency, and serving cost.
4. Record base model, tokenizer, training recipe, data provenance, and adapter version.
5. Test out-of-domain behavior and regressions. Keep a rollback path to the unmodified model.

## Watch out

Parameter-efficient methods such as LoRA reduce the number of trained parameters; they do not remove data-governance or serving requirements. An adapter generally depends on a compatible base model. A model can memorize sensitive examples. Do not describe a fine-tuned model as an authoritative knowledge base or assume every provider supports the same training methods.

## Learn more

- [Hugging Face PEFT](https://huggingface.co/docs/peft/index) — Learn parameter-efficient adaptation and the relationship between adapters and base models.
- [TRL supervised fine-tuning](https://huggingface.co/docs/trl/sft_trainer) — Inspect a concrete training workflow, dataset formats, and configuration choices.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
