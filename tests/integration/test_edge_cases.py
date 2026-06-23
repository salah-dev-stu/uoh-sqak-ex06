"""M13 — edge cases & rubric guards (small grids, seeds, no hardcoding, overrides)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from parley.sdk.facade import ParleySDK
from tests.unit.fakes import FakeProvider, RecordingSender

ROOT = Path(__file__).resolve().parents[2]


def _config_with(tmp_path, **game_over):
    cdir = tmp_path / "config"
    shutil.copytree(ROOT / "config", cdir)
    game = json.loads((cdir / "game.json").read_text())
    game.update(game_over)
    (cdir / "game.json").write_text(json.dumps(game))
    return str(cdir)


def _sdk(config_dir, run_label):
    return ParleySDK(
        config_dir, provider=FakeProvider("Closing in.\nMOVE: SE"), sender=RecordingSender(),
        now_iso=lambda: "t0", now_seconds=lambda: 0.0, run_label=run_label,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("grid", [[2, 2], [3, 3], [4, 3]])
async def test_pipeline_runs_on_small_and_nonsquare_grids(tmp_path, monkeypatch, grid):
    monkeypatch.chdir(tmp_path)
    cdir = _config_with(tmp_path, grid_size=grid, start_positions={"cop": [0, 0], "thief": [grid[0] - 1, grid[1] - 1]})
    result = await _sdk(cdir, f"g{grid[0]}{grid[1]}").play()
    assert len(result.subgames) == 6
    assert all(s.moves <= 25 for s in result.subgames)


@pytest.mark.asyncio
async def test_seed_reproducibility_identical_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cdir = _config_with(tmp_path)
    a = await _sdk(cdir, "a").play()
    b = await _sdk(cdir, "b").play()
    assert a.totals == b.totals
    assert [s.winner for s in a.subgames] == [s.winner for s in b.subgames]


@pytest.mark.asyncio
async def test_config_scoring_override_changes_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cdir = _config_with(tmp_path, scoring={"cop_win": 99, "thief_win": 10, "cop_loss": 5, "thief_loss": 5})
    result = await _sdk(cdir, "score").play()
    # cop wins all six with the convergent strategy → 6 * 99
    assert result.totals["cop"] == 6 * 99


def test_domain_constants_not_hardcoded():
    """Scoring/rules/terminal must read game constants from config, not literals (R10)."""
    for rel in ("domain/scoring.py", "domain/rules.py", "domain/terminal.py"):
        text = (ROOT / "src" / "parley" / rel).read_text()
        for literal in (" 20", " 10", " 25", "=20", "=25"):
            assert literal not in text, f"{rel} hardcodes a game constant ('{literal}')"


def test_ports_and_tokens_differ_between_servers():
    sdk = _sdk("config", "x")
    urls = sdk.server_urls()
    assert urls["cop"] != urls["thief"]
    assert sdk.cfg.mcp.role("cop")["token_env"] != sdk.cfg.mcp.role("thief")["token_env"]
