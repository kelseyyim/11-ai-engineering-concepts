"""Offline contract tests: no boto3 installation, credentials, or AWS calls."""

import contextlib
import copy
import io
import json
import types
import unittest
from unittest.mock import Mock, patch

from examples import bedrock_chat as lab


ENV = {"AWS_REGION": "test-region-1", "BEDROCK_MODEL_ID": "test.approved-model-v1"}
RESPONSE = {
    "output": {"message": {"role": "assistant", "content": [{"text": "A short answer."}]}},
    "stopReason": "end_turn",
    "usage": {"inputTokens": 12, "outputTokens": 5, "totalTokens": 17},
}


class FakeClient:
    def __init__(self, response=None, error=None):
        self.response = copy.deepcopy(RESPONSE if response is None else response)
        self.error = error
        self.calls = []

    def converse(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.response


class FakeServiceError(Exception):
    def __init__(self, code):
        super().__init__("secret prompt or credential must never be shown")
        self.response = {"Error": {"Code": code, "Message": str(self)}}


class BedrockChatTests(unittest.TestCase):
    def test_dry_run_is_default_without_environment_or_client(self):
        with patch.object(lab, "make_client", side_effect=AssertionError("must not create client")):
            result = lab.run(env={})
        self.assertEqual(result["mode"], "dry-run")
        self.assertEqual(result["aws_calls"], 0)

    def test_dry_run_never_uses_injected_client_or_exposes_prompt(self):
        client = FakeClient()
        result = lab.run(client=client, env=ENV, prompt="synthetic private text")
        self.assertEqual(client.calls, [])
        self.assertNotIn("synthetic private text", json.dumps(result))
        self.assertEqual(result["prompt_characters"], 22)

    def test_one_converse_call_has_expected_contract(self):
        client = FakeClient()
        result = lab.run(live=True, env=ENV, client=client, prompt="Test", max_tokens=48)
        self.assertEqual(client.calls, [{
            "modelId": ENV["BEDROCK_MODEL_ID"],
            "messages": [{"role": "user", "content": [{"text": "Test"}]}],
            "inferenceConfig": {"maxTokens": 48},
        }])
        self.assertEqual(result["text"], "A short answer.")
        self.assertEqual(result["stop_reason"], "end_turn")
        self.assertEqual(result["usage"], RESPONSE["usage"])

    def test_inference_profile_arn_is_passed_unchanged(self):
        profile = "arn:aws:bedrock:test-region-1:123456789012:inference-profile/test"
        client = FakeClient()
        lab.run(live=True, env={**ENV, "BEDROCK_MODEL_ID": profile}, client=client)
        self.assertEqual(client.calls[0]["modelId"], profile)

    def test_live_requires_region_and_model_before_client_creation(self):
        for env in ({}, {"AWS_REGION": "test-region-1"}, {"BEDROCK_MODEL_ID": "test"}):
            with self.subTest(env=env):
                with patch.object(lab, "make_client") as create:
                    with self.assertRaises(lab.LabError):
                        lab.run(live=True, env=env)
                    create.assert_not_called()

    def test_request_validation_prevents_calls(self):
        for options in ({"prompt": " "}, {"prompt": "x" * 8001},
                        {"max_tokens": 0}, {"max_tokens": 513}, {"max_tokens": True}):
            with self.subTest(options=options):
                client = FakeClient()
                with self.assertRaises(lab.LabError):
                    lab.run(live=True, env=ENV, client=client, **options)
                self.assertEqual(client.calls, [])

    def test_empty_model_is_rejected_by_builder(self):
        with self.assertRaises(lab.LabError):
            lab.build_request(" ", "Test")

    def test_all_text_blocks_join_and_non_text_is_not_dumped(self):
        response = copy.deepcopy(RESPONSE)
        response["output"]["message"]["content"] = [
            {"text": "One"}, {"reasoningContent": {"text": "not for output"}}, {"text": "Two"},
        ]
        result = lab.parse_response(response)
        self.assertEqual(result["text"], "One\nTwo")
        self.assertEqual(result["non_text_blocks"], 1)
        self.assertNotIn("not for output", json.dumps(result))

    def test_truncation_and_filtering_remain_visible(self):
        for reason in ("max_tokens", "content_filtered", "guardrail_intervened", "tool_use"):
            response = copy.deepcopy(RESPONSE)
            response["stopReason"] = reason
            response["output"]["message"]["content"] = []
            result = lab.parse_response(response)
            self.assertEqual(result["stop_reason"], reason)
            self.assertEqual(result["text"], "")

    def test_optional_cache_token_counters_are_preserved(self):
        response = copy.deepcopy(RESPONSE)
        response["usage"]["cacheReadInputTokens"] = 20
        self.assertEqual(lab.parse_response(response)["usage"]["cacheReadInputTokens"], 20)

    def test_malformed_responses_fail_without_dumping_data(self):
        malformed = [None, {}, {"output": "secret"}]
        for field, value in (("stopReason", None), ("usage", {})):
            response = copy.deepcopy(RESPONSE)
            response[field] = value
            malformed.append(response)
        bad_tokens = copy.deepcopy(RESPONSE)
        bad_tokens["usage"]["inputTokens"] = True
        malformed.append(bad_tokens)
        bad_block = copy.deepcopy(RESPONSE)
        bad_block["output"]["message"]["content"] = [{"text": 123}]
        malformed.append(bad_block)
        for response in malformed:
            with self.subTest(response=response):
                with self.assertRaisesRegex(lab.LabError, "Unexpected Converse response"):
                    lab.parse_response(response)

    def test_known_service_errors_are_actionable_and_sanitized(self):
        for code in ("AccessDeniedException", "ValidationException", "ThrottlingException"):
            client = FakeClient(error=FakeServiceError(code))
            with self.subTest(code=code):
                with self.assertRaises(lab.LabError) as caught:
                    lab.run(live=True, env=ENV, client=client)
                self.assertIn(code, str(caught.exception))
                self.assertNotIn("secret", str(caught.exception))
                self.assertEqual(len(client.calls), 1)  # No application retry loop.

    def test_unknown_errors_do_not_echo_exception_or_error_code(self):
        client = FakeClient(error=FakeServiceError("secret-data-in-an-unexpected-code"))
        with self.assertRaises(lab.LabError) as caught:
            lab.run(live=True, env=ENV, client=client)
        self.assertNotIn("secret", str(caught.exception))

    def test_credential_error_is_safe_without_botocore_dependency(self):
        NoCredentialsError = type("NoCredentialsError", (Exception,), {})
        error = lab.safe_sdk_error(NoCredentialsError("secret"))
        self.assertIn("SSO", str(error))
        self.assertNotIn("secret", str(error))

    def test_sdk_client_configuration_has_bounded_timeouts_and_retries(self):
        boto3 = types.ModuleType("boto3")
        boto3.client = Mock(return_value=FakeClient())
        botocore = types.ModuleType("botocore")
        config_module = types.ModuleType("botocore.config")
        config_module.Config = Mock(side_effect=lambda **kwargs: kwargs)
        with patch.dict("sys.modules", {"boto3": boto3, "botocore": botocore,
                                       "botocore.config": config_module}):
            lab.make_client("test-region-1")
        boto3.client.assert_called_once_with(
            "bedrock-runtime", region_name="test-region-1",
            config={"connect_timeout": 5, "read_timeout": 60,
                    "retries": {"mode": "standard", "total_max_attempts": 2}},
        )

    def test_missing_sdk_has_optional_install_hint(self):
        with patch.dict("sys.modules", {"boto3": None}):
            with self.assertRaisesRegex(lab.LabError, "requires boto3"):
                lab.make_client("test-region-1")

    def test_cli_default_remains_offline(self):
        with patch.object(lab, "make_client") as create:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(lab.main([]), 0)
            create.assert_not_called()
        self.assertEqual(json.loads(output.getvalue())["mode"], "dry-run")

    def test_cli_invalid_limit_is_nonzero_without_traceback(self):
        with contextlib.redirect_stderr(io.StringIO()) as output:
            self.assertEqual(lab.main(["--max-tokens", "0"]), 1)
        self.assertIn("Error:", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
