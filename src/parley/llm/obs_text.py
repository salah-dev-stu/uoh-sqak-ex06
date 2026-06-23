"""Render a partial observation as prose (H2 — qualitative, no coordinate tuples).

The agent reasons spatially in words; positions are described relative to walls
and as compass directions, never as ``(x, y)`` tuples that would leak structure.
"""

from __future__ import annotations

from parley.domain.geometry import Position
from parley.domain.observation import Observation


def relative_dir(me: Position, other: Position) -> str:
    dr, dc = other.row - me.row, other.col - me.col
    ns = "north" if dr < 0 else "south" if dr > 0 else ""
    ew = "west" if dc < 0 else "east" if dc > 0 else ""
    compass = "-".join(p for p in (ns, ew) if p) or "right on top of you"
    dist = max(abs(dr), abs(dc))
    steps = "one step" if dist == 1 else f"{dist} steps"
    return f"{steps} to the {compass}" if compass != "right on top of you" else compass


def _walls(obs: Observation) -> str:
    rows, cols = obs.grid_size
    edges = []
    if obs.self_pos.row == 0:
        edges.append("the north wall")
    if obs.self_pos.row == rows - 1:
        edges.append("the south wall")
    if obs.self_pos.col == 0:
        edges.append("the west wall")
    if obs.self_pos.col == cols - 1:
        edges.append("the east wall")
    return "You are pressed against " + " and ".join(edges) + "." if edges else ""


def render_observation(obs: Observation) -> str:
    rows, cols = obs.grid_size
    lines = [
        f"You are the {obs.role}.",
        f"The board is {rows} by {cols} cells; rows count downward from the top.",
        f"You stand at row {obs.self_pos.row}, column {obs.self_pos.col}.",
    ]
    wall = _walls(obs)
    if wall:
        lines.append(wall)
    if obs.opponent_seen and obs.opponent_pos is not None:
        lines.append(f"You catch sight of your opponent {relative_dir(obs.self_pos, obs.opponent_pos)}.")
    else:
        lines.append("Your opponent is out of sight — judge their whereabouts only from what they tell you.")
    if obs.visible_barriers:
        lines.append(f"You notice {len(obs.visible_barriers)} barrier(s) close by.")
    tail = f" You have {obs.barriers_left} barrier(s) left." if obs.role == "cop" else ""
    lines.append(f"This is move {obs.move_count}.{tail}")
    return "\n".join(lines)
