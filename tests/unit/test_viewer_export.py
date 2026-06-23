"""Viewer P2 — replay exporter (V003–V028). Deterministic, pure."""

from __future__ import annotations

import json

from parley.viewer.replay_export import build_replay
from parley.viewer.replay_io import write_replay


def _report():
    """A fixed two-sub-game report: one cop-capture, one barrier move."""
    sg0 = {
        "index": 0, "winner": "cop", "moves": 2, "scores": {"cop": 20, "thief": 5},
        "log": [
            {"move_no": 1, "role": "thief", "action": "MOVE S", "message": "I bolt south.",
             "before": [0, 2], "after": [1, 2], "barriers_left": 5, "ts": "t0"},
            {"move_no": 2, "role": "cop", "action": "MOVE SE", "message": "Got you.",
             "before": [0, 1], "after": [1, 2], "barriers_left": 5, "ts": "t1"},
        ],
    }
    sg1 = {
        "index": 1, "winner": "thief", "moves": 2, "scores": {"cop": 5, "thief": 10},
        "log": [
            {"move_no": 1, "role": "thief", "action": "MOVE N", "message": "Up high.",
             "before": [2, 2], "after": [1, 2], "barriers_left": 5, "ts": "t0"},
            {"move_no": 2, "role": "cop", "action": "BARRIER", "message": "Wall up.",
             "before": [0, 0], "after": [0, 0], "barriers_left": 4, "ts": "t1"},
        ],
    }
    return {
        "config": {"grid_size": [3, 3], "vision_radius": 1,
                   "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5}},
        "subgames": [sg0, sg1], "totals": {"cop": 25, "thief": 15},
    }


def test_meta_fields():
    r = build_replay(_report())
    m = r["meta"]
    assert m["grid_size"] == [3, 3] and m["vision_radius"] == 1
    assert m["num_subgames"] == 2 and m["scoring"]["cop_win"] == 20
    assert m["totals"] == {"cop": 25, "thief": 15}
    assert "sample" in m["source"] and "deterministic" in m["source"]


def test_subgame_shape_and_start():
    r = build_replay(_report())
    sg = r["subgames"][0]
    assert sg["index"] == 0 and sg["winner"] == "cop"
    assert sg["scores"] == {"cop": 20, "thief": 5}
    assert sg["start"] == {"thief": [0, 2], "cop": [0, 1]}


def test_frames_have_both_positions_and_message():
    r = build_replay(_report())
    f0 = r["subgames"][0]["frames"][0]
    assert f0["cop"] == [0, 1] and f0["thief"] == [1, 2]  # thief moved, cop unchanged
    assert f0["message"] == "I bolt south." and f0["action"] == "MOVE S"
    assert f0["vision_radius"] == 1 and f0["barriers_left"] == 5


def test_capture_flagged_only_on_overlap():
    r = build_replay(_report())
    frames = r["subgames"][0]["frames"]
    assert frames[0]["capture"] is False
    assert frames[1]["capture"] is True  # cop moves onto thief at [1,2]


def test_thief_survive_has_no_capture():
    r = build_replay(_report())
    assert all(f["capture"] is False for f in r["subgames"][1]["frames"])


def test_barrier_action_appends_barrier():
    r = build_replay(_report())
    last = r["subgames"][1]["frames"][1]
    assert last["barriers"] == [[0, 0]] and last["barriers_left"] == 4


def test_frame_count_equals_moves():
    r = build_replay(_report())
    for sg in r["subgames"]:
        assert len(sg["frames"]) == 2


def test_no_coordinate_tuple_in_messages():
    import re
    r = build_replay(_report())
    for sg in r["subgames"]:
        for f in sg["frames"]:
            assert not re.search(r"\(\s*\d+\s*,\s*\d+\s*\)", f["message"])


def test_deterministic():
    assert build_replay(_report()) == build_replay(_report())


def test_custom_source_label():
    r = build_replay(_report(), source="live Claude CLI run")
    assert r["meta"]["source"] == "live Claude CLI run"


def test_write_replay_emits_json_and_js(tmp_path):
    replay = build_replay(_report())
    out = write_replay(replay, tmp_path)
    assert out["json"].endswith("replay.json")
    data = json.loads((tmp_path / "replay.json").read_text())
    assert data["meta"]["num_subgames"] == 2
    js = (tmp_path / "replay-data.js").read_text()
    assert js.lstrip().startswith("//")
    assert "window.REPLAY = {" in js
    # the JS payload parses back equal to the json
    payload = js.split("window.REPLAY = ", 1)[1].rsplit(";", 1)[0].strip()
    assert json.loads(payload) == data
