#!/usr/bin/env python3
"""Fail if the single-source version desyncs (R5).

``src/parley/shared/version.py`` holds the one literal. This asserts that
``parley.__version__`` and the runtime config's ``version`` field both agree
with it. hatchling reads the same file for the build version, so every place
the version appears stays in lock-step.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERSION_FILE = Path("src/parley/shared/version.py")
CONFIG_FILE = Path("config/runtime.json")


def literal_version() -> str:
    text = VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    if not match:
        raise SystemExit("FAIL: __version__ literal not found in version.py")
    return match.group(1)


def main() -> int:
    src = literal_version()
    sys.path.insert(0, "src")
    import parley  # noqa: E402

    if parley.__version__ != src:
        print(f"FAIL: parley.__version__={parley.__version__} != version.py {src}")
        return 1

    cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    if cfg.get("version") != src:
        print(f"FAIL: config version={cfg.get('version')} != version.py {src}")
        return 1

    print(f"OK: version single-source in sync ({src}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
