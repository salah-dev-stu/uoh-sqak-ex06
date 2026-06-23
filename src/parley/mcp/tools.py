"""Register the agent tool surface + a rules resource on a FastMCP server.

Tools only read/write the mailbox; no game rules, no LLM (H3). This module is what
the meta-test inspects to prove the servers stay free of engine/LLM imports.
"""

from __future__ import annotations

from typing import Any

from parley.mcp.mailbox import Mailbox


def register_tools(mcp: Any, mailbox: Mailbox) -> None:
    @mcp.tool
    def observe() -> str:
        """Return this agent's current partial observation (prose)."""
        return mailbox.read_observation()

    @mcp.tool
    def read_messages() -> list[str]:
        """Return the free-NL messages the opponent has sent so far."""
        return mailbox.read_messages()

    @mcp.tool
    def send_message(text: str) -> str:
        """Send a free-natural-language message to the opponent."""
        return mailbox.post_message(text)

    @mcp.tool
    def act(token: str) -> str:
        """Record this agent's action token (e.g. 'MOVE: NE' or 'BARRIER')."""
        return mailbox.submit_action(token)

    @mcp.tool
    def push_observation(text: str) -> str:
        """Orchestrator control: set the agent's observation for this turn."""
        return mailbox.push_observation(text)

    @mcp.tool
    def deliver_message(text: str) -> str:
        """Orchestrator control: deliver the opponent's latest message."""
        return mailbox.deliver_message(text)

    @mcp.tool
    def collect() -> dict[str, str | None]:
        """Orchestrator control: read back the agent's message + action."""
        return mailbox.collect()

    @mcp.tool
    def reset() -> str:
        """Orchestrator control: clear the mailbox between sub-games."""
        return mailbox.reset()


def register_resources(mcp: Any, rules_text: str) -> None:
    @mcp.resource("game://rules")
    def rules() -> str:
        """The agreed game rules (config-derived; static, no LLM)."""
        return rules_text
