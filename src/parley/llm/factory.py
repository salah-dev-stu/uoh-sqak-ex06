"""Build the configured LLM provider (cloud Claude CLI or local Ollama) (H9)."""

from __future__ import annotations

from parley.llm.claude_cli import ClaudeCliProvider
from parley.llm.ollama import OllamaProvider
from parley.llm.provider import LLMProvider
from parley.shared.config_models import LlmConfig
from parley.shared.gatekeeper import ApiGatekeeper


def make_provider(cfg: LlmConfig, gate: ApiGatekeeper) -> LLMProvider:
    if cfg.provider == "claude_cli":
        return ClaudeCliProvider(gate, cfg.claude_cli)
    if cfg.provider == "ollama":
        return OllamaProvider(gate, cfg.ollama, temperature=cfg.temperature)
    raise ValueError(f"unknown llm provider: {cfg.provider!r}")
