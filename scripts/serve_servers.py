#!/usr/bin/env python3
"""Start the Cop and Thief FastMCP HTTP servers locally (two separate processes).

Each is bound to its own port and bearer token from config/env. Use this before a
real `parley play --provider ...` over HTTP, or before opening ngrok tunnels.
"""

from __future__ import annotations

import sys
from multiprocessing import Process
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parley.shared.config import load_config  # noqa: E402


def role_endpoints(config_dir: str = "config") -> dict[str, str]:
    cfg = load_config(config_dir)
    out = {}
    for role in ("cop", "thief"):
        rc = cfg.mcp.role(role)
        out[role] = f"http://{rc['host']}:{rc['port']}{rc['path']}"
    return out


def main() -> int:  # pragma: no cover - launches live servers
    from parley.mcp.launch import run_http

    procs = [Process(target=run_http, args=(role,), daemon=False) for role in ("cop", "thief")]
    for p in procs:
        p.start()
    print("serving:", role_endpoints())
    for p in procs:
        p.join()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
