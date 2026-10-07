# Verification and limits

## What can be checked offline

The required validation suite uses Python's standard library. It does not install packages, resolve AWS credentials, connect to Ollama, or call a model.

- Provider examples: request construction, dry-run safety, expected response shapes, malformed output, sanitized errors, bounded SDK configuration, and transport cleanup
- Orchestration example: tool allowlist, argument validation, trusted exact-argument approvals, read scope, citation membership, replay handling, call-ID conflicts, and step/tool budgets
- Evaluation harness: ten synthetic cases and a negative test proving a known-bad case fails its grader
- Repository: exactly 36 numbered concepts in six groups, useful chapter sections, reviewed-resource date fields, regenerated README indexes, local paths, and Markdown anchors
- Python source: compilation plus test coverage for documentation tooling

Run all checks with python3 scripts/validate.py from any directory. Individual commands are listed in [CONTRIBUTING.md](../CONTRIBUTING.md).

## Initial build, 2026-10-07

The offline tests, documentation checks, example previews, synthetic evaluation, and compilation were run on Python 3.12.14. Current primary documentation was consulted for the resource list and provider contracts. The committed CI workflow runs the same offline checks on Python 3.11 and 3.12; inspect GitHub Actions for the result on the exact commit you are reviewing.

No live Ollama inference, model download, AWS inference, model subscription, cloud resource provisioning, or paid model-quality evaluation was run as part of this build. Those require suitable hardware or an authorized cloud account and explicit setup.

## External links

The offline link check verifies local paths and anchors. Public source pages were reviewed through a research browser/search interface; that is separate from the optional bulk HTTP checker. Do not describe the entire external URL set as automatically healthy unless a dated --external report supports it. Network restrictions, bot protection, and redirects can require manual review.

## Deliberate boundaries

- The examples are learning implementations, not a production SDK, agent framework, security sandbox, or service deployment.
- The orchestration model is scripted. Passing its fixtures says nothing about a live model's tool selection or answer accuracy.
- Citation membership does not establish factual support.
- Socket/SDK timeouts and token limits do not provide a strict process-level wall-clock deadline.
- In-memory replay protection does not survive process failure or guarantee exactly-once external effects.
- The scripts validate small explicit schemas; they do not implement all of JSON Schema.
- Live provider compatibility and billing remain specific to the selected model, runtime, Region, and account.
