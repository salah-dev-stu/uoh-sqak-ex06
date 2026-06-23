"""The LLM provider interface — lives in the MCP client, never in a server (H3)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Anything that turns a prompt into a completion string."""

    def complete(self, prompt: str) -> str: ...
