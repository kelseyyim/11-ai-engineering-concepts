# 21. Model Context Protocol (MCP)

MCP standardizes communication between an AI application's integrations and servers that expose capabilities. It is a protocol, not an agent orchestrator, a guarantee of tool quality, or a security barrier.

## Why it matters

Without a common integration contract, every application needs custom glue for every data source. MCP can make capabilities reusable across compatible hosts. Your application still owns task state, model selection, permissions, user experience, and recovery when a server fails.

## Build it

1. Identify the roles: the host is the AI application, its client communicates with an MCP server, and that server exposes capabilities. Keep this boundary separate from your business authorization layer.
2. Decide what to expose. Resources provide context, tools perform operations, and prompts supply reusable templates. A read-only inventory resource and a stock-adjustment tool should have distinct access rules.
3. Pin a supported protocol revision and compatible SDK versions. Test discovery, capability support, request validation, errors, cancellation, and reconnect behavior against the clients you actually support.
4. Authenticate protected deployments using the applicable authorization specification. Validate token audience, minimize scopes, and authorize each requested resource or operation for the authenticated user.
5. Treat server descriptions, annotations, and returned content according to their trust level. Inspect an unknown server before running it, and constrain local server processes just as you would other third-party software.

Start with read-only documentation search. Before adding writes, implement approval checks, audit records, and negative authorization tests.

## Watch out

Interoperability does not mean every client supports every feature or extension. Optional asynchronous task support also does not make your entire application durable. Never forward arbitrary client tokens to downstream services or infer that an advertised “read-only” annotation enforces anything.

**Version note:** The specification reviewed here is revision `2026-07-28`. Check compatibility before copying examples written for older revisions; protocol details evolve.

## Learn more

- [MCP specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) — understand the protocol's roles, capabilities, and limits.
- [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) — study token misuse, confused-deputy risks, local-server compromise, and scope minimization.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
