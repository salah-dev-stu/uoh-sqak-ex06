"""Build the structured JSON report emailed at game end (H7/E1)."""

from __future__ import annotations

from typing import Any

from parley.domain.records import GameResult
from parley.shared.config_models import Config


def build_report(result: GameResult, cfg: Config, server_urls: dict[str, str], version: str) -> dict[str, Any]:
    """Aggregate the full game into a parseable report with all required fields."""
    game = cfg.game
    return {
        "exercise": "EX06",
        "title": "Dual AI Agent Conversation via MCP Servers — Cops & Robbers",
        "version": version,
        "recipient": cfg.report.recipient,
        "subject": cfg.report.subject,
        "team": cfg.report.team,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
        "config": {
            "grid_size": list(game.grid_size),
            "max_moves": game.max_moves,
            "num_games": game.num_games,
            "max_barriers": game.max_barriers,
            "vision_radius": game.vision_radius,
            "scoring": game.scoring,
        },
        "servers": server_urls,
        "totals": result.totals,
        "subgames": [s.to_dict() for s in result.subgames],
    }
