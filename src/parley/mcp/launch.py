"""Shared bootstrap for the two agent servers (build from config, run over HTTP)."""

from __future__ import annotations

import os

from parley.domain.config_bridge import GameRules
from parley.mcp.server_factory import ServerHandle, make_server
from parley.shared.config import load_config


def build_role_server(role: str, config_dir: str = "config") -> ServerHandle:
    """Construct a FastMCP server for ``role`` with bearer auth from config/env."""
    cfg = load_config(config_dir)
    rules = GameRules.from_game_config(cfg.game)
    token = os.environ.get(cfg.mcp.role(role)["token_env"])
    return make_server(role, rules, token)


def run_http(role: str, config_dir: str = "config") -> None:  # pragma: no cover - live server
    cfg = load_config(config_dir)
    role_cfg = cfg.mcp.role(role)
    handle = build_role_server(role, config_dir)
    handle.mcp.run(
        transport="http",
        host=role_cfg["host"],
        port=role_cfg["port"],
        path=role_cfg["path"],
    )
