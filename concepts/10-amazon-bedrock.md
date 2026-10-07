# 10. Amazon Bedrock and IAM

Amazon Bedrock provides managed access to foundation models through AWS. This guide uses the **Converse API** on `bedrock-runtime`: a shared message format for compatible models, rather than provider-specific request bodies. A common interface reduces integration work; it does not make model capabilities, availability, or behavior identical.

## Why it matters

For a team already using AWS, Bedrock can fit an existing approach to roles, account boundaries, and operational controls. Your application still owns evaluation, prompt construction, failure handling, and spending limits. A successful API response establishes connectivity, not answer quality.

Think of deployment as a tuple: **AWS account, source Region, model or inference profile, API features, and permissions**. Copying a model ID from a tutorial does not establish that this tuple is valid for your account. An inference profile can route requests across Regions; review its destinations and your data-location requirements before adopting it.

## Build it

Complete [Lab 2: a bounded Bedrock request](../labs/02-bedrock.md). Its Python example starts in dry-run mode, without importing an SDK or resolving credentials. The optional live path sends one short, synthetic prompt and displays text, token usage, and the stop reason.

1. Choose a text model that supports Converse and the selected source Region. If the model needs an inference profile, use its approved ID or ARN.
2. Use an existing short-lived login or workload role. Keep credentials out of code and version control.
3. Set `AWS_REGION` and `BEDROCK_MODEL_ID`. Give the runtime role only the invocation permissions for the intended resources.
4. Inspect the offline tests before adding `--live`. Then evaluate the answer against a small, written expectation.

## Watch out

- A role for runtime inference should not automatically become a model-subscription or infrastructure-administration role. Have an authorized administrator handle access and terms.
- `max_tokens` means the answer may be cut short. A filtering or tool-use stop reason also needs application handling; neither is ordinary task completion.
- Cross-Region profiles need permissions covering their underlying model resources. Organization policies can still restrict the route.
- Keep prompts synthetic during setup. Existing account logging and your own downstream output handling need separate review.

## Learn more

- [Converse API reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) — request structure, return fields, and invocation permission.
- [Models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html) — select a model and verify its current capabilities and Regions.
- [Inference-profile prerequisites](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html) — resource scoping for profile-based invocation.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
