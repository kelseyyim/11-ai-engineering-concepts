# 20. Tool calling and contracts

Tool calling lets a model propose a named operation with structured arguments. Trusted application code decides whether that proposal is valid, authorized, and safe to execute. Producing well-formed JSON is not permission.

## Why it matters

Tools connect language to real data and side effects. A shipping assistant can retrieve delivery status or change an address, so a mistaken argument can become a real-world mistake.

## Build it

1. Define narrow operations such as `get_delivery_status(order_id)` instead of a generic `execute_request(url, body)`. Describe when to use each tool, its inputs, and its failure modes.
2. Validate arguments against a schema, then validate business rules. An order ID can be syntactically valid but belong to another customer. Derive tenant and actor identity from authenticated application context, never model-provided fields.
3. Check the proposed action against trusted authorization. For side effects, require approval covering the target and change unless an applicable policy already authorizes them.
4. Execute through a controlled handler with deadlines and an operation identifier. Deduplicate retries when the operation can change external state.
5. Return a compact, typed result: status, relevant facts, stable resource IDs, and actionable errors. Associate it with the originating call and let the model explain the result.

Test missing arguments, stale records, unauthorized targets, timeouts, and duplicate proposals. Measure task completion and incorrect actions, not just schema validity.

## Watch out

Tool outputs remain data: a retrieved document cannot authorize another tool call. Avoid returning secrets or huge raw responses. Parallel calls are appropriate only when their dependencies and side effects permit it; an update that depends on a lookup must wait.

**Provider note:** Claude distinguishes client tools, which your application executes, from server tools executed by Anthropic. Message formats and execution responsibility differ across providers; keep authorization in your integration layer.

## Learn more

- [Anthropic: Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents) — design clear interfaces and evaluate tool usability on realistic tasks.
- [Claude: Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — follow a provider-specific tool request/result cycle and understand execution responsibility.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
