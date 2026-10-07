#!/usr/bin/env python3
"""Offline orchestration teaching example, NOT a production agent or sandbox.

A scripted model emits proposals. Trusted application code validates and permits
operations. The only write is an in-memory note, never disk or network. No imports
of provider SDKs, API calls, subprocesses, or model downloads.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

CORPUS = {
    "ollama": "Ollama can serve local models. Localhost alone does not prove inference stays local.",
    "bedrock": "Bedrock inference requires an eligible model, Region, IAM permissions, and billing approval.",
    "tools": "A model proposes a tool call. Trusted application code validates and authorizes it.",
}


class ContractError(ValueError):
    pass


def fingerprint(name: str, arguments: dict[str, Any]) -> str:
    """Bind a trusted approval to exact operation content, not model prose."""
    raw = json.dumps([name, arguments], sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def bounded_text(value: Any, maximum: int) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= maximum


@dataclass(frozen=True)
class Policy:
    readable_ids: frozenset[str] = frozenset(CORPUS)
    approved_writes: frozenset[str] = frozenset()
    max_steps: int = 4
    max_tool_calls: int = 2

    def __post_init__(self) -> None:
        for value in (self.max_steps, self.max_tool_calls):
            if type(value) is not int or not 1 <= value <= 20:
                raise ValueError("Budgets must be integers from 1 through 20.")


@dataclass
class Result:
    status: str
    answer: str = ""
    citations: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    reason: str = ""


def run(model: Callable[[list[dict]], dict], policy: Policy = Policy()) -> Result:
    """Run a bounded proposal loop; model must be a trusted callable for this lab.

    In-memory deduplication works ONLY inside one invocation. It does not survive
    crashes, prove exactly-once delivery, or provide a production approval system.
    """
    history: list[dict] = []
    observed: set[str] = set()
    calls: dict[str, tuple[str, dict]] = {}
    result = Result(status="exhausted")
    tool_count = 0
    for step in range(policy.max_steps):
        try:
            proposal = model(json.loads(json.dumps(history)))
            if not isinstance(proposal, dict):
                raise ContractError("Proposal must be an object.")
            if proposal.get("type") == "final":
                if set(proposal) != {"type", "answer", "citations", "abstain"}:
                    raise ContractError("Final output has unexpected or missing fields.")
                cites = proposal["citations"]
                if not bounded_text(proposal["answer"], 1000) or type(proposal["abstain"]) is not bool:
                    raise ContractError("Invalid final answer or abstention flag.")
                if not isinstance(cites, list) or not all(isinstance(x, str) for x in cites):
                    raise ContractError("Citations must be a list of source IDs.")
                if len(cites) != len(set(cites)) or not set(cites) <= observed:
                    raise ContractError("Citations must be unique IDs actually retrieved in this run.")
                if proposal["abstain"] and cites:
                    raise ContractError("This lab's abstention contract requires no citations.")
                if not proposal["abstain"] and not cites:
                    raise ContractError("A non-abstaining answer needs retrieved evidence.")
                result.status = "abstained" if proposal["abstain"] else "completed"
                result.answer, result.citations = proposal["answer"], cites
                result.trace.append({"step": step + 1, "event": result.status})
                return result
            if proposal.get("type") != "tool_call" or set(proposal) != {"type", "id", "name", "arguments"}:
                raise ContractError("Invalid tool proposal fields.")
            call_id, name, arguments = proposal["id"], proposal["name"], proposal["arguments"]
            if not bounded_text(call_id, 80) or not isinstance(name, str) or not isinstance(arguments, dict):
                raise ContractError("Invalid tool identity or arguments.")
            if name not in {"get_concept", "store_note"}:
                result.status, result.reason = "denied", "Tool is not allowlisted."
                return result
            expected = "concept_id" if name == "get_concept" else "text"
            if set(arguments) != {expected} or not bounded_text(arguments[expected], 256):
                raise ContractError("Tool arguments do not match the contract.")
            digest = fingerprint(name, arguments)
            if call_id in calls:
                old_digest, output = calls[call_id]
                if old_digest != digest:
                    raise ContractError("A call ID was reused with different content.")
                result.trace.append({"step": step + 1, "event": "replayed", "tool": name, "call_id": call_id})
            else:
                if tool_count >= policy.max_tool_calls:
                    result.reason = "Tool-call budget reached."
                    return result
                if name == "get_concept":
                    concept_id = arguments["concept_id"]
                    if concept_id not in policy.readable_ids:
                        result.status, result.reason = "denied", "Source is outside readable scope."
                        return result
                    if concept_id not in CORPUS:
                        raise ContractError("Unknown concept ID.")
                    output = {"source_id": concept_id, "text": CORPUS[concept_id]}
                    observed.add(concept_id)
                else:
                    if digest not in policy.approved_writes:
                        result.status, result.reason = "denied", "Write requires trusted approval for these exact arguments."
                        return result
                    result.notes.append(arguments["text"])
                    output = {"stored": True, "storage": "in-memory-demo-only"}
                tool_count += 1
                calls[call_id] = (digest, output)
                result.trace.append({"step": step + 1, "event": "tool_completed", "tool": name, "call_id": call_id})
            history.append({"proposal": proposal, "tool_result": output})
        except (ContractError, StopIteration):
            result.status, result.reason = "invalid", "The proposal or scripted sequence violated the lab contract."
            return result
        except Exception:
            # Provider/tool exception text can contain secrets; keep the demo CLI sanitized.
            result.status, result.reason = "failed", "A model or tool failed; raw details withheld."
            return result
    result.reason = "Step budget reached."
    return result


def scripted(actions: list[dict]) -> Callable[[list[dict]], dict]:
    """A deterministic stand-in, not an LLM or a quality demonstration."""
    sequence = iter(actions)
    return lambda _history: next(sequence)


def evaluate(cases: list[dict]) -> dict:
    if not cases:
        raise ValueError("An empty evaluation is not a passing evaluation.")
    outcomes = []
    for case in cases:
        result = run(scripted(case["actions"]))
        checks = {
            "status": result.status == case["expected_status"],
            "citations": result.citations == case.get("expected_citations", []),
            "no_writes": result.notes == [],
        }
        outcomes.append({"id": case["id"], "passed": all(checks.values()), "checks": checks, "status": result.status})
    return {"mode": "offline-contract-fixtures", "cases": len(cases),
            "passed": sum(x["passed"] for x in outcomes), "results": outcomes}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval", action="store_true", help="Run synthetic contract cases")
    args = parser.parse_args()
    if args.eval:
        cases = json.loads((Path(__file__).parent / "eval_cases.json").read_text())
        report = evaluate(cases)
        print(json.dumps(report, indent=2))
        return 0 if report["passed"] == report["cases"] else 1
    result = run(scripted([
        {"type": "tool_call", "id": "read-1", "name": "get_concept", "arguments": {"concept_id": "tools"}},
        {"type": "final", "answer": "Application code validates and authorizes tool calls.", "citations": ["tools"], "abstain": False},
    ]))
    print(json.dumps(asdict(result), indent=2))
    return 0 if result.status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
