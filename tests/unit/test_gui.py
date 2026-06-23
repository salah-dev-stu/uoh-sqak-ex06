"""M7 — ASCII renderer + renderer factory (T302–T313)."""

from __future__ import annotations

from parley.domain.geometry import Position
from parley.domain.records import MoveRecord
from parley.domain.state import GameState
from parley.gui.ascii_renderer import AsciiRenderer
from parley.gui.renderer import make_renderer
from parley.shared.config import load_config
from tests.unit.domain_helpers import make_rules


def record(msg="closing in"):
    return MoveRecord(1, "cop", "MOVE SE", msg, (0, 0), (1, 1), 5, "t0")


def test_ascii_renders_pieces_and_barrier():
    r = make_rules(start_positions={"cop": Position(1, 1), "thief": Position(3, 3)})
    state = GameState.initial(r)
    state.grid.add_barrier(Position(2, 2))
    renderer = AsciiRenderer()
    renderer.render(state, record())
    frame = renderer.frames[0]
    assert "C" in frame and "T" in frame and "#" in frame
    assert "barriers left 5" in frame and "closing in" in frame


def test_ascii_overlap_glyph():
    r = make_rules(start_positions={"cop": Position(2, 2), "thief": Position(2, 2)})
    renderer = AsciiRenderer()
    renderer.render(GameState.initial(r), record())
    assert "X" in renderer.frames[0]


def test_ascii_non_square_grid():
    r = make_rules(grid_size=(4, 3), start_positions={"cop": Position(0, 0), "thief": Position(3, 2)})
    renderer = AsciiRenderer()
    renderer.render(GameState.initial(r), record())
    rows = [ln for ln in renderer.frames[0].splitlines() if " " in ln and "move" not in ln]
    assert len(rows) == 4 and len(rows[0].split()) == 3


def test_transcript_accumulates_frames():
    renderer = AsciiRenderer()
    renderer.render(GameState.initial(make_rules()), record("a"))
    renderer.render(GameState.initial(make_rules()), record("b"))
    assert "a" in renderer.transcript() and "b" in renderer.transcript()


def test_factory_defaults_to_ascii():
    cfg = load_config("config")
    assert isinstance(make_renderer(cfg.runtime), AsciiRenderer)
