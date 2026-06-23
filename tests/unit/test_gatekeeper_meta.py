"""M9 — R3 meta-test: no external call may bypass the Gatekeeper.

Greps every source file under ``src/parley`` and fails if a raw network / shell /
mail / Google import appears anywhere except the one sanctioned gatekeeper module.
This is what keeps the Gatekeeper *wired*, not decorative (the HW3/HW4 lesson).
"""

from __future__ import annotations

from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src" / "parley"
GATEKEEPER = SRC / "shared" / "gatekeeper.py"

FORBIDDEN = {
    "subprocess": "import subprocess",
    "httpx": "import httpx",
    "requests": "import requests",
    "smtplib": "import smtplib",
    "googleapiclient": "googleapiclient",
    "google.oauth2": "google.oauth2",
    "urllib.request": "urllib.request",
}


def _sources():
    return [p for p in SRC.rglob("*.py") if p != GATEKEEPER]


def test_no_raw_external_calls_outside_gatekeeper():
    offenders: list[str] = []
    for path in _sources():
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN.values():
            if token in text:
                offenders.append(f"{path.relative_to(SRC)} uses '{token}'")
    assert not offenders, "external calls must route through the Gatekeeper:\n" + "\n".join(offenders)


def test_gatekeeper_actually_confines_them():
    text = GATEKEEPER.read_text(encoding="utf-8")
    for token in ("import subprocess", "import httpx", "import smtplib", "googleapiclient"):
        assert token in text, f"gatekeeper should own '{token}'"


def test_mcp_servers_import_no_llm():
    for name in ("mailbox", "tools", "server_factory", "cop_server", "thief_server"):
        text = (SRC / "mcp" / f"{name}.py").read_text(encoding="utf-8")
        assert "parley.llm" not in text, f"mcp/{name}.py must not import the LLM (H3)"


def test_mcp_servers_import_no_engine_mutation():
    for name in ("mailbox", "tools"):
        text = (SRC / "mcp" / f"{name}.py").read_text(encoding="utf-8")
        assert "from parley.domain.rules" not in text
        assert "from parley.domain.state" not in text


def test_every_provider_and_sender_references_the_gate():
    for rel in ("llm/claude_cli.py", "llm/ollama.py", "report/gmail_sender.py", "report/smtp_sender.py"):
        text = (SRC / rel).read_text(encoding="utf-8")
        assert "gate." in text or "self.gate" in text, f"{rel} must call the Gatekeeper"
