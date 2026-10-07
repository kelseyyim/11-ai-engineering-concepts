# 23. Durable execution and human approval

Durable execution preserves enough state to continue useful work after a worker crashes, a deployment restarts, or a person takes hours to approve a step. It does not automatically make external side effects happen exactly once.

## Why it matters

Consider a report workflow that gathers evidence, waits for approval, and sends a message. Restarting from the beginning wastes work. Restarting immediately before sending can duplicate the message if the first send succeeded but its acknowledgment was lost. Persistence and side-effect reconciliation solve different parts of this problem.

## Build it

1. Assign a stable workflow ID and persist meaningful transitions, validated inputs, artifact references, pending approvals, and external operation IDs.
2. Isolate nondeterministic work such as model calls, network requests, timestamps, and random choices. Save results at boundaries that your runtime can replay or resume correctly.
3. Give each logical write a stable idempotency key when the destination supports it. Otherwise record intent and reconcile the destination's state before retrying an uncertain operation.
4. Persist approval for the exact action and target. On resume, recheck permissions and whether approved details have materially changed.
5. Inject failures before execution, after the external side effect, and before checkpoint completion. Verify recovery, cancellation, duplicate suppression, and terminal status.

Version workflow history and set retention limits for sensitive state.

## Watch out

An in-memory checkpointer cannot survive process loss. A saved transcript cannot prove that an external write completed. Replaying a model call can produce different output, so do not treat it as a deterministic calculation.

**Framework note:** LangGraph offers persistent checkpointers and different durability modes. Its interrupts may re-execute code before the pause. Temporal similarly requires careful Activity design and idempotency; neither removes the need to reason about external systems.

## Learn more

- [LangGraph: Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers) — inspect persisted state and understand durability tradeoffs.
- [LangGraph: Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) — learn pause/resume behavior and why pre-interrupt side effects need care.
- [Temporal: Activity definition](https://docs.temporal.io/activity-definition) — understand retryable execution and idempotent Activities.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
