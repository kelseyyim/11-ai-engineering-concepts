# Lab 1. Make one bounded local Ollama request

**Outcome:** inspect an HTTP request offline, test its boundaries with mocks, then optionally ask your own local model for a small validated JSON object. Python is the transport demonstration, not a requirement of AI engineering. The request, validation, resource limits, and failure handling transfer to other languages.

## Prerequisites and boundaries

- Python 3.11 or newer. The example uses only the standard library.
- For the optional live step only: Ollama installed from its official distribution, enough RAM/disk for your chosen model, and an already-installed local text model.
- Run commands from this repository's root. On Windows, use `py -3.11` instead of `python` if appropriate.
- The lab does not install Ollama, download a model, create an account, use a secret, or contact a paid API. Setup and model acquisition are separate choices. Review the model's license and hardware requirements first.
- Live requests contain your prompt. Use the provided harmless prompt; never test with credentials or private documents.

**Local-only prerequisite:** a loopback URL identifies the server, not where that server runs inference. Configure the Ollama daemon with cloud features disabled and restart it before using `--live`. For a foreground POSIX-shell server that you start yourself, after stopping an existing daemon through its normal controls:

```sh
OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11434 ollama serve
```

For desktop applications or managed services, follow the [official environment configuration instructions](https://docs.ollama.com/faq#how-do-i-configure-ollama-server) instead. Setting an environment variable in the Python terminal does not reconfigure an already-running daemon. Verify the daemon log reports cloud disabled. Do not expose port 11434 publicly. This example cannot independently attest to the daemon's configuration.

## 1. Inspect the offline preview

```sh
python --version
python examples/ollama_chat.py
```

Expect a JSON object with `mode: "offline-preview"`, `network_called: false`, the fixed loopback endpoint, and the proposed request. This is a preview, not a generated answer or evidence that Ollama works.

Read the request: it explicitly disables streaming, requests a schema with `topic` and `summary`, limits generation to 192 tokens, uses a 2,048-token context setting, and asks the daemon to unload the model after completion. The prompt-length limit counts characters, not model tokens; keep prompts short enough for the context budget.

## 2. Run the offline checks

```sh
python -m unittest discover -s tests -p test_ollama_chat.py -v
```

Expect the named tests to end with `OK`. Connections are mocked, including the successful-response test. Coverage includes no-network preview, explicit live model selection, HTTP errors, timeouts, malformed/oversized responses, incomplete generations, schema violations, and local cancellation cleanup. These checks do not establish model quality, hardware compatibility, or actual daemon behavior.

## 3. Optionally request a real local answer

In another terminal, inspect the already-installed models:

```sh
ollama ls
```

Replace `YOUR_INSTALLED_MODEL` below with the exact name of your installed local text model. Do not select a cloud-backed model. If the list is empty, stop here; the offline portion is still useful.

```sh
python examples/ollama_chat.py --live --model YOUR_INSTALLED_MODEL --prompt "Explain an embedding in one sentence." --timeout 30
```

The shape of a successful result is illustrated below; this is an example, not a captured live result:

```json
{
  "mode": "live",
  "schema_validated": true,
  "result": {
    "topic": "Embeddings",
    "summary": "An embedding is a vector representation used to compare or process data."
  }
}
```

Wording will vary. Passing the schema check only establishes field names, types, and length limits. Evaluate accuracy separately. A model can ignore instructions, exhaust its token budget, or produce unusable content.

## 4. Inspect a failure

Use a deliberately nonexistent model name, with local-only mode still enabled:

```sh
python examples/ollama_chat.py --live --model nonexistent-lab-model
```

Normally this yields an HTTP error and a nonzero exit code. No model is automatically downloaded and no automatic retry occurs. A missing daemon instead produces a transport error. Exact server behavior depends on the installed version.

The client fixes the address to `127.0.0.1:11434`, does not follow redirects or use proxy environment settings, caps response bytes at 1 MiB, and limits the request's generation budget. Its socket timeout applies to blocking operations, not total elapsed time. A hard wall-clock limit requires an external supervisor; the example does not claim one.

## Teardown and troubleshooting

- Press Ctrl-C to cancel the client. It closes its connection and exits with code 130; that is not proof the server has stopped computation.
- Inspect `ollama ps`. If your lab model remains loaded, run `ollama stop YOUR_INSTALLED_MODEL` using its exact name. This unloads it rather than deleting its downloaded files.
- If you started a foreground `ollama serve` only for this lab, stop that process normally. Leave unrelated services alone.
- A first request can include model loading time. Inspect memory and daemon logs before deliberately increasing `--timeout` (maximum 120 seconds).
- No local output files are written by the client. Keep the installed model unless you separately choose to remove it.

## Further reading

Source review date: **2026-10-07**.

- [Ollama chat endpoint](https://docs.ollama.com/api/chat): request fields and completion envelope.
- [Structured outputs](https://docs.ollama.com/capabilities/structured-outputs): schema requests and client-side validation.
- [Ollama FAQ](https://docs.ollama.com/faq): local-only mode, daemon configuration, and privacy boundaries.
- [Ollama CLI](https://docs.ollama.com/cli): inspect installed/running models and unload a model.

[Back to the guide](../README.md#table-of-contents)
