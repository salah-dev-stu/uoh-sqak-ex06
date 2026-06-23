"""Load + validate the JSON config directory into a typed ``Config`` (R4)."""

from __future__ import annotations

import json
from pathlib import Path

from parley.shared.config_models import (
    Config,
    GameConfig,
    GateConfig,
    LlmConfig,
    McpConfig,
    ReportConfig,
    RuntimeConfig,
)

_FILES = ("game", "llm", "mcp", "report", "gatekeeper", "runtime")


def _read(config_dir: Path, name: str) -> dict:
    path = config_dir / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"missing config file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_game(game: GameConfig) -> None:
    rows, cols = game.grid_size
    if rows <= 0 or cols <= 0:
        raise ValueError(f"grid_size must be positive, got {game.grid_size}")
    if game.max_moves <= 0:
        raise ValueError("max_moves must be positive")
    if game.num_games <= 0:
        raise ValueError("num_games must be positive")
    if game.max_barriers < 0:
        raise ValueError("max_barriers must be non-negative")


def load_config(config_dir: str | Path) -> Config:
    """Read the six config files from ``config_dir`` into a validated ``Config``."""
    cdir = Path(config_dir)
    raw = {name: _read(cdir, name) for name in _FILES}
    game = GameConfig.from_dict(raw["game"])
    _validate_game(game)
    return Config(
        game=game,
        llm=LlmConfig.from_dict(raw["llm"]),
        mcp=McpConfig.from_dict(raw["mcp"]),
        report=ReportConfig.from_dict(raw["report"]),
        gate=GateConfig.from_dict(raw["gatekeeper"]),
        runtime=RuntimeConfig.from_dict(raw["runtime"]),
    )
