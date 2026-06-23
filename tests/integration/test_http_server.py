"""Integration — a REAL FastMCP HTTP server with bearer auth (H1 HTTP + H8).

Proves the two-server design works over the wire, not just in-memory: a uvicorn
server is started on an ephemeral port; a valid token round-trips a tool, a wrong
token is rejected. Skipped only if the port cannot be bound.
"""

from __future__ import annotations

import socket
import threading
import time

import pytest

from parley.mcp.client import McpClient
from parley.mcp.server_factory import make_server
from tests.unit.domain_helpers import make_rules

TOKEN = "integration-cop-token-123"


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _serve(app, host, port, ready):
    import uvicorn

    config = uvicorn.Config(app, host=host, port=port, log_level="error")
    server = uvicorn.Server(config)

    def runner():
        import asyncio

        asyncio.run(server.serve())

    threading.Thread(target=runner, daemon=True).start()
    for _ in range(50):
        with socket.socket() as probe:
            if probe.connect_ex((host, port)) == 0:
                ready.set()
                return server
        time.sleep(0.1)
    return server


@pytest.mark.asyncio
async def test_real_http_server_auth_accept_and_reject():
    handle = make_server("cop", make_rules(), token=TOKEN)
    handle.mailbox.push_observation("you guard the northern alley")
    app = handle.mcp.http_app(path="/mcp")
    host, port = "127.0.0.1", _free_port()
    ready = threading.Event()
    server = _serve(app, host, port, ready)
    if not ready.wait(timeout=6):
        pytest.skip("could not bind a local HTTP server in this environment")
    url = f"http://{host}:{port}/mcp"
    try:
        async with McpClient.http(url, TOKEN) as client:
            assert "northern alley" in await client.observe()
        with pytest.raises(Exception):  # noqa: B017 - any auth failure is acceptable
            async with McpClient.http(url, "wrong-token") as bad:
                await bad.observe()
    finally:
        server.should_exit = True
        time.sleep(0.2)
