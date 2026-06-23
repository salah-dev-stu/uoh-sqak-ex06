# Plan — 3D Replay Viewer

> Derived from `docs/viewer/prd.md`. Isolated, additive. Python files ≤150 lines
> (raw+logical); web stays out of CI.

## 1. Module map

### Python (`src/parley/viewer/`, unit-tested)
| File | Responsibility | Public surface |
|---|---|---|
| `replay_export.py` | report dict → replay dict (reconstruct both positions, capture, frames) | `build_replay()` |
| `replay_io.py` | write `replay.json` + `replay-data.js` (`window.REPLAY=…`) | `write_replay()` |

### Scripts
| File | Responsibility |
|---|---|
| `scripts/export_replay.py` | load sample report + config → build + write replay artifacts |
| `scripts/serve_viewer.py` | static server over `viewer/` + auto-open browser |

### Web (`viewer/`, classic scripts — no ES modules, file://-safe)
| File | Responsibility |
|---|---|
| `index.html` | layout, `<script>` load order, HUD/controls/chat DOM |
| `css/theater.css` | neon-noir styling, chat panel, HUD, bubbles |
| `vendor/three.min.js` | Three.js r128 global build (vendored) |
| `vendor/OrbitControls.js` | classic OrbitControls (attaches `THREE.OrbitControls`) |
| `replay-data.js` | generated — `window.REPLAY = {…}` |
| `js/util.js` | shared helpers + `window.PARLEY` namespace (lerp, color, project) |
| `js/scene.js` | renderer, camera, lights, rooftop board tiles |
| `js/agents.js` | cop/thief meshes + glide/arc animation |
| `js/dialogue.js` | speech bubbles (projected DOM) + chat panel feed |
| `js/controls.js` | play/pause/step/speed/scrubber/sub-game/score HUD |
| `js/app.js` | main: read `window.REPLAY`, drive frames, wire modules |
| *(SHOULD)* `js/fog.js`, `js/barriers.js`, `js/fx.js` | fog-of-war + view toggle, barriers, capture FX |

## 2. Replay schema (`window.REPLAY`)

```
{
  meta: { title, source, grid_size:[r,c], vision_radius, num_subgames, scoring, generated_from },
  subgames: [
    { index, winner, start:{cop:[r,c],thief:[r,c]}, scores:{cop,thief},
      frames: [
        { move, role, action, message, cop:[r,c], thief:[r,c],
          barriers:[[r,c]...], barriers_left, capture:bool, vision_radius }
      ] }
  ]
}
```
Positions are reconstructed by replaying each record's `after` onto the acting role,
starting from each role's first `before`. `capture` = cop and thief share a cell.

## 3. Rendering approach

- **Board:** N×M plane of emissive tiles with dark gaps (rooftop). Subtle grid glow.
- **Agents:** low-poly columns/cones with emissive blue (cop) / amber (thief) + point
  lights. Glide via position lerp over ~0.6s; diagonals add a vertical arc (sin hop).
- **Speech bubbles:** HTML divs positioned by projecting the agent's world position to
  screen each frame (crisp text, no canvas sprites).
- **Chat panel:** scrolling DOM list, one line per taunt, role-coloured; auto-scrolls.
- **Controls:** DOM buttons + range input; a global frame index walks the active sub-game.
- **Camera:** OrbitControls (drag to orbit, scroll to zoom).
- **Offline:** every script is classic (`<script>`); data is inlined; no `fetch`, no CDN.

## 4. Milestones
1. Exporter + `replay_io` + tests → generate `viewer/replay.json` + `replay-data.js`.
2. Vendor Three.js r128 + OrbitControls.
3. MUST viewer: scene + agents + dialogue + controls + app (+ css + index.html).
4. `serve_viewer.py` + Makefile; verify both open paths.
5. Screenshots + GIF + README section. **Checkpoint.**
6. (After approval) SHOULD: fog-of-war + view toggle, barriers, capture FX, bloom.

## 5. Test strategy
- `build_replay` from a fixed synthetic report → exact frames (deterministic).
- Schema assertions (keys present, capture flagged, both positions per frame).
- `write_replay` round-trips JSON; `replay-data.js` starts with `window.REPLAY =`.
- `serve_viewer` handler/port wiring tested (no live bind needed).
- Coverage stays ≥85%; web JS is out of pytest/ruff scope.

## 6. Gate safety
- No new CI steps; Python-only CI unchanged.
- `ruff`/line-guard cover the new Python (exporter, io, scripts) — keep them tiny.
- Three.js vendored binary committed (offline); large but standard.
- Version bumped per change (1.20 → …) with config mirror.
