"""The one wired Gatekeeper: every external call gates + records here (R3).

This is the ONLY module permitted to import ``subprocess``/``httpx``/``smtplib``/
google libraries — a meta-test greps the source and fails CI on any escape. Real
backends are imported lazily inside ``_real_*`` so tests (which inject fakes via
``backends=``) never touch the network, a shell, or credentials.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from parley.shared.config_models import Config, GateConfig
from parley.shared.gatekeeper_types import GateEvent, GateLimitError, RunResult
from parley.shared.rate_limiter import RateLimiter


def _real_subprocess(argv: list[str], timeout: int) -> RunResult:  # pragma: no cover
    import subprocess  # noqa: PLC0415 — intentionally confined to the Gatekeeper

    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
    return RunResult(returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)


def _real_http(method: str, url: str, headers: dict, body: Any, timeout: int) -> dict:  # pragma: no cover
    import httpx  # noqa: PLC0415

    resp = httpx.request(method, url, headers=headers, json=body, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _real_smtp(host: str, port: int, user: str, password: str, message: str) -> None:  # pragma: no cover
    import smtplib  # noqa: PLC0415

    with smtplib.SMTP(host, port) as s:
        s.starttls()
        s.login(user, password)
        s.sendmail(user, [user], message)


def _real_google(token_path: str, raw: str) -> dict:  # pragma: no cover
    from google.oauth2.credentials import Credentials  # noqa: PLC0415
    from googleapiclient.discovery import build  # noqa: PLC0415

    creds = Credentials.from_authorized_user_file(token_path)
    service = build("gmail", "v1", credentials=creds)
    return service.users().messages().send(userId="me", body={"raw": raw}).execute()


class ApiGatekeeper:
    """Gates (rate + budget) and records (ledger) every external call."""

    def __init__(
        self,
        gate: GateConfig,
        now_seconds: Callable[[], float],
        now_iso: Callable[[], str],
        backends: dict[str, Callable] | None = None,
    ) -> None:
        self.limiter = RateLimiter(gate.limits, now_seconds)
        self.ledger_path = Path(gate.ledger_path)
        self._now_iso = now_iso
        self._backends = backends or {}
        self.events: list[GateEvent] = []

    @classmethod
    def from_config(
        cls,
        cfg: Config,
        now_seconds: Callable[[], float],
        now_iso: Callable[[], str],
        backends: dict[str, Callable] | None = None,
    ) -> ApiGatekeeper:
        return cls(cfg.gate, now_seconds, now_iso, backends)

    def _gate(self, service: str, action: str, meta: dict) -> None:
        allowed = self.limiter.allow(service)
        self.events.append(GateEvent(service, action, allowed, self._now_iso(), meta))
        if not allowed:
            raise GateLimitError(f"{service} limit exceeded for '{action}'")

    def run_subprocess(self, argv: list[str], timeout: int) -> RunResult:
        self._gate("subprocess", argv[0] if argv else "", {"argv": argv})
        backend = self._backends.get("subprocess", _real_subprocess)
        return backend(argv, timeout)

    def http_request(
        self, method: str, url: str, headers: dict | None = None, body: Any = None, timeout: int = 30
    ) -> dict:
        self._gate("http", method, {"url": url, "headers": headers or {}})
        backend = self._backends.get("http", _real_http)
        return backend(method, url, headers or {}, body, timeout)

    def smtp_send(self, host: str, port: int, user: str, password: str, message: str) -> None:
        self._gate("smtp", "send", {"host": host, "user": user, "password": password})
        backend = self._backends.get("smtp", _real_smtp)
        backend(host, port, user, password, message)

    def google_send(self, token_path: str, raw: str) -> dict:
        self._gate("google", "messages.send", {"token_path": token_path})
        backend = self._backends.get("google", _real_google)
        return backend(token_path, raw)

    def flush(self) -> Path:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [e.to_dict() for e in self.events]
        self.ledger_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.ledger_path
