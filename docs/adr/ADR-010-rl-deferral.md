# ADR-010 — RL / Q-learning deferral

**Status:** accepted · **Gates:** H11 (optional)

**Context.** Tabular Q-learning is recommended-only; the grade rewards pipeline +
communication, not strategy. The 8 GB M2 and the deadline favour focus.

**Decision.** RL is out of scope for v1.00. Agents use the LLM plus a safe-move
heuristic fallback. The `LLMProvider` seam is where a learned policy would later
plug in; no RL code ships, by deliberate choice.

**Consequences.** Effort concentrates on the graded core. Recorded as a decision so
the verify phase does not flag RL's absence as a gap.
