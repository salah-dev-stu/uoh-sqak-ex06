#!/usr/bin/env python3
"""Thin wrapper: run the full autonomous pipeline and write artifacts (H4).

Equivalent to `parley play`, exposed as a script for the README's reproduce block.
Uses the real configured provider (Claude CLI by default) and report sender.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parley.sdk.facade import ParleySDK  # noqa: E402


def main(run_label: str = "latest") -> int:  # pragma: no cover - real run
    sdk = ParleySDK("config", run_label=run_label)
    result = asyncio.run(sdk.play())
    print(f"done: {len(result.subgames)} sub-games, totals {result.totals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "latest"))
