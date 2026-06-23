"""M10 — scripts wiring + committed sample artifacts are valid + NL-only."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import deploy_ngrok  # noqa: E402
import gmail_oauth_setup  # noqa: E402
import serve_servers  # noqa: E402


def test_ngrok_argv_and_url_parse():
    assert deploy_ngrok.ngrok_argv(8011) == ["ngrok", "http", "8011", "--log", "stdout"]
    url = deploy_ngrok.parse_tunnel_url("t=info msg url=https://abc-1-2.ngrok-free.app done")
    assert url == "https://abc-1-2.ngrok-free.app"


def test_ngrok_plan_uses_distinct_ports():
    plan = deploy_ngrok.plan("config")
    assert plan["cop"] != plan["thief"]


def test_serve_endpoints_distinct():
    eps = serve_servers.role_endpoints("config")
    assert eps["cop"] != eps["thief"] and eps["cop"].startswith("http://")


def test_gmail_oauth_build_flow(monkeypatch):
    built = {}

    class FakeFlow:
        @staticmethod
        def from_client_secrets_file(path, scopes):
            built["path"] = path
            built["scopes"] = scopes
            return "flow"

    monkeypatch.setitem(sys.modules, "google_auth_oauthlib", type("m", (), {}))
    monkeypatch.setitem(sys.modules, "google_auth_oauthlib.flow",
                        type("m", (), {"InstalledAppFlow": FakeFlow}))
    flow = gmail_oauth_setup.build_flow("creds.json", ["scope"])
    assert flow == "flow" and built["path"] == "creds.json"


def test_sample_report_is_valid_and_complete():
    report = json.loads((ROOT / "reports" / "sample_report.json").read_text())
    assert len(report["subgames"]) == 6
    assert report["recipient"] == "rmisegal+uoh26b@gmail.com"
    assert report["totals"]["cop"] + report["totals"]["thief"] > 0


def test_sample_transcript_is_free_nl_no_coordinates():
    text = (ROOT / "reports" / "transcripts" / "sample" / "transcript.md").read_text()
    dialogue = text.split("## Board frames")[0]
    assert not re.search(r"\(\s*\d+\s*,\s*\d+\s*\)", dialogue)
    assert "cop:" in dialogue and "thief:" in dialogue


def test_sample_ledger_records_all_gate_kinds():
    ledger = json.loads((ROOT / "reports" / "sample_gate_ledger.json").read_text())
    kinds = {e["service"] for e in ledger}
    assert {"mcp", "subprocess", "google"} <= kinds


def test_sample_moves_log_schema():
    lines = (ROOT / "reports" / "transcripts" / "sample" / "moves.jsonl").read_text().splitlines()
    row = json.loads(lines[0])
    for key in ("subgame", "move_no", "role", "action", "message", "before", "after", "barriers_left", "ts"):
        assert key in row
