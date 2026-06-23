# Todo — `parley` (≥500 tasks, TDD-ordered)

> Walked one-by-one in Phase 5. `[x]` = done. Each module follows **red test →
> implement → ruff/line-check → commit**. Tasks map to `Plan.md` milestones.
> Tags: **(H#)** HW6 gate, **(R#)** standing rule.

## M0 — Project setup & config (scaffold)

- [x] T001 `git init`, `main` branch
- [x] T002 Directory tree `src/parley/{shared,domain,mcp,llm,orchestrator,report,gui,sdk}`
- [x] T003 `tests/{unit,integration,fixtures}` tree
- [x] T004 `.gitignore` excludes toolkit/plugin/venv/cache/secrets (R11)
- [x] T005 `pyproject.toml` — uv, hatch version, ruff, pytest, coverage≥85 (R8/R9/R12)
- [x] T006 `src/parley/shared/version.py` = "1.00" (R5)
- [x] T007 `src/parley/__init__.py` imports `__version__`
- [x] T008 Subpackage `__init__.py` files
- [x] T009 `.env-example` (no secrets) (R11)
- [x] T010 CI workflow pins Python 3.13 via setup-python@v5 (R13)
- [x] T011 `LICENSE` (MIT)
- [x] T012 `scripts/check_file_lines.py` raw+logical ≤150 (R7)
- [x] T013 `scripts/check_version_sync.py` (R5)
- [x] T014 `config/runtime.json` with version mirror
- [x] T015 `uv sync --dev` green; ruff + guards green
- [ ] T016 `config/game.json` — grid_size, max_moves, num_games, max_barriers, vision_radius, diagonal, thief_first, start, seed, scoring (R4/H5)
- [ ] T017 `config/llm.json` — provider, claude_cli{bin,model,args,timeout}, ollama{base_url,model,timeout}, temperature, max_tokens (R4/H9)
- [ ] T018 `config/mcp.json` — cop{host,port,path}, thief{host,port,path}, transport=http, auth{scheme=bearer,token_env} (R4/H1/H8)
- [ ] T019 `config/report.json` — sender, recipient, gmail{creds_env,token_env,scopes}, smtp{host,port,user_env,pass_env,from} (R4/H7)
- [ ] T020 `config/gatekeeper.json` — per-service rate limits, budgets, ledger path (R3/R4)
- [ ] T021 Add team metadata block (names, IDs, group, repo) to `config/report.json`
- [ ] T022 `pre-commit` config (ruff + line guard) — optional dev nicety
- [ ] T023 `tests/conftest.py` — shared fixtures (tmp config, fake clock, seeds)
- [ ] T024 `tests/fixtures/config/*.json` — minimal valid configs for tests
- [ ] T025 Commit M0 config layer

## M1 — shared core

### shared/paths
- [ ] T026 Test `Paths` resolves repo root, reports, transcripts, ledger
- [ ] T027 Implement `shared/paths.py`
- [ ] T028 Test paths create-on-demand (mkdir parents) behaviour
- [ ] T029 Ruff + line-check M1 paths

### shared/config_models + config loader
- [ ] T030 Test `GameConfig` dataclass parses all fields + defaults
- [ ] T031 Test `LlmConfig`, `McpConfig`, `ReportConfig`, `GateConfig`, `RuntimeConfig`
- [ ] T032 Implement `shared/config_models.py` (frozen dataclasses)
- [ ] T033 Test `load_config()` reads a config dir → `Config`
- [ ] T034 Test loader raises on missing required key (clear message)
- [ ] T035 Test loader rejects unknown grid sizes ≤0 / max_moves ≤0
- [ ] T036 Test loader env-substitution for `*_env` token references
- [ ] T037 Implement `shared/config.py`
- [ ] T038 Test config `version` field matches `__version__` (R5)
- [ ] T039 Ruff + line-check config layer

### shared/logging
- [ ] T040 Test `get_logger()` returns configured logger, level from config
- [ ] T041 Implement `shared/logging_config.py`
- [ ] T042 Test log records carry component name
- [ ] T043 Ruff + line-check logging

### shared/auth (H8)
- [ ] T044 Test `TokenStore` reads bearer tokens from env per role
- [ ] T045 Test `verify_bearer()` accepts correct, rejects wrong/missing token
- [ ] T046 Test token revocation (rotating env invalidates old)
- [ ] T047 Implement `shared/auth.py`
- [ ] T048 Ruff + line-check auth

### shared/gatekeeper types + rate limiter
- [ ] T049 Test `ServiceKind` enum covers subprocess/http/smtp/google
- [ ] T050 Test `GateEvent`/`GateResult` dataclasses serialise to ledger dict
- [ ] T051 Implement `shared/gatekeeper_types.py`
- [ ] T052 Test `RateLimiter` token-bucket: allows N, blocks N+1, refills
- [ ] T053 Test rate limits read from `GateConfig` per service (R4)
- [ ] T054 Implement `shared/rate_limiter.py`
- [ ] T055 Ruff + line-check gate types + limiter

### shared/gatekeeper (R3 — the wired gate)
- [ ] T056 Test gate `run_subprocess` calls injected runner + records event
- [ ] T057 Test gate `http` calls injected client + records event
- [ ] T058 Test gate `smtp` send routes through + records
- [ ] T059 Test gate `google_send` routes through + records
- [ ] T060 Test gate enforces rate limit (raises/blocks when exceeded)
- [ ] T061 Test gate enforces budget cap from config
- [ ] T062 Test ledger is appended (JSON) and flushable to disk
- [ ] T063 Test gate redacts secrets from recorded events
- [ ] T064 Implement `shared/gatekeeper.py` (ApiGatekeeper)
- [ ] T065 Test gate is the single construction point (factory from Config)
- [ ] T066 Ruff + line-check gatekeeper
- [ ] T067 Commit M1 shared core

## M2 — domain (pure game logic)

### domain/geometry
- [ ] T068 Test `Position` equality, hashing, repr
- [ ] T069 Test 8 `Direction`s map to correct (dr,dc) deltas (incl diagonals) (H5)
- [ ] T070 Test `step(pos,dir)` returns neighbour
- [ ] T071 Test diagonal step changes both row and col
- [ ] T072 Implement `domain/geometry.py`
- [ ] T073 Test direction parsing from name (N, NE, ...)
- [ ] T074 Ruff + line-check geometry

### domain/grid
- [ ] T075 Test `Grid` stores dims from config (default 5×5, configurable) (H5)
- [ ] T076 Test `in_bounds()` true inside, false outside (no wrapping) (H5)
- [ ] T077 Test barrier add/contains/count
- [ ] T078 Test barrier cap awareness (grid stores set; cap enforced in rules)
- [ ] T079 Test grid rejects negative/zero dims
- [ ] T080 Implement `domain/grid.py`
- [ ] T081 Test grid with non-square dims (e.g. 4×3) (H5)
- [ ] T082 Ruff + line-check grid

### domain/pieces
- [ ] T083 Test `Role` enum COP/THIEF
- [ ] T084 Test `Piece` holds role + position; move updates position
- [ ] T085 Implement `domain/pieces.py`
- [ ] T086 Ruff + line-check pieces

### domain/actions
- [ ] T087 Test `Move` carries a Direction
- [ ] T088 Test `PlaceBarrier` is cop-only marker
- [ ] T089 Test action validation rejects thief barrier (H6)
- [ ] T090 Test action equality/repr for logging
- [ ] T091 Implement `domain/actions.py`
- [ ] T092 Ruff + line-check actions

### domain/observation (Dec-POMDP partial observability) (H6)
- [ ] T093 Test agent sees own position always
- [ ] T094 Test agent sees opponent only within vision_radius
- [ ] T095 Test agent sees barriers within vision_radius
- [ ] T096 Test observation hides opponent when out of range (None)
- [ ] T097 Test observation is NL-renderable summary (no full board leak)
- [ ] T098 Test vision_radius read from config (R4)
- [ ] T099 Implement `domain/observation.py`
- [ ] T100 Test observation on 2×2 (everything visible) vs 5×5 (partial)
- [ ] T101 Ruff + line-check observation

### domain/rules
- [ ] T102 Test legal move stays in bounds
- [ ] T103 Test illegal move into wall rejected
- [ ] T104 Test illegal move into barrier rejected (H6)
- [ ] T105 Test diagonal moves allowed (H5)
- [ ] T106 Test cop barrier legal when count < max (H6)
- [ ] T107 Test cop barrier illegal at max (5) (H6)
- [ ] T108 Test barrier placed on current cell counts as a move (H6)
- [ ] T109 Test thief cannot place barrier (H6)
- [ ] T110 Test `apply()` returns new state (immutability) 
- [ ] T111 Implement `domain/rules.py`
- [ ] T112 Test apply updates move counter + turn
- [ ] T113 Ruff + line-check rules

### domain/terminal
- [ ] T114 Test capture: cop on thief cell → cop wins (H6)
- [ ] T115 Test thief survives max_moves → thief wins (H6)
- [ ] T116 Test thief forced into barrier (no legal move) → cop wins (H6)
- [ ] T117 Test cop entering own barrier → thief wins (H6)
- [ ] T118 Test non-terminal mid-game returns None
- [ ] T119 Implement `domain/terminal.py`
- [ ] T120 Ruff + line-check terminal

### domain/scoring (config-driven) (H5)
- [ ] T121 Test cop-win → cop 20 / thief 5 (from config)
- [ ] T122 Test thief-win → thief 10 / cop 5 (from config)
- [ ] T123 Test scoring reads table from config, not hardcoded (R10)
- [ ] T124 Test `aggregate()` sums 6 sub-games
- [ ] T125 Test aggregate max 90 / min 30 sanity (3 cop + 3 thief) 
- [ ] T126 Implement `domain/scoring.py`
- [ ] T127 Ruff + line-check scoring

### domain/state
- [ ] T128 Test `GameState` initial positions from config/seed
- [ ] T129 Test state tracks positions, barriers, move#, whose-turn
- [ ] T130 Test state reset between sub-games
- [ ] T131 Test state clone/immutability for apply
- [ ] T132 Test thief-first turn order (H6)
- [ ] T133 Implement `domain/state.py`
- [ ] T134 Ruff + line-check state

### domain/records
- [ ] T135 Test `MoveRecord` captures before/after pos, action, NL msg, barriers-left (logging req)
- [ ] T136 Test `SubGameResult` captures winner, scores, move-count, log
- [ ] T137 Test `GameResult` accumulates 6 sub-games + totals
- [ ] T138 Test records serialise to JSON-ready dict
- [ ] T139 Implement `domain/records.py`
- [ ] T140 Ruff + line-check records
- [ ] T141 Integration: scripted 2×2 sub-game reaches capture deterministically (H6)
- [ ] T142 Integration: scripted thief-survives sub-game on 5×5 seed
- [ ] T143 Integration: barrier-trap scenario ends correctly
- [ ] T144 Coverage check domain ≥95%
- [ ] T145 Commit M2 domain

## M3 — llm providers (client-side, mocked IO)

### llm/provider
- [ ] T146 Test `LLMProvider` protocol shape (`complete(prompt)->str`)
- [ ] T147 Implement `llm/provider.py`
- [ ] T148 Ruff + line-check provider

### llm/claude_cli (default, no API key) (H9)
- [ ] T149 Test builds `claude -p <prompt>` argv with model + args from config
- [ ] T150 Test calls Gatekeeper.run_subprocess (never raw subprocess) (R3)
- [ ] T151 Test parses stdout (json/text) into completion string
- [ ] T152 Test handles non-zero exit → raises clear error
- [ ] T153 Test honours timeout from config
- [ ] T154 Implement `llm/claude_cli.py`
- [ ] T155 Ruff + line-check claude_cli

### llm/ollama (local fallback) (H9)
- [ ] T156 Test POSTs to `/api/chat` with model from config
- [ ] T157 Test routes through Gatekeeper.http (R3)
- [ ] T158 Test parses ollama response → string
- [ ] T159 Test base_url from env/config (R4/R11)
- [ ] T160 Implement `llm/ollama.py`
- [ ] T161 Ruff + line-check ollama

### llm/factory
- [ ] T162 Test factory returns ClaudeCliProvider when provider=claude_cli
- [ ] T163 Test factory returns OllamaProvider when provider=ollama
- [ ] T164 Test factory raises on unknown provider
- [ ] T165 Implement `llm/factory.py`
- [ ] T166 Ruff + line-check factory

### llm/prompts (NL-only contract) (H2)
- [ ] T167 Test cop persona prompt includes role + objective
- [ ] T168 Test thief persona prompt includes role + objective
- [ ] T169 Test prompt **forbids coordinates/JSON**, demands free NL (H2)
- [ ] T170 Test prompt injects partial observation summary
- [ ] T171 Test prompt injects opponent's last NL message
- [ ] T172 Test prompt injects dialogue history window
- [ ] T173 Test prompt requests a single `MOVE:`/`BARRIER` tail token
- [ ] T174 Test prompt allows board-origin negotiation in NL (H2)
- [ ] T175 Implement `llm/prompts.py`
- [ ] T176 Ruff + line-check prompts

### llm/parser
- [ ] T177 Test extracts `MOVE: NE` → Direction
- [ ] T178 Test extracts `BARRIER` → PlaceBarrier (cop)
- [ ] T179 Test keeps message body (prose) separate from action token
- [ ] T180 Test rejects/falls back when no token found (safe default move)
- [ ] T181 Test parser ignores coordinates if model leaks them (strips from msg)
- [ ] T182 Test parser case-insensitive direction names
- [ ] T183 Implement `llm/parser.py`
- [ ] T184 Ruff + line-check parser
- [ ] T185 Coverage check llm ≥90%
- [ ] T186 Commit M3 llm

## M4 — MCP servers + client (FastMCP, HTTP) (H1/H3)

### mcp/mailbox
- [ ] T187 Test `Mailbox` enqueues outgoing NL message
- [ ] T188 Test `Mailbox` reads opponent messages in order
- [ ] T189 Test `Mailbox` stores latest pushed observation
- [ ] T190 Test `Mailbox` records latest chosen action
- [ ] T191 Test mailbox isolation between two roles
- [ ] T192 Implement `mcp/mailbox.py`
- [ ] T193 Ruff + line-check mailbox

### mcp/tools
- [ ] T194 Test `observe()` returns pushed partial observation (H3/H6)
- [ ] T195 Test `send_message(text)` stores NL message (H2)
- [ ] T196 Test `read_messages()` returns opponent NL queue (H2)
- [ ] T197 Test `act(intent)` records move/barrier
- [ ] T198 Test tools contain NO game rules + NO llm import (H3)
- [ ] T199 Implement `mcp/tools.py`
- [ ] T200 Ruff + line-check tools

### mcp/server_factory + bearer auth (H1/H8)
- [ ] T201 Test `make_server(role)` builds a FastMCP app
- [ ] T202 Test server registers the 4 tools
- [ ] T203 Test bearer middleware rejects missing/invalid token (H8)
- [ ] T204 Test bearer middleware accepts valid token (H8)
- [ ] T205 Test server binds host/port from config (H1/R4)
- [ ] T206 Test transport is HTTP, not STDIO (H1, lecture)
- [ ] T207 Implement `mcp/server_factory.py`
- [ ] T208 Ruff + line-check server_factory

### mcp/cop_server + thief_server (two separate servers) (H1)
- [ ] T209 Test cop server uses cop port + cop token
- [ ] T210 Test thief server uses thief port + thief token
- [ ] T211 Test the two servers are independent apps (separate processes) (H1)
- [ ] T212 Test `main()` honors `--port` override
- [ ] T213 Implement `mcp/cop_server.py`
- [ ] T214 Implement `mcp/thief_server.py`
- [ ] T215 Assert servers import no orchestrator/engine mutation (H3)
- [ ] T216 Ruff + line-check servers

### mcp/client transport
- [ ] T217 Test `McpClient` calls a tool via Gatekeeper.http (R3)
- [ ] T218 Test client adds bearer Authorization header (H8)
- [ ] T219 Test client targets correct server URL per role
- [ ] T220 Test client `observe/send/read/act` round-trips (FastMCP in-memory)
- [ ] T221 Test client handles tool error/timeout gracefully (orchestration maturity)
- [ ] T222 Implement `mcp/client.py`
- [ ] T223 Ruff + line-check client
- [ ] T224 Integration: in-memory FastMCP server + client exchange NL message
- [ ] T225 Coverage check mcp ≥88%
- [ ] T226 Commit M4 mcp

## M5 — orchestrator (the MCP client / game driver)

### orchestrator/dialogue
- [ ] T227 Test `DialogueLog` appends (role, message) turns
- [ ] T228 Test dialogue window returns last K messages
- [ ] T229 Test dialogue renders transcript text
- [ ] T230 Implement `orchestrator/dialogue.py`
- [ ] T231 Ruff + line-check dialogue

### orchestrator/agent_driver
- [ ] T232 Test driver pushes observation to that role's server (H6)
- [ ] T233 Test driver builds prompt from obs + opponent msg + history
- [ ] T234 Test driver calls LLM provider (mocked) (H3)
- [ ] T235 Test driver parses action + posts NL message via client (H2)
- [ ] T236 Test driver returns chosen Action to engine
- [ ] T237 Test driver falls back to safe move on LLM error (maturity)
- [ ] T238 Implement `orchestrator/agent_driver.py`
- [ ] T239 Ruff + line-check agent_driver

### orchestrator/turn_engine
- [ ] T240 Test thief driven first, then cop (H6)
- [ ] T241 Test engine applies validated actions to state
- [ ] T242 Test engine checks terminal after each half-turn (H6)
- [ ] T243 Test engine rejects illegal action → re-prompt or safe move
- [ ] T244 Test engine increments move counter correctly
- [ ] T245 Test engine records MoveRecord per half-turn (logging req)
- [ ] T246 Implement `orchestrator/turn_engine.py`
- [ ] T247 Ruff + line-check turn_engine

### orchestrator/subgame_runner
- [ ] T248 Test runs until capture (cop-win) (H6)
- [ ] T249 Test runs to max_moves → thief-win (H6)
- [ ] T250 Test produces `SubGameResult` with scores from config
- [ ] T251 Test enforces ≤25 moves cap (H6)
- [ ] T252 Test renders board each move (renderer injected)
- [ ] T253 Implement `orchestrator/subgame_runner.py`
- [ ] T254 Ruff + line-check subgame_runner

### orchestrator/game_runner
- [ ] T255 Test runs exactly 6 sub-games (config num_games) (H6/R4)
- [ ] T256 Test alternates roles across sub-games
- [ ] T257 Test accumulates scores into `GameResult`
- [ ] T258 Test resets board between sub-games
- [ ] T259 Test produces full game log for report
- [ ] T260 Implement `orchestrator/game_runner.py`
- [ ] T261 Ruff + line-check game_runner

### orchestrator/pipeline (autonomous) (H4)
- [ ] T262 Test init phase: load config, build gatekeeper/providers/clients
- [ ] T263 Test play phase: run game_runner unattended (no input) (H4)
- [ ] T264 Test report phase: build + send report (mocked) (H4/H7)
- [ ] T265 Test pipeline writes transcript + JSON artifacts
- [ ] T266 Test pipeline is fully autonomous (no prompt/input calls) (H4)
- [ ] T267 Test pipeline handles a server/LLM failure without manual step (maturity)
- [ ] T268 Implement `orchestrator/pipeline.py`
- [ ] T269 Ruff + line-check pipeline
- [ ] T270 Integration: full seeded pipeline with fake LLM → deterministic GameResult (H4)
- [ ] T271 Integration: assert dialogue is NL (no coordinate tuples) (H2)
- [ ] T272 Coverage check orchestrator ≥88%
- [ ] T273 Commit M5 orchestrator

## M6 — report + email (H7)

### report/builder
- [ ] T274 Test report JSON has all 6 sub-game results
- [ ] T275 Test report includes per-game + total scores
- [ ] T276 Test report includes timestamp (injected clock) 
- [ ] T277 Test report includes GitHub link + team names + IDs (H7)
- [ ] T278 Test report includes server URLs + config snapshot
- [ ] T279 Test report is valid parseable JSON (H7)
- [ ] T280 Implement `report/builder.py`
- [ ] T281 Ruff + line-check builder

### report/sender protocol + selection
- [ ] T282 Test `ReportSender` protocol (`send(report)`)
- [ ] T283 Test `make_sender()` returns Gmail when sender=gmail
- [ ] T284 Test `make_sender()` returns SMTP when sender=smtp
- [ ] T285 Test selection raises on unknown sender
- [ ] T286 Implement `report/sender.py`
- [ ] T287 Ruff + line-check sender

### report/gmail_sender (OAuth) (H7)
- [ ] T288 Test builds MIME message to recipient from config
- [ ] T289 Test routes send through Gatekeeper.google_send (R3)
- [ ] T290 Test loads OAuth token from env path (R11)
- [ ] T291 Test raises clear error when creds absent (documented)
- [ ] T292 Implement `report/gmail_sender.py` (mock googleapiclient in tests)
- [ ] T293 Ruff + line-check gmail_sender

### report/smtp_sender (fallback) (H7)
- [ ] T294 Test builds email, routes through Gatekeeper.smtp (R3)
- [ ] T295 Test reads host/port/user/pass from env (R11)
- [ ] T296 Test STARTTLS path invoked (mocked)
- [ ] T297 Implement `report/smtp_sender.py`
- [ ] T298 Ruff + line-check smtp_sender
- [ ] T299 Integration: build report → send via mocked sender → ledger records (H7)
- [ ] T300 Coverage check report ≥90%
- [ ] T301 Commit M6 report

## M7 — GUI (ASCII default + optional Tk)

### gui/renderer
- [ ] T302 Test `Renderer` protocol (`render(state, dialogue)`) 
- [ ] T303 Test `make_renderer()` returns Ascii by default
- [ ] T304 Test `make_renderer()` returns Tk when gui.enabled (import-guarded)
- [ ] T305 Implement `gui/renderer.py`
- [ ] T306 Ruff + line-check renderer

### gui/ascii_renderer (tested)
- [ ] T307 Test renders grid with C/T/#/. glyphs
- [ ] T308 Test shows move counter + barriers-left
- [ ] T309 Test shows last NL messages under the board (H2 visibility)
- [ ] T310 Test renders non-square grids
- [ ] T311 Test output captured to transcript string
- [ ] T312 Implement `gui/ascii_renderer.py`
- [ ] T313 Ruff + line-check ascii_renderer

### gui/tk_renderer (flagged, omitted from cov)
- [ ] T314 Implement `gui/tk_renderer.py` (guarded import; no-op if no display)
- [ ] T315 Test Tk renderer import-guarded does not crash headless
- [ ] T316 Ruff + line-check tk_renderer
- [ ] T317 Commit M7 gui

## M8 — SDK façade + CLI (R1)

### sdk/facade
- [ ] T318 Test `ParleySDK` constructs from a config dir
- [ ] T319 Test `ParleySDK.play()` runs full pipeline (mocked) → GameResult (R1/H4)
- [ ] T320 Test `ParleySDK.report_only()` rebuilds+sends from a saved result
- [ ] T321 Test `ParleySDK.deploy_info()` returns server URLs + auth scheme (H8)
- [ ] T322 Test SDK owns the single Gatekeeper instance (R3)
- [ ] T323 Test all business logic reachable via SDK only (R1)
- [ ] T324 Implement `sdk/facade.py`
- [ ] T325 Ruff + line-check facade

### cli
- [ ] T326 Test `parley version` prints single-source version (R5)
- [ ] T327 Test `parley play` invokes SDK.play (mocked)
- [ ] T328 Test `parley serve-cop` / `serve-thief` start servers (mocked)
- [ ] T329 Test `parley report` invokes SDK.report_only
- [ ] T330 Test CLI bad command → usage + non-zero exit
- [ ] T331 Implement `sdk/../cli_handlers.py`
- [ ] T332 Implement `cli.py` (argparse → handlers → SDK)
- [ ] T333 Ruff + line-check cli
- [ ] T334 Integration: `parley play` end-to-end mocked → artifacts written (H4)
- [ ] T335 Coverage check sdk+cli ≥88%
- [ ] T336 Commit M8 sdk+cli

## M9 — Gatekeeper meta-test (R3)

- [ ] T337 Test greps `src/parley` for `import subprocess` outside gatekeeper → none
- [ ] T338 Test greps for `import httpx`/`requests` outside gatekeeper + providers-via-gate
- [ ] T339 Test greps for `import smtplib` outside gatekeeper
- [ ] T340 Test greps for `googleapiclient` outside gatekeeper
- [ ] T341 Test asserts mcp server modules import no llm provider (H3)
- [ ] T342 Test asserts every external call site references the gatekeeper
- [ ] T343 Implement `tests/unit/test_gatekeeper_meta.py`
- [ ] T344 Fix any escape found; re-run
- [ ] T345 Commit M9 meta-test

## M10 — deploy + run scripts + sample artifacts

- [ ] T346 `scripts/serve_servers.py` — start cop+thief servers locally (HTTP)
- [ ] T347 Test serve script wires ports/tokens from config
- [ ] T348 `scripts/deploy_ngrok.py` — open two tunnels, print HTTPS URLs (H8)
- [ ] T349 Test deploy script builds ngrok cmd via Gatekeeper subprocess (mocked)
- [ ] T350 `scripts/run_game.py` — thin SDK.play wrapper writing artifacts
- [ ] T351 Test run_game writes transcript + report JSON
- [ ] T352 `scripts/make_sample_run.py` — deterministic fake-LLM run → committed artifacts
- [ ] T353 Generate `reports/sample_report.json` (committed proof) (H7)
- [ ] T354 Generate `reports/transcripts/sample_run.md` (NL dialogue proof) (H2)
- [ ] T355 Generate ASCII board frames `reports/transcripts/sample_run.txt`
- [ ] T356 Test sample artifacts are valid + NL-only (no coordinates) (H2)
- [ ] T357 `scripts/capture_cloud_proof.md` — how to capture ngrok proof (H8)
- [ ] T358 Ruff + line-check scripts
- [ ] T359 Commit M10 scripts + artifacts

## M11 — diagrams + ADRs + per-mechanism PRDs (H10)

- [ ] T360 `diagrams/class_diagram.mmd` (R2/H10)
- [ ] T361 `diagrams/block_diagram.mmd` — system/MCP architecture (H10)
- [ ] T362 `diagrams/sequence_diagram.mmd` — MCP turn sequence (H10)
- [ ] T363 Validate Mermaid renders (syntax check)
- [ ] T364 ADR-001 Client/Server split + LLM placement (H3)
- [ ] T365 ADR-002 HTTP over STDIO
- [ ] T366 ADR-003 Claude-CLI provider + Ollama fallback (H9)
- [ ] T367 ADR-004 Partial-observability model (H6)
- [ ] T368 ADR-005 NL-only dialogue contract (H2)
- [ ] T369 ADR-006 Wired Gatekeeper + meta-test (R3)
- [ ] T370 ADR-007 Pluggable report sender (H7)
- [ ] T371 ADR-008 ngrok + Bearer deploy (H8)
- [ ] T372 ADR-009 Mock-everything tests (R9)
- [ ] T373 ADR-010 RL deferral (H11)
- [ ] T374 `docs/prd/mech-game-engine.md`
- [ ] T375 `docs/prd/mech-mcp.md`
- [ ] T376 `docs/prd/mech-orchestration.md`
- [ ] T377 `docs/prd/mech-llm.md`
- [ ] T378 `docs/prd/mech-report.md`
- [ ] T379 `docs/prd/mech-deploy-security.md`
- [ ] T380 Commit M11 docs + diagrams

## M12 — README + finalize + run + push

- [ ] T381 README header + CI/python/tests/coverage/license badges
- [ ] T382 README §1 Dec-POMDP formal modelling (tuple) (H10)
- [ ] T383 README §2 architecture diagram embed + Client/Server explainer (H3/H10)
- [ ] T384 README §3 MCP sequence diagram embed (H10)
- [ ] T385 README §4 class diagram embed (R2/H10)
- [ ] T386 README §5 free-NL dialogue sample transcript (H2)
- [ ] T387 README §6 autonomous pipeline walkthrough (H4)
- [ ] T388 README §7 config-driven design table (H5/R4)
- [ ] T389 README §8 partial-observability discussion (H6)
- [ ] T390 README §9 report + Gmail/SMTP (H7) + sample artifact link
- [ ] T391 README §10 remote deploy + OAuth/Bearer security (H8)
- [ ] T392 README §11 cloud+Ollama LLM support (H9)
- [ ] T393 README §12 reproduce (uv sync, pytest, run) — no keys needed (R9)
- [ ] T394 README §13 repo structure + engineering standards (R1–R13)
- [ ] T395 README §14 orchestration challenges + self-grade note
- [ ] T396 Final `uv run ruff check .` clean (R8)
- [ ] T397 Final `uv run python scripts/check_file_lines.py` green (R7)
- [ ] T398 Final `uv run python scripts/check_version_sync.py` green (R5)
- [ ] T399 Final `uv run pytest` green, coverage ≥85% (R6/R9)
- [ ] T400 Run `uv run parley play` locally → fresh artifacts (H4)
- [ ] T401 Verify emailed-report path documented + sample committed (H7)
- [ ] T402 `scripts/fill_submission_pdf.py` → `uoh-sqak-ex06.pdf` (adapt fields)
- [ ] T403 Create PUBLIC GitHub repo `uoh-sqak-ex06`
- [ ] T404 Push main; confirm CI green badge (R13)
- [ ] T405 Verify repo public / shared with rmisegal@gmail.com (else auto-zero)
- [ ] T406 Final commit + tag v1.00

## M13 — extra hardening / coverage backfill (buffer to ≥500)

- [ ] T407 Edge: 2×2 grid full pipeline sanity (lecture "start small") 
- [ ] T408 Edge: 3×3 grid run
- [ ] T409 Edge: 4×3 non-square run
- [ ] T410 Edge: vision_radius=0 (blind) behaviour
- [ ] T411 Edge: vision_radius covers whole board (full obs)
- [ ] T412 Edge: max_barriers=0 (cop cannot block)
- [ ] T413 Edge: thief escapes every sub-game (all thief-wins) scoring
- [ ] T414 Edge: cop captures every sub-game (all cop-wins) scoring
- [ ] T415 Edge: tie-less invariant (no draw within a sub-game) (H6)
- [ ] T416 Edge: move at exactly move 25 boundary
- [ ] T417 Edge: capture on move 1
- [ ] T418 Edge: barrier placed then thief routes around
- [ ] T419 Edge: all 5 barriers form a trap
- [ ] T420 Edge: cop self-trap loss path
- [ ] T421 Test config hot values all overridable (grid/ports/scoring) (R10)
- [ ] T422 Test no module hardcodes 5/25/6/20/10 literals (grep) (R10)
- [ ] T423 Test ports differ for cop vs thief (H1)
- [ ] T424 Test bearer tokens differ for cop vs thief (H8)
- [ ] T425 Test ledger persists across a full run
- [ ] T426 Test rate-limit breach is logged, not crashed
- [ ] T427 Test budget cap stops further LLM calls gracefully
- [ ] T428 Test transcript redacts no NL (full dialogue retained for disputes)
- [ ] T429 Test report timestamp deterministic under injected clock
- [ ] T430 Test seed reproducibility: same seed → identical GameResult
- [ ] T431 Test different seed → different start positions
- [ ] T432 Test observation NL summary contains no raw coordinates (H2)
- [ ] T433 Test prompt context truncation keeps last opponent msg
- [ ] T434 Test parser handles multi-line prose + trailing token
- [ ] T435 Test agent_driver retries once on parse failure
- [ ] T436 Test turn_engine logs barriers-left each cop turn
- [ ] T437 Test subgame_runner stops immediately on capture
- [ ] T438 Test game_runner role assignment 3 cop / 3 thief
- [ ] T439 Test pipeline emits exactly one email (H7)
- [ ] T440 Test pipeline transcript lists all 6 sub-games
- [ ] T441 Test SDK.play idempotent re: fresh state per call
- [ ] T442 Test CLI `--config` dir override
- [ ] T443 Test CLI `--gui` flag toggles renderer
- [ ] T444 Test CLI `--provider ollama` override (H9)
- [ ] T445 Test logging level honored from config
- [ ] T446 Test gatekeeper factory single instance reused
- [ ] T447 Test mcp client closes transport cleanly
- [ ] T448 Test server factory rejects unknown role
- [ ] T449 Test mailbox thread-safe enqueue (basic)
- [ ] T450 Test observation symmetric for both roles
- [ ] T451 Test scoring totals match sum of sub-games
- [ ] T452 Test records JSON round-trips (load == dump)
- [ ] T453 Test report schema documented matches builder output
- [ ] T454 Test gmail sender base64-url encodes MIME
- [ ] T455 Test smtp sender quits connection (mocked)
- [ ] T456 Test ascii renderer stable snapshot (golden)
- [ ] T457 Test renderer handles barriers glyph
- [ ] T458 Test deploy_ngrok parses tunnel URLs (mocked stdout)
- [ ] T459 Test serve script binds both ports distinctly
- [ ] T460 Test sample-run script deterministic output
- [ ] T461 Coverage backfill any module <85%
- [ ] T462 Remove dead code / unused imports (ruff)
- [ ] T463 Docstring pass on public surfaces
- [ ] T464 Type-hint pass on public functions
- [ ] T465 Final file-line audit (raw+logical) all files (R7)
- [ ] T466 Confirm no secret literals anywhere (scan) (R11)
- [ ] T467 Confirm `.env` git-ignored, `.env-example` present (R11)
- [ ] T468 Confirm uv.lock tracked, no requirements.txt (R12)
- [ ] T469 Confirm CI workflow green on push (R13)
- [ ] T470 Confirm continuous commit history spread (R13)
- [ ] T471 Self-grade note (default 85) in README/submission
- [ ] T472 Cross-check every H-gate has a test or artifact
- [ ] T473 Cross-check every R-rule has enforcement
- [ ] T474 ADR index page links all ADRs
- [ ] T475 PRD index links all per-mechanism PRDs
- [ ] T476 Diagrams referenced from README render correctly
- [ ] T477 Sample transcript embedded/linked in README (H2)
- [ ] T478 Verify pipeline runs with provider=ollama config (mocked) (H9)
- [ ] T479 Verify pipeline runs with sender=smtp config (mocked) (H7)
- [ ] T480 Verify deploy doc covers Cloudflare alt (H8)
- [ ] T481 Verify partial-observability explained with example in README (H6)
- [ ] T482 Verify scoring table in README matches config (H5)
- [ ] T483 Verify turn-order (thief-first) documented (H6)
- [ ] T484 Verify barrier rules documented (H6)
- [ ] T485 Verify "LLM in client, not server" stated + diagrammed (H3)
- [ ] T486 Verify two-separate-servers stated + diagrammed (H1)
- [ ] T487 Verify autonomous "no manual steps" claim demonstrated (H4)
- [ ] T488 Verify Gmail-API mandatory path present (H7)
- [ ] T489 Verify free-NL "no coordinates" enforced by test (H2)
- [ ] T490 Verify config-driven "nothing hardcoded" by test (R10/H5)
- [ ] T491 Final ruff + line + version + pytest all green together
- [ ] T492 Generate fresh sample artifacts from final code
- [ ] T493 Write CHANGELOG / version bump note (R5)
- [ ] T494 Tag and prepare submission PDF
- [ ] T495 Push to public GitHub
- [ ] T496 Confirm repo accessible (public) 
- [ ] T497 Confirm CI badge green post-push
- [ ] T498 Final review against PRD acceptance criteria §5
- [ ] T499 Final review against grader Path D (no keys/servers)
- [ ] T500 Mark Todo complete; lifecycle done
- [ ] T501 Buffer: address any review nit found in T498
- [ ] T502 Buffer: address any review nit found in T499
- [ ] T503 Buffer: re-run full suite one last time
- [ ] T504 Buffer: confirm memory + submission metadata correct

## M14 — gap-closing tasks (from Phase 4 critical verify)

- [ ] T505 `scripts/gmail_oauth_setup.py` — one-time OAuth consent → token.json (H7 real path); documented, not run in tests
- [ ] T506 Test gmail_oauth_setup builds flow from creds path (mocked google_auth_oauthlib)
- [ ] T507 Integration: start a REAL uvicorn FastMCP cop server on an ephemeral port; client round-trips a tool with bearer auth (proves H1 HTTP + H8 auth, not just in-memory)
- [ ] T508 Integration: real server rejects a request with a bad bearer token (H8)
- [ ] T509 Expose an MCP **resource** (`game://rules`) on each server (tools AND resources per spec) (H1/H3)
- [ ] T510 Test the rules resource returns config-derived rules text (no LLM, no mutation) (H3)
- [ ] T511 Commit `reports/sample_gate_ledger.json` as wired-Gatekeeper proof (R3); adjust .gitignore to allow the sample
- [ ] T512 Test the committed sample ledger has gate events for llm + mcp + report (R3)
- [ ] T513 `claude` CLI preflight in ClaudeCliProvider: clear, actionable error if bin/subscription missing (H9 robustness)
- [ ] T514 Test preflight raises documented error when bin absent (mocked which)
- [ ] T515 Pin default report recipient `rmisegal+uoh26b@gmail.com` in `config/report.json` (spec) (H7)
- [ ] T516 Test report builder addresses the configured recipient (H7)
- [ ] T517 Persist a per-move **dispute log** file `reports/transcripts/<run>/moves.jsonl` (lecture: mandatory logs — timestamp, positions, action, NL msg, barriers-left)
- [ ] T518 Test dispute log line schema is complete + parseable
- [ ] T519 README: add a "logs as evidence" note + link the dispute log (lecture)
- [ ] T520 Cross-check coverage matrix `docs/verify-coverage-matrix.md` — every PRD demand → task(s); no orphans
