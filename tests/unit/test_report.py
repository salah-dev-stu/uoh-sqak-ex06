"""M6 — report builder + Gmail/SMTP senders (T274–T301). Senders mocked."""

from __future__ import annotations

import base64
import json

import pytest

from parley.domain.records import GameResult, SubGameResult
from parley.report.builder import build_report
from parley.report.gmail_sender import GmailApiSender
from parley.report.sender import make_sender
from parley.report.smtp_sender import SmtpSender
from parley.shared.config import load_config
from parley.shared.gatekeeper import ApiGatekeeper


def gate(backends):
    cfg = load_config("config")
    return ApiGatekeeper.from_config(cfg, lambda: 0.0, lambda: "t0", backends=backends)


def sample_result():
    subs = [
        SubGameResult(i, "uoh-sqak", "cop" if i % 2 == 0 else "thief", 5,
                      {"cop": 20 if i % 2 == 0 else 5, "thief": 5 if i % 2 == 0 else 10})
        for i in range(6)
    ]
    return GameResult(subs, {"cop": 75, "thief": 45}, "t0", "t1")


def test_report_has_all_required_fields():
    cfg = load_config("config")
    report = build_report(sample_result(), cfg, {"cop": "http://cop", "thief": "http://thief"}, "1.00")
    assert len(report["subgames"]) == 6
    assert report["totals"] == {"cop": 75, "thief": 45}
    assert report["recipient"] == "rmisegal+uoh26b@gmail.com"
    assert report["team"]["group_code"] == "uoh-sqak"
    assert report["team"]["members"][0]["id"] == "323039974"
    assert report["servers"]["cop"] == "http://cop"
    assert report["config"]["scoring"]["cop_win"] == 20
    assert report["version"] == "1.00"
    json.dumps(report)  # must be serialisable


def test_make_sender_selects_gmail_and_smtp():
    cfg = load_config("config")
    assert isinstance(make_sender(cfg.report, gate({})), GmailApiSender)
    smtp_cfg = type(cfg.report)(**{**cfg.report.__dict__, "sender": "smtp"})
    assert isinstance(make_sender(smtp_cfg, gate({})), SmtpSender)
    bad = type(cfg.report)(**{**cfg.report.__dict__, "sender": "carrier-pigeon"})
    with pytest.raises(ValueError):
        make_sender(bad, gate({}))


def test_gmail_sender_routes_through_gatekeeper(monkeypatch):
    monkeypatch.setenv("PARLEY_GMAIL_TOKEN", "token.json")
    sent = {}
    g = gate({"google": lambda token, raw: sent.update(token=token, raw=raw) or {"id": "1"}})
    sender = GmailApiSender(g, load_config("config").report)
    out = sender.send(build_report(sample_result(), load_config("config"), {}, "1.00"))
    assert out["id"] == "1" and sent["token"] == "token.json"
    decoded = base64.urlsafe_b64decode(sent["raw"]).decode()
    assert "rmisegal+uoh26b@gmail.com" in decoded and "EX06" in decoded
    assert any(e.service == "google" for e in g.events)


def test_gmail_sender_raises_without_token(monkeypatch):
    monkeypatch.delenv("PARLEY_GMAIL_TOKEN", raising=False)
    sender = GmailApiSender(gate({}), load_config("config").report)
    with pytest.raises(RuntimeError, match="oauth_setup"):
        sender.send({"recipient": "x", "subject": "y"})


def test_smtp_sender_routes_through_gatekeeper(monkeypatch):
    monkeypatch.setenv("PARLEY_SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("PARLEY_SMTP_PORT", "587")
    monkeypatch.setenv("PARLEY_SMTP_USER", "me@example.com")
    monkeypatch.setenv("PARLEY_SMTP_PASSWORD", "secret")
    monkeypatch.setenv("PARLEY_REPORT_FROM", "me@example.com")
    captured = {}
    g = gate({"smtp": lambda h, p, u, pw, m: captured.update(host=h, msg=m)})
    smtp_cfg = type(load_config("config").report)(**{**load_config("config").report.__dict__, "sender": "smtp"})
    sender = SmtpSender(g, smtp_cfg)
    sender.send(build_report(sample_result(), load_config("config"), {}, "1.00"))
    assert captured["host"] == "smtp.example.com" and "EX06" in captured["msg"]
    assert any(e.service == "smtp" for e in g.events)
