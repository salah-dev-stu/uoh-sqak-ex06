# ADR-004 — Partial-observability model (Dec-POMDP)

**Status:** accepted · **Gates:** H6

**Decision.** Each agent sees its own cell always, and the opponent/barriers only
within a configurable Chebyshev `vision_radius`. Beyond that the opponent is
unknown and must be inferred from the opponent's free-NL messages. The observation
is rendered to prose with no coordinate tuples, forcing genuine NL reasoning.

**Consequences.** Partial observability is the central challenge, exactly as the
spec frames it. `vision_radius` is config-driven (default 1 on 5×5).
