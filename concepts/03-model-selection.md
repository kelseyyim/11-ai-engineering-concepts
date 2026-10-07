# 3. Model selection and capability checks

The best model is the one that satisfies your task’s quality floor and operating constraints. A leaderboard rank is a starting hypothesis, not an application acceptance test.

## Why it matters

Capability is multidimensional: language coverage, modality, tool use, schema support, context length, latency, deployment region, license, and hardware requirements. An economical text model can outperform an expensive general model on a tightly specified classification task while failing badly on a tool workflow.

## Build it

1. Write hard constraints first: permitted data locations, acceptable licenses, required API features, and maximum latency.
2. Select two or three eligible candidates, plus the simplest non-model baseline.
3. Run the same representative dataset through each. Record quality by case type, refusals, malformed output, latency distribution, and cost per successful task.
4. Record the exact model identifier or artifact digest and runtime settings. Store the chosen model’s capability checks in code rather than in a hopeful comment.

## Watch out

An instruction-tuned model and its base checkpoint are not drop-in substitutes. A provider adapter cannot invent a missing tool-calling or schema feature. Keep safety-critical and minority cases visible instead of hiding them inside one average score. Re-evaluate after provider migrations or model-tag changes.

## Learn more

- [Hugging Face model cards](https://huggingface.co/docs/hub/model-cards) — Inspect intended uses, limitations, provenance, and licensing.
- [OpenAI evaluation design principles](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Task-specific cases, scoring, and continuous evaluation; check the page's Evals-platform deprecation notice before adopting its service APIs.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
