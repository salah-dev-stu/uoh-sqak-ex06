"""Claude CLI provider — drives the local `claude` subscription, no API key (H9).

The orchestrator shells out to `claude -p <prompt>` through the Gatekeeper, so the
grader never needs an Anthropic API key and tests mock the subprocess entirely.
"""

from __future__ import annotations

import json
import os
import shutil
from collections.abc import Callable
from typing import Any

from parley.shared.gatekeeper import ApiGatekeeper


def _parse_stdout(stdout: str) -> str:
    text = stdout.strip()
    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(data, dict) and "result" in data:
        return str(data["result"]).strip()
    return text


class ClaudeCliProvider:
    def __init__(
        self,
        gate: ApiGatekeeper,
        cfg: dict[str, Any],
        which: Callable[[str], str | None] = shutil.which,
    ) -> None:
        self.gate = gate
        self.bin = os.environ.get(cfg["bin_env"], "claude")
        self.model = cfg["model"]
        self.extra_args = list(cfg.get("extra_args", []))
        self.timeout_s = int(cfg["timeout_s"])
        self._which = which

    def preflight(self) -> None:
        """Fail early with an actionable message if the CLI is unavailable (H9)."""
        if self._which(self.bin) is None:
            raise RuntimeError(
                f"claude CLI '{self.bin}' not found on PATH — install it and sign in, "
                "or set llm.provider='ollama' in config/llm.json"
            )

    def complete(self, prompt: str) -> str:
        argv = [self.bin, "-p", prompt, "--model", self.model, *self.extra_args]
        result = self.gate.run_subprocess(argv, self.timeout_s)
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI failed (exit {result.returncode}): {result.stderr.strip()}")
        return _parse_stdout(result.stdout)
