# Mechanism PRD — Orchestration

**Modules:** `orchestrator/{dialogue,agent_driver,turn_engine,subgame_runner,game_runner,pipeline}`

The MCP client / game driver holds the LLM and the authoritative state. Per turn:
compute partial observation → push to the role's server → prompt the LLM with the
opponent's NL message + history → parse a free-NL message and an action → speak +
act through the server → apply to state → log → check terminal. `SubGameRunner`
runs ≤25 moves; `GameRunner` runs 6 sub-games and accumulates scores; `Pipeline`
ties init → play → report → artifacts with zero manual steps. Any LLM/parse failure
falls back to a safe legal move. **Gates:** H4, H2, H3.
