"""Repo-relative path resolution for reports, transcripts, and the ledger."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    root: Path
    reports: Path
    transcripts: Path
    ledger: Path

    @classmethod
    def from_runtime(cls, root: str | Path, runtime_paths: dict[str, str]) -> Paths:
        base = Path(root)
        reports = base / runtime_paths.get("reports_dir", "reports")
        transcripts = base / runtime_paths.get("transcripts_dir", "reports/transcripts")
        ledger = base / runtime_paths.get("ledger", "reports/runs/gate_ledger.json")
        return cls(root=base, reports=reports, transcripts=transcripts, ledger=ledger)

    def ensure(self) -> Paths:
        """Create the report/transcript/ledger directories on demand."""
        self.reports.mkdir(parents=True, exist_ok=True)
        self.transcripts.mkdir(parents=True, exist_ok=True)
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        return self
