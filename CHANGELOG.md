# Changelog

Versioning per R5: start at 1.00, **+0.01 per change**, single source of truth in
`src/parley/shared/version.py` (mirrored in `config/runtime.json`, asserted by
`scripts/check_version_sync.py`).

## 1.24 — 2026-06-23 · Standout: 3D Replay Theater (SHOULD tier)
- **Fog of war + COP / THIEF / DIRECTOR view toggle** — the partial-observation
  (Dec-POMDP) showcase: tiles beyond the viewed agent's vision radius go dark and the
  opponent figure vanishes, while its taunt still arrives in the chat
- Neon **barriers** that slam down (cop drops one in sub-game 1 of the sample now)
- **Capture particle burst** + the existing CAPTURE banner; brighter neon polish
- README fog-of-war/barrier/capture showcase; 142 tests green, 98% cov; CI Python-only

## 1.21–1.23 — 2026-06-23 · Standout: 3D Replay Theater (MUST tier)
- **1.21** viewer PRD + Plan + Todo (303 tasks) under `docs/viewer/`
- **1.22** `parley.viewer` replay exporter + tests; generated real replay data
- **1.23** 3D viewer (vendored Three.js, board/agents/dialogue/controls), `serve_viewer`
  + `make viewer`, screenshots + GIF, prominent README section. Capture polish:
  agents stand side-by-side (no clipping), only the active speaker's bubble shows.
  CI unchanged (Python-only); 142 tests green, 98% coverage.

## 1.20 — 2026-06-23
Full vibe-coding lifecycle for EX06 `parley`, milestone by milestone:

- **1.00** scaffold — uv, ruff, Python-3.13 CI, version single-source, line guard
- **1.01–1.04** docs package — PRD, design doc, Plan, Todo (520 tasks)
- **1.05** critical verify — coverage matrix, 7 gaps closed
- **1.06** M1 shared core — config, paths, logging, wired Gatekeeper, auth
- **1.07** M2 domain — grid, rules, partial observability, terminal, scoring
- **1.08** M3 llm — Claude CLI + Ollama providers, NL prompts, parser
- **1.09** M4 mcp — two FastMCP HTTP servers, async client, bearer auth
- **1.10** M5 orchestrator — autonomous turn loop, 6 sub-games, pipeline
- **1.11** M6 report — JSON builder + pluggable Gmail/SMTP senders
- **1.12** M7 gui — ASCII renderer (+ optional Tkinter)
- **1.13** M8 sdk + cli — single public entry, full wiring
- **1.14** M9 Gatekeeper meta-test (R3 enforced by source grep)
- **1.15** M10 deploy/run scripts + committed sample artifacts
- **1.16** M11 diagrams + 10 ADRs + 6 mechanism PRDs
- **1.17** M12 visual README (scientific report)
- **1.18** M13 edge-case & rubric-guard tests
- **1.19** live validation with the real Claude CLI
- **1.20** rendered visuals (board figures, architecture diagram PNGs) + this changelog
