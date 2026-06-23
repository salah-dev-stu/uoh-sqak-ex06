#!/usr/bin/env python3
"""Export the committed sample game into viewer replay artifacts.

Reads reports/sample_report.json (real moves + genuine NL taunts) and writes
viewer/replay.json + viewer/replay-data.js. Run after make_sample_run.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parley.viewer.replay_export import build_replay  # noqa: E402
from parley.viewer.replay_io import write_replay  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    report = json.loads((REPO / "reports" / "sample_report.json").read_text(encoding="utf-8"))
    replay = build_replay(report)
    paths = write_replay(replay, REPO / "viewer")
    n = replay["meta"]["num_subgames"]
    print(f"exported {n} sub-games → {paths['json']} and {paths['js']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
