#!/usr/bin/env python3
"""One-time Gmail OAuth consent → cached token.json (H7 real path).

Run once locally: it opens a browser for consent and writes the revocable token
the autonomous pipeline later reuses. Lives in scripts/ (outside src/parley) so it
may import google libraries without tripping the Gatekeeper meta-test.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parley.shared.config import load_config  # noqa: E402


def build_flow(credentials_path: str, scopes: list[str]):
    from google_auth_oauthlib.flow import InstalledAppFlow  # noqa: PLC0415

    return InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)


def main() -> int:  # pragma: no cover - interactive browser consent
    cfg = load_config("config").report.gmail
    creds = os.environ.get(cfg["credentials_env"], "credentials.json")
    token = os.environ.get(cfg["token_env"], "token.json")
    flow = build_flow(creds, cfg["scopes"])
    creds_obj = flow.run_local_server(port=0)
    Path(token).write_text(creds_obj.to_json(), encoding="utf-8")
    print(f"saved Gmail token to {token} (git-ignored). The pipeline can now send mail.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
