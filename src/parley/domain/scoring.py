"""Scoring — all values come from config (R10), never hardcoded here."""

from __future__ import annotations

from parley.domain.pieces import Role


def score_subgame(winner: Role, scoring: dict[str, int]) -> dict[Role, int]:
    """Map a sub-game winner to per-role scores using the configured table."""
    if winner is Role.COP:
        return {Role.COP: scoring["cop_win"], Role.THIEF: scoring["thief_loss"]}
    return {Role.THIEF: scoring["thief_win"], Role.COP: scoring["cop_loss"]}


def aggregate(per_subgame: list[dict[Role, int]]) -> dict[Role, int]:
    """Sum per-role scores across all sub-games (the group score)."""
    totals = {Role.COP: 0, Role.THIEF: 0}
    for scores in per_subgame:
        for role, value in scores.items():
            totals[role] += value
    return totals
