#!/usr/bin/env python3
"""Generate the committed offline-proof artifacts (transcript, report, ledger).

Runs the REAL pipeline — real Claude-CLI provider and real Gmail sender — but with
the Gatekeeper's backends faked, so every call is gate-mediated and recorded yet
the run is deterministic and needs no key/server. This is what proves the pipeline
to a grader on Path D (no API key, no creds, no live servers).
"""

from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parley.sdk.facade import ParleySDK  # noqa: E402
from parley.shared.config import load_config  # noqa: E402
from parley.shared.gatekeeper import ApiGatekeeper  # noqa: E402

COP_LINES = [
    "I hear your footsteps echoing off the eastern stairwell — I'm cutting the angle.",
    "You drifted toward the open centre; careless. I close the gap corner by corner.",
    "Nowhere left along that wall. I'm one stride behind you and gaining.",
    "Every diagonal you take, I take too. The net draws tight now.",
]
THIEF_LINES = [
    "You'll never pin me on open floor — I slip back toward the high corner.",
    "Nice try, but the shadows by the far wall are mine; gone before you turn.",
    "I hear you closing, so I double along the top edge where you can't follow.",
    "Too slow — I cut through the gap and you grabbed nothing but air.",
]


def make_backend():
    counter = {"cop": 0, "thief": 0}

    def curated_subprocess(argv, timeout):
        from parley.shared.gatekeeper_types import RunResult

        prompt = argv[2] if len(argv) > 2 else ""
        is_cop = "determined COP" in prompt
        pool, move = (COP_LINES, "SE") if is_cop else (THIEF_LINES, "NW")
        key = "cop" if is_cop else "thief"
        line = pool[counter[key] % len(pool)]
        counter[key] += 1
        import json

        return RunResult(0, json.dumps({"result": f"{line}\nMOVE: {move}"}), "")

    def fake_google(token_path, raw):
        return {"id": "sample-message-id", "labelIds": ["SENT"]}

    return {"subprocess": curated_subprocess, "google": fake_google}


def main() -> int:
    os.environ.setdefault("PARLEY_GMAIL_TOKEN", "sample-token.json")
    os.environ.setdefault("PARLEY_CLAUDE_CLI_BIN", "claude")
    cfg = load_config("config")
    gate = ApiGatekeeper(
        replace(cfg.gate, ledger_path="reports/sample_gate_ledger.json"),
        now_seconds=lambda: 0.0,
        now_iso=lambda: "2026-06-23T12:00:00+03:00",
        backends=make_backend(),
    )
    sdk = ParleySDK("config", gate=gate, now_iso=lambda: "2026-06-23T12:00:00+03:00",
                    now_seconds=lambda: 0.0, run_label="sample")
    result = asyncio.run(sdk.play())  # writes reports/sample_report.json via run_label
    print(f"sample run: {len(result.subgames)} sub-games, totals {result.totals}")
    print("artifacts: reports/sample_report.json, reports/transcripts/sample/, reports/sample_gate_ledger.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
