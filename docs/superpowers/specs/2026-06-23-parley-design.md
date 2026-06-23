# Design — `parley` (EX06 Dual-Agent MCP Cops & Robbers)

**Date:** 2026-06-23 · **Status:** Approved (user pre-approved the full lifecycle).

## Problem

Two LLM agents must play a turn-based, partially-observable chase, each on its own
MCP server, talking in free natural language, fully autonomously, ending in an
emailed report. Graded on **pipeline > communication > orchestration**, not strategy.

## Decisions (locked with the user)

| # | Decision | Choice |
|---|---|---|
| 1 | Agent LLM | **Claude CLI subscription** (no API key; orchestrator shells `claude -p` via Gatekeeper); **Ollama** local fallback via config. |
| 2 | Remote deploy | **ngrok** free tunnel + Bearer auth (Cloudflare Tunnel documented as alt). |
| 3 | GUI | **ASCII default** (tested) **+ optional Tkinter** behind a config flag. |
| 4 | Report | **Pluggable sender**: Gmail API (OAuth) default + **SMTP fallback**. |
| 5 | Bonus / RL | Declined / deferred. |

## Architecture (layers, each unit one purpose)

```
shared/        version · config loader · ApiGatekeeper (+ledger) · auth tokens · paths · logging
domain/        pure game logic, no IO: grid · positions · moves · barriers · rules ·
               partial-observation · scoring · state machine · sub-game/game records
mcp/           two FastMCP HTTP servers (cop, thief) · tool surface · server factory ·
               bearer auth middleware · client transport wrapper (through Gatekeeper)
llm/           LLMProvider interface · ClaudeCliProvider (subprocess) · OllamaProvider (http) ·
               prompt builder (role personas, NL-only contract) · NL action parser
orchestrator/  the MCP client: turn engine · dialogue manager · sub-game runner ·
               game runner (6×) · observation publisher · agent driver
report/        report builder (JSON) · GmailApiSender · SmtpSender · sender selection
gui/           Renderer interface · AsciiRenderer (default) · TkRenderer (flag, omitted from cov)
sdk/           ParleySDK façade — the single public entry (R1)
cli.py         thin CLI → SDK only
```

### The key separation (H3)
- **Orchestrator (MCP client)** owns the **authoritative `GameState`** and the **LLM**.
- **MCP servers** are per-agent I/O surfaces. Tools: `observe()` (returns the partial
  view the orchestrator pushed), `send_message(text)` / `read_messages()` (NL mailbox),
  `act(intent)` (records the agent's chosen move/barrier). They contain **no game rules
  and no LLM** — a meta-test asserts the server modules import neither the engine's
  mutation API nor any llm module beyond shared types.

### Turn loop (one sub-game)
```
reset to start positions (seeded)
for move in 1..max_moves:
    push Thief's partial observation → thief_server          # partial observability
    drive Thief: LLM reads cop's last NL msg + obs → emits NL msg + move(dir)
    apply Thief action to GameState; log; check terminal
    push Cop's partial observation → cop_server
    drive Cop: LLM reads thief's last NL msg + obs → emits NL msg + move|barrier
    apply Cop action; log; check terminal (capture / barrier-trap)
    if terminal: break
if not captured by max_moves: Thief wins
record outcome (winner, scores, moves, full NL+move log)
```
Six sub-games accumulate into a game record → JSON report → emailed.

### Natural-language contract (H2)
The prompt builder gives each agent a persona and **forbids coordinates/JSON**. The
agent must phrase intent in prose ("I'm hugging the north wall, sliding east") and read
the opponent's prose to *infer* position. The NL parser extracts a discrete move from
the model's structured tail (a single `MOVE: <dir>` line) while the **message body stays
free prose** — the move token is mechanics, the dialogue is the graded artifact. A test
scans committed sample dialogue and fails on raw `(x,y)` coordinate leakage.

### Gatekeeper (R3)
`ApiGatekeeper` is the only place allowed to call `subprocess`, `httpx`, `smtplib`, or
the Google client. It **gates** (per-service rate/budget from config) and **records**
every call to a JSON ledger. A meta-test greps `src/parley` for raw external-call
imports/usages outside `shared/gatekeeper*.py` and fails CI on any escape.

### Testing (R6/R9) — mock everything
Domain is pure → exhaustive fast unit tests. LLM providers mock subprocess/httpx. MCP
tools tested via FastMCP in-memory client. Orchestrator tested with a scripted fake LLM
+ fake transport → deterministic seeded outcomes. Report senders mocked. Target ≥85%.

### Config (R4/R10)
`config/{game,llm,mcp,report,gatekeeper,runtime}.json`. Nothing hardcoded; `runtime.json`
mirrors the version literal for the sync test.

## Diagrams to produce (H10)
Class diagram, system/MCP block diagram, MCP turn **sequence** diagram (Mermaid) — all
embedded in the README.

## Out of scope
RL policy (stub + ADR), inter-team bonus (declined), optimal strategy, web UI.
