"""Shared domain test helper: build a GameRules with overrides."""

from __future__ import annotations

from parley.domain.config_bridge import GameRules
from parley.domain.geometry import Position


def make_rules(**over) -> GameRules:
    base = {
        "grid_size": (5, 5),
        "max_moves": 25,
        "num_games": 6,
        "max_barriers": 5,
        "vision_radius": 1,
        "diagonal_moves": True,
        "thief_first": True,
        "start_positions": {"cop": Position(0, 0), "thief": Position(4, 4)},
        "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
    }
    base.update(over)
    return GameRules(**base)
