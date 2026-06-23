"""Drive one agent's turn: observe → prompt → LLM → parse → speak + act via MCP.

The LLM lives here in the client (H3). The agent perceives only its partial
observation and the opponent's free-NL messages (H2/H6). On any LLM/parse failure
it falls back to a safe legal move so the autonomous pipeline never stalls.
"""

from __future__ import annotations

from dataclasses import dataclass

from parley.domain.actions import Action, Move
from parley.domain.geometry import Direction
from parley.domain.observation import observe
from parley.domain.pieces import Role
from parley.domain.rules import is_legal, legal_moves
from parley.domain.state import GameState
from parley.llm.obs_text import render_observation
from parley.llm.parser import parse_reply
from parley.llm.prompts import build_prompt


@dataclass(frozen=True)
class TurnDecision:
    action: Action
    message: str


class AgentDriver:
    def __init__(self, role, provider, client, rules, dialogue) -> None:
        self.role = role
        self.provider = provider
        self.client = client
        self.rules = rules
        self.dialogue = dialogue

    def _safe_action(self, state: GameState) -> Action:
        legal = legal_moves(state, self.role, self.rules)
        return legal[0] if legal else Move(Direction.N)

    async def take_turn(self, state: GameState) -> TurnDecision:
        obs = observe(state, self.role, self.rules.vision_radius, self.rules.max_barriers)
        obs_text = render_observation(obs)
        await self.client.push_observation(obs_text)
        opp_last = self.dialogue.last_from(self.role.opponent)
        if opp_last:
            await self.client.deliver_message(opp_last)
        prompt = build_prompt(self.role, obs_text, opp_last, self.dialogue.lines())
        action, message = self._decide(prompt, state)
        await self.client.send_message(message)
        await self.client.act(str(action))
        await self.client.collect()
        self.dialogue.append(self.role, message)
        return TurnDecision(action=action, message=message)

    def _decide(self, prompt: str, state: GameState) -> tuple[Action, str]:
        try:
            parsed = parse_reply(self.provider.complete(prompt))
            action, message = parsed.action, parsed.message
        except Exception:  # noqa: BLE001 - any provider failure → safe fallback
            action, message = None, ""
        if action is None or not is_legal(state, self.role, action, self.rules):
            action = self._safe_action(state)
        if not message:
            verb = "circling closer" if self.role is Role.COP else "slipping away"
            message = f"I'm {verb}; you won't read my next step."
        return action, message
