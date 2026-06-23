"""Async MCP client — the orchestrator's handle on one agent's FastMCP server.

Wraps ``fastmcp.Client`` (in-memory for the deterministic local run + tests, HTTP
for the remote/cloud demonstration). Every tool call is recorded through the
Gatekeeper so the MCP traffic stays on the audited ledger (R3).
"""

from __future__ import annotations

from typing import Any

from fastmcp import Client

from parley.shared.gatekeeper import ApiGatekeeper


class McpClient:
    def __init__(self, client: Client, gate: ApiGatekeeper | None = None) -> None:
        self._client = client
        self._gate = gate

    @classmethod
    def in_memory(cls, server: Any, gate: ApiGatekeeper | None = None) -> McpClient:
        return cls(Client(server), gate)

    @classmethod
    def http(cls, url: str, token: str, gate: ApiGatekeeper | None = None) -> McpClient:
        return cls(Client(url, auth=token), gate)

    async def __aenter__(self) -> McpClient:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self._client.__aexit__(*exc)

    async def _call(self, tool: str, args: dict[str, Any] | None = None) -> Any:
        if self._gate is not None:
            self._gate.note("mcp", tool, {"args": list((args or {}).keys())})
        result = await self._client.call_tool(tool, args or {})
        return result.data

    # ── agent surface ───────────────────────────────────────────────────
    async def observe(self) -> str:
        return await self._call("observe")

    async def read_messages(self) -> list[str]:
        return await self._call("read_messages")

    async def send_message(self, text: str) -> str:
        return await self._call("send_message", {"text": text})

    async def act(self, token: str) -> str:
        return await self._call("act", {"token": token})

    # ── orchestrator control surface ────────────────────────────────────
    async def push_observation(self, text: str) -> str:
        return await self._call("push_observation", {"text": text})

    async def deliver_message(self, text: str) -> str:
        return await self._call("deliver_message", {"text": text})

    async def collect(self) -> dict[str, Any]:
        return await self._call("collect")

    async def reset(self) -> str:
        return await self._call("reset")
