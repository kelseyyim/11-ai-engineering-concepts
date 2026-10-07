# 24. Multi-agent systems

A multi-agent system coordinates model-driven workers with separate contexts or responsibilities. Adopt it only when coordination produces measurable value over a single agent or fixed workflow.

## Why it matters

Independent research questions can run in parallel, and a specialist can receive a smaller, more relevant context. But delegation adds message traffic, duplicate work, lost information, inconsistent assumptions, and more places to fail. Closely coupled tasks often benefit more from a shared state machine than from a simulated team.

## Build it

1. Establish a single-agent baseline on representative tasks. Compare task success, unsupported claims, elapsed time, total cost, and recovery behavior.
2. Decompose only where boundaries are clear. For a migration assessment, separate workers might inspect API compatibility, database changes, and deployment risks using defined evidence sources.
3. Give each worker an explicit assignment, input context, permitted tools, output schema, budget, and stopping condition. A worker's instructions cannot expand the user's authorization.
4. Have workers return findings, source references, uncertainties, and concrete artifacts. Keep shared facts in an authoritative store instead of relying on repeated conversational summaries.
5. Make one coordinator responsible for deduplication, resolving contradictions, validating artifacts, and deciding whether the overall task is complete. Use bounded delegation depth and concurrency.

Have workers propose side effects through one approval-checking execution path. Concurrent writers need ownership or conflict handling.

## Watch out

Agreement among agents is not independent verification when they share a model, prompt, or faulty source. Adding a reviewer can reproduce the same error. Evaluate the assembled system, including handoff failures and partial worker completion, rather than only each worker in isolation.

**Implementation note:** Anthropic's research system and LangChain's multi-agent patterns illustrate different coordination choices. Their reported benefits and costs are workload-specific; they are not guarantees for your application.

## Learn more

- [Anthropic: Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — examine parallel research, delegation design, and coordination costs in a concrete deployment.
- [LangChain: Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent) — compare specialist subagents, handoffs, and other ways to divide context and control.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
