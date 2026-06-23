#!/usr/bin/env python3
"""Expose the two local FastMCP servers over public HTTPS via ngrok (H8).

Each tunnel fronts a bearer-token-protected server, so the public URL is useless
without the token (Dr. Segal: "no URL without a token"). Cloudflare Tunnel is a
documented zero-session-limit alternative — see docs/adr/ADR-008.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parley.shared.config import load_config  # noqa: E402

_URL = re.compile(r"https://[\w-]+\.ngrok[\w.-]*\.\w+")


def ngrok_argv(port: int) -> list[str]:
    return ["ngrok", "http", str(port), "--log", "stdout"]


def parse_tunnel_url(stdout: str) -> str | None:
    match = _URL.search(stdout)
    return match.group(0) if match else None


def plan(config_dir: str = "config") -> dict[str, list[str]]:
    cfg = load_config(config_dir)
    return {role: ngrok_argv(cfg.mcp.role(role)["port"]) for role in ("cop", "thief")}


def main() -> int:  # pragma: no cover - launches live tunnels
    for role, argv in plan().items():
        print(f"{role}: run `{' '.join(argv)}` in its own terminal, then publish the HTTPS URL + token")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
