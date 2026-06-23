"""ASCII board renderer (default) — feeds game logs, transcripts, and the README."""

from __future__ import annotations

from parley.domain.geometry import Position
from parley.domain.pieces import Role
from parley.domain.records import MoveRecord
from parley.domain.state import GameState


class AsciiRenderer:
    GLYPHS = {"cop": "C", "thief": "T", "barrier": "#", "empty": ".", "both": "X"}

    def __init__(self, echo: bool = False) -> None:
        self.echo = echo
        self.frames: list[str] = []

    def _draw(self, state: GameState) -> str:
        cop, thief = state.position(Role.COP), state.position(Role.THIEF)
        rows = []
        for r in range(state.grid.rows):
            cells = []
            for c in range(state.grid.cols):
                p = Position(r, c)
                if p == cop and p == thief:
                    cells.append(self.GLYPHS["both"])
                elif p == cop:
                    cells.append(self.GLYPHS["cop"])
                elif p == thief:
                    cells.append(self.GLYPHS["thief"])
                elif state.grid.is_barrier(p):
                    cells.append(self.GLYPHS["barrier"])
                else:
                    cells.append(self.GLYPHS["empty"])
            rows.append(" ".join(cells))
        return "\n".join(rows)

    def render(self, state: GameState, record: MoveRecord) -> None:
        header = (
            f"move {record.move_no:>2} | {record.role:<5} {record.action:<8} "
            f"| barriers left {record.barriers_left} | \"{record.message}\""
        )
        frame = f"{header}\n{self._draw(state)}\n"
        self.frames.append(frame)
        if self.echo:  # pragma: no cover - console side effect
            print(frame)

    def transcript(self) -> str:
        return "\n".join(self.frames)
