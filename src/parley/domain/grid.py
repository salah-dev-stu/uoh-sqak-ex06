"""The board: dimensions, bounds, and barrier set (no wrapping; walls at edges)."""

from __future__ import annotations

from dataclasses import dataclass, field

from parley.domain.geometry import Position


@dataclass
class Grid:
    rows: int
    cols: int
    barriers: set[Position] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError(f"grid dims must be positive, got {self.rows}x{self.cols}")

    @classmethod
    def from_size(cls, size: tuple[int, int]) -> Grid:
        return cls(rows=size[0], cols=size[1])

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def is_barrier(self, pos: Position) -> bool:
        return pos in self.barriers

    def add_barrier(self, pos: Position) -> None:
        self.barriers.add(pos)

    @property
    def barrier_count(self) -> int:
        return len(self.barriers)

    def is_blocked(self, pos: Position) -> bool:
        """A cell is unenterable if it is off the board or holds a barrier."""
        return not self.in_bounds(pos) or self.is_barrier(pos)
