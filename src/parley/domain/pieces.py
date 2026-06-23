"""Agent roles and their on-board pieces."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from parley.domain.geometry import Position


class Role(StrEnum):
    COP = "cop"
    THIEF = "thief"

    @property
    def opponent(self) -> Role:
        return Role.THIEF if self is Role.COP else Role.COP


@dataclass
class Piece:
    role: Role
    position: Position

    def moved_to(self, position: Position) -> Piece:
        return Piece(role=self.role, position=position)
