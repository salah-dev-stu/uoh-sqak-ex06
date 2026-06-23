"""Build a FastMCP server for one agent role (H1 — one server per agent).

Servers are stateless tool/resource providers with NO LLM (H3). When a bearer
token is supplied the HTTP transport is protected by a StaticTokenVerifier (H8).
"""

from __future__ import annotations

from dataclasses import dataclass

from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

from parley.mcp.mailbox import Mailbox
from parley.mcp.tools import register_resources, register_tools


def rules_text(rules) -> str:
    rows, cols = rules.grid_size
    return (
        f"Cops & Robbers on a {rows}x{cols} grid. Thief moves first, then cop, "
        f"alternating, up to {rules.max_moves} moves. Eight-direction movement "
        f"{'with' if rules.diagonal_moves else 'without'} diagonals. The cop may drop "
        f"up to {rules.max_barriers} barriers. Cop wins by sharing the thief's cell; "
        "the thief wins by surviving. Speak only in free natural language."
    )


@dataclass
class ServerHandle:
    role: str
    mcp: FastMCP
    mailbox: Mailbox


def make_server(role: str, rules, token: str | None = None) -> ServerHandle:
    auth = None
    if token:
        auth = StaticTokenVerifier(tokens={token: {"client_id": role, "scopes": []}})
    mcp = FastMCP(name=f"parley-{role}", auth=auth)
    mailbox = Mailbox()
    register_tools(mcp, mailbox)
    register_resources(mcp, rules_text(rules))
    return ServerHandle(role=role, mcp=mcp, mailbox=mailbox)
