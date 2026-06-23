#!/usr/bin/env python3
"""Render a crisp, high-DPI MCP message-flow diagram for the README.

Matches the viewer's live inset (orchestrator ⇄ two FastMCP servers, message dots
on the edges) but drawn vector-clean so it stays sharp in the README.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BG, NEON, COP, THIEF, INK, MUTED = "#080c14", "#14e0d0", "#39a0ff", "#ff9d3a", "#dfe8f6", "#7a89a6"

NODES = {
    "orch": (0.5, 0.74, "Orchestrator", "MCP client · holds the LLM", NEON),
    "cop": (0.2, 0.2, "Cop server", "FastMCP", COP),
    "thief": (0.8, 0.2, "Thief server", "FastMCP", THIEF),
}


def _box(ax, x, y, title, sub, color):
    ax.add_patch(FancyBboxPatch(
        (x - 0.155, y - 0.075), 0.31, 0.15, boxstyle="round,pad=0.012,rounding_size=0.03",
        linewidth=2, edgecolor=color, facecolor="#0a1018",
    ))
    ax.text(x, y + 0.022, title, color=INK, ha="center", va="center", fontsize=13, fontweight="bold")
    ax.text(x, y - 0.03, sub, color=MUTED, ha="center", va="center", fontsize=9.5)


def _edge(ax, a, b, color, dot_t):
    ax_, ay = NODES[a][0], NODES[a][1] - 0.078
    bx, by = NODES[b][0], NODES[b][1] + 0.078
    ax.plot([ax_, bx], [ay, by], color="#39455e", linewidth=1.4, zorder=1)
    dx, dy = ax_ + (bx - ax_) * dot_t, ay + (by - ay) * dot_t
    ax.scatter([dx], [dy], s=170, color=color, zorder=3,
               path_effects=[pe.withStroke(linewidth=7, foreground=color, alpha=0.35)])


def main() -> int:
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.95, "M C P   M E S S A G E   F L O W", color=NEON, ha="center",
            va="center", fontsize=13, fontweight="bold")
    _edge(ax, "orch", "cop", COP, 0.45)
    _edge(ax, "orch", "thief", NEON, 0.6)
    for key, (x, y, title, sub, color) in NODES.items():
        _box(ax, x, y, title, sub, color)
    ax.text(0.5, 0.045, "observation / prompt out  →   free-NL message + action back",
            color=MUTED, ha="center", va="center", fontsize=9, style="italic")

    out = ROOT / "assets" / "viewer" / "mcp-flow.png"
    fig.savefig(out, dpi=200, facecolor=BG, bbox_inches="tight", pad_inches=0.18)
    print(f"wrote {out} (crisp, 200 dpi)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
