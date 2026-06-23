"""The autonomous pipeline: init → play 6 sub-games → emailed report (H4).

No manual steps at runtime. Clients are opened, the game is played, the report is
built and dispatched, and artifacts are written — all unattended.
"""

from __future__ import annotations

from contextlib import AsyncExitStack

from parley.domain.pieces import Role
from parley.domain.records import GameResult
from parley.mcp.client import McpClient
from parley.orchestrator.agent_driver import AgentDriver
from parley.orchestrator.game_runner import GameRunner
from parley.orchestrator.subgame_runner import SubGameRunner
from parley.orchestrator.turn_engine import TurnEngine


class Pipeline:
    def __init__(self, *, rules, gate, providers, handles, dialogue, renderer,
                 report_builder, sender, now_iso, team, artifacts) -> None:
        self.rules = rules
        self.gate = gate
        self.providers = providers
        self.handles = handles
        self.dialogue = dialogue
        self.renderer = renderer
        self.report_builder = report_builder
        self.sender = sender
        self._now_iso = now_iso
        self.team = team
        self.artifacts = artifacts

    async def run(self) -> GameResult:
        async with AsyncExitStack() as stack:
            clients = {}
            for role, handle in self.handles.items():
                clients[role] = await stack.enter_async_context(
                    McpClient.in_memory(handle.mcp, self.gate)
                )
            result = await self._play(clients)
        report = self.report_builder(result)
        self.sender.send(report)
        self.artifacts(result, self.dialogue, report)
        return result

    async def _play(self, clients) -> GameResult:
        drivers = {
            role: AgentDriver(role, self.providers[role], clients[role], self.rules, self.dialogue)
            for role in (Role.COP, Role.THIEF)
        }
        engine = TurnEngine(self.rules, self._now_iso)
        subrunner = SubGameRunner(self.rules, engine, self.team, self.renderer)
        game = GameRunner(self.rules, subrunner, drivers, clients, self.dialogue, self._now_iso)
        return await game.run()
