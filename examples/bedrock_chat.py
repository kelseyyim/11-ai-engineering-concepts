#!/usr/bin/env python3
"""One bounded Bedrock Converse call; offline by default. Python 3.11+.

Run without --live to inspect a redacted plan without importing boto3 or
resolving AWS credentials. See labs/02-bedrock.md before enabling live mode.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Mapping, Sequence
from typing import Any, Protocol


DEFAULT_PROMPT = "Explain retrieval-augmented generation in two short sentences."
MAX_PROMPT_CHARACTERS = 8000  # A lab guardrail, not a tokenizer or AWS limit.
MAX_OUTPUT_TOKENS = 512  # A lab guardrail; model-specific limits still apply.


class LabError(Exception):
    """An actionable, sanitized error safe to show in this lab's CLI."""


class ConverseClient(Protocol):
    def converse(self, **kwargs: Any) -> Mapping[str, Any]: ...


def build_request(model_id: str, prompt: str, max_tokens: int = 128) -> dict[str, Any]:
    """Build the text-only request shared by dry-run and live modes."""
    if not isinstance(model_id, str) or not model_id.strip():
        raise LabError("Set BEDROCK_MODEL_ID to your approved model or inference profile.")
    if not isinstance(prompt, str) or not prompt.strip():
        raise LabError("The prompt must contain text.")
    if len(prompt) > MAX_PROMPT_CHARACTERS:
        raise LabError("The lab accepts at most 8000 prompt characters.")
    if type(max_tokens) is not int or not 1 <= max_tokens <= MAX_OUTPUT_TOKENS:
        raise LabError("The lab accepts max_tokens from 1 through 512.")
    return {
        "modelId": model_id.strip(),
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": max_tokens},
    }


def make_client(region: str) -> ConverseClient:
    """Only called for --live; use the SDK's normal credential provider chain."""
    try:
        import boto3
        from botocore.config import Config
    except ImportError:
        raise LabError("Live mode requires boto3. Follow the lab's optional setup.") from None
    return boto3.client(
        "bedrock-runtime",
        region_name=region,
        config=Config(
            connect_timeout=5,
            read_timeout=60,
            retries={"mode": "standard", "total_max_attempts": 2},
        ),
    )


ERROR_HINTS = {
    "AccessDeniedException": "Check your approved model access, role policy, and organization restrictions.",
    "ValidationException": "Check Converse support, model/profile ID, Region, and model-specific token limits.",
    "ResourceNotFoundException": "Verify the model/profile exists in the selected source Region.",
    "ThrottlingException": "Check account/model quotas; reduce request rate before retrying manually.",
    "ServiceUnavailableException": "The service is unavailable; check status before retrying manually.",
    "InternalServerException": "The service failed after bounded SDK retries; try later.",
    "ModelNotReadyException": "The model is not ready after bounded SDK retries; try later.",
    "ModelTimeoutException": "The model timed out; review usage before retrying.",
    "ModelErrorException": "The model could not process this request; review model compatibility.",
    "ExpiredTokenException": "Refresh your approved short-lived AWS login.",
    "UnrecognizedClientException": "Refresh your approved AWS login and verify the selected profile.",
    "NoCredentialsError": "No AWS credentials found; use your approved SSO login or workload role.",
    "PartialCredentialsError": "Your AWS credential chain is incomplete; refresh the approved login.",
    "UnauthorizedSSOTokenError": "Refresh your approved AWS SSO login.",
    "SSOTokenLoadError": "Refresh your approved AWS SSO login.",
    "CredentialRetrievalError": "Your credential provider failed; refresh the approved login.",
    "ProfileNotFound": "Select an existing approved AWS_PROFILE.",
    "EndpointConnectionError": "Check connectivity and the source AWS_REGION.",
    "ReadTimeoutError": "The response timed out; the request may still have incurred a charge.",
    "ConnectTimeoutError": "The connection timed out; check networking before retrying.",
    "ParamValidationError": "Check the request parameters against your installed SDK and model.",
}


def safe_sdk_error(error: Exception) -> LabError:
    """Never expose exception text: it may contain request data or credentials."""
    code = type(error).__name__
    response = getattr(error, "response", None)
    if isinstance(response, Mapping):
        detail = response.get("Error")
        if isinstance(detail, Mapping) and isinstance(detail.get("Code"), str):
            code = detail["Code"]
    if code in ERROR_HINTS:
        return LabError(f"{code}: {ERROR_HINTS[code]}")
    return LabError("AWS/SDK request failed. Check the lab troubleshooting steps; raw details are withheld.")


def parse_response(response: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the expected shape, retaining usage and non-text block counts."""
    try:
        message = response["output"]["message"]
        blocks = message["content"]
        stop_reason = response["stopReason"]
        usage = response["usage"]
        if message["role"] != "assistant" or not isinstance(blocks, list):
            raise ValueError
        if not isinstance(stop_reason, str) or not stop_reason or not isinstance(usage, Mapping):
            raise ValueError
        for key in ("inputTokens", "outputTokens", "totalTokens"):
            if type(usage[key]) is not int or usage[key] < 0:
                raise ValueError
        text_parts = []
        for block in blocks:
            if not isinstance(block, Mapping):
                raise ValueError
            if "text" in block:
                if not isinstance(block["text"], str):
                    raise ValueError
                text_parts.append(block["text"])
        # Copy only token counters. Do not dump arbitrary provider payloads.
        counters = {key: usage[key] for key in ("inputTokens", "outputTokens", "totalTokens")}
        for key in ("cacheReadInputTokens", "cacheWriteInputTokens"):
            if key in usage:
                if type(usage[key]) is not int or usage[key] < 0:
                    raise ValueError
                counters[key] = usage[key]
    except (KeyError, TypeError, ValueError):
        raise LabError("Unexpected Converse response shape; raw response is withheld.") from None
    return {
        "mode": "live",
        "text": "\n".join(text_parts),
        "stop_reason": stop_reason,
        "usage": counters,
        "non_text_blocks": len(blocks) - len(text_parts),
    }


def run(
    *,
    live: bool = False,
    prompt: str = DEFAULT_PROMPT,
    max_tokens: int = 128,
    env: Mapping[str, str] | None = None,
    client: ConverseClient | None = None,
) -> dict[str, Any]:
    """An injected fake client enables dependency-free offline contract tests."""
    environment = os.environ if env is None else env
    region = environment.get("AWS_REGION", "").strip()
    model_id = environment.get("BEDROCK_MODEL_ID", "").strip()
    if live and not region:
        raise LabError("Set AWS_REGION to the approved source Region before using --live.")
    if live and not model_id:
        raise LabError("Set BEDROCK_MODEL_ID before using --live; no model is selected automatically.")
    request = build_request(model_id or "<set BEDROCK_MODEL_ID>", prompt, max_tokens)
    if not live:
        return {
            "mode": "dry-run",
            "aws_calls": 0,
            "region": region or "<set AWS_REGION>",
            "model_id": request["modelId"],
            "operation": "Converse",
            "message_count": len(request["messages"]),
            "prompt_characters": len(prompt),
            "inference_config": request["inferenceConfig"],
            "note": "Prompt withheld. Nothing sent; add --live only after completing the lab checklist.",
        }
    try:
        runtime = client if client is not None else make_client(region)
        response = runtime.converse(**request)
    except LabError:
        raise
    except Exception as error:
        raise safe_sdk_error(error) from None
    return parse_response(response)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Send one billable logical request to AWS.")
    parser.add_argument("--max-tokens", type=int, default=128, help="Output limit, 1–512 (default: 128).")
    args = parser.parse_args(argv)
    try:
        result = run(live=args.live, max_tokens=args.max_tokens)
    except LabError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
