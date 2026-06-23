"""Run a full game: six consecutive sub-games, accumulating the group score."""

from __future__ import annotations

from parley.domain.pieces import Role
from parley.domain.records import GameResult
from parley.domain.state import GameState
from parley.orchestrator.subgame_runner import SubGameRunner


class GameRunner:
    def __init__(self, rules, runner: SubGameRunner, drivers, clients, dialogue, now_iso) -> None:
        self.rules = rules
        self.runner = runner
        self.drivers = drivers
        self.clients = clients
        self.dialogue = dialogue
        self._now_iso = now_iso

    async def run(self) -> GameResult:
        started = self._now_iso()
        subgames = []
        totals = {str(Role.COP): 0, str(Role.THIEF): 0}
        for index in range(self.rules.num_games):
            self.dialogue.turns.clear()
            for client in self.clients.values():
                await client.reset()
            state = GameState.initial(self.rules)
            result = await self.runner.run(index, state, self.drivers)
            subgames.append(result)
            for role, value in result.scores.items():
                totals[role] += value
        return GameResult(
            subgames=subgames,
            totals=totals,
            started_at=started,
            finished_at=self._now_iso(),
        )
