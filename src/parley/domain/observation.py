"""Partial observability (Dec-POMDP): each agent sees only a vision-limited region.

An agent always knows its own position. It sees the opponent and barriers ONLY
within ``vision_radius`` (Chebyshev distance). Beyond that the opponent is unknown
— the agent must infer it from the opponent's free natural-language messages.
"""

from __future__ import annotations

from dataclasses import dataclass

from parley.domain.geometry import Position
from parley.domain.pieces import Role
from parley.domain.state import GameState


def _chebyshev(a: Position, b: Position) -> int:
    return max(abs(a.row - b.row), abs(a.col - b.col))


@dataclass(frozen=True)
class Observation:
    role: Role
    self_pos: Position
    grid_size: tuple[int, int]
    vision_radius: int
    opponent_seen: bool
    opponent_pos: Position | None
    visible_barriers: tuple[Position, ...]
    move_count: int
    barriers_left: int


def observe(state: GameState, role: Role, vision_radius: int, max_barriers: int) -> Observation:
    me = state.position(role)
    opp = state.position(role.opponent)
    seen = _chebyshev(me, opp) <= vision_radius
    visible = tuple(b for b in state.grid.barriers if _chebyshev(me, b) <= vision_radius)
    return Observation(
        role=role,
        self_pos=me,
        grid_size=(state.grid.rows, state.grid.cols),
        vision_radius=vision_radius,
        opponent_seen=seen,
        opponent_pos=opp if seen else None,
        visible_barriers=visible,
        move_count=state.move_count,
        barriers_left=max_barriers - state.barriers_placed,
    )
