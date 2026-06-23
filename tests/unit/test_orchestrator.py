"""M5 — dialogue, driver, engine, sub-game/game runners, pipeline (T227–T273)."""

from __future__ import annotations

import re

import pytest

from parley.domain.geometry import Position
from parley.domain.pieces import Role
from parley.domain.state import GameState
from parley.mcp.client import McpClient
from parley.mcp.server_factory import make_server
from parley.orchestrator.agent_driver import AgentDriver
from parley.orchestrator.dialogue import DialogueLog
from parley.orchestrator.game_runner import GameRunner
from parley.orchestrator.pipeline import Pipeline
from parley.orchestrator.subgame_runner import SubGameRunner
from parley.orchestrator.turn_engine import TurnEngine
from parley.shared.config import load_config
from parley.shared.gatekeeper import ApiGatekeeper
from tests.unit.domain_helpers import make_rules
from tests.unit.fakes import FakeProvider, RecordingSender


def iso():
    return "2026-06-23T12:00:00+03:00"


def gate():
    cfg = load_config("config")
    return ApiGatekeeper.from_config(cfg, lambda: 0.0, iso, backends={})


def test_dialogue_log():
    d = DialogueLog()
    d.append("cop", "hi")
    d.append("thief", "nope")
    d.append("cop", "closing")
    assert d.last_from("thief") == "nope"
    assert d.lines()[0] == "cop: hi"
    assert "thief: nope" in d.transcript()


@pytest.mark.asyncio
async def test_agent_driver_falls_back_on_bad_reply():
    handle = make_server("cop", make_rules())
    d = DialogueLog()
    async with McpClient.in_memory(handle.mcp) as client:
        driver = AgentDriver(Role.COP, FakeProvider("no token here at all"), client, make_rules(), d)
        decision = await driver.take_turn(GameState.initial(make_rules()))
    assert decision.action is not None  # safe fallback chosen
    assert decision.message  # default message supplied
    assert d.last_from("cop") == decision.message


@pytest.mark.asyncio
async def test_subgame_reaches_capture_deterministically():
    rules = make_rules()
    cop = make_server("cop", rules)
    thief = make_server("thief", rules)
    d = DialogueLog()
    async with McpClient.in_memory(cop.mcp) as cc, McpClient.in_memory(thief.mcp) as tc:
        drivers = {
            Role.COP: AgentDriver(Role.COP, FakeProvider("Closing in.\nMOVE: SE"), cc, rules, d),
            Role.THIEF: AgentDriver(Role.THIEF, FakeProvider("Fleeing!\nMOVE: NW"), tc, rules, d),
        }
        engine = TurnEngine(rules, iso)
        runner = SubGameRunner(rules, engine, "uoh-sqak")
        result = await runner.run(0, GameState.initial(rules), drivers)
    assert result.winner == "cop"
    assert result.scores["cop"] == 20 and result.scores["thief"] == 5
    assert result.moves <= 25 and len(result.log) == result.moves


@pytest.mark.asyncio
async def test_subgame_thief_survives_short_game():
    rules = make_rules(max_moves=4, start_positions={"cop": Position(0, 0), "thief": Position(2, 4)})
    cop = make_server("cop", rules)
    thief = make_server("thief", rules)
    d = DialogueLog()
    async with McpClient.in_memory(cop.mcp) as cc, McpClient.in_memory(thief.mcp) as tc:
        drivers = {
            Role.COP: AgentDriver(Role.COP, FakeProvider("Patrolling east.\nMOVE: E"), cc, rules, d),
            Role.THIEF: AgentDriver(Role.THIEF, FakeProvider("Drifting east.\nMOVE: E"), tc, rules, d),
        }
        runner = SubGameRunner(rules, TurnEngine(rules, iso), "uoh-sqak")
        result = await runner.run(0, GameState.initial(rules), drivers)
    assert result.winner == "thief" and result.moves == 4


@pytest.mark.asyncio
async def test_full_pipeline_six_subgames_deterministic():
    rules = make_rules()
    handles = {Role.COP: make_server("cop", rules), Role.THIEF: make_server("thief", rules)}
    providers = {
        Role.COP: FakeProvider("Closing in on you.\nMOVE: SE"),
        Role.THIEF: FakeProvider("You'll never corner me.\nMOVE: NW"),
    }
    d = DialogueLog()
    sender = RecordingSender()
    captured = {}

    def artifacts(result, dialogue, report):
        captured["transcript"] = dialogue.transcript()

    pipeline = Pipeline(
        rules=rules, gate=gate(), providers=providers, handles=handles, dialogue=d,
        renderer=None, report_builder=lambda r: {"totals": r.totals, "subgames": len(r.subgames)},
        sender=sender, now_iso=iso, team="uoh-sqak", artifacts=artifacts,
    )
    result = await pipeline.run()
    assert len(result.subgames) == 6
    assert result.totals["cop"] == 6 * 20  # cop wins all six
    assert len(sender.sent) == 1  # exactly one email dispatched
    # dialogue is free natural language — no coordinate tuples leaked
    assert not re.search(r"\(\s*\d+\s*,\s*\d+\s*\)", captured["transcript"])
    assert "MOVE" not in captured["transcript"]


@pytest.mark.asyncio
async def test_game_runner_resets_between_subgames():
    rules = make_rules(num_games=2)
    handles = {Role.COP: make_server("cop", rules), Role.THIEF: make_server("thief", rules)}
    d = DialogueLog()
    async with McpClient.in_memory(handles[Role.COP].mcp) as cc, \
            McpClient.in_memory(handles[Role.THIEF].mcp) as tc:
        clients = {Role.COP: cc, Role.THIEF: tc}
        drivers = {
            Role.COP: AgentDriver(Role.COP, FakeProvider("Here.\nMOVE: SE"), cc, rules, d),
            Role.THIEF: AgentDriver(Role.THIEF, FakeProvider("Gone.\nMOVE: NW"), tc, rules, d),
        }
        runner = SubGameRunner(rules, TurnEngine(rules, iso), "uoh-sqak")
        game = GameRunner(rules, runner, drivers, clients, d, iso)
        res = await game.run()
    assert len(res.subgames) == 2
