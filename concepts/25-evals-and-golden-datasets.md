# 25. Evaluations and golden datasets

An evaluation is a repeatable way to compare a system’s behavior against an explicit task goal. A golden dataset contains reviewed examples and expected outcomes or scoring criteria.

## Why it matters

Without stable cases, a prompt change can look better simply because the latest demo was easier. Good evaluation separates common cases, important edge cases, unsafe behavior, and operating cost. It also defines the baseline and release criteria before looking at the result.

## Build it

1. Write the user-visible outcome and a rubric. Prefer executable checks where possible.
2. Collect representative, permissioned or synthetic cases. Label provenance and separate development examples from a held-out set.
3. Include failures: ambiguity, no evidence, hostile content, tool errors, and unsupported requests.
4. Run repeated trials when model variability matters. Report denominators and results by case type.
5. Inspect failures, add independently reviewed cases, and re-run the baseline. Use a model grader only after comparing it with human judgments.

## Watch out

Tiny fixture suites teach the mechanics but cannot establish production quality. A model judging its own prose can favor style over correctness. Avoid leakage from the evaluation set into prompts or training. If you tune a release against the same held-out set repeatedly, it is no longer truly held out.

## Learn more

- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Study task-specific cases, scoring, and continuous evaluation; service APIs are provider-specific.
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Distinguish tasks, trials, graders, transcripts, and outcomes.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
