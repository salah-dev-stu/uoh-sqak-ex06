"""The natural-language conversation log between the two agents."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DialogueLog:
    turns: list[tuple[str, str]] = field(default_factory=list)

    def append(self, role: str, message: str) -> None:
        self.turns.append((role, message))

    def last_from(self, role: str) -> str | None:
        for r, m in reversed(self.turns):
            if r == role:
                return m
        return None

    def lines(self) -> list[str]:
        return [f"{r}: {m}" for r, m in self.turns]

    def transcript(self) -> str:
        return "\n".join(self.lines())
