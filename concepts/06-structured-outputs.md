# 6. Structured outputs and validation

An output schema defines the shape your program can consume. It can constrain syntax and types, but it cannot establish that a claim is true or an action is authorized.

## Why it matters

A JSON parser accepting a response is only the first gate. A generated price can be the wrong number; a source ID can refer to a document the user cannot access. Applications need schema validation, domain checks, and explicit handling of refusal, truncation, and missing values.

## Build it

1. Define a small schema with required fields, enums, length limits, and a deliberate unknown case. Avoid an unconstrained object as your interface.
2. Use the selected provider’s schema-constrained generation feature where supported. Document the supported JSON Schema subset.
3. Parse the response, validate its structure, then check domain invariants: allowed IDs, consistent totals, current permissions, and evidence membership.
4. Return a typed success or failure to the caller. Limit any repair loop and evaluate it as part of the system.
5. Try the [Ollama lab](../labs/01-ollama.md) and deliberately feed its validator malformed output.

## Watch out

JSON mode and schema-constrained output are different features. Neither replaces normal input validation. Do not execute strings with eval, trust self-reported confidence, or accept an extra field named approved as permission. A syntactically valid partial answer is still incomplete if the provider reports a length limit.

## Learn more

- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — Compare JSON output and schema constraints, including refusal handling.
- [JSON Schema reference](https://json-schema.org/understanding-json-schema/reference) — Learn the underlying vocabulary independently of any model provider.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
