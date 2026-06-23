"""Thin CLI command handlers — they only call into ParleySDK (R1)."""

from __future__ import annotations

import asyncio

from parley.sdk.facade import ParleySDK
from parley.shared.version import __version__


def handle_version(_args) -> int:
    print(f"parley {__version__}")
    return 0


def handle_play(args) -> int:
    sdk = ParleySDK(
        args.config,
        run_label=args.run_label,
        echo=args.gui,
        provider_name=args.provider,
    )
    result = asyncio.run(sdk.play())
    print(
        f"played {len(result.subgames)} sub-games | "
        f"cop {result.totals.get('cop', 0)} / thief {result.totals.get('thief', 0)} | "
        f"report emailed to the configured recipient"
    )
    return 0


def handle_serve(args) -> int:  # pragma: no cover - live server
    from parley.mcp.launch import run_http

    run_http(args.role, args.config)
    return 0


def handle_report(args) -> int:
    import json
    from pathlib import Path

    report = json.loads(Path(args.file).read_text(encoding="utf-8"))
    ParleySDK(args.config).report_only(report)
    print(f"re-sent report from {args.file}")
    return 0
