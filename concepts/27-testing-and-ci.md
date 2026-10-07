# 27. Testing and CI for AI systems

Conventional tests verify application contracts. Model evaluations estimate behavior on sampled tasks. You need both, and they should fail for understandable reasons.

## Why it matters

Network-dependent model calls make unit tests slow, expensive, and flaky. Pure contract tests can verify request construction, parsing, policy gates, retry limits, and state transitions without a model. Live integration tests and task evaluations then test the assumptions mocks cannot establish.

## Build it

1. Inject provider clients so tests use deterministic fakes.
2. Cover malformed output, empty content, truncation, unexpected tool names, bad arguments, refused actions, duplicate calls, and timeouts.
3. Run offline tests on every change. Keep paid integration tests explicitly configured with bounded credentials and spend.
4. Store evaluation artifacts with model, prompt, tool, dataset, and grader versions.
5. Test the grader too: a known-bad fixture should fail. Run this repository’s suite with `python3 -m unittest discover -s tests -v`.

## Watch out

A mock passing proves your assumptions are consistent; it does not prove the provider currently implements those assumptions. A live call succeeding once does not prove the model is reliable. Avoid workflows that expose secrets to untrusted pull requests, automatically grant tool permissions, or silently lower thresholds after a regression.

## Learn more

- [Python unittest](https://docs.python.org/3/library/unittest.html) — Use a zero-dependency unit-test runner and deterministic fixtures.
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — Study task-specific cases, scoring, and continuous evaluation; service APIs are provider-specific.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
