# 7. Local models with Ollama

## Why it matters

A local inference server separates an application from the machinery that loads model weights and generates tokens. Your application sends a request; the server manages execution. Ollama provides one practical way to explore this boundary. It is a runtime and model-management tool, rather than a single model or a training framework.

Local operation can help you experiment without sending prompts to a hosted inference provider. It also makes hardware, model storage, loading delays, and memory pressure your responsibility. Decide using your actual workload: a small extraction task and a long coding conversation can need very different resources.

## Build it

Follow [the Ollama lab](../labs/01-ollama.md). Start with the offline request preview and mocked tests. When you choose to run live, select an already-installed local model and configure the daemon to disable cloud features. The Python example uses HTTP from the standard library so the transport boundary stays visible. You can implement the same contract in JavaScript, Go, or another language.

Record the model name, artifact identity, Ollama version, context setting, and hardware alongside results. Compare the first request after loading with subsequent requests before drawing latency conclusions. Run a small fixed set of prompts and grade their usefulness yourself. Keep these measurements separate from the client unit tests, which test software behavior using fixtures.

## Watch out

“Localhost” does not establish that inference is local: a daemon can use a cloud-backed model. Check its configuration and the selected model. Keep the service on loopback unless you have deliberately designed access controls.

Available RAM is not identical to downloaded model size. Context and runtime buffers also consume memory. A model that loads successfully may still be unsuitable for your latency or accuracy target. Finally, a valid JSON response is not a verified fact. Treat generated claims as model output and evaluate them accordingly.

## Learn more

- [Ollama FAQ](https://docs.ollama.com/faq): cloud-disable configuration, loopback binding, and memory inspection.
- [Ollama CLI reference](https://docs.ollama.com/cli): model inventory and running-model controls.
- [Chat API](https://docs.ollama.com/api/chat): the application-to-runtime request boundary.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
