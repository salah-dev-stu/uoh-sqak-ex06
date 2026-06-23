# HW6 Worker Session — Orchestration of AI Agents (Course 203.3763)

## Who you are
You are the **HW6 worker session**. The orchestrator scaffolded this directory:
- **`CLAUDE.md`** (this file) — orientation, rules, workflow, gotchas
- **`IDEA.md`** — vibe input distilled from the HW6 spec; feed into Plan Mode → PRD
- **`RULES.md`** — grading rubric (R1–R13) + HW6-specific audit gates
- **`CONTEXT-lec09-and-spec.md`** — deep digest of the 17pp HW6 spec (= the Lec 09 summary, which IS the assignment definition). Your backbone.
- **`CONTEXT-lecture-09.md`** — digest of the spoken Lec 09 recording *(added when whisper finishes)*
- **`IDEA-raw.txt`** — raw spec text (verbatim quoting)
Source PDF: `../materials/hw6-spec-ex06-mcp-cops-robbers.pdf`.

## Course context
- Course 203.3763, University of Haifa, Spring 2026 · Lecturer Dr. Yoram Segal (`rmisegal@gmail.com`)
- **HW6 deadline: Friday 3 July 2026, 23:59** (Asia/Jerusalem) — Moodle `id=282206`. Opened 19 June.
- Late penalty −5/24h.
- **BONUS task: up to 10 pts on the final project.** Bonus deadline = **Friday 08:30 AM before the lecture** (earlier than the main deadline). ⚠️ **Submitting the bonus EXTENDS the HW5 deadline to 3 July 2026** — relevant since HW5 is due 6/26.

## What HW6 is — short version
**EX06 — Dual AI Agent Conversation via MCP Servers: a "Cops & Robbers" chase between two autonomous LLM agents on a partially-observable grid.** Two agents — **Cop** and **Thief** — play a turn-based chase on a configurable 2D grid (default 5×5), each running on **its own MCP (Model Context Protocol) server**, communicating in **free natural language** (never raw coordinates/JSON tuples). The whole pipeline is **autonomous**: init → play 6 sub-games → send an **automated summary report (Gmail API)** — zero manual intervention. **Graded on COMMUNICATION + ORCHESTRATION, not game strategy.** RL/Q-learning is *recommended-only*, NOT required.

## Core requirements (spec §§3–7 — see CONTEXT-lec09-and-spec.md for detail)
- **Game structure:** sub-game = one chase, **≤25 moves**, turn-based (**thief moves first**, then cop). game = **6 consecutive sub-games**, results accumulated + reported together.
- **Grid:** 2D, default **5×5**, **size configurable via config file (NOT hardcoded)**; coordinates; diagonal moves allowed; **partial observation** (Dec-POMDP — each agent sees only part of the board).
- **MCP architecture:** two **separate MCP servers** (one per agent, different ports), built with **FastMCP**. The **MCP *Client*/orchestrator holds the LLM** (cloud API or local **Ollama**); the **MCP *Servers* expose tools/resources only** — putting the LLM inside the server is an architecture violation.
- **Natural-language dialogue:** the agents must converse in **free natural language** — this is the central graded requirement.
- **Remote/distributed:** servers deployable remotely (ngrok / Localtonet / Nginx / **Prefect Cloud**) with **OAuth token-based auth** (not passwords), public HTTPS.
- **Autonomy:** fully automatic from init to the emailed summary report — no manual steps.
- **Config-driven:** grid size, max moves, num games, scoring, etc. all in JSON/YAML config.
- **Reporting:** automated summary via **Gmail API**. GUI if required by the spec.
- **(Optional) RL:** tabular Q-learning, Bellman, epsilon-greedy — recommended extension only.

## The BONUS (worth doing — see spec)
Up to **10 project points**; you may agree on additional game rules; dialogue must stay free natural language. Bonus due **Fri 08:30 before lecture**. **Submitting it extends the HW5 deadline to 3 July** — strong incentive given HW5.

## Workflow (Vibe Coding Lifecycle — mandatory)
`Idea → PRD → Plan → TODO (≥500 tasks) → Verify → Execute → README → Run → Push`. Two approval gates: stop after PRD, and after the full docs package, before code. **Continuous commits, spread over time** (HW4 lost a notch on one-day history; HW5 fixed this — keep it up).

## Standing hard rules (R1–R13 — grading agent enforces; see RULES.md)
| # | Rule |
|---|---|
| R1 | All business logic through an SDK layer |
| R2 | OOP, no duplication; **submit a class diagram** |
| R3 | Every external call (LLM, MCP server calls, Gmail API, Ollama) routes through a **Gatekeeper** — wired for real, not decorative (HW3/4 lesson) |
| R4 | Rate limits / game params / endpoints in JSON config, never hardcoded |
| R5 | Versioning 1.00 +0.01/change, **single source of truth** in code AND config (HW4: `__init__` imports VERSION from version.py) |
| R6 | TDD; suite GREEN — red suite fails outright |
| R7 | **≤150 lines per Python file — BOTH logical AND raw** (HW5 lesson: the user enforces raw too, not just logical) |
| R8 | `ruff check` zero failures |
| R9 | `pytest --cov` ≥ 85% — **mock the LLM + MCP network calls** so tests need no API key / no live servers (grader Path D) |
| R10 | Zero hardcoded values — grid size, ports, model ids, endpoints all via config |
| R11 | Zero secrets; `.env-example` + `os.environ.get`; `.env` git-ignored (OAuth tokens, Gmail creds, API keys) |
| R12 | `uv` only — no pip/venv/requirements.txt; `uv.lock` tracked |
| R13 | Continuous commits + **GREEN GitHub CI** — pin Python 3.13 via `actions/setup-python@v5` (HW4 trap) |

## HW6-specific gates (H1–Hn — see RULES.md for audit methods)
H1 Two separate MCP servers (FastMCP), one per agent · H2 Natural-language dialogue between agents (not coordinates/JSON) · H3 MCP Client holds the LLM; servers expose tools only · H4 Full autonomous pipeline init→6 sub-games→emailed report, no manual steps · H5 Config-driven grid/rules (nothing hardcoded) · H6 Partial-observation game logic (≤25 moves/sub-game, 6 sub-games, turn-based) · H7 Automated summary report (Gmail API) · H8 Remote-deployable + OAuth security · H9 Cloud + local (Ollama) LLM support · H10 Class diagram + architecture diagram · H11 (Optional) RL/Q-learning extension · H12 Bonus task (if attempted).

## Grader auth paths (carry over; keep all working)
The grader must evaluate WITHOUT your API keys, OAuth creds, or live MCP servers. So **tests mock the LLM, the MCP transport, and Gmail** (Path D = `uv run pytest`). Commit game logs / a recorded sample run / report artifacts so the pipeline's behavior is provable offline. Never gate the grade on live cloud servers.

## User-specific info (pre-filled — confirm, don't re-ask)
| Field | Value |
|---|---|
| Group code | `uoh-sqak` |
| Pair | Salah Qadah (ID 323039974) + Andalus Kalash (ID 211435797) |
| Repo (suggested) | `https://github.com/salah-dev-stu/uoh-sqak-ex06` (PUBLIC or shared w/ rmisegal@gmail.com — inaccessible = auto-zero) |
| Submission PDF | `uoh-sqak-ex06.pdf` via `scripts/fill_submission_pdf.py` (adapted) |
| Self-grade placeholder | 85 |
| Machine | macOS / Apple Silicon M2, 8 GB (Ollama local models must be small; cloud LLM for the agents is fine) |

**Ask the user at session start:** (1) cloud LLM provider for the agents (Claude default) vs local Ollama (small models only on 8 GB), (2) remote-deploy target (ngrok / Prefect Cloud / local-only-with-documented-remote-design), (3) whether to attempt the bonus (recommended — it adds ≤10 project pts AND extends the HW5 deadline), (4) GUI scope.

## First action — required reading order
1. `IDEA.md` · 2. `RULES.md` · 3. `CONTEXT-lec09-and-spec.md` · 4. `CONTEXT-lecture-09.md` (when present) · 5. `../hw5/README.md` + `../hw4/docs/PLAN.md` (patterns that worked: wired Gatekeeper, Python-3.13 CI, single-source version, mock-so-no-hardware tests, ≤150 both ways, visual README) · 6. `../hw1/feedback/Detailed_Feedback_Report.pdf`.
Then ask the 4 setup questions, enter Plan Mode, begin the lifecycle. **No code until PRD + PLAN + TODO are approved.**
