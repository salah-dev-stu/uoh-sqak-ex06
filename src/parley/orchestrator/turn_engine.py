"""Apply one agent's chosen action to the authoritative state and log it."""

from __future__ import annotations

from parley.domain.observation import observe
from parley.domain.records import MoveRecord
from parley.domain.rules import apply
from parley.domain.state import GameState
from parley.orchestrator.agent_driver import AgentDriver


class TurnEngine:
    def __init__(self, rules, now_iso) -> None:
        self.rules = rules
        self._now_iso = now_iso

    async def half_turn(self, state: GameState, driver: AgentDriver) -> tuple[GameState, MoveRecord]:
        role = driver.role
        before = state.position(role)
        decision = await driver.take_turn(state)
        new_state = apply(state, role, decision.action, self.rules)
        after = new_state.position(role)
        obs = observe(new_state, role, self.rules.vision_radius, self.rules.max_barriers)
        record = MoveRecord(
            move_no=new_state.move_count,
            role=str(role),
            action=str(decision.action),
            message=decision.message,
            before=(before.row, before.col),
            after=(after.row, after.col),
            barriers_left=obs.barriers_left,
            ts=self._now_iso(),
        )
        return new_state, record
