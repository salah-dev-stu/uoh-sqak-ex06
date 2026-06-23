# HW6 — Grading Rules & Audit Gates

> Two layers: the standing software rubric (R1–R13, same `software_submission_guidelines` PDF since HW1) + HW6-specific gates (H1–H12, from the EX06 spec). The grading agent runs automated checks on the committed repo and must be able to do so WITHOUT your API keys, OAuth creds, or live MCP servers — so tests mock the LLM/MCP/Gmail and a sample run is committed. High self-grade → pedantic pass; 85 is the honest default. Full rubric digest: `../hw2/CONTEXT-rubric-and-pdfs.md`.

## Standing software rubric (R1–R13)
| # | Rule | Audit |
|---|---|---|
| R1 | **SDK layer** — all business logic behind one public SDK entry | Code review |
| R2 | **OOP, no duplication**; **class diagram** submitted | Review + `diagrams/` |
| R3 | **Gatekeeper** — every external call (LLM, MCP server/tool calls, Gmail API, Ollama, deploy) routes through one `ApiGatekeeper`, **wired for real** (gates AND records). HW3/4 lesson: not decorative. | grep for raw network/LLM/subprocess calls outside it |
| R4 | **Config, not code** — grid size, ports, endpoints, model ids, scoring, num-games in JSON/YAML | config inspection |
| R5 | **Versioning** — 1.00, +0.01/change, **single source of truth** (`__init__` imports VERSION from `shared/version.py`; test asserts it) | version module + test |
| R6 | **TDD** — suite GREEN. Red suite fails. | `uv run pytest` |
| R7 | **≤150 lines/file — BOTH logical AND raw.** (HW5 lesson: the user enforces raw too; check `wc -l` and the logical count, all of src/tests/scripts.) | `scripts/check_file_lines.py` + raw `wc -l` |
| R8 | **`ruff check` = 0** | ruff |
| R9 | **`pytest --cov` ≥ 85%.** **Mock the LLM, the MCP transport, and Gmail** so tests need no key/servers (grader Path D). | pytest-cov |
| R10 | **Zero hardcoded values** — grid/ports/model/endpoints/scoring via config | review |
| R11 | **Zero secrets** — `.env-example` + `os.environ.get`; `.env` git-ignored (OAuth tokens, Gmail creds, API keys) | scan |
| R12 | **`uv` only** — no pip/venv/requirements.txt; `uv.lock` tracked | auto |
| R13 | **Continuous commits + GREEN GitHub CI** — pin **Python 3.13** via `actions/setup-python@v5`. Spread commits over time (not one big-bang day). | git history + Actions badge |

## HW6-specific gates (H1–H12)
| # | Gate | Pass = | Audit |
|---|---|---|---|
| H1 | **Two MCP servers (FastMCP)** | One per agent (Cop, Thief), separate ports, built on FastMCP. | code + run logs |
| H2 | **Free natural-language dialogue** | Agents exchange NL messages (not coordinates/JSON tuples); each decodes the other + infers position. **The central graded requirement.** | message logs / sample run |
| H3 | **Client holds the LLM; servers expose tools only** | LLM lives in the MCP client/orchestrator; servers = tools/resources. Putting LLM in the server fails. | architecture review |
| H4 | **Autonomous end-to-end pipeline** | init → 6 sub-games → emailed summary, **zero manual steps**. | run script + logs |
| H5 | **Config-driven game** | grid size, max moves, num games, scoring all from config (default 5×5, ≤25 moves/sub-game, 6 sub-games, thief-first, diagonal moves, partial observation). Nothing hardcoded. | config + engine review |
| H6 | **Partial-observation game logic** | Each agent sees only part of the board (Dec-POMDP); turn-based state machine; correct sub-game/game accounting. | engine + tests |
| H7 | **Automated summary report (Gmail API)** | Aggregated results emailed automatically at game end. | code + sample report artifact |
| H8 | **Remote-deployable + OAuth security** | Servers deployable (ngrok/Prefect/Nginx), token/OAuth auth (not passwords), public HTTPS design. | code + README + ADR |
| H9 | **Cloud + local (Ollama) LLM** | Both supported via config. | config + adapter |
| H10 | **Class + architecture diagrams** | Class diagram (R2) + a system/MCP architecture diagram, in the README. | `diagrams/` + README |
| H11 | **(Optional) RL/Q-learning** | If attempted: tabular Q-learning (Bellman, epsilon-greedy) behind a flag. Recommended-only. | code |
| H12 | **(Optional) Bonus task** | If attempted: agreed extra rules, NL dialogue preserved; submitted by Fri 08:30 deadline. Worth ≤10 project pts + extends HW5 deadline. | separate submission |

## Standing submission rules (spec §§1–8, identical to HW1–HW5)
1. One GitHub link for both members; **public OR shared with `rmisegal@gmail.com`** — inaccessible = auto-zero.
2. Each member **submits separately** on Moodle (`id=282206`); per-individual timestamp.
3. Group code `uoh-sqak` (8 chars, no spaces).
4. Fill the Word template, **don't alter fields**, save as PDF **`uoh-sqak-ex06.pdf`**, nothing extra. (`scripts/fill_submission_pdf.py` ready.)
5. **Self-grade** honest (default **85**).
6. **Late** −5/24h. Deadline **Fri 2026-07-03 23:59**. **Bonus** deadline Fri 08:30 before the lecture (earlier) — and submitting it extends the **HW5** deadline to 3 July.
7–8. Reserve-duty exceptions per spec.

## Reuse from HW4/HW5 (don't re-discover)
`scripts/check_file_lines.py` (+ enforce raw ≤150 too), the Python-3.13-pinned CI workflow, the wired Gatekeeper + meter pattern, the SDK façade, per-mechanism-PRD + ADR + class-diagram docs shape, the **mock-everything-so-no-keys/servers** test pattern (critical here — mock LLM + MCP transport + Gmail), and the **visual README** style (architecture + MCP sequence diagrams, sample game transcript). Copy/adapt; cite in ADRs.
