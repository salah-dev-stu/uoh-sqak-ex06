"""M2 — records + a scripted deterministic sub-game (T135–T143)."""

from __future__ import annotations

import json

from parley.domain.actions import Move
from parley.domain.geometry import Direction, Position
from parley.domain.pieces import Role
from parley.domain.records import GameResult, MoveRecord, SubGameResult
from parley.domain.rules import apply
from parley.domain.scoring import aggregate, score_subgame
from parley.domain.state import GameState
from parley.domain.terminal import check_terminal
from tests.unit.domain_helpers import make_rules


def _rules(**over):
    over.setdefault("grid_size", (3, 3))
    over.setdefault("start_positions", {"cop": Position(0, 0), "thief": Position(0, 1)})
    return make_rules(**over)


def test_move_record_to_dict():
    rec = MoveRecord(1, "thief", "MOVE S", "slipping south", (0, 1), (1, 1), 5, "t0")
    d = rec.to_dict()
    assert d["before"] == [0, 1] and d["after"] == [1, 1] and d["role"] == "thief"


def test_subgame_and_game_result_json_roundtrip():
    rec = MoveRecord(1, "cop", "MOVE E", "advancing east", (0, 0), (0, 1), 5, "t0")
    sub = SubGameResult(0, "uoh-sqak", "cop", 1, {"cop": 20, "thief": 5}, [rec])
    game = GameResult([sub], {"cop": 20, "thief": 5}, "t0", "t1")
    blob = json.dumps(game.to_dict())
    loaded = json.loads(blob)
    assert loaded["subgames"][0]["winner"] == "cop"
    assert loaded["totals"]["cop"] == 20
    assert loaded["subgames"][0]["log"][0]["message"] == "advancing east"


def test_scripted_subgame_reaches_capture():
    # Cop at (0,0), thief at (0,1). Thief moves first (S to (1,1)), cop chases SE then S.
    r = _rules()
    st = GameState.initial(r)
    st = apply(st, Role.THIEF, Move(Direction.S), r)   # thief (0,1)->(1,1)
    st = apply(st, Role.COP, Move(Direction.SE), r)    # cop (0,0)->(1,1) == capture
    assert check_terminal(st, r) is Role.COP
    scores = score_subgame(Role.COP, r.scoring)
    assert scores[Role.COP] == 20


def test_scripted_six_subgame_aggregate():
    r = _rules()
    per = [score_subgame(Role.COP if i % 2 == 0 else Role.THIEF, r.scoring) for i in range(6)]
    totals = aggregate(per)
    assert totals[Role.COP] + totals[Role.THIEF] == sum(sum(s.values()) for s in per)
