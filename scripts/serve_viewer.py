#!/usr/bin/env python3
"""Serve viewer/ over a local static server and open the browser (zero-setup path).

The viewer also works by double-clicking viewer/index.html (file://) because the
replay is inlined and Three.js is vendored — but serving guarantees correct MIME
types and avoids any browser file:// quirks.
"""

from __future__ import annotations

import contextlib
import functools
import http.server
import socket
import webbrowser
from pathlib import Path

VIEWER = Path(__file__).resolve().parents[1] / "viewer"


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def make_handler():
    return functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(VIEWER))


def main() -> int:  # pragma: no cover - blocking server loop
    port = free_port()
    url = f"http://127.0.0.1:{port}/index.html"
    httpd = http.server.HTTPServer(("127.0.0.1", port), make_handler())
    print(f"parley viewer → {url}   (Ctrl-C to stop)")
    with contextlib.suppress(Exception):  # headless boxes have no browser; URL is printed
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
