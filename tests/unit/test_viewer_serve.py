"""Viewer P4 — serve_viewer wiring (V108–V109). No live bind."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import serve_viewer  # noqa: E402


def test_free_port_returns_int():
    port = serve_viewer.free_port()
    assert isinstance(port, int) and 1024 < port < 65536


def test_handler_serves_from_viewer_dir():
    handler = serve_viewer.make_handler()
    assert handler.keywords["directory"].endswith("viewer")


def test_viewer_assets_present():
    viewer = Path(__file__).resolve().parents[2] / "viewer"
    for rel in ("index.html", "replay-data.js", "vendor/three.min.js",
                "js/app.js", "css/theater.css"):
        assert (viewer / rel).exists(), f"missing viewer asset: {rel}"
