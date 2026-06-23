"""Logging shapes: per-move records, sub-game results, and the full game result.

These are the dispute-evidence logs the lecture requires: every move stores the
positions before/after, the action, the free-NL message, and barriers-left.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MoveRecord:
    move_no: int
    role: str
    action: str
    message: str
    before: tuple[int, int]
    after: tuple[int, int]
    barriers_left: int
    ts: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "move_no": self.move_no,
            "role": self.role,
            "action": self.action,
            "message": self.message,
            "before": list(self.before),
            "after": list(self.after),
            "barriers_left": self.barriers_left,
            "ts": self.ts,
        }


@dataclass(frozen=True)
class SubGameResult:
    index: int
    cop_role_team: str
    winner: str
    moves: int
    scores: dict[str, int]
    log: list[MoveRecord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "cop_role_team": self.cop_role_team,
            "winner": self.winner,
            "moves": self.moves,
            "scores": self.scores,
            "log": [m.to_dict() for m in self.log],
        }


@dataclass(frozen=True)
class GameResult:
    subgames: list[SubGameResult]
    totals: dict[str, int]
    started_at: str
    finished_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "subgames": [s.to_dict() for s in self.subgames],
            "totals": self.totals,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }
