"""Move/barrier legality and state transition (deterministic, immutable)."""

from __future__ import annotations

from dataclasses import replace

from parley.domain.actions import Action, Move, PlaceBarrier, validate_action
from parley.domain.config_bridge import GameRules
from parley.domain.geometry import step
from parley.domain.pieces import Role
from parley.domain.state import GameState


def is_legal(state: GameState, role: Role, action: Action, rules: GameRules) -> bool:
    """True iff ``action`` is legal for ``role`` in ``state``."""
    if isinstance(action, PlaceBarrier):
        return role is Role.COP and state.barriers_placed < rules.max_barriers
    if not rules.diagonal_moves and action.direction.is_diagonal:
        return False
    target = step(state.position(role), action.direction)
    return not state.grid.is_blocked(target)


def apply(state: GameState, role: Role, action: Action, rules: GameRules) -> GameState:
    """Return a NEW state with ``action`` applied (caller checks legality first)."""
    validate_action(role, action)
    if isinstance(action, PlaceBarrier):
        grid = replace(state.grid, barriers=state.grid.barriers | {state.position(role)})
        nxt = replace(state, grid=grid, barriers_placed=state.barriers_placed + 1)
    elif isinstance(action, Move):
        moved = state.piece(role).moved_to(step(state.position(role), action.direction))
        nxt = state.with_piece(moved)
    else:  # pragma: no cover - exhaustive guard
        raise TypeError(f"unknown action: {action!r}")
    return replace(nxt, move_count=nxt.move_count + 1, turn=role.opponent)


def legal_moves(state: GameState, role: Role, rules: GameRules) -> list[Action]:
    """All legal move directions for ``role`` (used for safe fallbacks / trap checks)."""
    from parley.domain.geometry import CARDINALS, DIAGONALS

    dirs = list(CARDINALS) + (list(DIAGONALS) if rules.diagonal_moves else [])
    return [Move(d) for d in dirs if is_legal(state, role, Move(d), rules)]
