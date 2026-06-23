# ADR-001 — MCP Client/Server split & LLM placement

**Status:** accepted · **Gates:** H1, H3

**Context.** The spec requires two MCP servers and the LLM in the *client*. Putting
the LLM in a server is an explicit failure.

**Decision.** The orchestrator IS the MCP client: it owns the authoritative
`GameState` and the single `LLMProvider`. Each FastMCP server is a per-agent I/O
surface (mailbox + tools `observe`/`send_message`/`read_messages`/`act` + a
`game://rules` resource). Servers hold no game rules and import no LLM.

**Consequences.** A meta-test (`test_gatekeeper_meta`) asserts `parley.mcp.*`
imports neither `parley.llm` nor the engine mutation API. The split is provable,
not just claimed.
