"""Per-agent mailbox — the only state an MCP server holds (transient I/O, no rules).

Holds the partial observation the orchestrator pushed, the opponent's delivered
messages, this agent's outgoing messages, and the last action token. It contains
NO game logic and imports NO LLM — that keeps the server a pure tool provider (H3).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Mailbox:
    observation: str = ""
    inbox: list[str] = field(default_factory=list)
    outbox: list[str] = field(default_factory=list)
    last_action: str | None = None

    # ── agent-facing surface ────────────────────────────────────────────
    def read_observation(self) -> str:
        return self.observation

    def read_messages(self) -> list[str]:
        return list(self.inbox)

    def post_message(self, text: str) -> str:
        self.outbox.append(text)
        return "queued"

    def submit_action(self, token: str) -> str:
        self.last_action = token
        return "recorded"

    # ── orchestrator control surface ────────────────────────────────────
    def push_observation(self, text: str) -> str:
        self.observation = text
        return "ok"

    def deliver_message(self, text: str) -> str:
        self.inbox.append(text)
        return "ok"

    def collect(self) -> dict[str, str | None]:
        return {"message": self.outbox[-1] if self.outbox else "", "action": self.last_action}

    def reset(self) -> str:
        self.observation = ""
        self.inbox.clear()
        self.outbox.clear()
        self.last_action = None
        return "reset"
