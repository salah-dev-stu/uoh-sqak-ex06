"""M4 — mailbox, tools, server factory, async client (T187–T226). In-memory FastMCP."""

from __future__ import annotations

import pytest

from parley.mcp.client import McpClient
from parley.mcp.mailbox import Mailbox
from parley.mcp.server_factory import make_server, rules_text
from parley.shared.config import load_config
from parley.shared.gatekeeper import ApiGatekeeper
from tests.unit.domain_helpers import make_rules


class Clock:
    def seconds(self):
        return 0.0

    def iso(self):
        return "t0"


def gate():
    cfg = load_config("config")
    return ApiGatekeeper.from_config(cfg, Clock().seconds, Clock().iso, backends={})


# ── mailbox ───────────────────────────────────────────────────────────────
def test_mailbox_message_and_observation_flow():
    mb = Mailbox()
    assert mb.push_observation("you are at the wall") == "ok"
    assert mb.read_observation() == "you are at the wall"
    mb.deliver_message("I'm near the gate")
    assert mb.read_messages() == ["I'm near the gate"]
    mb.post_message("I see you")
    mb.submit_action("MOVE: N")
    assert mb.collect() == {"message": "I see you", "action": "MOVE: N"}


def test_mailbox_reset_clears():
    mb = Mailbox()
    mb.push_observation("x")
    mb.post_message("y")
    mb.reset()
    assert mb.read_observation() == "" and mb.read_messages() == []


def test_rules_text_is_nl_and_mentions_constraints():
    text = rules_text(make_rules())
    assert "natural language" in text and "Thief moves first" in text


# ── server factory + in-memory client round-trip ───────────────────────────
@pytest.mark.asyncio
async def test_server_tools_round_trip_in_memory():
    handle = make_server("cop", make_rules())
    handle.mailbox.push_observation("you face the north wall")
    handle.mailbox.deliver_message("catch me if you can")
    async with McpClient.in_memory(handle.mcp, gate()) as client:
        assert "north wall" in await client.observe()
        assert await client.read_messages() == ["catch me if you can"]
        await client.send_message("I'm closing in from the south")
        await client.act("MOVE: S")
        collected = await client.collect()
    assert collected["message"] == "I'm closing in from the south"
    assert collected["action"] == "MOVE: S"


@pytest.mark.asyncio
async def test_two_servers_have_independent_mailboxes():
    cop = make_server("cop", make_rules())
    thief = make_server("thief", make_rules())
    cop.mailbox.push_observation("cop view")
    thief.mailbox.push_observation("thief view")
    async with McpClient.in_memory(cop.mcp) as c1, McpClient.in_memory(thief.mcp) as c2:
        assert await c1.observe() == "cop view"
        assert await c2.observe() == "thief view"


@pytest.mark.asyncio
async def test_resource_exposes_rules():
    handle = make_server("thief", make_rules())
    async with McpClient.in_memory(handle.mcp) as client:
        res = await client._client.read_resource("game://rules")
    assert "natural language" in res[0].text


@pytest.mark.asyncio
async def test_client_records_calls_through_gatekeeper():
    handle = make_server("cop", make_rules())
    g = gate()
    async with McpClient.in_memory(handle.mcp, g) as client:
        await client.observe()
    assert any(e.service == "mcp" and e.action == "observe" for e in g.events)


def test_server_with_token_builds_auth():
    handle = make_server("cop", make_rules(), token="secret-cop-token")
    assert handle.mcp.name == "parley-cop"


# ── H3: servers must not import the engine mutation API or any LLM ──────────
def test_mcp_modules_are_llm_and_rule_free():
    from pathlib import Path

    import parley.mcp.mailbox as mailbox_mod
    import parley.mcp.tools as tools_mod

    for mod in (mailbox_mod, tools_mod):
        src = Path(mod.__file__).read_text()
        assert "parley.llm" not in src
        assert "from parley.domain.rules" not in src
        assert "from parley.domain.state" not in src
