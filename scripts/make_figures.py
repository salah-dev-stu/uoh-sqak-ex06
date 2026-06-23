#!/usr/bin/env python3
"""Render board figures from the committed sample run (visual proof for the README).

Reconstructs sub-game 1 frame by frame from reports/transcripts/sample/moves.jsonl
and draws the chase: cop (blue), thief (red), grid, and the natural-language taunt
under each frame. Writes a hero board + a 4-frame filmstrip to docs/figures/.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GRID = 5
COP_C, THIEF_C = "#2471a3", "#c0392b"


def frames_for_subgame(index: int = 0):
    rows = [json.loads(line) for line in (ROOT / "reports/transcripts/sample/moves.jsonl")
            .read_text().splitlines()]
    cop, thief = (0, 0), (GRID - 1, GRID - 1)
    out = []
    for r in rows:
        if r["subgame"] != index:
            continue
        pos = tuple(r["after"])
        if r["role"] == "cop":
            cop = pos
        else:
            thief = pos
        out.append({"cop": cop, "thief": thief, "role": r["role"],
                    "move": r["move_no"], "msg": r["message"]})
    return out


def draw(ax, frame) -> None:
    ax.set_xlim(-0.5, GRID - 0.5)
    ax.set_ylim(-0.5, GRID - 0.5)
    ax.set_xticks(range(GRID))
    ax.set_yticks(range(GRID))
    ax.grid(True, color="#ccc")
    ax.set_aspect("equal")
    ax.invert_yaxis()
    tr, tc = frame["thief"]
    cr, cc = frame["cop"]
    ax.scatter([tc], [tr], s=900, c=THIEF_C, edgecolors="k", zorder=3, label="Thief")
    ax.scatter([cc], [cr], s=900, c=COP_C, edgecolors="k", zorder=3, label="Cop")
    if frame["cop"] == frame["thief"]:
        ax.scatter([cc], [cr], s=1800, facecolors="none", edgecolors="gold", linewidths=3, zorder=4)
    ax.set_title(f"move {frame['move']} · {frame['role']}", fontsize=10)


def main() -> int:
    out_dir = ROOT / "docs" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = frames_for_subgame(0)

    fig, axes = plt.subplots(1, len(frames), figsize=(4 * len(frames), 4.6))
    axes = axes if hasattr(axes, "__len__") else [axes]
    for ax, frame in zip(axes, frames, strict=False):
        draw(ax, frame)
        ax.text(0.5, -0.18, _wrap(frame["msg"]), transform=ax.transAxes,
                ha="center", va="top", fontsize=7, style="italic", wrap=True)
    fig.suptitle("parley — sub-game 1: the Cop closes a diagonal net on the Thief (free-NL chase)", fontsize=12)
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))
    fig.savefig(out_dir / "chase_filmstrip.png", dpi=130, bbox_inches="tight")

    hero, hax = plt.subplots(figsize=(5, 5.4))
    draw(hax, frames[-1])
    hax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2, frameon=False)
    hero.suptitle("Capture — the Cop shares the Thief's cell", fontsize=12)
    hero.savefig(out_dir / "board_hero.png", dpi=130, bbox_inches="tight")
    print(f"wrote {out_dir/'chase_filmstrip.png'} and {out_dir/'board_hero.png'}")
    return 0


def _wrap(text: str, width: int = 42) -> str:
    import textwrap

    return "\n".join(textwrap.wrap(text, width)[:3])


if __name__ == "__main__":
    sys.exit(main())
