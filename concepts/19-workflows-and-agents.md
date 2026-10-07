# 19. Workflows versus agents

A workflow follows application-defined transitions. An agent uses a model to choose some of its next actions. Both need explicit state, bounded execution, and an owner for failures. Most useful systems combine the two.

## Why it matters

Choosing the right control flow makes failures easier to reproduce. Invoice extraction usually benefits from a predictable pipeline: parse, validate, request missing fields, then save. Investigating an unfamiliar build failure may require an agent to decide which logs or files to inspect next. Neither task improves merely by adding more model calls.

## Build it

1. Start with a single call and a deterministic validator. Add a second step only when evaluations show a specific failure it can address.
2. Define a state object containing the task ID, validated inputs, evidence references, attempt counters, pending approvals, and outcome. Keep credentials outside model-visible state.
3. Draw allowed transitions before writing prompts. For example: `received → extracted → validated → awaiting_approval → committed`. Give errors and cancellation their own transitions.
4. Put model discretion inside a bounded region: it may inspect three additional documents, but cannot bypass validation or grant itself permission to save.
5. Set limits on elapsed time, cost, tool calls, and repeated failures. When a limit is reached, return useful partial work and an explicit unresolved status.

## Watch out

A conversation transcript is not a complete execution record. Store what actually happened, not just what the model said it would do. An elegant graph also does not prove that its branches terminate or preserve invariants; test loops, missing inputs, cancellation, and denied approvals.

**Framework note:** LangGraph represents state, work, and transitions with graph primitives. The same design can be implemented with ordinary application code or another workflow engine.

## Learn more

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — distinguish predefined workflows from model-directed loops and choose the simplest useful pattern.
- [LangGraph: Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) — learn explicit state, nodes, conditional edges, and execution limits.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
