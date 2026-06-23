"""Agent actions: a move in a direction, or a cop-only barrier placement."""

from __future__ import annotations

from dataclasses import dataclass

from parley.domain.geometry import Direction
from parley.domain.pieces import Role


@dataclass(frozen=True)
class Move:
    direction: Direction

    def __str__(self) -> str:
        return f"MOVE {self.direction.name}"


@dataclass(frozen=True)
class PlaceBarrier:
    """Cop places a barrier on its current cell instead of moving."""

    def __str__(self) -> str:
        return "BARRIER"


Action = Move | PlaceBarrier


def validate_action(role: Role, action: Action) -> None:
    """Reject structurally illegal actions (the thief can never place barriers)."""
    if isinstance(action, PlaceBarrier) and role is not Role.COP:
        raise ValueError("only the cop may place a barrier")
