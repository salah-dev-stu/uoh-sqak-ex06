# Phase 4 — Critical Verification: PRD → Todo coverage matrix

Every PRD demand and grading gate mapped to the Todo task(s) that satisfy it.
**Verdict:** all gates covered after adding gap-closing tasks T505–T520. No orphan
requirements; no orphan out-of-scope items flagged as gaps.

## HW6 gates (H1–H12)

| Gate | Requirement | Tasks | Status |
|---|---|---|---|
| **H1** | Two separate FastMCP servers, distinct ports, **HTTP** | T201–T216, T206, T211, T423, **T507** (real HTTP server), T509 (resource) | ✅ |
| **H2** | Free **NL** dialogue, no coordinates/JSON | T167–T184, T195–T196, T271, T354–T356, T432, T477, T489 | ✅ |
| **H3** | LLM in client; servers tools/resources only | T198, T215, T234, T341, T485, T509–T510 | ✅ |
| **H4** | Autonomous init→6 games→report, no manual steps | T262–T270, T334, T400, T440, T487 | ✅ |
| **H5** | Config-driven grid/rules, nothing hardcoded | T016, T075–T081, T098, T121–T123, T388, T482, T490 | ✅ |
| **H6** | Partial obs, ≤25 moves, 6 games, thief-first, barriers | T093–T100, T102–T119, T132, T240, T251, T255, T481, T517 | ✅ |
| **H7** | Automated Gmail-API report (+SMTP fallback) | T274–T300, T353, T439, T488, **T505–T506**, T515–T516 | ✅ |
| **H8** | Remote deploy + OAuth/Bearer, public HTTPS | T044–T047, T203–T204, T218, T348, T371, T391, T424, T480, **T507–T508** | ✅ |
| **H9** | Cloud (Claude CLI) + local (Ollama) via config | T149–T165, T366, T392, T444, T478, T513–T514 | ✅ |
| **H10** | Class + architecture + sequence diagrams | T360–T363, T383–T385, T476 | ✅ |
| **H11** | RL optional — **deferred** (stub + ADR) | T373 (ADR-010), PRD §I1 | ✅ (deferred, recorded) |
| **H12** | Bonus — **declined** | PRD §I2 | ✅ (declined, not pursued) |

## Standing rules (R1–R13)

| Rule | Tasks | Status |
|---|---|---|
| **R1** SDK layer | T318–T324 | ✅ |
| **R2** OOP + class diagram | T360, T385 | ✅ |
| **R3** Wired Gatekeeper + meta-test + ledger | T056–T066, T150, T157, T289, T294, T337–T344, **T511–T512** | ✅ |
| **R4** Config not code | T016–T021, T053, T098, T123, T421 | ✅ |
| **R5** Version single-source | T006, T013, T038, T326, T398, T493 | ✅ |
| **R6** TDD green | all M1–M8 red-first pairs | ✅ |
| **R7** ≤150 raw+logical | T012, per-module line-checks, T397, T465 | ✅ |
| **R8** ruff = 0 | per-module, T396 | ✅ |
| **R9** cov ≥85 mocked | T399, T461, T499 | ✅ |
| **R10** zero hardcoded | T422, T490 | ✅ |
| **R11** no secrets | T009, T466–T467 | ✅ |
| **R12** uv only | T468 | ✅ |
| **R13** continuous commits + green CI | T010, T469–T470, T497 | ✅ |

## Spec bullets (PRD §3)

| Bullet | Tasks |
|---|---|
| A1–A3 MCP architecture | T187–T226, T507–T510 |
| B1–B8 game rules | T068–T144 |
| C1–C3 NL dialogue | T167–T184, T271 |
| D1–D4 autonomous pipeline | T262–T270 |
| E1–E3 reporting | T274–T301, T353–T356, T517 |
| F1–F3 deploy & security | T044–T048, T203–T204, T348–T357, T507–T508 |
| G1 cloud+local LLM | T146–T166, T478, T513–T514 |
| H1–H2 viz & docs | T302–T317, T360–T395 |
| I1–I2 RL/bonus deferred | T373, PRD §I |

## Lecture hardenings (CONTEXT-lecture-09)

| Hardening | Tasks |
|---|---|
| HTTP not STDIO (insisted) | T206, ADR-002 (T365), T507 |
| Cloud execution mandatory | T348, T357, T391, T507–T508 |
| Bearer token, revocable | T044–T047, T203–T204, T424 |
| Mandatory dispute logs | T135, T245, T428, T517–T519 |
| Start small (2×2) then grow | T100, T141, T407–T409 |
| Pipeline > communication > strategy | grading priorities baked into PRD §2; RL deferred |
| Board-origin negotiated in NL | T174, T354 |

**Critical-review conclusion:** the Todo now covers 100% of PRD demands and all 12
H-gates / 13 R-rules. The seven gaps found in review are closed by T505–T520. Total
tasks: **520**.
