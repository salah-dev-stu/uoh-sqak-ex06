"""Parse an LLM reply into a free-NL message + a discrete action token.

The prose body is the graded artifact; the trailing ``MOVE:``/``BARRIER`` token is
mechanics. Any leaked ``(x, y)`` coordinates are scrubbed from the message so the
dialogue stays free natural language (H2).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from parley.domain.actions import Action, Move, PlaceBarrier
from parley.domain.geometry import Direction

_COORD = re.compile(r"\(\s*\d+\s*,\s*\d+\s*\)")
_MOVE = re.compile(r"MOVE\s*:?\s*([A-Za-z]{1,2})", re.IGNORECASE)
_BARRIER = re.compile(r"\bBARRIER\b", re.IGNORECASE)


@dataclass(frozen=True)
class ParsedReply:
    message: str
    action: Action | None


def parse_reply(text: str) -> ParsedReply:
    action: Action | None = None
    move_match = _MOVE.search(text)
    if move_match:
        try:
            action = Move(Direction.from_name(move_match.group(1)))
        except ValueError:
            action = None
    if action is None and _BARRIER.search(text):
        action = PlaceBarrier()

    message = _MOVE.sub("", text)
    message = _BARRIER.sub("", message)
    message = _COORD.sub("", message)
    message = re.sub(r"\n{2,}", "\n", message).strip(" \n\t\"")
    return ParsedReply(message=message, action=action)
