"""A pure-domain view of the game config (keeps domain decoupled from IO/config)."""

from __future__ import annotations

from dataclasses import dataclass

from parley.domain.geometry import Position


@dataclass(frozen=True)
class GameRules:
    grid_size: tuple[int, int]
    max_moves: int
    num_games: int
    max_barriers: int
    vision_radius: int
    diagonal_moves: bool
    thief_first: bool
    start_positions: dict[str, Position]
    scoring: dict[str, int]

    @classmethod
    def from_game_config(cls, game) -> GameRules:
        starts = {role: Position(*coords) for role, coords in game.start_positions.items()}
        return cls(
            grid_size=game.grid_size,
            max_moves=game.max_moves,
            num_games=game.num_games,
            max_barriers=game.max_barriers,
            vision_radius=game.vision_radius,
            diagonal_moves=game.diagonal_moves,
            thief_first=game.thief_first,
            start_positions=starts,
            scoring=dict(game.scoring),
        )
