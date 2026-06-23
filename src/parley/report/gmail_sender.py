"""Gmail API report sender (OAuth token, routed through the Gatekeeper) (H7)."""

from __future__ import annotations

import base64
import json
import os
from email.mime.text import MIMEText
from typing import Any

from parley.shared.gatekeeper import ApiGatekeeper


class GmailApiSender:
    def __init__(self, gate: ApiGatekeeper, report_cfg: Any) -> None:
        self.gate = gate
        self.recipient = report_cfg.recipient
        self.subject = report_cfg.subject
        self.token_env = report_cfg.gmail["token_env"]

    def _raw(self, report: dict) -> str:
        mime = MIMEText(json.dumps(report, indent=2), "plain", "utf-8")
        mime["to"] = report.get("recipient", self.recipient)
        mime["subject"] = report.get("subject", self.subject)
        return base64.urlsafe_b64encode(mime.as_bytes()).decode("ascii")

    def send(self, report: dict) -> dict:
        token_path = os.environ.get(self.token_env)
        if not token_path:
            raise RuntimeError(
                f"Gmail token path env '{self.token_env}' unset — run "
                "scripts/gmail_oauth_setup.py once, or set report.sender='smtp'"
            )
        return self.gate.google_send(token_path, self._raw(report))
