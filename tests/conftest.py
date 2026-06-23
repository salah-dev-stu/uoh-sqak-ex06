"""Shared pytest fixtures — all external IO is mocked, no keys/servers needed."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"


@pytest.fixture
def config_dir() -> Path:
    """The repo's real config directory (valid, complete)."""
    return CONFIG_DIR


@pytest.fixture
def env_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Inject fake bearer tokens + provider env so config env-refs resolve."""
    monkeypatch.setenv("PARLEY_COP_TOKEN", "cop-token-abc")
    monkeypatch.setenv("PARLEY_THIEF_TOKEN", "thief-token-xyz")
    monkeypatch.setenv("PARLEY_CLAUDE_CLI_BIN", "claude")
    monkeypatch.setenv("PARLEY_OLLAMA_BASE_URL", "http://localhost:11434")


@pytest.fixture
def fixed_clock() -> str:
    """A deterministic timestamp for report/record tests."""
    return "2026-06-23T12:00:00+03:00"
