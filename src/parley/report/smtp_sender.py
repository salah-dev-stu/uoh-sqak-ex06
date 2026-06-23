"""SMTP fallback report sender (routed through the Gatekeeper) (H7)."""

from __future__ import annotations

import json
import os
from email.mime.text import MIMEText
from typing import Any

from parley.shared.gatekeeper import ApiGatekeeper


class SmtpSender:
    def __init__(self, gate: ApiGatekeeper, report_cfg: Any) -> None:
        self.gate = gate
        self.recipient = report_cfg.recipient
        self.subject = report_cfg.subject
        self.smtp = report_cfg.smtp

    def _message(self, report: dict, sender: str) -> str:
        mime = MIMEText(json.dumps(report, indent=2), "plain", "utf-8")
        mime["from"] = sender
        mime["to"] = report.get("recipient", self.recipient)
        mime["subject"] = report.get("subject", self.subject)
        return mime.as_string()

    def send(self, report: dict) -> None:
        host = os.environ.get(self.smtp["host_env"], "localhost")
        port = int(os.environ.get(self.smtp["port_env"], "587"))
        user = os.environ.get(self.smtp["user_env"], "")
        password = os.environ.get(self.smtp["password_env"], "")
        sender = os.environ.get(self.smtp["from_env"], user)
        self.gate.smtp_send(host, port, user, password, self._message(report, sender))
