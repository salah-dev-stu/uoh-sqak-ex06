"""M1 — gatekeeper, rate limiter, auth (T044–T066). All backends injected."""

from __future__ import annotations

import pytest

from parley.shared.auth import TokenStore, verify_bearer
from parley.shared.config import load_config
from parley.shared.gatekeeper import ApiGatekeeper
from parley.shared.gatekeeper_types import GateLimitError, RunResult, redact
from parley.shared.rate_limiter import RateLimiter


class Clock:
    def __init__(self) -> None:
        self.t = 0.0

    def seconds(self) -> float:
        return self.t

    def iso(self) -> str:
        return f"2026-06-23T12:00:{int(self.t):02d}+03:00"


def make_gate(cfg, backends, clock=None):
    clock = clock or Clock()
    return ApiGatekeeper.from_config(cfg, clock.seconds, clock.iso, backends=backends)


def test_subprocess_routes_through_backend_and_records(config_dir):
    cfg = load_config(config_dir)
    calls = []
    gate = make_gate(cfg, {"subprocess": lambda argv, t: calls.append(argv) or RunResult(0, "ok", "")})
    out = gate.run_subprocess(["claude", "-p", "hi"], 5)
    assert out.stdout == "ok"
    assert calls == [["claude", "-p", "hi"]]
    assert gate.events[-1].service == "subprocess"


def test_http_routes_through_backend(config_dir):
    cfg = load_config(config_dir)
    gate = make_gate(cfg, {"http": lambda m, u, h, b, t: {"echo": u}})
    assert gate.http_request("POST", "http://x/y")["echo"] == "http://x/y"


def test_smtp_and_google_route_and_record(config_dir):
    cfg = load_config(config_dir)
    sent = {}
    gate = make_gate(
        cfg,
        {
            "smtp": lambda h, p, u, pw, m: sent.update(smtp=(h, u)),
            "google": lambda tok, raw: sent.update(google=raw) or {"id": "1"},
        },
    )
    gate.smtp_send("smtp.x", 587, "me@x", "pw", "msg")
    assert gate.google_send("token.json", "RAW")["id"] == "1"
    assert sent["smtp"] == ("smtp.x", "me@x")
    services = {e.service for e in gate.events}
    assert {"smtp", "google"} <= services


def test_rate_limit_raises_when_exceeded(config_dir):
    cfg = load_config(config_dir)
    clock = Clock()
    gate = make_gate(cfg, {"smtp": lambda *a: None}, clock)
    # smtp rate_per_min=10 → 11th call within the same instant exceeds the bucket.
    with pytest.raises(GateLimitError):
        for _ in range(11):
            gate.smtp_send("h", 1, "u", "p", "m")


def test_budget_cap_blocks(config_dir):
    limits = {"http": {"rate_per_min": 1000, "budget": 2}}
    clock = Clock()
    rl = RateLimiter(limits, clock.seconds)
    assert rl.allow("http") and rl.allow("http")
    assert rl.allow("http") is False  # budget spent


def test_ledger_flush_writes_json(config_dir, tmp_path):
    cfg = load_config(config_dir)
    gate = make_gate(cfg, {"subprocess": lambda a, t: RunResult(0, "", "")})
    gate.ledger_path = tmp_path / "ledger.json"
    gate.run_subprocess(["claude"], 1)
    path = gate.flush()
    assert path.exists()
    assert "subprocess" in path.read_text()


def test_redaction_masks_secrets():
    masked = redact({"password": "hunter2", "url": "http://x", "token_path": "t.json"})
    assert masked["password"] == "***"
    assert masked["token_path"] == "***"
    assert masked["url"] == "http://x"


def test_token_store_reads_env(env_tokens):
    store = TokenStore({"cop": "PARLEY_COP_TOKEN", "thief": "PARLEY_THIEF_TOKEN"})
    assert store.token("cop") == "cop-token-abc"
    assert store.header("thief")["Authorization"] == "Bearer thief-token-xyz"


def test_token_store_raises_when_unset():
    store = TokenStore({"cop": "PARLEY_MISSING_TOKEN_X"})
    with pytest.raises(RuntimeError, match="unset"):
        store.token("cop")


def test_verify_bearer():
    assert verify_bearer("Bearer abc", "abc") is True
    assert verify_bearer("Bearer abc", "xyz") is False
    assert verify_bearer(None, "abc") is False
    assert verify_bearer("abc", "abc") is False
