# Lab 3: A bounded tool loop and an evaluation harness

**Goal:** understand the control flow between a model proposal and trusted execution. Then test that flow with repeatable cases, including cases that should fail.

**Prerequisites:** Python 3.11+, a terminal, and this repository. No models, packages, accounts, credentials, network calls, or payment are needed.

**Related concepts:** [workflows](../concepts/19-workflows-and-agents.md), [tool contracts](../concepts/20-tool-calling.md), [evaluation](../concepts/25-evals-and-golden-datasets.md), and [permissions](../concepts/30-permissions-and-sandboxing.md).

## 1. Read the boundary

Open [bounded_agent.py](../examples/bounded_agent.py). A scripted function stands in for a model. It can propose either:

- A tool call: type, ID, tool name, and arguments
- A final answer: type, answer, citation IDs, and an abstention flag

The trusted loop performs schema checks and a tool allowlist check. It applies its own read scope or write approval before executing. Neither the model's answer nor an extra field such as approved can grant permission.

The source corpus is three synthetic paragraphs. The only available write appends a note to an in-memory list. No actual storage service, shell, filesystem writer, or external communication is exposed.

## 2. Run a successful trace

From the repository root:

```sh
python3 examples/bounded_agent.py
```

Expected properties:

```json
{
  "status": "completed",
  "citations": ["tools"],
  "notes": []
}
```

The full output also contains the answer and a trace: one completed tool call followed by a completed final response. The final citation must refer to evidence retrieved in that run.

**Important:** citation membership is not evidence entailment. This validator can reject a fabricated source ID, but it cannot prove that every claim is supported by the cited paragraph.

## 3. Run the evaluation fixtures

```sh
python3 examples/bounded_agent.py --eval
python3 -m unittest discover -s tests -p 'test_bounded_agent.py' -v
```

The evaluation report identifies its mode as offline-contract-fixtures. It includes 10 cases: a normal answer, abstention, fabricated citation, missing evidence, unapproved write, unknown tool, malformed arguments, replayed read, bounded loop, and call-ID collision.

The evaluator checks terminal status, citations, and absence of writes. A refused unauthorized write is a passing safety case. This is why “did the task return completed?” cannot be your only score.

The unit tests also deliberately give the grader a known-bad case and verify it fails. A grader that always returns success would make a very reassuring, very useless dashboard.

## 4. Inspect approval and replay behavior

The tests show trusted approval built outside the scripted model. Approval is bound to the exact tool name and canonical arguments. Changing the note text invalidates that approval.

Repeated calls with the same ID and same arguments reuse the earlier result. Reusing an ID with different arguments fails. Step and tool-call budgets cap the loop. Read permissions are checked before returning a source.

These choices teach interface boundaries, but they are deliberately incomplete production infrastructure:

- Approval fingerprints are not authentication or cryptographic signatures. A real approval record needs an authenticated actor, scope, expiry, revocation, and durable storage.
- Deduplication lasts for only one in-memory run. External effects need durable operation IDs and service-side idempotency or reconciliation.
- The synchronous callable must return. There is no hard wall-clock deadline, process sandbox, concurrent execution, or network isolation layer here.
- Two different call IDs with the same approved arguments are two separate operations. This is not a single-use approval system.

## 5. Extend it deliberately

A useful next exercise is to replace the scripted function with an adapter to the [Ollama client](../examples/ollama_chat.py) or [Bedrock client](../examples/bedrock_chat.py). That requires designing a compatible output schema, preserving trusted policy outside the prompt, and handling provider-specific responses. The samples are not already wired together.

Before enabling a real model, add independent labeled cases for tool choice and argument accuracy. Before enabling any external write, add a durable approval flow and idempotency tests. Record model, prompt, schema, dataset, and grader versions alongside every evaluation.

## Teardown

The lab stores nothing persistently. Exiting the process discards notes and replay state. Python may create normal __pycache__ files; these are ignored by Git.

## What this lab proves

It demonstrates and tests a deterministic contract. It does not measure an actual model's reasoning, a production retrieval system, or resistance to arbitrary adversarial inputs. Keep those claims separate when reporting your own results.
