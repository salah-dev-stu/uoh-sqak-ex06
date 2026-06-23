"""Ollama provider — local, free, small models (H9 local fallback)."""

from __future__ import annotations

import os
from typing import Any

from parley.shared.gatekeeper import ApiGatekeeper


class OllamaProvider:
    def __init__(self, gate: ApiGatekeeper, cfg: dict[str, Any], temperature: float = 0.8) -> None:
        self.gate = gate
        self.base_url = os.environ.get(cfg["base_url_env"], "http://localhost:11434")
        self.model = cfg["model"]
        self.timeout_s = int(cfg["timeout_s"])
        self.temperature = temperature

    def complete(self, prompt: str) -> str:
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        url = f"{self.base_url.rstrip('/')}/api/chat"
        data = self.gate.http_request("POST", url, body=body, timeout=self.timeout_s)
        return str(data["message"]["content"]).strip()
