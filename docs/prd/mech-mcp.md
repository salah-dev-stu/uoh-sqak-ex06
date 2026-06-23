# Mechanism PRD — MCP Infrastructure

**Modules:** `mcp/{mailbox,tools,server_factory,launch,cop_server,thief_server,client}`

Two separate FastMCP servers (Cop :8011, Thief :8012), HTTP transport, bearer auth
via `StaticTokenVerifier`. Each server exposes tools (`observe`, `send_message`,
`read_messages`, `act`, orchestrator-control tools) + a `game://rules` resource, all
operating on a transient `Mailbox`; no game rules, no LLM inside (H3). The async
`McpClient` wraps `fastmcp.Client` (in-memory for local/tests, HTTP for cloud) and
records every call through the Gatekeeper. **Gates:** H1, H3, H8.
