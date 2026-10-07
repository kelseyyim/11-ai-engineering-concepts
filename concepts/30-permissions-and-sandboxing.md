# 30. Permissions and sandboxing

Permissions determine which actions an actor may take on which resources. Sandboxing restricts what a process can reach even if its behavior is wrong. Use both: user approval does not isolate a process, and a sandbox does not establish business authorization.

## Why it matters

A coding agent may legitimately edit a repository without needing access to browser cookies, production credentials, or arbitrary network destinations. Narrow capabilities reduce the damage from model mistakes, malicious dependencies, and prompt injection while allowing routine approved work to proceed.

## Build it

1. Define capabilities by action and resource: read a specific document collection, write within a workspace, or call a particular service endpoint. Deny anything outside the required scope by default.
2. Enforce identity and tenant ownership in trusted services on every request. Never accept a model-supplied user ID as proof of identity or an accessible resource ID as proof of permission.
3. Run tools with constrained filesystem access, network egress, process privileges, and resource limits. Avoid mounting secrets, host control sockets, or unrelated directories.
4. Separate read-only operations from writes. Obtain approval for side effects at the level the user can understand: the exact target, change, destination, and consequence. Bind approval to those details rather than a generic “continue.”
5. Record authorization decisions and execution receipts without credentials. Test denied paths, revoked access, cross-tenant requests, and disallowed files or hosts.

A coding setup can grant a disposable workspace and test runner; publishing and production access require separate capability decisions.

## Watch out

A tool labeled “read-only” can still disclose data through outbound requests. Network restrictions and filesystem isolation must work together. Containers also vary in isolation strength and configuration; the word “container” alone says little about your threat model. Avoid broad approvals that train users to click through warnings.

## Learn more

- [OWASP: Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — implement least privilege, deny-by-default behavior, and per-request checks.
- [Anthropic: Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) — examine a provider-specific implementation of combined filesystem and network boundaries; verify current product settings separately.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
