"""Prompt construction — personas + the binding free-natural-language contract (H2)."""

from __future__ import annotations

from parley.domain.pieces import Role

_PERSONAS = {
    Role.COP: (
        "You are a determined COP chasing a thief across a grid. Your goal is to land "
        "on the thief's exact cell to make the arrest. You may also drop barriers to box "
        "the thief in."
    ),
    Role.THIEF: (
        "You are a cunning THIEF evading a cop on a grid. Your goal is to survive without "
        "being caught until the clock runs out. Mislead and slip away."
    ),
}

_CONTRACT = (
    "COMMUNICATION RULES (binding):\n"
    "- Speak to your opponent in free, natural language only — like two people taunting "
    "across a rooftop.\n"
    "- NEVER send raw coordinates, (x,y) tuples, JSON, or grid indices. Describe positions "
    "in words (walls, corners, compass directions).\n"
    "- You may negotiate framing with your opponent in prose (e.g. which corner is 'the top').\n"
    "- React to what your opponent just said; infer where they are from their words.\n"
)

_FORMAT = (
    "Respond with TWO parts:\n"
    "1) One or two sentences of natural-language message to your opponent.\n"
    "2) On the FINAL line, your action token: `MOVE: <N|NE|E|SE|S|SW|W|NW>` or, if you are "
    "the cop and choose to drop a barrier, `BARRIER`.\n"
)


def build_prompt(
    role: Role,
    observation_text: str,
    opponent_message: str | None,
    history: list[str],
) -> str:
    """Assemble the full prompt for one agent's turn."""
    last = opponent_message or "(your opponent has not spoken yet)"
    convo = "\n".join(history[-6:]) if history else "(no prior dialogue)"
    return (
        f"{_PERSONAS[role]}\n\n"
        f"{_CONTRACT}\n"
        f"WHAT YOU PERCEIVE:\n{observation_text}\n\n"
        f"YOUR OPPONENT JUST SAID:\n\"{last}\"\n\n"
        f"RECENT DIALOGUE:\n{convo}\n\n"
        f"{_FORMAT}"
    )
