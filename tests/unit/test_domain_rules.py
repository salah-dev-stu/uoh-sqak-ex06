"""M2 — rules, terminal, scoring, state seeding (T102–T134)."""

from __future__ import annotations

import random

from parley.domain.actions import Move, PlaceBarrier
from parley.domain.geometry import CARDINALS, Direction, Position
from parley.domain.pieces import Role
from parley.domain.rules import apply, is_legal, legal_moves
from parley.domain.scoring import aggregate, score_subgame
from parley.domain.state import GameState, random_start
from parley.domain.terminal import check_terminal, is_captured, trapped_winner
from tests.unit.domain_helpers import make_rules


def test_legal_move_in_bounds_and_diagonal():
    st = GameState.initial(make_rules())
    assert is_legal(st, Role.COP, Move(Direction.SE), make_rules())
    assert not is_legal(st, Role.COP, Move(Direction.N), make_rules())


def test_diagonal_disabled_blocks_diagonal():
    st = GameState.initial(make_rules())
    assert not is_legal(st, Role.COP, Move(Direction.SE), make_rules(diagonal_moves=False))


def test_barrier_legal_until_max():
    st = GameState.initial(make_rules())
    st.barriers_placed = 4
    assert is_legal(st, Role.COP, PlaceBarrier(), make_rules())
    st.barriers_placed = 5
    assert not is_legal(st, Role.COP, PlaceBarrier(), make_rules())


def test_apply_move_is_immutable_and_advances_turn():
    st = GameState.initial(make_rules())
    nxt = apply(st, Role.THIEF, Move(Direction.NW), make_rules())
    assert nxt.position(Role.THIEF) == Position(3, 3)
    assert st.position(Role.THIEF) == Position(4, 4)
    assert nxt.move_count == 1 and nxt.turn is Role.COP


def test_apply_barrier_adds_and_counts():
    st = GameState.initial(make_rules())
    nxt = apply(st, Role.COP, PlaceBarrier(), make_rules())
    assert nxt.grid.is_barrier(Position(0, 0)) and nxt.barriers_placed == 1
    assert nxt.position(Role.COP) == Position(0, 0)


def test_illegal_move_into_barrier():
    r = make_rules(start_positions={"cop": Position(2, 2), "thief": Position(0, 0)})
    st = GameState.initial(r)
    st.grid.add_barrier(Position(2, 3))
    assert not is_legal(st, Role.COP, Move(Direction.E), r)


def test_capture_cop_wins():
    r = make_rules(start_positions={"cop": Position(2, 2), "thief": Position(2, 2)})
    st = GameState.initial(r)
    assert is_captured(st) and check_terminal(st, r) is Role.COP


def test_survive_thief_wins():
    st = GameState.initial(make_rules())
    st.move_count = 25
    assert check_terminal(st, make_rules()) is Role.THIEF


def test_midgame_non_terminal():
    assert check_terminal(GameState.initial(make_rules()), make_rules()) is None


def test_trapped_thief_cop_wins():
    r = make_rules(grid_size=(2, 2), start_positions={"cop": Position(0, 1), "thief": Position(0, 0)})
    st = GameState.initial(r)
    for p in (Position(0, 1), Position(1, 0), Position(1, 1)):
        st.grid.add_barrier(p)
    assert trapped_winner(st, Role.THIEF, r) is Role.COP


def test_score_cop_win_and_thief_win():
    sc = {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5}
    assert score_subgame(Role.COP, sc) == {Role.COP: 20, Role.THIEF: 5}
    assert score_subgame(Role.THIEF, sc) == {Role.THIEF: 10, Role.COP: 5}


def test_aggregate_sums_six_subgames():
    sc = {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5}
    per = [score_subgame(Role.COP, sc) for _ in range(3)] + [score_subgame(Role.THIEF, sc) for _ in range(3)]
    totals = aggregate(per)
    assert totals[Role.COP] == 3 * 20 + 3 * 5
    assert totals[Role.THIEF] == 3 * 5 + 3 * 10


def test_random_start_distinct_and_seeded():
    a = random_start(make_rules(), random.Random(1))
    b = random_start(make_rules(), random.Random(1))
    assert a == b and a["cop"] != a["thief"]


def test_legal_moves_count_center():
    st = GameState.initial(make_rules(start_positions={"cop": Position(2, 2), "thief": Position(0, 0)}))
    assert len(legal_moves(st, Role.COP, make_rules())) == len(CARDINALS) + 4
