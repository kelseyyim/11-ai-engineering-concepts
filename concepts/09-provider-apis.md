# 9. Provider APIs and adapters

## Why it matters

A provider API is the contract between your application and an inference service. That contract includes request fields, authentication, response structure, error handling, limits, and lifecycle behavior. An SDK makes calls convenient, but the underlying responsibilities remain yours.

An “OpenAI-compatible” endpoint implements some familiar interface; it does not automatically reproduce every endpoint, option, response event, or model behavior. Ollama explicitly documents compatibility as a subset. Treat migration as a tested integration change rather than replacing a hostname and hoping for equivalence.

## Build it

Begin with [the local HTTP lab](../labs/01-ollama.md). Its payload builder, transport function, and result validator are distinct. Python is used to expose the mechanics without additional dependencies; this design also works in other languages.

Write a narrow application-facing adapter, for example “summarize this text into our two-field result.” Inside it, translate provider-specific request fields and normalize the response. Preserve useful diagnostics such as model identity, finish reason, usage, and request identifiers when available. Do not erase every provider difference behind an unrealistically universal interface.

Test the adapter with recorded or synthetic fixtures for success, authentication failure, rate limits, truncated output, invalid JSON, and network loss. Add a separate, explicitly enabled integration test for a real provider. A mocked response only validates your handling of that fixture.

Before using a hosted service, decide what data may leave the application, where credentials belong, how much a request can spend, and who can approve changes. The local lab neither obtains credentials nor calls a hosted provider.

## Watch out

Retry policies can multiply load and cost. A timeout may mean the client stopped waiting while the service kept working. Avoid unlimited retries and check the provider's idempotency guarantees before retrying operations with side effects.

Check errors inside the response as well as HTTP status. Streaming failures can arrive after a successful status line. Keep logs useful without copying sensitive prompts or secrets into them.

## Learn more

- [Ollama compatibility reference](https://docs.ollama.com/api/openai-compatibility): supported interfaces and compatibility boundaries.
- [Native chat endpoint](https://docs.ollama.com/api/chat): a concrete provider-specific request/response contract.
- [Ollama API errors](https://docs.ollama.com/api/errors): status codes and errors within streamed responses.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
