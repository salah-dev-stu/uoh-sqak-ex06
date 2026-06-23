"""Persist the offline-provable artifacts of a run (transcript, dispute log, report)."""

from __future__ import annotations

import json

from parley.domain.records import GameResult
from parley.orchestrator.dialogue import DialogueLog
from parley.shared.gatekeeper import ApiGatekeeper
from parley.shared.paths import Paths


def write_artifacts(
    paths: Paths,
    run_label: str,
    result: GameResult,
    dialogue: DialogueLog,
    report: dict,
    renderer,
    gate: ApiGatekeeper,
) -> dict[str, str]:
    paths.ensure()
    run_dir = paths.transcripts / run_label
    run_dir.mkdir(parents=True, exist_ok=True)

    board = renderer.transcript() if hasattr(renderer, "transcript") else ""
    transcript = f"# parley run — {run_label}\n\n## Dialogue (free natural language)\n\n{dialogue.transcript()}\n\n## Board frames\n\n```\n{board}\n```\n"
    (run_dir / "transcript.md").write_text(transcript, encoding="utf-8")

    moves_path = run_dir / "moves.jsonl"
    lines = []
    for sub in result.subgames:
        for move in sub.log:
            lines.append(json.dumps({"subgame": sub.index, **move.to_dict()}))
    moves_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    report_path = paths.reports / f"{run_label}_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    ledger = gate.flush()
    return {
        "transcript": str(run_dir / "transcript.md"),
        "moves": str(moves_path),
        "report": str(report_path),
        "ledger": str(ledger),
    }
