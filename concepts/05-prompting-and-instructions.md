# 5. Prompting and instruction design

A useful prompt specifies the task, relevant context, output contract, and how to handle insufficient evidence. Treat it as versioned application configuration with tests.

## Why it matters

Many apparent model failures are specification failures: unclear categories, missing examples, contradictory instructions, or impossible output requirements. A compact prompt that makes these choices explicit is easier to evaluate and maintain than a growing collection of emphatic rules.

## Build it

1. Write a task statement and a concrete success criterion before editing the prompt.
2. Separate application instructions from user input and retrieved content. Label sources and delimit quoted data.
3. Add a few representative examples, including an ambiguous input and an appropriate abstention. Keep evaluation cases separate from prompt examples.
4. Ask for observable artifacts, such as an answer with source IDs or a patch with tests. Evaluate those artifacts rather than requiring private reasoning transcripts.
5. Version the prompt alongside its tests and roll back when a change causes regressions.

## Watch out

Formatting helps organization; it does not enforce a security boundary. Retrieved text can contain hostile instructions even when wrapped in XML or Markdown. Put authorization and required business rules in application code. Provider-specific message roles and instruction precedence need an explicit adapter mapping.

## Learn more

- [Claude prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — Start from success criteria and empirical prompt tests.
- [Transformers chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating) — Understand how roles and message content become the model’s input tokens.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
