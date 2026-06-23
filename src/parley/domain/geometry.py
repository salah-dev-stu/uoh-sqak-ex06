"""Grid geometry: positions and the eight movement directions (incl. diagonals)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __iter__(self):
        yield self.row
        yield self.col


class Direction(Enum):
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1)
    W = (0, -1)
    NW = (-1, -1)

    @property
    def is_diagonal(self) -> bool:
        dr, dc = self.value
        return dr != 0 and dc != 0

    @classmethod
    def from_name(cls, name: str) -> Direction:
        try:
            return cls[name.strip().upper()]
        except KeyError as exc:
            raise ValueError(f"unknown direction: {name!r}") from exc


CARDINALS = (Direction.N, Direction.E, Direction.S, Direction.W)
DIAGONALS = (Direction.NE, Direction.SE, Direction.SW, Direction.NW)


def step(pos: Position, direction: Direction) -> Position:
    """Return the neighbouring cell one step in ``direction`` (no bounds check)."""
    dr, dc = direction.value
    return Position(pos.row + dr, pos.col + dc)
