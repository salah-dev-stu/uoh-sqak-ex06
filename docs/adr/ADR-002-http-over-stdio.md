# ADR-002 — HTTP transport over STDIO

**Status:** accepted · **Gates:** H1, H8

**Context.** FastMCP supports STDIO and HTTP. Dr. Segal "insists" on HTTP, even
locally, because it is the same code locally and in the cloud and is tunnelable.

**Decision.** Servers run `transport="http"`. The async `McpClient` wraps
`fastmcp.Client` — in-memory for the deterministic local run and tests, real HTTP
for the cloud demonstration (`test_http_server` starts a uvicorn server).

**Consequences.** The same servers deploy behind ngrok/Cloudflare unchanged; the
integration test proves bearer-protected HTTP works over the wire.
