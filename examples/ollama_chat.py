#!/usr/bin/env python3
"""Python 3.11+ transport demo. Offline preview unless --live is explicit.

The caller must first configure the Ollama daemon for local-only operation.
The fixed loopback address alone cannot prevent a daemon from using cloud models.
No SDK, credentials, downloads, automatic retries, redirects, or proxy handling.
"""

from __future__ import annotations

import argparse
import http.client
import json
import math
import sys

HOST = "127.0.0.1"
PORT = 11434
PATH = "/api/chat"
MAX_RESPONSE_BYTES = 1_048_576
MAX_PROMPT_CHARS = 8_000
PLACEHOLDER_MODEL = "YOUR_INSTALLED_MODEL"
SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string", "minLength": 1, "maxLength": 80},
        "summary": {"type": "string", "minLength": 1, "maxLength": 500},
    },
    "required": ["topic", "summary"],
    "additionalProperties": False,
}


class OllamaError(Exception):
    """A failed transport, incomplete generation, or invalid model response."""


def build_payload(model: str, prompt: str) -> dict:
    """Build the same reviewable request in preview and live modes."""
    if not model.strip() or len(model) > 200:
        raise OllamaError("Choose a nonempty model name of at most 200 characters.")
    if not prompt.strip() or len(prompt) > MAX_PROMPT_CHARS:
        raise OllamaError(f"Prompt must contain 1–{MAX_PROMPT_CHARS} characters.")
    return {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Give a concise explanation. Return only JSON matching "
                + json.dumps(SCHEMA, separators=(",", ":")),
            },
            {"role": "user", "content": prompt},
        ],
        "format": SCHEMA,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 192, "num_ctx": 2048},
        "keep_alive": 0,
    }


def parse_response(raw: bytes) -> dict[str, str]:
    """Validate both the API envelope and this example's tiny result schema.

    This is intentionally not a general-purpose JSON Schema implementation.
    Passing validation establishes shape, never factual correctness.
    """
    if len(raw) > MAX_RESPONSE_BYTES:
        raise OllamaError("Response exceeded the 1 MiB limit.")
    try:
        envelope = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        raise OllamaError("Server response was not valid UTF-8 JSON.") from exc
    if not isinstance(envelope, dict) or "error" in envelope:
        raise OllamaError("Server returned an invalid envelope or an API error.")
    if envelope.get("done") is not True:
        raise OllamaError("Generation was incomplete; no result was accepted.")
    if envelope.get("done_reason") == "length":
        raise OllamaError("Generation reached its token limit; no result was accepted.")
    message = envelope.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise OllamaError("Response did not contain a text message.")
    try:
        result = json.loads(message["content"])
    except (ValueError, RecursionError) as exc:
        raise OllamaError("Model content was not valid JSON.") from exc
    if not isinstance(result, dict) or set(result) != {"topic", "summary"}:
        raise OllamaError("Model result must contain exactly topic and summary.")
    for key, maximum in (("topic", 80), ("summary", 500)):
        value = result[key]
        if not isinstance(value, str) or not value.strip() or len(value) > maximum:
            raise OllamaError(f"Model result has an invalid {key} field.")
    return result


def chat(model: str, prompt: str, timeout: float = 30.0) -> dict[str, str]:
    """Make one local request. Timeout bounds blocking socket operations.

    It is not an absolute wall-clock deadline. Token and response-size limits
    provide additional bounds; callers needing a hard deadline need a supervisor.
    """
    if not math.isfinite(timeout) or not 1 <= timeout <= 120:
        raise OllamaError("Timeout must be a finite value between 1 and 120 seconds.")
    payload = build_payload(model, prompt)
    connection = http.client.HTTPConnection(HOST, PORT, timeout=timeout)
    response = None
    try:
        connection.request(
            "POST", PATH, body=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        response = connection.getresponse()
        if response.status != 200:
            hint = " Check the installed model name with 'ollama ls'." if response.status == 404 else ""
            raise OllamaError(f"Ollama returned HTTP {response.status}.{hint}")
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        return parse_response(raw)
    except (OSError, http.client.HTTPException) as exc:
        raise OllamaError(
            "Local request failed or timed out. Check the daemon, model, and available memory."
        ) from exc
    finally:
        if response is not None:
            response.close()
        connection.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Send one request to local Ollama")
    parser.add_argument("--model", default=PLACEHOLDER_MODEL, help="Exact installed LOCAL model name")
    parser.add_argument("--prompt", default="Explain an embedding in one sentence.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Socket-operation timeout, 1–120 seconds")
    args = parser.parse_args(argv)
    try:
        payload = build_payload(args.model, args.prompt)
        if not args.live:
            output = {
                "mode": "offline-preview",
                "network_called": False,
                "endpoint": f"http://{HOST}:{PORT}{PATH}",
                "request": payload,
            }
        else:
            if args.model == PLACEHOLDER_MODEL:
                raise OllamaError("Live mode requires --model with an installed local model name.")
            result = chat(args.model, args.prompt, args.timeout)
            output = {"mode": "live", "schema_validated": True, "result": result}
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except OllamaError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Cancelled locally; check the daemon if generation is still running.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
