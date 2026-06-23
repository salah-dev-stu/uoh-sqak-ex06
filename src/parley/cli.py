"""parley CLI — argparse front door that delegates to the SDK handlers."""

from __future__ import annotations

import argparse

from parley.cli_handlers import handle_play, handle_report, handle_serve, handle_version


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="parley", description="Dual-agent MCP cops & robbers")
    parser.add_argument("--config", default="config", help="config directory")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="print the single-source version")

    play = sub.add_parser("play", help="run the full autonomous pipeline")
    play.add_argument("--run-label", default="latest")
    play.add_argument("--gui", action="store_true", help="enable the Tkinter board window")
    play.add_argument("--provider", default=None, help="override llm provider (claude_cli|ollama)")

    sub.add_parser("serve-cop", help="run the Cop FastMCP server (HTTP)")
    sub.add_parser("serve-thief", help="run the Thief FastMCP server (HTTP)")

    rep = sub.add_parser("report", help="re-send a saved report JSON")
    rep.add_argument("--file", default="reports/latest_report.json")
    return parser


_HANDLERS = {
    "version": handle_version,
    "play": handle_play,
    "report": handle_report,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command in ("serve-cop", "serve-thief"):
        args.role = "cop" if args.command == "serve-cop" else "thief"
        return handle_serve(args)
    return _HANDLERS[args.command](args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
