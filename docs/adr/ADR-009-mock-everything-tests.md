# ADR-009 — Mock-everything test strategy (grader Path D)

**Status:** accepted · **Gates:** R6, R9

**Decision.** Every external boundary is injectable: the Gatekeeper takes fake
backends, providers/senders are swappable, the MCP client runs in-memory, the clock
is injected. Tests need no API key, no creds, no live servers, and are deterministic
via a seed + scripted fake LLM. A recorded sample run is committed as offline proof.

**Consequences.** `uv run pytest` is green and self-contained; coverage ≥85%.
