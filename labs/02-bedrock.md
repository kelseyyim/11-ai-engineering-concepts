# Lab 2: Make a bounded Amazon Bedrock request

Build a text-only Converse request, inspect it offline, and optionally send it using an existing AWS account. Learn the boundary between application code, credentials, model availability, permissions, and billing.

**Time:** about 20–30 minutes if an approved AWS setup already exists. Access or administrative work can take longer.

**Requirements:** Python 3.11+ for the offline lab. The optional live section also needs `boto3`, an existing approved AWS identity, and access to a compatible model or inference profile.

**Verification status:** the request construction, response parsing, error handling, dry-run behavior, and SDK configuration are tested offline with fake clients. Live AWS inference has **not** been run or verified for this guide. No AWS resources were provisioned.

## 1. Start offline, with no AWS setup

Run these commands from the repository root:

```bash
python3 examples/bedrock_chat.py
python3 -m unittest discover -s tests -p 'test_bedrock_chat.py' -v
```

No packages, credentials, network connection, or AWS account are needed. The script imports `boto3` only when explicitly invoked with `--live`. Even an injected client is unused in dry-run mode.

The result includes:

```json
{
  "mode": "dry-run",
  "aws_calls": 0,
  "region": "<set AWS_REGION>",
  "model_id": "<set BEDROCK_MODEL_ID>",
  "operation": "Converse",
  "message_count": 1,
  "prompt_characters": 62,
  "inference_config": {"maxTokens": 128},
  "note": "Prompt withheld. Nothing sent; add --live only after completing the lab checklist."
}
```

Dry-run validates this example's local request shape and limits. It does **not** establish model access, model-specific parameter compatibility, credentials, IAM permissions, or price. The code uses a built-in, non-sensitive prompt about retrieval-augmented generation; it does not print the raw prompt or credentials.

Read [the example](../examples/bedrock_chat.py) and [its tests](../tests/test_bedrock_chat.py). The request uses `modelId`, a user `messages` entry containing a text block, and `inferenceConfig.maxTokens`. No provider-specific sampling parameters are assumed. See the [Converse guide](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) for how these fields fit together.

## 2. Understand the live boundary

Stop here if you only want the offline lab. Adding `--live` sends the synthetic prompt to AWS and can incur inference charges. It is one logical request, with at most two SDK attempts for eligible failures. Retries can add work and cost; a timeout does not establish whether processing or billing occurred.

Before any live invocation:

- Select a model already approved for your account and use case. The example does not activate model access, create profiles, or provision capacity.
- Review the chosen model's terms. First use of a third-party model can start Marketplace subscription setup and constitutes agreement to its EULA. An authorized administrator should complete approval/access prerequisites first. Do not resolve this by granting the runtime role broad Marketplace permissions. [AWS model-access guidance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- Check the selected model, Region, inference mode, and current [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/). There is no promised free tier or fixed price for this lab.
- Check your organization's existing logging settings. [Invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) can capture prompts and outputs. This script neither enables nor disables it.
- Use only synthetic, non-sensitive text. The live result prints generated text, which could repeat any prompt you later substitute. Do not add SDK debug logging or dump raw error payloads.

The 128-token default and 512-token lab ceiling limit requested output, not input cost or total spend. The 8,000-character input ceiling is a simple lab safeguard, **not** an accurate token counter. Budget alerts are useful but [can lag spending](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).

## 3. Optional: prepare your existing local environment

Use a separate virtual environment for the optional SDK dependency:

```bash
python3 -m venv .venv-bedrock
source .venv-bedrock/bin/activate
python -m pip install boto3
python -m pip show boto3 botocore
```

On Windows PowerShell, activate with `.venv-bedrock\Scripts\Activate.ps1`. Record the installed `boto3` and `botocore` versions in your lab notes alongside the model identifier and date. This guide does not invent a dependency pin or claim a live-tested SDK version. For a deployed application, validate and lock the complete dependency set under your normal release process.

Use the SDK's [credential provider chain](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html), preferably an existing IAM Identity Center/SSO session or an attached workload role with temporary credentials. Do not create long-lived access keys for this exercise, put keys in source code, or commit `.aws` files. An existing profile can be selected with `AWS_PROFILE`; the script explicitly takes its source Region from `AWS_REGION`.

If using an **already configured** SSO profile and AWS CLI v2, replace the profile name and log in:

```bash
export AWS_PROFILE="your-existing-sso-profile"
aws sso login --profile "$AWS_PROFILE"
aws sts get-caller-identity --profile "$AWS_PROFILE"
```

Verify that the returned account and role are the ones intended for the lab. Follow your organization's setup process if you do not have an existing profile; the [AWS CLI SSO guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) explains the supported flow. Workload roles generally do not need `AWS_PROFILE`.

## 4. Choose a compatible model and source Region

There is intentionally no default model ID or Region. Find an approved text model in the [current model catalog](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html). Open its details and verify Converse support, text input/output, regional availability, lifecycle status, and inference parameters. Choose a model that supports this small `maxTokens` request without requiring additional provider-specific fields.

If you have authorized catalog-read access, these optional CLI commands inspect the selected Region without invoking a model. Replace the Region placeholder first:

```bash
export AWS_REGION="your-approved-source-region"
aws bedrock list-foundation-models \
  --region "$AWS_REGION" --by-output-modality TEXT \
  --query 'modelSummaries[].{id:modelId,arn:modelArn,inference:inferenceTypesSupported}' \
  --output json --no-cli-pager

aws bedrock list-inference-profiles \
  --region "$AWS_REGION" --output json --no-cli-pager
```

These are catalog results, not proof that your identity can invoke every listed item. See the official [model-list command](https://docs.aws.amazon.com/cli/latest/reference/bedrock/list-foundation-models.html) and [profile-list command](https://docs.aws.amazon.com/cli/latest/reference/bedrock/list-inference-profiles.html).

Some models/inference configurations require a profile rather than a direct foundation-model ID. Use an existing approved profile; do not guess an ID by prepending a region prefix. Inspect its routing with `get-inference-profile` if permitted, and review destinations and organization restrictions. A source endpoint Region does not necessarily equal the processing Region. [Profile usage](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-use.html) and [profile inspection](https://docs.aws.amazon.com/cli/latest/reference/bedrock/get-inference-profile.html) explain the distinction.

Set the exact approved model ID or profile ARN (a system-defined profile ID is also supported):

```bash
export BEDROCK_MODEL_ID="your-approved-model-id-or-profile-arn"
python examples/bedrock_chat.py
```

This is still offline. Check that the displayed values match your intended configuration.

## 5. Scope runtime permissions

The non-streaming `Converse` call requires `bedrock:InvokeModel`; it does not need `bedrock:*` or a full-access policy. Keep catalog discovery permissions separate from the runtime role. An administrator can scope direct foundation-model invocation to its exact ARN. The following is an **illustrative policy template**, not a provisioning instruction or a valid ready-to-apply policy until the resource is replaced:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "bedrock:InvokeModel",
    "Resource": "REPLACE_WITH_EXACT_APPROVED_FOUNDATION_MODEL_ARN"
  }]
}
```

For an inference profile, that direct-model template is insufficient: the policy needs the approved profile resource plus its underlying model resources across the applicable destinations. Adapt the official [profile prerequisites](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html) to the specific profile, narrowing actions and resources. Use the documented profile condition where appropriate. Organization service-control policies and Region restrictions also apply. Do not blindly copy a wildcard example to solve an access error.

## 6. Optional: make one live request

Only after the billing, terms, access, and model checks above, run:

```bash
python examples/bedrock_chat.py --live --max-tokens 128
```

The [Botocore configuration](https://docs.aws.amazon.com/botocore/latest/reference/config.html) sets a 5-second connection timeout and a 60-second read timeout. [Standard retries](https://docs.aws.amazon.com/boto3/latest/guide/retries.html) are explicitly capped at two total attempts, including the original. There is no application retry loop. These socket timeouts are not a strict end-to-end deadline; credential resolution, backoff, and other overhead can add time. This short lab is not configured for long-running reasoning workloads.

A successful result has the following shape. **This is illustrative, not output from a live run**; text and token counts vary:

```json
{
  "mode": "live",
  "text": "An explanation generated by your chosen model.",
  "stop_reason": "end_turn",
  "usage": {"inputTokens": 20, "outputTokens": 30, "totalTokens": 50},
  "non_text_blocks": 0
}
```

Check the [API response contract](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html): `max_tokens` means truncation; filtering/guardrail stop reasons require their own handling. The sample reports non-text blocks without printing their contents. It does not execute tool requests or continue a conversation. Exit code zero means a response was parsed, not that the answer met your quality expectations.

## 7. Diagnose failures safely

The CLI returns a nonzero exit code and a sanitized message on failure. It intentionally withholds raw SDK error text.

- **Missing configuration:** set both `AWS_REGION` and `BEDROCK_MODEL_ID`. Do not rely on the example to choose a model.
- **Missing/expired credentials:** refresh your approved SSO session or role credentials. Check for an unintended `AWS_PROFILE` or stale credential environment variables.
- **AccessDeniedException:** verify account, runtime policy, approved model access, and organization restrictions. Profile invocation needs more than a permission on the profile alone. An administrator should handle terms/access changes.
- **ValidationException or ResourceNotFoundException:** verify the exact ID/ARN, source Region, Converse support, inference mode, and token limits. If the model requires a profile, use an existing approved one; do not provision capacity as a workaround.
- **ThrottlingException:** inspect the applicable [Bedrock quota](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html). Reduce rate or wait; repeating the command rapidly is not a fix.
- **Network, service, or model timeout:** check connectivity/status and usage before retrying. Do not assume the first request was free or cancelled.
- **Unexpected response shape:** retain only non-sensitive diagnostics, SDK version, and the model identifier for investigation. Do not enable raw prompt logging just to debug this exercise.

## 8. Finish and explain what you learned

The example creates no cloud infrastructure, so it has no provisioned resource to delete. A live invocation's charges are not undone by closing the terminal. Review usage/cost reporting later, allowing for reporting delays. If an administrator separately enabled access, logging, subscriptions, or capacity, ask them to review those separately rather than assuming the script removed them.

Optionally deactivate the virtual environment and unset lab-specific variables:

```bash
deactivate
unset BEDROCK_MODEL_ID AWS_REGION
```

Unset `AWS_PROFILE` too if you set it only for this exercise. Follow your normal session sign-out procedure; do not delete shared profiles or credentials.

You are done when you can explain why dry-run makes no call, identify the exact live model/profile and Region, describe the request permission, and distinguish a parsed response from a complete, correct answer. As an offline extension, add a test for a different stop reason or response shape before changing the example.

Reviewed against official documentation: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
