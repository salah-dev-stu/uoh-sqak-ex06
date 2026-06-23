# PRD — "Parley: Rooftop Pursuit" — 3D Replay Theater (HW6 standout extension)

> **Additive** to the audit-clean core (`parley` v1.20). It must NOT destabilize any
> existing gate (ruff, pytest ≥85%, CI green Py3.13, ≤150 lines/file raw+logical,
> no secrets, mock-everything). Built isolated under `viewer/` + one tested Python
> exporter under `src/parley/viewer/`.

## 1. Vision

A cinematic **replay theater** that turns a **real committed agent transcript** into a
watchable neon-noir rooftop duel. The grid is a glowing rooftop at night; the **Cop**
(cool blue) and **Thief** (amber/red) glide between tiles as the replay plays. Their
**free-natural-language taunts** rise as speech bubbles **and** stream into a noir chat
panel — putting the **graded heart (communication)** at the visual centre. A fog-of-war
shrouds the board except each agent's vision radius, and a COP / THIEF / DIRECTOR toggle
literally shows the **partial-observation (Dec-POMDP)** problem. Capture triggers a
camera zoom + particle burst. A timeline scrubber steps through the 6 sub-games; a HUD
shows the score. **Not a playable game — a replay theater.**

## 2. Non-negotiable principles

- **A. Honest.** Replays a REAL game — real moves + real NL dialogue from the committed
  sample run (deterministic, regenerable via `make_sample_run`; genuine natural
  language). The data source is labeled on screen. No fabricated dialogue.
- **B. Zero-setup for the grader.** Works **two ways**: (a) `python scripts/serve_viewer.py`
  / `make viewer` (local static server + opens browser), and (b) **double-clicking
  `viewer/index.html`** offline. To make (b) work from `file://`: Three.js is **vendored
  as a classic global build** (`viewer/vendor/three.min.js` via `<script>`), all app JS is
  classic (no ES modules), and the replay is **inlined** as `viewer/replay-data.js`
  (`window.REPLAY = {…}`) so **no `fetch()`** is ever needed. No CDN at grade time.
- **C. Gate-safe.** The 3D viewer is web (HTML/JS/CSS) under `viewer/`. The Python side is
  a small, unit-tested exporter + a tiny server. **No Node/Vite build** for CI to run; CI
  stays Python-only and green.

## 3. Data source

The exporter reads `reports/sample_report.json` (the committed sample game — real engine
moves + genuine NL taunts) and config (`grid_size`, `vision_radius`, `scoring`). It
reconstructs **both** agents' positions per frame (the move log records only the acting
agent), detects capture, and emits the replay. The exporter is provider-agnostic: a live
Claude-CLI run can be exported the same way later.

## 4. Scope (priority)

**MUST**
- 3D rooftop board (glowing tiles, neon edges).
- Animated Cop/Thief gliding tile-to-tile per the replay (diagonals arc).
- NL taunts as **speech bubbles** over the agents **+** a synced **chat panel**.
- Playback controls: play/pause, step fwd/back, speed; **sub-game selector** (1–6);
  **timeline scrubber**; **score HUD**; **capture highlight**.
- Reads a REAL replay (`window.REPLAY`); orbit camera.
- Opens **zero-setup** both ways (served + double-click).
- 3–4 screenshots + a short screen-capture GIF in `assets/`, embedded in the README.

**SHOULD** (after the MUST checkpoint)
- Fog-of-war + **COP / THIEF / DIRECTOR** view toggle (partial-observation showcase).
- Neon barriers slamming down; capture particle burst; bloom/neon polish.

**COULD** (only if time)
- MCP message-flow inset (two server nodes + animated messages).
- Cinematic auto-follow camera.

**DON'T**
- Require a live agent / API key / server for the viewer.
- Add a fragile build the grader can't run.
- Turn it into a real-time playable game.
- Break the green Python build.

## 5. Acceptance

1. Viewer opens **both** ways and animates the real game with NL dialogue, controls,
   sub-game selection, and capture FX.
2. `replay_export.py` is unit-tested (schema + deterministic from a fixed game); all
   existing gates still green; Three.js vendored (offline); replay data is real.
3. README has a prominent **3D Replay Viewer** section with screenshots + GIF + one-line
   "how to open" (both paths). Version bumped; pushed.

## 6. Checkpoint

After the MUST tier works (3D board + animated agents + NL dialogue + controls, zero
setup), **STOP and report with a screenshot** before SHOULD/COULD polish.
