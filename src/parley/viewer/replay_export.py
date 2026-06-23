"""Transform a real game report into replay data for the 3D viewer.

Honest by construction: it consumes the committed sample report (real engine moves
+ genuine NL taunts) and reconstructs both agents' positions per frame (the move log
records only the acting agent). Pure — no file IO (that lives in ``replay_io``).
"""

from __future__ import annotations

from typing import Any

DEFAULT_SOURCE = "committed sample run (deterministic; regenerate via make_sample_run)"


def _start_positions(log: list[dict]) -> dict[str, list[int]]:
    start: dict[str, list[int]] = {}
    for rec in log:
        role = rec["role"]
        if role not in start:
            start[role] = list(rec["before"])
        if {"cop", "thief"} <= start.keys():
            break
    start.setdefault("cop", [0, 0])
    start.setdefault("thief", [0, 0])
    return start


def _frames(log: list[dict], start: dict[str, list[int]], vision_radius: int) -> list[dict]:
    cop, thief = list(start["cop"]), list(start["thief"])
    barriers: list[list[int]] = []
    frames: list[dict] = []
    for rec in log:
        after = list(rec["after"])
        if rec["role"] == "cop":
            cop = after
        else:
            thief = after
        if "BARRIER" in rec["action"]:
            barriers.append(list(after))
        frames.append({
            "move": rec["move_no"],
            "role": rec["role"],
            "action": rec["action"],
            "message": rec["message"],
            "cop": list(cop),
            "thief": list(thief),
            "barriers": [list(b) for b in barriers],
            "barriers_left": rec["barriers_left"],
            "capture": cop == thief,
            "vision_radius": vision_radius,
        })
    return frames


def build_replay(report: dict[str, Any], source: str = DEFAULT_SOURCE) -> dict[str, Any]:
    """Build the ``window.REPLAY`` structure from a game ``report`` dict."""
    cfg = report["config"]
    vision_radius = cfg["vision_radius"]
    subgames = []
    for sub in report["subgames"]:
        start = _start_positions(sub["log"])
        subgames.append({
            "index": sub["index"],
            "winner": sub["winner"],
            "start": start,
            "scores": sub["scores"],
            "frames": _frames(sub["log"], start, vision_radius),
        })
    return {
        "meta": {
            "title": "Parley: Rooftop Pursuit",
            "source": source,
            "grid_size": list(cfg["grid_size"]),
            "vision_radius": vision_radius,
            "num_subgames": len(subgames),
            "scoring": cfg["scoring"],
            "totals": report.get("totals", {}),
            "generated_from": "reports/sample_report.json",
        },
        "subgames": subgames,
    }
