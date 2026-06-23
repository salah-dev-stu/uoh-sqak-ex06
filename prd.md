# PRD — `parley`: Dual AI Agent Conversation via MCP Servers (EX06)

> **Course** 203.3763 *Orchestration of AI Agents* · University of Haifa · Spring 2026 · Dr. Yoram Segal
> **Team** Salah Qadah (323039974) · Andalus Kalash (211435797) · **Group** `uoh-sqak`
> **Deadline** Fri 3 July 2026, 23:59 (Asia/Jerusalem) · Moodle `id=282206`
> **Status** Approved — drives `Plan.md` → `Todo.md` → execution.

---

## 1. Vision & one-sentence mission

Build a **fully autonomous, distributed multi-agent pipeline** in which two LLM
agents — a **Cop** and a **Thief** — play a turn-based *cops & robbers* chase on a
**partially-observable, config-driven grid**, **each on its own FastMCP server**,
**conversing in free natural language**, from one-command init through **six
sub-games** to an **automatically emailed summary report**, with **zero manual
intervention at runtime**.

## 2. What is graded (the north star)

Per Dr. Segal (Lecture 09), the grading hierarchy is explicit and we optimise to it:

| Priority | Dimension | Our commitment |
|---|---|---|
| 1 (highest) | **Pipeline works end-to-end** (init → 6 games → emailed report, autonomous) | One command runs the whole thing; a recorded run is committed as proof. |
| 2 | **Communication is free natural language** | Agents exchange meaningful NL messages that reference prior turns and drive moves; **never** coordinates/JSON tuples. |
| 3 | **Orchestration maturity** (Client vs Server, LLM placement, error handling) | LLM in the MCP client; two stateless FastMCP servers; graceful timeout/retry. |
| 4 | Modular, configurable architecture | Everything in config; SDK + Gatekeeper; ≤150-line modules. |
| 5 | Cloud deploy & security | ngrok HTTPS + Bearer-token auth; no embedded secrets. |
| 6 (lowest) | Game strategy / RL | Heuristic-plus-LLM agents; RL explicitly **out of scope** (optional only). |

**Design rule:** when a trade-off pits "smarter strategy" against "cleaner pipeline
or richer dialogue", we always choose the pipeline/dialogue.

## 3. In scope (the bullets)

**A. Distributed MCP architecture**
- A1. **Two separate FastMCP servers**, one per agent (Cop, Thief), on **different
  ports**, **HTTP transport** (not STDIO — Dr. Segal insists, even locally). → *H1*
- A2. The **MCP client / orchestrator holds the LLM** (Claude CLI default, Ollama
  fallback); **servers expose tools/resources only**, no LLM inside. → *H3*
- A3. Each server exposes a small tool surface: `observe`, `send_message`,
  `read_messages`, `act` (move / place-barrier). Servers are **stateless re: game
  rules** — they hold only a transient per-turn mailbox + the partial observation
  the orchestrator pushes. → *H1, H3*

**B. The game (config-driven, partially observable)**
- B1. 2D grid, **default 5×5**, size **from config, never hardcoded**; no wrapping,
  walls at edges. → *H5*
- B2. **8-direction movement including diagonals**. → *H5*
- B3. **Sub-game ≤ 25 moves**, **turn-based, Thief moves first**, then Cop. → *H6*
- B4. A **game = 6 consecutive sub-games**; scores accumulate. → *H6*
- B5. **Partial observability (Dec-POMDP):** each agent sees only a vision-limited
  local region; it learns the opponent's whereabouts **only from NL messages**. → *H6*
- B6. **Barriers:** Cop may place up to **5 per sub-game** instead of moving; barriers
  block both agents; entering one is fatal (Thief→capture, Cop→Thief wins). → *H5/H6*
- B7. **Scoring from config:** Cop-win 20 / Thief-win 10 / Cop-loss 5 / Thief-loss 5. → *H5*
- B8. **Win conditions:** Cop on Thief's cell = capture (Cop wins); Thief survives 25 = Thief wins. → *H6*

**C. Free natural-language dialogue**
- C1. Agents exchange **free-text** messages (intent, observation, bluff) that
  **reference the opponent's prior message**; no rigid protocol. → *H2*
- C2. Each agent **decodes** the opponent's NL message, **infers** opponent position
  under partial observability, and **translates** that into a grid move. → *H2*
- C3. The board origin / framing is **negotiable in NL by the agents**, not hardcoded. → *H2*

**D. Autonomous pipeline**
- D1. **One command** runs init → 6 sub-games → report, **no manual steps at runtime**. → *H4*
- D2. **Init:** load config, start both MCP servers, instantiate agents, place pieces,
  connect the LLM. → *H4*
- D3. **Play:** the turn loop runs unattended through all 6 sub-games. → *H4*
- D4. **Report:** aggregate results and email automatically (below). → *H4, H7*

**E. Reporting**
- E1. **Structured JSON report**: all 6 sub-game outcomes, per-game + total scores,
  timestamps, GitHub link, team names + IDs, server URLs, config snapshot. → *H7*
- E2. **Automated email** via a **pluggable sender**: **Gmail API (OAuth)** default,
  **SMTP fallback**; recipient from config. → *H7*
- E3. A **sample report artifact** + a **recorded sample run transcript** are committed
  as offline proof. → *H7, grader Path D*

**F. Remote deployment & security**
- F1. Servers **deployable remotely** via **ngrok** (free; Cloudflare Tunnel documented
  as a no-session-limit alternative); public **HTTPS**. → *H8*
- F2. **Bearer-token auth** on every server URL (not passwords); **revocable**; tokens
  from env, never committed. → *H8*
- F3. **Cloud execution demonstrated** at submission (deploy script + captured proof). → *H8*

**G. LLM flexibility**
- G1. **Cloud + local** both supported via config: **Claude CLI subscription** (default,
  no API key) and **Ollama** (local, free, small models). → *H9*

**H. Visualization & docs**
- H1. **ASCII grid renderer** (default, always-on, feeds logs/README) **+ optional
  Tkinter GUI** behind a config flag. → *GUI (spec optional-recommended)*
- H2. **Class diagram + system/MCP architecture + MCP sequence diagram** (Mermaid),
  embedded in a **visual README** (Dec-POMDP modelling, orchestration challenges,
  proof-of-concept traces). → *H10*

**I. Optional / explicitly deferred**
- I1. **RL / tabular Q-learning** — recommended-only; **OUT OF SCOPE** for v1.00. A
  stub interface + ADR records the deliberate deferral. → *H11 (optional)*
- I2. **Bonus inter-team tournament — DECLINED by the user; NOT pursued.** → *H12 (declined)*

## 4. Non-functional requirements (standing rubric R1–R13)

| Ref | Requirement |
|---|---|
| R1 | All business logic behind a single public **SDK** entry (`ParleySDK`). |
| R2 | **OOP, no duplication**; class diagram submitted. |
| R3 | **Every external call** (LLM subprocess/HTTP, MCP HTTP, Gmail/SMTP, deploy) routes through one **wired `ApiGatekeeper`** (gates **and** records a ledger). A source-grep meta-test fails CI if anything escapes it. |
| R4 / R10 | **Zero hardcoded values** — grid, ports, moves, games, scoring, model ids, endpoints, recipient all in JSON config. |
| R5 | **Versioning** 1.00, +0.01/change, **single source** (`shared/version.py`) mirrored in config; sync test. |
| R6 | **TDD**; suite GREEN. |
| R7 | **≤150 lines/file — BOTH raw and logical** — across src, tests, scripts. |
| R8 | `ruff check` = 0. |
| R9 | `pytest --cov` **≥85%**, **fully mocked** (LLM + MCP transport + Gmail/SMTP) so the grader needs **no keys, no creds, no live servers** (Path D). |
| R11 | **Zero secrets**; `.env-example` + `os.environ.get`; `.env` git-ignored. |
| R12 | **`uv` only**; `uv.lock` tracked. |
| R13 | **Continuous commits** (spread over time) + **green Python-3.13 CI**. |

## 5. Acceptance criteria (Definition of Done)

1. `uv run pytest` → **all green, ≥85% coverage**, with **no** API key / creds / live server.
2. `uv run ruff check .` → clean; `check_file_lines.py` + `check_version_sync.py` → green.
3. `uv run parley play` runs the **full autonomous pipeline** locally end-to-end and
   writes a **transcript + JSON report** under `reports/`.
4. The committed sample run shows **free-NL dialogue** between Cop and Thief that
   references prior turns (not coordinates/JSON).
5. Two **separate FastMCP HTTP servers** start on distinct ports; the **LLM lives only
   in the client**; a meta-test proves no raw external call bypasses the Gatekeeper.
6. The report is **emailed** through the pluggable sender (mocked in tests; real path
   documented + a sample artifact committed).
7. **ngrok deploy script + Bearer-token auth** present; cloud-execution proof captured.
8. **Visual README** with class + architecture + MCP sequence diagrams and a sample
   transcript; **GitHub repo is public**; CI badge green.

## 6. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Tests requiring live LLM/servers/creds (grader can't run) | **Mock everything**; deterministic seed; commit recorded artifacts. |
| Agents leaking coordinates instead of NL | Prompt design forbids tuples; a test scans sample dialogue for raw-coordinate patterns. |
| LLM in the wrong layer | Architecture + meta-test assert servers import no LLM module. |
| Files creeping past 150 lines | Guard script in CI on raw **and** logical counts; layered decomposition keeps modules tiny. |
| Big-bang commit history (HW4 ding) | Commit per milestone, spread over time. |
| ngrok free-tier session limits | Bearer auth is tunnel-agnostic; Cloudflare Tunnel documented as fallback. |

## 7. Out of scope (explicit)

RL/Q-learning policy (deferred, stub only); the inter-team bonus tournament
(declined); winning-optimal strategy; a production web UI. These are recorded so the
verify phase does not flag them as gaps.
