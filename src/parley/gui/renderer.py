"""Renderer protocol + factory (ASCII default, optional Tkinter via config flag)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from parley.domain.records import MoveRecord
from parley.domain.state import GameState
from parley.gui.ascii_renderer import AsciiRenderer


@runtime_checkable
class Renderer(Protocol):
    def render(self, state: GameState, record: MoveRecord) -> None: ...


def make_renderer(runtime_cfg: Any, echo: bool = False) -> Renderer:
    gui = getattr(runtime_cfg, "gui", {}) or {}
    if gui.get("enabled") and gui.get("backend") == "tkinter":  # pragma: no cover - display
        from parley.gui.tk_renderer import TkRenderer

        return TkRenderer(cell_pixels=int(gui.get("cell_pixels", 64)))
    return AsciiRenderer(echo=echo)
