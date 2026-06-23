# Plan — `parley` implementation

> Derived from `prd.md`. Drives `Todo.md`. Every source file stays **≤150 lines
> (raw and logical, R7)** — the file map below is sized to that budget, which is
> *why* the design is decomposed this finely.

## 1. Layered module map

Legend: each entry is one file with one responsibility + its public surface.

### `src/parley/shared/` — cross-cutting (no domain knowledge)
| File | Responsibility | Public surface |
|---|---|---|
| `version.py` | single version literal (R5) | `__version__` |
| `paths.py` | repo/report/transcript/ledger path resolution | `Paths` |
| `config.py` | load + validate JSON config files into typed dataclasses | `load_config()`, `Config`, sub-configs |
| `config_models.py` | dataclasses: `GameConfig`, `LlmConfig`, `McpConfig`, `ReportConfig`, `GateConfig`, `RuntimeConfig` | dataclasses |
| `logging_config.py` | structured logger setup | `get_logger()` |
| `auth.py` | Bearer-token mint/verify, env-sourced (H8) | `TokenStore`, `verify_bearer()` |
| `gatekeeper_types.py` | `GateEvent`, `GateResult`, `ServiceKind` enums/dataclasses | types |
| `rate_limiter.py` | token-bucket per service from config (R4) | `RateLimiter` |
| `gatekeeper.py` | **the one wired gate**: `subprocess`/`http`/`smtp`/`google` + ledger (R3) | `ApiGatekeeper` |

### `src/parley/domain/` — pure game logic (no IO, no LLM)
| File | Responsibility | Public surface |
|---|---|---|
| `geometry.py` | `Position`, 8 `Direction`s, neighbour math, bounds | `Position`, `Direction`, `step()` |
| `grid.py` | grid dims, in-bounds, cell occupancy, barriers set | `Grid` |
| `pieces.py` | `Role` (COP/THIEF), `Piece` state | `Role`, `Piece` |
| `actions.py` | `Move`, `PlaceBarrier`, `Action` union + validation rules | action types, `validate()` |
| `observation.py` | partial-observability: vision-limited view per agent (Dec-POMDP) | `observe(state, role) -> Observation` |
| `rules.py` | move legality, barrier legality (≤max, fatal-entry) | `is_legal()`, `apply()` |
| `terminal.py` | capture / survive / barrier-trap detection | `check_terminal()` |
| `scoring.py` | scoring table → per-sub-game + aggregate (config-driven) | `score_subgame()`, `aggregate()` |
| `state.py` | authoritative `GameState` (positions, barriers, move#, turn) | `GameState` |
| `records.py` | `MoveRecord`, `SubGameResult`, `GameResult` (logging shapes) | dataclasses |

### `src/parley/llm/` — LLM providers (client-side only)
| File | Responsibility | Public surface |
|---|---|---|
| `provider.py` | `LLMProvider` protocol (`complete(prompt) -> str`) | `LLMProvider` |
| `claude_cli.py` | shell `claude -p` via Gatekeeper subprocess (default, no API key) | `ClaudeCliProvider` |
| `ollama.py` | POST `/api/chat` via Gatekeeper http (local fallback) | `OllamaProvider` |
| `factory.py` | build provider from `LlmConfig` | `make_provider()` |
| `prompts.py` | role personas + **NL-only contract** + context framing | `build_prompt()` |
| `parser.py` | extract `MOVE:`/`BARRIER` token; keep message body free prose | `parse_action()` |

### `src/parley/mcp/` — two FastMCP servers + client transport
| File | Responsibility | Public surface |
|---|---|---|
| `mailbox.py` | per-agent NL message queue + latest observation store | `Mailbox` |
| `tools.py` | tool fns: `observe`/`send_message`/`read_messages`/`act` | tool callables |
| `server_factory.py` | build a FastMCP app for a role + bearer middleware | `make_server()` |
| `cop_server.py` | Cop FastMCP app entry (port from config) | `app`, `main()` |
| `thief_server.py` | Thief FastMCP app entry (port from config) | `app`, `main()` |
| `client.py` | MCP client transport wrapper (calls tools via Gatekeeper http) | `McpClient` |

### `src/parley/orchestrator/` — the MCP client / game driver
| File | Responsibility | Public surface |
|---|---|---|
| `dialogue.py` | NL message exchange bookkeeping across turns | `DialogueLog` |
| `agent_driver.py` | one agent's turn: obs → prompt → LLM → parse → act | `AgentDriver` |
| `turn_engine.py` | thief-then-cop ordering, apply, terminal check | `TurnEngine` |
| `subgame_runner.py` | run ≤25 moves → `SubGameResult` | `SubGameRunner` |
| `game_runner.py` | run 6 sub-games, accumulate → `GameResult` | `GameRunner` |
| `pipeline.py` | init → play → report orchestration (autonomous) | `Pipeline` |

### `src/parley/report/` — reporting + email
| File | Responsibility | Public surface |
|---|---|---|
| `builder.py` | `GameResult` → JSON report (all fields, E1) | `build_report()` |
| `sender.py` | `ReportSender` protocol + selection from config | `ReportSender`, `make_sender()` |
| `gmail_sender.py` | Gmail API send via OAuth + Gatekeeper | `GmailApiSender` |
| `smtp_sender.py` | SMTP fallback via Gatekeeper | `SmtpSender` |

### `src/parley/gui/` — visualization
| File | Responsibility | Public surface |
|---|---|---|
| `renderer.py` | `Renderer` protocol + factory | `Renderer`, `make_renderer()` |
| `ascii_renderer.py` | text grid + counter + last NL messages (default, tested) | `AsciiRenderer` |
| `tk_renderer.py` | optional Tkinter window (flag; omitted from coverage) | `TkRenderer` |

### `src/parley/sdk/` + CLI
| File | Responsibility | Public surface |
|---|---|---|
| `facade.py` | `ParleySDK` — single public entry (R1): `play()`, `deploy_info()`, `report_only()` | `ParleySDK` |
| `cli.py` | argparse → SDK (`play`, `serve-cop`, `serve-thief`, `report`, `version`) | `main()` |
| `cli_handlers.py` | thin per-command handlers | handlers |

## 2. Class diagram (sketch → `diagrams/class_diagram.mmd`)

```
ParleySDK ──owns──> ApiGatekeeper, Config, Pipeline
Pipeline ──> GameRunner ──> SubGameRunner ──> TurnEngine ──> AgentDriver
AgentDriver ──uses──> LLMProvider, McpClient, prompts, parser
McpClient ──http via Gatekeeper──> {cop_server, thief_server}  (FastMCP, Mailbox, tools)
TurnEngine ──mutates──> GameState (Grid, Piece, barriers); reads rules/terminal/scoring/observation
GameRunner ──> build_report ──> ReportSender{GmailApiSender|SmtpSender}
Renderer{AsciiRenderer|TkRenderer} <── Pipeline (per move)
```

## 3. Milestones (TDD order — red test first, then code)

- **M1 — shared core:** config models + loader, paths, logging, gatekeeper types,
  rate limiter, **ApiGatekeeper** + ledger, auth tokens. Meta-test stub.
- **M2 — domain:** geometry → grid → pieces → actions → observation → rules →
  terminal → scoring → state → records. Exhaustive pure unit tests (seeded).
- **M3 — llm:** provider protocol, claude_cli (mock subprocess), ollama (mock http),
  factory, prompts (NL-only contract), parser. Tests mock all IO.
- **M4 — mcp:** mailbox, tools, server_factory + bearer middleware, cop/thief servers,
  client transport. Test via FastMCP in-memory; assert no-LLM-in-server.
- **M5 — orchestrator:** dialogue, agent_driver, turn_engine, subgame_runner,
  game_runner, pipeline. Deterministic seeded full-run test with fake LLM + fake transport.
- **M6 — report:** builder, sender protocol, gmail + smtp senders (mocked). JSON shape test.
- **M7 — gui:** renderer protocol, ascii renderer (tested), tk renderer (flag).
- **M8 — sdk + cli:** façade wiring everything; CLI commands; end-to-end mocked test.
- **M9 — gatekeeper meta-test:** grep src for raw external calls → fail on escape.
- **M10 — deploy + scripts:** ngrok deploy script, run scripts, sample-run generator.
- **M11 — diagrams + docs:** class/block/sequence Mermaid; ADRs; per-mechanism PRDs.
- **M12 — README + sample artifacts + final green + push public.**

## 4. Test strategy (R6/R9)

- **Pure-domain** tests dominate (fast, deterministic, high coverage).
- **All external IO mocked:** subprocess (claude), httpx (ollama + MCP + gmail), smtplib.
- **Seeded** start positions + a **scripted fake LLM** make full pipeline runs
  reproducible → assert exact scores/winners.
- **Meta-test** greps source: only `shared/gatekeeper*.py` may import
  `subprocess`/`httpx`/`smtplib`/`googleapiclient`.
- **NL-leak test:** committed sample dialogue contains no `(\d+,\s*\d+)` coordinates.
- **Version-sync test** + **file-line guard** run in CI.
- Coverage gate **≥85%**; `tk_renderer.py` omitted (untestable UI).

## 5. ADRs to record (`docs/adr/`)
1. MCP Client/Server split + LLM placement (H3).
2. HTTP transport over STDIO (Dr. Segal's insistence).
3. Claude-CLI-subscription provider (no API key) + Ollama fallback (H9).
4. Partial-observability model (vision radius; Dec-POMDP).
5. NL-only dialogue contract + move-token parsing (H2).
6. Wired Gatekeeper + ledger + meta-test (R3).
7. Pluggable report sender (Gmail API + SMTP) (H7).
8. ngrok + Bearer-token deploy; Cloudflare alt (H8).
9. Mock-everything test strategy (grader Path D).
10. RL deferral (out of scope, stub interface) (H11).

## 6. Per-mechanism PRDs (`docs/prd/`)
`mech-game-engine.md`, `mech-mcp.md`, `mech-orchestration.md`, `mech-llm.md`,
`mech-report.md`, `mech-deploy-security.md`.

## 7. Config files (`config/`)
`game.json`, `llm.json`, `mcp.json`, `report.json`, `gatekeeper.json`, `runtime.json`
(already stubbed). Each loaded + validated by `shared/config.py`; nothing hardcoded.

## 8. Deliverable artifacts (committed proof)
`reports/sample_report.json`, `reports/transcripts/sample_run.md` (+ `.txt` ASCII board
frames), CI badge, diagrams, filled submission PDF via `scripts/fill_submission_pdf.py`.
