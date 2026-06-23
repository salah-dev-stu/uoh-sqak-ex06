"""M2 — geometry, grid, pieces, actions, observation (T068–T101)."""

from __future__ import annotations

import pytest

from parley.domain.actions import PlaceBarrier, validate_action
from parley.domain.geometry import Direction, Position, step
from parley.domain.grid import Grid
from parley.domain.observation import observe
from parley.domain.pieces import Piece, Role
from parley.domain.state import GameState
from tests.unit.domain_helpers import make_rules


def test_position_iter_and_eq():
    assert tuple(Position(1, 2)) == (1, 2)
    assert Position(1, 2) == Position(1, 2)


def test_directions_deltas_and_diagonals():
    assert Direction.N.value == (-1, 0)
    assert Direction.SE.value == (1, 1)
    assert Direction.NE.is_diagonal and not Direction.N.is_diagonal


def test_step_and_diagonal_changes_both():
    assert step(Position(2, 2), Direction.E) == Position(2, 3)
    p = step(Position(2, 2), Direction.NE)
    assert p.row != 2 and p.col != 2


def test_direction_from_name():
    assert Direction.from_name("ne") is Direction.NE
    with pytest.raises(ValueError):
        Direction.from_name("ZZ")


def test_grid_bounds_no_wrapping():
    g = Grid.from_size((5, 5))
    assert g.in_bounds(Position(0, 0)) and g.in_bounds(Position(4, 4))
    assert not g.in_bounds(Position(5, 0)) and not g.in_bounds(Position(-1, 0))


def test_grid_barriers_and_blocked():
    g = Grid.from_size((4, 3))
    g.add_barrier(Position(1, 1))
    assert g.is_barrier(Position(1, 1)) and g.barrier_count == 1
    assert g.is_blocked(Position(1, 1)) and g.is_blocked(Position(9, 9))


def test_grid_rejects_bad_dims():
    with pytest.raises(ValueError):
        Grid(0, 5)


def test_role_opponent():
    assert Role.COP.opponent is Role.THIEF and Role.THIEF.opponent is Role.COP


def test_piece_moved_to_immutable():
    p = Piece(Role.COP, Position(0, 0))
    assert p.moved_to(Position(1, 1)).position == Position(1, 1)
    assert p.position == Position(0, 0)


def test_validate_action_rejects_thief_barrier():
    with pytest.raises(ValueError):
        validate_action(Role.THIEF, PlaceBarrier())
    validate_action(Role.COP, PlaceBarrier())


def test_observation_sees_self_always():
    obs = observe(GameState.initial(make_rules()), Role.COP, 1, 5)
    assert obs.self_pos == Position(0, 0)


def test_observation_hides_distant_opponent():
    obs = observe(GameState.initial(make_rules()), Role.COP, 1, 5)
    assert obs.opponent_seen is False and obs.opponent_pos is None


def test_observation_reveals_close_opponent():
    r = make_rules(start_positions={"cop": Position(2, 2), "thief": Position(2, 3)})
    obs = observe(GameState.initial(r), Role.COP, 1, 5)
    assert obs.opponent_seen and obs.opponent_pos == Position(2, 3)


def test_observation_full_vision_on_tiny_grid():
    r = make_rules(grid_size=(2, 2), start_positions={"cop": Position(0, 0), "thief": Position(1, 1)})
    obs = observe(GameState.initial(r), Role.COP, vision_radius=2, max_barriers=5)
    assert obs.opponent_seen


def test_observation_barriers_left_tracks_placements():
    st = GameState.initial(make_rules())
    st.barriers_placed = 2
    assert observe(st, Role.COP, 1, 5).barriers_left == 3
