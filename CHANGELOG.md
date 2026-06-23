# Changelog

Versioning per R5: start at 1.00, **+0.01 per change**, single source of truth in
`src/parley/shared/version.py` (mirrored in `config/runtime.json`, asserted by
`scripts/check_version_sync.py`).

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
