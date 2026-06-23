"""M8 — ParleySDK façade + CLI (T318–T336). Provider + sender injected/mocked."""

from __future__ import annotations

import json

import pytest

from parley import __version__
from parley.cli import build_parser, main
from parley.sdk.facade import ParleySDK
from tests.unit.fakes import FakeProvider, RecordingSender


def make_sdk(run_label="test", **kw):
    return ParleySDK(
        "config",
        provider=FakeProvider("Closing in.\nMOVE: SE"),
        sender=RecordingSender(),
        now_iso=lambda: "2026-06-23T12:00:00+03:00",
        now_seconds=lambda: 0.0,
        run_label=run_label,
        **kw,
    )


def test_sdk_deploy_info_lists_servers_and_auth():
    info = make_sdk().deploy_info()
    assert info["transport"] == "http"
    assert info["auth"]["scheme"] == "bearer"
    assert "cop" in info["servers"] and "thief" in info["servers"]


@pytest.mark.asyncio
async def test_sdk_play_runs_full_pipeline(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # write config into the temp cwd so artifacts land there
    import shutil
    from pathlib import Path

    shutil.copytree(Path(__file__).resolve().parents[2] / "config", tmp_path / "config")
    sdk = ParleySDK(
        str(tmp_path / "config"),
        provider=FakeProvider("On your tail.\nMOVE: SE"),
        sender=RecordingSender(),
        now_iso=lambda: "2026-06-23T12:00:00+03:00",
        now_seconds=lambda: 0.0,
        run_label="unit",
    )
    result = await sdk.play()
    assert len(result.subgames) == 6
    assert len(sdk.sender.sent) == 1
    report = sdk.sender.sent[0]
    assert report["recipient"] == "rmisegal+uoh26b@gmail.com"
    assert (tmp_path / "reports" / "unit_report.json").exists()
    assert (tmp_path / "reports" / "transcripts" / "unit" / "moves.jsonl").exists()


def test_sdk_report_only_dispatches():
    sdk = make_sdk()
    sdk.report_only({"recipient": "x", "subject": "y", "totals": {}})
    assert sdk.sender.sent[-1]["recipient"] == "x"


def test_cli_version(capsys):
    assert main(["version"]) == 0
    assert __version__ in capsys.readouterr().out


def test_cli_play_invokes_sdk(monkeypatch, capsys):
    calls = {}

    class FakeSDK:
        def __init__(self, *a, **k):
            calls["init"] = k

        async def play(self):
            from parley.domain.records import GameResult

            return GameResult([], {"cop": 120, "thief": 30}, "t0", "t1")

    monkeypatch.setattr("parley.cli_handlers.ParleySDK", FakeSDK)
    assert main(["play", "--provider", "ollama", "--run-label", "x"]) == 0
    assert calls["init"]["provider_name"] == "ollama"
    assert "cop 120" in capsys.readouterr().out


def test_cli_report_reads_file(tmp_path, monkeypatch):
    path = tmp_path / "r.json"
    path.write_text(json.dumps({"recipient": "a", "subject": "b"}))
    sent = {}
    monkeypatch.setattr(
        "parley.cli_handlers.ParleySDK",
        lambda *a, **k: type("S", (), {"report_only": lambda self, r: sent.update(r)})(),
    )
    assert main(["report", "--file", str(path)]) == 0
    assert sent["recipient"] == "a"


def test_cli_requires_command():
    with pytest.raises(SystemExit):
        build_parser().parse_args([])
