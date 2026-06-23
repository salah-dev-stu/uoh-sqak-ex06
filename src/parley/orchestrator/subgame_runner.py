"""Run a single sub-game: alternate turns until capture, survival, or a trap."""

from __future__ import annotations

from parley.domain.pieces import Role
from parley.domain.records import SubGameResult
from parley.domain.scoring import score_subgame
from parley.domain.state import GameState
from parley.domain.terminal import check_terminal, trapped_winner
from parley.orchestrator.turn_engine import TurnEngine


class SubGameRunner:
    def __init__(self, rules, engine: TurnEngine, team: str, renderer=None) -> None:
        self.rules = rules
        self.engine = engine
        self.team = team
        self.renderer = renderer

    async def run(self, index: int, state: GameState, drivers: dict[Role, object]) -> SubGameResult:
        records = []
        winner = None
        while winner is None and state.move_count < self.rules.max_moves:
            role = state.turn
            winner = trapped_winner(state, role, self.rules)
            if winner is not None:
                break
            state, record = await self.engine.half_turn(state, drivers[role])
            records.append(record)
            if self.renderer is not None:
                self.renderer.render(state, record)
            winner = check_terminal(state, self.rules)
        if winner is None:
            winner = Role.THIEF  # survived max_moves
        scores = {str(r): v for r, v in score_subgame(winner, self.rules.scoring).items()}
        return SubGameResult(
            index=index,
            cop_role_team=self.team,
            winner=str(winner),
            moves=state.move_count,
            scores=scores,
            log=records,
        )
