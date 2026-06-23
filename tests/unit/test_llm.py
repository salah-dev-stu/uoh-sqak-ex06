"""M3 — llm providers, prompts, parser (T146–T186). All IO mocked."""

from __future__ import annotations

import re

import pytest

from parley.domain.actions import Move, PlaceBarrier
from parley.domain.geometry import Direction, Position
from parley.domain.observation import observe
from parley.domain.pieces import Role
from parley.domain.state import GameState
from parley.llm.claude_cli import ClaudeCliProvider
from parley.llm.factory import make_provider
from parley.llm.obs_text import relative_dir, render_observation
from parley.llm.ollama import OllamaProvider
from parley.llm.parser import parse_reply
from parley.llm.prompts import build_prompt
from parley.shared.config import load_config
from parley.shared.gatekeeper import ApiGatekeeper
from parley.shared.gatekeeper_types import RunResult
from tests.unit.domain_helpers import make_rules


class Clock:
    def seconds(self):
        return 0.0

    def iso(self):
        return "t0"


def gate(backends):
    cfg = load_config("config")
    return ApiGatekeeper.from_config(cfg, Clock().seconds, Clock().iso, backends=backends)


def test_claude_cli_builds_argv_and_parses_json(env_tokens, monkeypatch):
    captured = {}

    def fake_sub(argv, timeout):
        captured["argv"] = argv
        return RunResult(0, '{"result": "I dash north. MOVE: N"}', "")

    prov = ClaudeCliProvider(gate({"subprocess": fake_sub}), load_config("config").llm.claude_cli)
    out = prov.complete("hello")
    assert "MOVE: N" in out
    assert captured["argv"][0:3] == ["claude", "-p", "hello"]
    assert "--model" in captured["argv"]


def test_claude_cli_plain_text_passthrough(env_tokens):
    prov = ClaudeCliProvider(gate({"subprocess": lambda a, t: RunResult(0, "plain reply", "")}),
                             load_config("config").llm.claude_cli)
    assert prov.complete("x") == "plain reply"


def test_claude_cli_nonzero_exit_raises(env_tokens):
    prov = ClaudeCliProvider(gate({"subprocess": lambda a, t: RunResult(2, "", "boom")}),
                             load_config("config").llm.claude_cli)
    with pytest.raises(RuntimeError, match="claude CLI failed"):
        prov.complete("x")


def test_claude_cli_preflight_raises_when_missing(env_tokens):
    prov = ClaudeCliProvider(gate({}), load_config("config").llm.claude_cli, which=lambda b: None)
    with pytest.raises(RuntimeError, match="not found on PATH"):
        prov.preflight()


def test_ollama_posts_and_parses(env_tokens):
    def fake_http(method, url, headers, body, timeout):
        assert url.endswith("/api/chat") and body["model"]
        return {"message": {"content": "I creep away. MOVE: SW"}}

    prov = OllamaProvider(gate({"http": fake_http}), load_config("config").llm.ollama)
    assert "MOVE: SW" in prov.complete("hi")


def test_factory_selects_provider(env_tokens):
    cfg = load_config("config")
    assert isinstance(make_provider(cfg.llm, gate({})), ClaudeCliProvider)


def test_factory_ollama_and_unknown(env_tokens):
    cfg = load_config("config")
    ollama_cfg = type(cfg.llm)(**{**cfg.llm.__dict__, "provider": "ollama"})
    assert isinstance(make_provider(ollama_cfg, gate({})), OllamaProvider)
    bad = type(cfg.llm)(**{**cfg.llm.__dict__, "provider": "nope"})
    with pytest.raises(ValueError):
        make_provider(bad, gate({}))


def test_prompt_forbids_coordinates_and_sets_persona():
    obs = render_observation(observe(GameState.initial(make_rules()), Role.COP, 1, 5))
    prompt = build_prompt(Role.COP, obs, "I'm by the south wall", ["cop: hi", "thief: bye"])
    assert "COP" in prompt
    assert "NEVER send raw coordinates" in prompt
    assert "I'm by the south wall" in prompt
    assert "MOVE:" in prompt


def test_prompt_thief_persona_and_empty_history():
    prompt = build_prompt(Role.THIEF, "obs", None, [])
    assert "THIEF" in prompt and "not spoken yet" in prompt


def test_render_observation_has_no_coordinate_tuples():
    obs = observe(GameState.initial(make_rules()), Role.COP, 1, 5)
    text = render_observation(obs)
    assert not re.search(r"\(\s*\d+\s*,\s*\d+\s*\)", text)
    assert "out of sight" in text  # thief at (4,4) not visible from (0,0)


def test_render_observation_reports_visible_opponent():
    r = make_rules(start_positions={"cop": Position(2, 2), "thief": Position(1, 2)})
    text = render_observation(observe(GameState.initial(r), Role.COP, 1, 5))
    assert "catch sight" in text and "north" in text


def test_relative_dir_words():
    assert "north-west" in relative_dir(Position(3, 3), Position(2, 2))
    assert relative_dir(Position(1, 1), Position(1, 1)) == "right on top of you"


def test_parse_move_token():
    p = parse_reply("I sprint to high ground.\nMOVE: NE")
    assert p.action == Move(Direction.NE) and "high ground" in p.message and "MOVE" not in p.message


def test_parse_barrier_token():
    p = parse_reply("You're trapped now.\nBARRIER")
    assert isinstance(p.action, PlaceBarrier) and "trapped" in p.message


def test_parse_no_token_returns_none():
    p = parse_reply("Just chatting, no move here.")
    assert p.action is None


def test_parse_strips_leaked_coordinates():
    p = parse_reply("I'm at (2,3) near the corner. MOVE: S")
    assert "(2,3)" not in p.message and p.action == Move(Direction.S)


def test_parse_case_insensitive():
    assert parse_reply("sliding off. move: w").action == Move(Direction.W)
