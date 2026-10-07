# 33. Cost, quotas, and capacity

Cost is what a workload consumes; capacity is how much work it can finish within its latency target. A cheaper request can still produce an expensive product through retries or human corrections. Optimize **cost per successful task**, alongside quality and response time.

## Why it matters

One user action might trigger classification, retrieval, a main answer, validation, and repair. Conversation histories also resend context. Count these calls before forecasting usage, then measure the workflow under realistic load.

For text inference, a first approximation is input tokens multiplied by the input rate, plus output tokens multiplied by the output rate. Normalize the pricing unit first. Treat cached input, other modalities, service tiers, and supporting services separately. Use the provider's current price sheet.

## Build it

Start with [Lab 2](../labs/02-bedrock.md), which exposes usage and limits output length. Record a synthetic benchmark with model identifier, date, input size, output size, latency, stop reason, and a pass/fail quality check. Avoid storing raw private prompts to measure performance.

Compare a few workloads: a short answer, a long input, and a deliberately constrained output. Compute average cost per successful task and examine slow cases separately. Measure peak demand as well as daily totals; an acceptable monthly forecast does not guarantee enough throughput during a burst.

Before scaling, add explicit concurrency limits, queue bounds, deadlines, and a maximum number of calls per task. Test overload behavior offline with a fake client. Decide whether to reject, queue, or return a smaller response before adding automatic retries.

## Watch out

- Bedrock quotas depend on the account, model, Region, and endpoint. Verify the applicable allocation instead of treating a published default as guaranteed capacity.
- Retrying a timed-out request can duplicate work and cost. A client timeout does not prove the service stopped processing.
- Output-token caps constrain one part of spending. They do not cap input costs, request volume, or infrastructure charges.
- Budget notifications can arrive after spending occurs. Treat them as alerts, not an immediate payment stop.
- Provisioned capacity and other commitments require a separate utilization and commercial review; this guide does not provision them.

## Learn more

- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) — verify rates and billing modes for the chosen workload.
- [Amazon Bedrock quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) — check capacity constraints and token accounting.
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) — understand budget tracking and notification delays.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
