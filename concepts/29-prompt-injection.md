# 29. Prompt injection and untrusted data

Prompt injection happens when an application treats attacker-controlled content as instructions with more authority than it deserves. Indirect injection can arrive inside a web page, retrieved document, email, image, tool description, or tool result.

## Why it matters

Suppose a support assistant reads a customer-uploaded log containing instructions to export account records. The assistant needs the log as evidence, but the log's author cannot authorize access or transmission. A system prompt asking the model to ignore malicious instructions is useful guidance, not an enforceable security boundary.

## Build it

1. Map trusted instructions, untrusted inputs, sensitive data, and action interfaces. Preserve provenance as content moves through retrieval, summaries, memory, and worker messages.
2. Keep authorization outside the model. Before every tool execution, validate the authenticated actor, permitted operation, target, arguments, and applicable user approval.
3. Limit what an exposed component can read and send. A parser of hostile documents should not also hold broad credentials and unrestricted network access.
4. Separate external content from higher-priority instructions and extract only needed fields. Validate extracted values; structured output does not make their meaning trustworthy.
5. Build adversarial tests around real outcomes: unauthorized writes, cross-tenant access, secret disclosure, or attacker-chosen destinations. Use synthetic canary data and controlled endpoints, then verify that the intended legitimate task still succeeds.

## Watch out

Keyword filters, delimiters, and a second model can reduce risk, but none guarantees safety. Summaries and stored memories can carry an attack into later steps. A blocked malicious request is not sufficient evidence of robustness, and a blanket refusal is not successful task completion.

**Research note:** Capability-based designs such as CaMeL explore separating privileged planning from untrusted data processing. Their protection depends on stated assumptions and policies; a research prototype is not a drop-in security guarantee.

## Learn more

- [OWASP: Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — study attack surfaces, layered defenses, and outcome-based tests.
- [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) — understand information-flow controls and the limits of the paper's threat model.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
