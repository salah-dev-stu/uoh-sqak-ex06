"""Optional Tkinter board window (config-flagged). Omitted from coverage — it is a
display side effect that cannot run headless in CI. The ASCII renderer is the
tested default; this exists for the interactive `--gui` experience."""

from __future__ import annotations

from parley.domain.pieces import Role
from parley.domain.records import MoveRecord
from parley.domain.state import GameState


class TkRenderer:  # pragma: no cover - requires a display
    def __init__(self, cell_pixels: int = 64) -> None:
        import tkinter as tk

        self.cell = cell_pixels
        self._tk = tk
        self.root = tk.Tk()
        self.root.title("parley — Cops & Robbers")
        self.canvas: tk.Canvas | None = None

    def render(self, state: GameState, record: MoveRecord) -> None:
        rows, cols = state.grid.rows, state.grid.cols
        if self.canvas is None:
            self.canvas = self._tk.Canvas(self.root, width=cols * self.cell, height=rows * self.cell)
            self.canvas.pack()
        self.canvas.delete("all")
        cop, thief = state.position(Role.COP), state.position(Role.THIEF)
        for r in range(rows):
            for c in range(cols):
                x0, y0 = c * self.cell, r * self.cell
                self.canvas.create_rectangle(x0, y0, x0 + self.cell, y0 + self.cell, outline="#888")
        self._dot(thief, "#c0392b")
        self._dot(cop, "#2471a3")
        self.root.update()

    def _dot(self, pos, color: str) -> None:
        x, y = pos.col * self.cell, pos.row * self.cell
        self.canvas.create_oval(x + 8, y + 8, x + self.cell - 8, y + self.cell - 8, fill=color)
