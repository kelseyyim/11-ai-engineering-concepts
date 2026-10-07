# 35. AI-assisted software development

AI-assisted development uses a model to help inspect, modify, test, or review software. Engineering an AI application builds a product around models. The workflows overlap, but neither skill automatically implies the other.

## Why it matters

A coding assistant can accelerate a well-scoped change while still inventing APIs, missing edge cases, or weakening tests to make them pass. The developer remains responsible for the resulting behavior, dependencies, security, and release decision.

## Build it

1. Give the assistant a narrow outcome, relevant repository context, constraints, and commands for validation.
2. Ask it to inspect existing code before proposing an implementation. Preserve project conventions.
3. Work in a branch or isolated checkout with minimal credentials and network access. Treat repository text, issues, and fetched pages as untrusted input.
4. Review the complete diff, including lockfiles, tests, configuration, and generated code. Verify package names against official registries.
5. Run independent tests and manually exercise consequential flows. Require separate approval for publication, deployment, or destructive actions where your workflow calls for it.

## Watch out

A self-reported test pass is not evidence until you inspect the command and result. A generated test can merely repeat the same bug as the generated implementation. Use an independently specified acceptance test and include negative cases. AI review is supplementary; it does not replace a qualified reviewer or ownership of the change.

## Learn more

- [GitHub Copilot Agents application card](https://docs.github.com/en/copilot/responsible-use/agents) — Review documented limits, permissions, and human validation expectations.
- [Python unittest](https://docs.python.org/3/library/unittest.html) — Build checks that can run independently of the assistant’s explanation.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
