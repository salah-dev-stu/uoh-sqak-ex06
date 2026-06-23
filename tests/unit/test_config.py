"""M1 — config models + loader, paths, logging (T030–T043)."""

from __future__ import annotations

import json

import pytest

from parley import __version__
from parley.shared.config import load_config
from parley.shared.config_models import GameConfig
from parley.shared.logging_config import get_logger
from parley.shared.paths import Paths


def test_load_config_parses_all_sections(config_dir):
    cfg = load_config(config_dir)
    assert cfg.game.grid_size == (5, 5)
    assert cfg.game.max_moves == 25
    assert cfg.game.num_games == 6
    assert cfg.game.max_barriers == 5
    assert cfg.llm.provider == "claude_cli"
    assert cfg.mcp.transport == "http"
    assert cfg.report.sender == "gmail"
    assert "subprocess" in cfg.gate.limits


def test_game_scoring_from_config_not_hardcoded(config_dir):
    cfg = load_config(config_dir)
    assert cfg.game.scoring["cop_win"] == 20
    assert cfg.game.scoring["thief_win"] == 10
    assert cfg.game.scoring["cop_loss"] == 5
    assert cfg.game.scoring["thief_loss"] == 5


def test_diagonal_and_thief_first_flags(config_dir):
    cfg = load_config(config_dir)
    assert cfg.game.diagonal_moves is True
    assert cfg.game.thief_first is True


def test_mcp_role_accessor_distinct_ports(config_dir):
    cfg = load_config(config_dir)
    assert cfg.mcp.role("cop")["port"] != cfg.mcp.role("thief")["port"]
    assert cfg.mcp.role("cop")["token_env"] != cfg.mcp.role("thief")["token_env"]


def test_config_version_matches_single_source(config_dir):
    cfg = load_config(config_dir)
    assert cfg.runtime.version == __version__


def test_loader_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path)


def test_loader_rejects_nonpositive_grid(tmp_path, config_dir):
    for name in ("game", "llm", "mcp", "report", "gatekeeper", "runtime"):
        (tmp_path / f"{name}.json").write_text((config_dir / f"{name}.json").read_text())
    bad = json.loads((config_dir / "game.json").read_text())
    bad["grid_size"] = [0, 5]
    (tmp_path / "game.json").write_text(json.dumps(bad))
    with pytest.raises(ValueError, match="grid_size"):
        load_config(tmp_path)


def test_game_from_dict_tuples():
    g = GameConfig.from_dict(
        {
            "grid_size": [3, 3], "max_moves": 10, "num_games": 6, "max_barriers": 5,
            "vision_radius": 1, "diagonal_moves": True, "thief_first": True, "seed": 1,
            "start_positions": {"cop": [0, 0], "thief": [2, 2]},
            "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
        }
    )
    assert g.start_positions["thief"] == (2, 2)


def test_paths_resolve_and_ensure(tmp_path):
    paths = Paths.from_runtime(
        tmp_path,
        {"reports_dir": "reports", "transcripts_dir": "reports/tr", "ledger": "reports/runs/l.json"},
    ).ensure()
    assert paths.reports.is_dir()
    assert paths.transcripts.is_dir()
    assert paths.ledger.parent.is_dir()


def test_get_logger_namespaced():
    log = get_logger("config", "DEBUG")
    assert log.name == "parley.config"
