"""Typed, frozen config dataclasses (R4/R10 — nothing hardcoded elsewhere)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GameConfig:
    grid_size: tuple[int, int]
    max_moves: int
    num_games: int
    max_barriers: int
    vision_radius: int
    diagonal_moves: bool
    thief_first: bool
    seed: int
    start_positions: dict[str, tuple[int, int]]
    scoring: dict[str, int]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> GameConfig:
        starts = {k: tuple(v) for k, v in d["start_positions"].items()}
        return cls(
            grid_size=tuple(d["grid_size"]),
            max_moves=int(d["max_moves"]),
            num_games=int(d["num_games"]),
            max_barriers=int(d["max_barriers"]),
            vision_radius=int(d["vision_radius"]),
            diagonal_moves=bool(d["diagonal_moves"]),
            thief_first=bool(d["thief_first"]),
            seed=int(d["seed"]),
            start_positions=starts,  # type: ignore[arg-type]
            scoring={k: int(v) for k, v in d["scoring"].items()},
        )


@dataclass(frozen=True)
class LlmConfig:
    provider: str
    temperature: float
    max_tokens: int
    history_window: int
    claude_cli: dict[str, Any]
    ollama: dict[str, Any]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LlmConfig:
        return cls(
            provider=str(d["provider"]),
            temperature=float(d["temperature"]),
            max_tokens=int(d["max_tokens"]),
            history_window=int(d["history_window"]),
            claude_cli=dict(d["claude_cli"]),
            ollama=dict(d["ollama"]),
        )


@dataclass(frozen=True)
class McpConfig:
    transport: str
    cop: dict[str, Any]
    thief: dict[str, Any]
    auth: dict[str, Any]
    request_timeout_s: int

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> McpConfig:
        return cls(
            transport=str(d["transport"]),
            cop=dict(d["cop"]),
            thief=dict(d["thief"]),
            auth=dict(d["auth"]),
            request_timeout_s=int(d["request_timeout_s"]),
        )

    def role(self, role: str) -> dict[str, Any]:
        return self.cop if role == "cop" else self.thief


@dataclass(frozen=True)
class ReportConfig:
    sender: str
    recipient: str
    subject: str
    team: dict[str, Any]
    gmail: dict[str, Any]
    smtp: dict[str, Any]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ReportConfig:
        return cls(
            sender=str(d["sender"]),
            recipient=str(d["recipient"]),
            subject=str(d["subject"]),
            team=dict(d["team"]),
            gmail=dict(d["gmail"]),
            smtp=dict(d["smtp"]),
        )


@dataclass(frozen=True)
class GateConfig:
    ledger_path: str
    limits: dict[str, dict[str, int]]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> GateConfig:
        limits = {k: {kk: int(vv) for kk, vv in v.items()} for k, v in d["limits"].items()}
        return cls(ledger_path=str(d["ledger_path"]), limits=limits)


@dataclass(frozen=True)
class RuntimeConfig:
    version: str
    log_level: str
    seed: int
    paths: dict[str, str]
    gui: dict[str, Any]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RuntimeConfig:
        return cls(
            version=str(d["version"]),
            log_level=str(d["log_level"]),
            seed=int(d["seed"]),
            paths=dict(d["paths"]),
            gui=dict(d["gui"]),
        )


@dataclass(frozen=True)
class Config:
    game: GameConfig
    llm: LlmConfig
    mcp: McpConfig
    report: ReportConfig
    gate: GateConfig
    runtime: RuntimeConfig = field()
