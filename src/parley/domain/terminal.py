"""Terminal-condition detection: capture, survival, and barrier-trap."""

from __future__ import annotations

from parley.domain.config_bridge import GameRules
from parley.domain.pieces import Role
from parley.domain.rules import legal_moves
from parley.domain.state import GameState


def is_captured(state: GameState) -> bool:
    """Cop occupies the same cell as the Thief."""
    return state.position(Role.COP) == state.position(Role.THIEF)


def is_trapped(state: GameState, role: Role, rules: GameRules) -> bool:
    """An agent with no legal move is trapped (forced into a wall/barrier)."""
    return len(legal_moves(state, role, rules)) == 0


def check_terminal(state: GameState, rules: GameRules) -> Role | None:
    """Return the winning Role if the sub-game has ended, else ``None``.

    Capture → Cop wins. Surviving ``max_moves`` without capture → Thief wins.
    """
    if is_captured(state):
        return Role.COP
    if state.move_count >= rules.max_moves:
        return Role.THIEF
    return None


def trapped_winner(state: GameState, role: Role, rules: GameRules) -> Role | None:
    """If ``role`` (to move) is trapped, the opponent wins implicitly."""
    if is_trapped(state, role, rules):
        return role.opponent
    return None
