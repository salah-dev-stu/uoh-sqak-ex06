"""Authoritative game state — positions, barriers, move counter, whose turn."""

from __future__ import annotations

import random
from dataclasses import dataclass, replace

from parley.domain.config_bridge import GameRules
from parley.domain.geometry import Position
from parley.domain.grid import Grid
from parley.domain.pieces import Piece, Role


@dataclass
class GameState:
    grid: Grid
    cop: Piece
    thief: Piece
    turn: Role
    move_count: int = 0
    barriers_placed: int = 0

    @classmethod
    def initial(cls, rules: GameRules, start: dict[str, Position] | None = None) -> GameState:
        grid = Grid.from_size(rules.grid_size)
        cop_pos, thief_pos = (start or rules.start_positions)["cop"], (start or rules.start_positions)["thief"]
        turn = Role.THIEF if rules.thief_first else Role.COP
        return cls(grid=grid, cop=Piece(Role.COP, cop_pos), thief=Piece(Role.THIEF, thief_pos), turn=turn)

    def piece(self, role: Role) -> Piece:
        return self.cop if role is Role.COP else self.thief

    def position(self, role: Role) -> Position:
        return self.piece(role).position

    def with_piece(self, piece: Piece) -> GameState:
        if piece.role is Role.COP:
            return replace(self, cop=piece)
        return replace(self, thief=piece)


def random_start(rules: GameRules, rng: random.Random) -> dict[str, Position]:
    """Seeded distinct start cells (used when randomised placement is desired)."""
    grid = Grid.from_size(rules.grid_size)
    cells = [Position(r, c) for r in range(grid.rows) for c in range(grid.cols)]
    cop, thief = rng.sample(cells, 2)
    return {"cop": cop, "thief": thief}
