#!/usr/bin/env python3
"""Run a LIVE game with the real Claude CLI and export it to the 3D viewer.

Unlike the committed deterministic sample, this is genuinely DYNAMIC: the LLM
plays, so moves and dialogue differ on every run, and chases run much longer
(with vision_radius 1 the cop rarely sees the thief, so games stretch out).
Needs the `claude` CLI signed in. Takes a few minutes; no email is sent.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parley.sdk.facade import ParleySDK  # noqa: E402
from parley.viewer.replay_export import build_replay  # noqa: E402
from parley.viewer.replay_io import write_replay  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
NUM_GAMES = int(os.environ.get("PARLEY_LIVE_GAMES", "3"))


class _NoEmail:
    def send(self, report: dict) -> None:
        return None


def _tuned_config(tmp: Path) -> str:
    cdir = tmp / "config"
    shutil.copytree(REPO / "config", cdir)
    game = json.loads((cdir / "game.json").read_text())
    game["num_games"] = NUM_GAMES  # fewer games, full-length live chases
    (cdir / "game.json").write_text(json.dumps(game))
    llm = json.loads((cdir / "llm.json").read_text())
    llm["claude_cli"]["model"] = "haiku"
    llm["claude_cli"]["timeout_s"] = 120
    (cdir / "llm.json").write_text(json.dumps(llm))
    return str(cdir)


def main() -> int:
    os.environ.setdefault("PARLEY_CLAUDE_CLI_BIN", "claude")
    tmp = REPO / ".live-tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    sdk = ParleySDK(_tuned_config(tmp), sender=_NoEmail(), run_label="live")
    print(f"running a LIVE {NUM_GAMES}-game match with the real Claude CLI — a few minutes…")
    result = asyncio.run(sdk.play())
    report = {
        "config": {
            "grid_size": list(sdk.cfg.game.grid_size),
            "vision_radius": sdk.cfg.game.vision_radius,
            "scoring": sdk.cfg.game.scoring,
        },
        "subgames": [s.to_dict() for s in result.subgames],
        "totals": result.totals,
    }
    replay = build_replay(report, source="LIVE Claude CLI run (dynamic — differs every run)")
    write_replay(replay, REPO / "viewer")
    moves = sum(len(sg["frames"]) for sg in replay["subgames"])
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(REPO / "reports" / "transcripts" / "live", ignore_errors=True)
    (REPO / "reports" / "live_report.json").unlink(missing_ok=True)
    print(f"exported LIVE replay → viewer/  ({len(replay['subgames'])} sub-games, {moves} moves)")
    print("refresh the viewer to watch it; re-run for a different game.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
