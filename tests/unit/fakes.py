"""Test doubles: a scripted LLM provider and a recording report sender."""

from __future__ import annotations


class FakeProvider:
    """Returns a fixed natural-language reply (deterministic, no IO)."""

    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.calls = 0

    def complete(self, prompt: str) -> str:
        self.calls += 1
        return self.reply


class RecordingSender:
    def __init__(self) -> None:
        self.sent: list[dict] = []

    def send(self, report: dict) -> None:
        self.sent.append(report)
