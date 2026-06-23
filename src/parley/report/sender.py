"""Pluggable report-sender selection: Gmail API default, SMTP fallback (H7)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from parley.report.gmail_sender import GmailApiSender
from parley.report.smtp_sender import SmtpSender
from parley.shared.config_models import ReportConfig
from parley.shared.gatekeeper import ApiGatekeeper


@runtime_checkable
class ReportSender(Protocol):
    def send(self, report: dict) -> Any: ...


def make_sender(cfg: ReportConfig, gate: ApiGatekeeper) -> ReportSender:
    if cfg.sender == "gmail":
        return GmailApiSender(gate, cfg)
    if cfg.sender == "smtp":
        return SmtpSender(gate, cfg)
    raise ValueError(f"unknown report sender: {cfg.sender!r}")
