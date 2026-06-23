"""Types for the Gatekeeper: service kinds, gate events, run results (R3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ServiceKind(StrEnum):
    SUBPROCESS = "subprocess"
    HTTP = "http"
    SMTP = "smtp"
    GOOGLE = "google"


class GateLimitError(RuntimeError):
    """Raised when a rate limit or budget cap is exceeded."""


_SECRET_HINTS = ("token", "password", "authorization", "secret", "key", "credential")


def redact(meta: dict[str, Any]) -> dict[str, Any]:
    """Mask any value whose key hints at a secret (R11)."""
    out: dict[str, Any] = {}
    for k, v in meta.items():
        if any(h in k.lower() for h in _SECRET_HINTS):
            out[k] = "***"
        else:
            out[k] = v
    return out


@dataclass(frozen=True)
class GateEvent:
    service: str
    action: str
    allowed: bool
    ts: str
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "action": self.action,
            "allowed": self.allowed,
            "ts": self.ts,
            "meta": redact(self.meta),
        }


@dataclass(frozen=True)
class RunResult:
    returncode: int
    stdout: str
    stderr: str
