# ADR-006 — Wired Gatekeeper + ledger + meta-test

**Status:** accepted · **Gates:** R3

**Decision.** One `ApiGatekeeper` mediates every external call — subprocess (LLM),
http (Ollama/MCP), smtp + google (report). It gates (per-service rate + budget from
config) and records a JSON ledger. Real backends are lazily imported *only* inside
the gatekeeper; a meta-test greps `src/parley` and fails if `subprocess`/`httpx`/
`smtplib`/`googleapiclient` appear anywhere else.

**Consequences.** The gate is wired, not decorative (the HW3/HW4 lesson). The
committed `sample_gate_ledger.json` shows mcp + subprocess + google events.
