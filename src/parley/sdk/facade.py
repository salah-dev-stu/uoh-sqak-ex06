"""ParleySDK — the single public entry point for all business logic (R1)."""

from __future__ import annotations

import time
from dataclasses import replace
from datetime import UTC, datetime

from parley.domain.config_bridge import GameRules
from parley.domain.pieces import Role
from parley.domain.records import GameResult
from parley.gui.renderer import make_renderer
from parley.llm.factory import make_provider
from parley.mcp.launch import build_role_server
from parley.orchestrator.dialogue import DialogueLog
from parley.orchestrator.pipeline import Pipeline
from parley.report.builder import build_report
from parley.report.sender import make_sender
from parley.sdk.artifacts import write_artifacts
from parley.shared.config import load_config
from parley.shared.gatekeeper import ApiGatekeeper
from parley.shared.paths import Paths
from parley.shared.version import __version__


def _default_iso() -> str:
    return datetime.now(UTC).astimezone().isoformat(timespec="seconds")


class ParleySDK:
    def __init__(self, config_dir: str = "config", *, provider=None, sender=None, gate=None,
                 now_iso=None, now_seconds=None, run_label: str = "latest", echo: bool = False,
                 provider_name: str | None = None) -> None:
        self.cfg = load_config(config_dir)
        self.version = __version__
        self.now_iso = now_iso or _default_iso
        self.now_seconds = now_seconds or time.monotonic
        self.gate = gate or ApiGatekeeper.from_config(self.cfg, self.now_seconds, self.now_iso)
        self.rules = GameRules.from_game_config(self.cfg.game)
        llm_cfg = replace(self.cfg.llm, provider=provider_name) if provider_name else self.cfg.llm
        self.provider = provider or make_provider(llm_cfg, self.gate)
        self.sender = sender or make_sender(self.cfg.report, self.gate)
        self.paths = Paths.from_runtime(".", self.cfg.runtime.paths)
        self.run_label = run_label
        self.echo = echo

    def server_urls(self) -> dict[str, str]:
        urls = {}
        for role in ("cop", "thief"):
            rc = self.cfg.mcp.role(role)
            urls[role] = f"http://{rc['host']}:{rc['port']}{rc['path']}"
        return urls

    def deploy_info(self) -> dict:
        return {"servers": self.server_urls(), "auth": self.cfg.mcp.auth, "transport": self.cfg.mcp.transport}

    async def play(self) -> GameResult:
        handles = {Role.COP: build_role_server("cop"), Role.THIEF: build_role_server("thief")}
        dialogue = DialogueLog()
        renderer = make_renderer(self.cfg.runtime, echo=self.echo)
        urls = self.server_urls()
        team = self.cfg.report.team.get("group_code", "uoh-sqak")

        def builder(result: GameResult) -> dict:
            return build_report(result, self.cfg, urls, self.version)

        def artifacts(result: GameResult, dlg: DialogueLog, report: dict) -> None:
            write_artifacts(self.paths, self.run_label, result, dlg, report, renderer, self.gate)

        pipeline = Pipeline(
            rules=self.rules, gate=self.gate, providers={Role.COP: self.provider, Role.THIEF: self.provider},
            handles=handles, dialogue=dialogue, renderer=renderer, report_builder=builder,
            sender=self.sender, now_iso=self.now_iso, team=team, artifacts=artifacts,
        )
        return await pipeline.run()

    def report_only(self, report: dict) -> object:
        """Dispatch an already-built report through the configured sender."""
        return self.sender.send(report)
