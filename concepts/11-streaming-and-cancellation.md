# 11. Streaming and cancellation

## Why it matters

Streaming delivers incremental output while generation is underway. It can improve perceived responsiveness without making the entire task finish sooner. Measure time to first useful content separately from time to a complete, validated result.

The transport is also part of the contract. Ollama's native streaming API uses newline-delimited JSON. A network read is not necessarily one JSON object: one object can span reads, and a read can contain several objects. Preserve a buffer and parse according to protocol boundaries.

## Build it

Start with [the Ollama lab](../labs/01-ollama.md), which deliberately requests one non-streaming JSON response. Its validation step gives you a clear completion boundary. As an extension, design a streaming reader that accumulates complete newline-delimited records, checks each record for errors, and combines content until a terminal completion record arrives.

Test that parser offline first. Feed it split records, multiple records in one chunk, split UTF-8 characters, an error after partial content, and an unexpected end of connection. Bound buffered bytes and reject an overlong record. Do not parse partial structured output as a finished result.

Design cancellation as an end-to-end path: the interface stops showing progress, the application stops reading, the connection closes, and server-side work is checked or cancelled through supported behavior. Preserve a distinct “cancelled” state rather than marking partial content successful. The Python lab closes its connection on Ctrl-C; it does not verify that server computation has stopped.

## Watch out

HTTP 200 does not guarantee a successful stream. Ollama can emit an error object after streaming has begun, when the HTTP status can no longer change. A closed socket without the required terminal event is also incomplete.

Timeouts need precise names. A socket-operation timeout is not a total deadline, and a UI cancel action is not proof that usage or billing stopped. Avoid promising either unless the specific service confirms it. Keep provisional text visually separate from validated structured data.

## Learn more

- [Ollama streaming guide](https://docs.ollama.com/api/streaming): NDJSON framing and non-streaming requests.
- [Ollama error behavior](https://docs.ollama.com/api/errors): failures after a stream has started.
- [Python HTTP client documentation](https://docs.python.org/3.11/library/http.client.html): response reading and connection lifecycle.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
