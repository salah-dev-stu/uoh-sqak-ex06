# HW6 — Vibe Input (feed into Plan Mode → PRD)

> Read `CLAUDE.md` and `RULES.md` first. Backbone: `CONTEXT-lec09-and-spec.md` (the 17pp spec digested) + `CONTEXT-lecture-09.md` (spoken lecture, when added). Raw spec: `IDEA-raw.txt`. Source PDF in `../materials/`.

## Mission (one sentence)
Build a fully **autonomous, distributed multi-agent pipeline** where two LLM agents — a **Cop** and a **Thief** — play a turn-based "cops & robbers" chase on a partially-observable grid, each on **its own MCP server**, **conversing in free natural language**, from init through 6 sub-games to an **automatically emailed summary report** — with **zero manual intervention**.

## Title (spec cover)
**EX06 — Dual AI Agent Conversation via MCP Servers** · "Cops & Robbers chase between autonomous agents in a partially-observable environment" · Lecture L09 · Dr. Yoram Segal · v1.0.
Keywords: MCP (Model Context Protocol), AI-agent orchestration, distributed multi-agent, free natural-language communication, cops-and-robbers chase, partial observation / Dec-POMDP, FastMCP (Client vs Server), cloud + local LLM, Ollama, ngrok/Localtonet/Nginx, Prefect Cloud, OAuth security tokens, RL + tabular Q-learning (Bellman, epsilon-greedy), JSON config + reporting, Gmail API, GUI, game theory / prisoner's dilemma, teamwork + time pressure.

## Evaluation lens
Graded on the **communication + orchestration** of the agent pair — building a working distributed multi-agent system with **meaningful natural-language dialogue** and a **fully autonomous pipeline** — **NOT** on the game-playing strategy. A "dumb" heuristic agent that *talks well and runs autonomously* scores higher than an RL-optimized agent with weak communication/orchestration. Same standing rubric (R1–R13) + envelope rules as HW1–HW5.

## The system to build (spec §§3–7)
- **Two agents, two MCP servers.** Cop and Thief each run on their own FastMCP server (separate ports / deployable remotely). They exchange **free natural-language messages**; each must (1) decode the other's NL message, (2) infer the opponent's position from **partial observation**, (3) translate that into a grid move.
- **MCP Client = orchestrator + LLM.** The client/orchestrator holds the LLM connection (cloud API or local Ollama); the MCP servers expose **tools/resources only** (move, observe, report). Do NOT put the LLM inside the server.
- **Game engine (config-driven, a state machine).** Grid default 5×5 (size via config, not hardcoded), diagonal moves, partial observation. Sub-game ≤25 moves, turn-based (thief first). A game = 6 sub-games; scores accumulate.
- **Autonomous pipeline.** init → run 6 sub-games → aggregate → **email an automated summary report via Gmail API**. No manual steps anywhere.
- **Remote + secure.** Servers deployable via ngrok/Localtonet/Nginx/Prefect Cloud; **OAuth token auth** (not passwords); public HTTPS.
- **(Optional) RL extension.** Tabular Q-learning (Bellman, epsilon-greedy) — recommended only, not required.

## Open decisions (resolve with the user, then lock in PRD)
| # | Decision | Default / lean | Notes |
|---|---|---|---|
| 1 | Agent LLM | **Claude (cloud) via the Gatekeeper** | Local Ollama only with small models on the 8 GB M2; cloud is cleaner for the NL dialogue. Support both via config. |
| 2 | MCP framework | **FastMCP** (Python) | Spec-named. Client holds LLM, servers expose tools. |
| 3 | Remote deploy | **Design for remote (ngrok/Prefect) but default to localhost for tests**; document the remote path | Don't gate the grade on a live cloud server; tests mock the transport. |
| 4 | Transport for tests | **Mock the MCP network + LLM + Gmail** so `pytest` needs no key/servers (grader Path D) | Commit a recorded sample game + report artifact as offline proof. |
| 5 | Bonus | **DECLINED by user — do NOT pursue.** Focus 100% on the core assignment. (No inter-team game, no 6/26 bonus deadline; HW5 already submitted so the extension is moot.) | — |
| 6 | RL | Optional Q-learning module behind a flag | Recommended-only; don't let it overshadow the orchestration/communication core. |
| 7 | GUI / reporting | Per spec; automated Gmail summary mandatory | Config-driven. |

## What you MUST do
- Two FastMCP servers (one per agent) + an MCP-client orchestrator that holds the LLM.
- Agents communicate in **free natural language** (the central graded thing).
- Config-driven game engine (grid/moves/games from config, partial observation, ≤25 moves/sub-game, 6 sub-games, thief-first).
- **Fully autonomous** init→play→**emailed summary report (Gmail API)**.
- Remote-deployable design + OAuth security; cloud + Ollama LLM support.
- Class diagram + architecture diagram; rich README.
- Our standards: SDK + **Gatekeeper wrapping every external call** + uv + ruff-clean + pytest ≥85% green (mocked — no keys/servers) + **≤150 lines/file BOTH raw and logical** + version single-source + **GitHub CI green (pin Py 3.13)** + continuous commits + ≥500-task TODO + two approval gates.

## What you must NOT do
- Don't make the agents talk in coordinates/JSON tuples — it must be **free natural language**.
- Don't put the LLM inside the MCP server — the **client** holds it.
- Don't hardcode grid size/ports/model/endpoints — all via config.
- Don't require manual steps — the pipeline must be autonomous end-to-end.
- Don't gate tests/grade on live servers or API keys — mock them (Path D).
- Don't over-invest in game strategy/RL at the expense of communication + orchestration (that's what's graded).
- Don't leave the Gatekeeper decorative (HW3/4), don't desync version (HW4), don't let CI break on Py 3.14 (HW4 — pin 3.13), don't exceed 150 lines raw OR logical (HW5), don't big-bang commits (HW4).
