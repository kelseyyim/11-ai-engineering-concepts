"""Offline tests: every HTTP connection is mocked; no Ollama is required."""

import contextlib
from http.client import RemoteDisconnected
import io
import json
import unittest
from unittest.mock import patch

from examples import ollama_chat as client


def envelope(content=None, **overrides):
    result = {"topic": "Embeddings", "summary": "Vectors representing useful features."}
    data = {
        "message": {"content": json.dumps(result) if content is None else content},
        "done": True,
        "done_reason": "stop",
    }
    data.update(overrides)
    return json.dumps(data).encode("utf-8")


class OllamaClientTests(unittest.TestCase):
    def test_default_is_offline_preview(self):
        with patch.object(client.http.client, "HTTPConnection") as http, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(client.main([]), 0)
        http.assert_not_called()
        value = json.loads(out.getvalue())
        self.assertEqual(value["mode"], "offline-preview")
        self.assertIs(value["network_called"], False)

    def test_live_requires_explicit_model(self):
        with patch.object(client.http.client, "HTTPConnection") as http, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(client.main(["--live"]), 1)
        http.assert_not_called()

    def test_payload_is_bounded_and_nonstreaming(self):
        payload = client.build_payload("fixture-model", "Explain a token.")
        self.assertIs(payload["stream"], False)
        self.assertEqual(payload["keep_alive"], 0)
        self.assertEqual(payload["options"]["num_predict"], 192)
        self.assertEqual(payload["format"], client.SCHEMA)

    def test_bad_inputs_rejected(self):
        for model, prompt in (("", "x"), ("x" * 201, "x"), ("m", " "), ("m", "x" * 8001)):
            with self.subTest(model=model[:10], length=len(prompt)), self.assertRaises(client.OllamaError):
                client.build_payload(model, prompt)

    @patch.object(client.http.client, "HTTPConnection")
    def test_live_success_uses_only_fixed_loopback(self, http):
        connection = http.return_value
        response = connection.getresponse.return_value
        response.status = 200
        response.read.return_value = envelope()
        result = client.chat("fixture-model", "Explain an embedding.", timeout=5)
        self.assertEqual(result["topic"], "Embeddings")
        http.assert_called_once_with("127.0.0.1", 11434, timeout=5)
        args, kwargs = connection.request.call_args
        self.assertEqual(args, ("POST", "/api/chat"))
        self.assertFalse(json.loads(kwargs["body"])["stream"])
        response.read.assert_called_once_with(client.MAX_RESPONSE_BYTES + 1)
        response.close.assert_called_once()
        connection.close.assert_called_once()

    @patch.object(client.http.client, "HTTPConnection")
    def test_http_errors_are_not_retried_or_followed(self, http):
        for status in (302, 400, 404, 429, 500):
            with self.subTest(status=status):
                http.reset_mock()
                http.return_value.getresponse.return_value.status = status
                with self.assertRaisesRegex(client.OllamaError, f"HTTP {status}"):
                    client.chat("fixture-model", "x")
                http.return_value.request.assert_called_once()
                http.return_value.getresponse.return_value.close.assert_called_once()
                http.return_value.close.assert_called_once()

    @patch.object(client.http.client, "HTTPConnection")
    def test_transport_failures_close_connection(self, http):
        for error in (TimeoutError(), ConnectionRefusedError(), RemoteDisconnected()):
            with self.subTest(error=type(error).__name__):
                http.reset_mock()
                http.return_value.request.side_effect = error
                with self.assertRaises(client.OllamaError):
                    client.chat("fixture-model", "x")
                http.return_value.close.assert_called_once()

    @patch.object(client.http.client, "HTTPConnection")
    def test_invalid_timeout_does_not_connect(self, http):
        for timeout in (0, -1, 121, float("inf"), float("nan")):
            with self.subTest(timeout=timeout), self.assertRaises(client.OllamaError):
                client.chat("fixture-model", "x", timeout)
        http.assert_not_called()

    def test_valid_response(self):
        self.assertEqual(set(client.parse_response(envelope())), {"topic", "summary"})

    def test_oversized_response(self):
        with self.assertRaisesRegex(client.OllamaError, "1 MiB"):
            client.parse_response(b"x" * (client.MAX_RESPONSE_BYTES + 1))

    def test_invalid_envelopes(self):
        for raw in (b"not json", b"\xff", b"[]", b'{}', envelope(error="untrusted error"), envelope(message=None)):
            with self.subTest(raw=raw[:50]), self.assertRaises(client.OllamaError):
                client.parse_response(raw)

    def test_incomplete_response_rejected(self):
        for fields in ({"done": False}, {"done": 1}, {"done_reason": "length"}):
            with self.subTest(fields=fields), self.assertRaises(client.OllamaError):
                client.parse_response(envelope(**fields))

    def test_bad_structured_results(self):
        cases = ("not json", "[]", "{}", '{"topic": "x", "summary": 3}',
                 '{"topic": "x", "summary": "y", "extra": true}',
                 json.dumps({"topic": " ", "summary": "y"}),
                 json.dumps({"topic": "x" * 81, "summary": "y"}),
                 json.dumps({"topic": "x", "summary": "y" * 501}))
        for content in cases:
            with self.subTest(content=content[:40]), self.assertRaises(client.OllamaError):
                client.parse_response(envelope(content))

    @patch.object(client.http.client, "HTTPConnection")
    def test_interruption_closes_connection(self, http):
        http.return_value.getresponse.side_effect = KeyboardInterrupt
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(client.main(["--live", "--model", "fixture-model"]), 130)
        self.assertIn("Cancelled locally", err.getvalue())
        http.return_value.close.assert_called_once()

    @patch.object(client.http.client, "HTTPConnection")
    def test_interruption_during_read_closes_response_and_connection(self, http):
        response = http.return_value.getresponse.return_value
        response.status = 200
        response.read.side_effect = KeyboardInterrupt
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(client.main(["--live", "--model", "fixture-model"]), 130)
        response.close.assert_called_once()
        http.return_value.close.assert_called_once()

    @patch.object(client, "chat", side_effect=client.OllamaError("fixture failure"))
    def test_cli_error_is_nonzero_and_not_a_success_object(self, chat):
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(client.main(["--live", "--model", "fixture-model"]), 1)
        self.assertEqual(out.getvalue(), "")
        self.assertIn("fixture failure", err.getvalue())


if __name__ == "__main__":
    unittest.main()
