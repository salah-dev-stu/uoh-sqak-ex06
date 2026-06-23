# ADR-003 — Claude CLI subscription provider + Ollama fallback

**Status:** accepted · **Gates:** H9

**Context.** The user wants no paid API key. The orchestrator must still hold a
cloud-quality LLM, with a local option.

**Decision.** Default provider shells out to the local `claude -p` binary (the
Claude Code subscription) via `Gatekeeper.run_subprocess`; `OllamaProvider` is the
config-switchable local fallback. Both are mocked in tests, so the grader needs no
key and no model.

**Consequences.** Zero API cost; a preflight gives an actionable error if the CLI
is absent. Provider is chosen purely by `config/llm.json` (R4).
