"""Thief FastMCP server entry point (separate process, its own port) (H1)."""

from __future__ import annotations

from parley.mcp.launch import build_role_server, run_http

ROLE = "thief"


def build(config_dir: str = "config"):
    return build_role_server(ROLE, config_dir)


def main() -> None:  # pragma: no cover - live server
    run_http(ROLE)


if __name__ == "__main__":  # pragma: no cover
    main()
