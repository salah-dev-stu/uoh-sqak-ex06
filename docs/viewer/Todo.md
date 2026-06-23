# Todo — 3D Replay Viewer (MUST → SHOULD → COULD)

> `[x]` = done. MUST first → **checkpoint** → SHOULD/COULD. Python TDD; web kept
> modular. Every Python file ≤150 lines (raw+logical); gates stay green.

## VA — replay exporter (Python, tested)
- [x] V001 `src/parley/viewer/__init__.py`
- [x] V002 Define replay schema in `docs/viewer/Plan.md` (done)
- [x] V003 Test: `build_replay` returns `meta` with grid_size/vision_radius/scoring
- [x] V004 Test: `meta.source` labels the data origin (honesty)
- [x] V005 Test: `meta.num_subgames` == len(subgames)
- [x] V006 Test: each subgame has index/winner/start/scores/frames
- [x] V007 Test: first frame's acting role moved from its start
- [x] V008 Test: every frame carries both `cop` and `thief` positions
- [x] V009 Test: positions reconstructed by replaying `after` onto acting role
- [x] V010 Test: capture frame flagged when cop == thief
- [x] V011 Test: non-capture frames have `capture=false`
- [x] V012 Test: frame carries the NL `message` (taunt) verbatim
- [x] V013 Test: frame carries `action`, `move`, `barriers_left`, `vision_radius`
- [x] V014 Test: BARRIER action appends a barrier cell to `barriers`
- [x] V015 Test: `start` inferred from first `before` per role
- [x] V016 Test: deterministic — same report → identical replay
- [x] V017 Implement `viewer/replay_export.py` (`build_replay`)
- [x] V018 Ruff + line-check exporter
- [x] V019 Test: `write_replay` writes `replay.json` (valid JSON)
- [x] V020 Test: `write_replay` writes `replay-data.js` starting `window.REPLAY =`
- [x] V021 Test: `replay-data.js` JSON payload parses back equal to replay.json
- [x] V022 Implement `viewer/replay_io.py` (`write_replay`)
- [x] V023 Ruff + line-check io
- [x] V024 `scripts/export_replay.py` — load sample report + config → build + write
- [x] V025 Test: export script wires sample_report + config (mocked write)
- [x] V026 Run export → `viewer/replay.json` + `viewer/replay-data.js`
- [x] V027 Verify replay has 6 subgames, capture flagged, NL messages present
- [x] V028 Coverage check ≥85% after exporter
- [x] V029 Commit VA

## VB — vendor Three.js (offline)
- [x] V030 Download `three.min.js` r128 global build → `viewer/vendor/`
- [x] V031 Download `OrbitControls.js` r128 classic → `viewer/vendor/`
- [x] V032 Verify both are classic globals (no `import`/`export`)
- [x] V033 Note vendored versions in `viewer/vendor/README.md`
- [x] V034 Commit VB

## VC — scene (rooftop board)
- [x] V035 `viewer/js/util.js` — `window.PARLEY` namespace
- [x] V036 util: `lerp`, `clamp`, `tileToWorld(r,c,grid)`
- [x] V037 util: `projectToScreen(vec3, camera, renderer)`
- [x] V038 util: color constants (cop blue, thief amber, neon)
- [x] V039 `viewer/js/scene.js` — create renderer (antialias, dark clear)
- [x] V040 scene: perspective camera + initial framing
- [x] V041 scene: ambient + key + rim lights (noir)
- [x] V042 scene: ground/rooftop plane (dark)
- [x] V043 scene: build N×M tile grid from `grid_size`
- [x] V044 scene: emissive tile material + neon edges
- [x] V045 scene: subtle tile glow / gap between tiles
- [x] V046 scene: resize handler (devicePixelRatio)
- [x] V047 scene: OrbitControls wired
- [x] V048 scene: expose `PARLEY.scene` API (init, tileMeshAt, render)
- [x] V049 scene: starfield / skyline backdrop (cheap)
- [x] V050 Tidy scene.js

## VD — agents (animated)
- [x] V051 `viewer/js/agents.js` — cop mesh (blue emissive + point light)
- [x] V052 agents: thief mesh (amber emissive + point light)
- [x] V053 agents: place at start tiles
- [x] V054 agents: `moveTo(role, fromTile, toTile)` tween over ~0.6s
- [x] V055 agents: diagonal arc (vertical sin hop)
- [x] V056 agents: snap mode (scrubbing) vs animated (play)
- [x] V057 agents: face direction of travel
- [x] V058 agents: capture pose (overlap highlight)
- [x] V059 agents: expose `PARLEY.agents` API (init, setFrame, update(dt))
- [x] V060 Tidy agents.js

## VE — dialogue (the graded centrepiece)
- [x] V061 `viewer/js/dialogue.js` — speech bubble DOM element per agent
- [x] V062 dialogue: position bubble by projecting agent world pos each frame
- [x] V063 dialogue: role-coloured bubble (cop/thief)
- [x] V064 dialogue: show current taunt, fade after N seconds
- [x] V065 dialogue: chat panel DOM list (scrolling)
- [x] V066 dialogue: append a line per frame (role + message)
- [x] V067 dialogue: auto-scroll chat to newest
- [x] V068 dialogue: highlight active speaker line
- [x] V069 dialogue: rebuild chat when sub-game / scrub changes
- [x] V070 dialogue: data-source label rendered in the panel header (honesty)
- [x] V071 dialogue: expose `PARLEY.dialogue` API (init, setFrame, reset)
- [x] V072 Tidy dialogue.js

## VF — controls + HUD
- [x] V073 `viewer/js/controls.js` — play/pause toggle
- [x] V074 controls: step forward / step back
- [x] V075 controls: speed selector (0.5x/1x/2x)
- [x] V076 controls: timeline scrubber (range over active sub-game frames)
- [x] V077 controls: scrubber updates board + chat without animation
- [x] V078 controls: sub-game selector (buttons 1–6)
- [x] V079 controls: switching sub-game resets frame index + chat
- [x] V080 controls: score HUD (cop/thief current + running totals)
- [x] V081 controls: winner badge per sub-game
- [x] V082 controls: capture highlight banner on capture frame
- [x] V083 controls: keyboard (space=play, arrows=step)
- [x] V084 controls: expose `PARLEY.controls` API (init, onFrame)
- [x] V085 Tidy controls.js

## VG — app wiring
- [x] V086 `viewer/js/app.js` — read `window.REPLAY`, guard if missing
- [x] V087 app: init scene/agents/dialogue/controls with replay
- [x] V088 app: global frame clock (requestAnimationFrame)
- [x] V089 app: advance frames on play at selected speed
- [x] V090 app: `setFrame(subgame, idx)` fans out to all modules
- [x] V091 app: capture frame → highlight (zoom hook for SHOULD)
- [x] V092 app: end-of-subgame → pause + winner badge
- [x] V093 app: error overlay if replay missing/invalid
- [x] V094 Tidy app.js

## VH — index.html + css
- [x] V095 `viewer/index.html` — canvas + HUD + chat + controls DOM
- [x] V096 index: `<script>` load order (vendor → data → util → modules → app)
- [x] V097 index: title + data-source caption
- [x] V098 `viewer/css/theater.css` — neon-noir palette, dark bg
- [x] V099 css: chat panel styling (scroll, role colours)
- [x] V100 css: speech bubble styling (tail, glow)
- [x] V101 css: HUD + controls bar styling
- [x] V102 css: responsive layout (canvas + side panel)
- [x] V103 css: buttons (active/hover/disabled)
- [x] V104 Tidy html/css

## VI — serve + make
- [x] V105 `scripts/serve_viewer.py` — SimpleHTTPRequestHandler over `viewer/`
- [x] V106 serve: pick a free port
- [x] V107 serve: auto-open browser to the URL
- [x] V108 Test: serve handler serves from the viewer dir (no live bind)
- [x] V109 Test: free-port helper returns an int
- [x] V110 Ruff + line-check serve_viewer
- [x] V111 `Makefile` — `viewer`, `replay`, `test`, `serve` targets
- [x] V112 Verify `python scripts/serve_viewer.py` serves + opens
- [x] V113 Verify double-click `viewer/index.html` works (file://)
- [x] V114 Commit VI

## VJ — screenshots + README + CHECKPOINT
- [x] V115 Launch served viewer in a headless browser
- [x] V116 Screenshot: opening board + both agents
- [x] V117 Screenshot: speech bubble + chat panel mid-chase
- [x] V118 Screenshot: capture highlight
- [x] V119 Screenshot: sub-game selector + score HUD
- [x] V120 Capture a short GIF of playback → `assets/`
- [x] V121 Optimize/trim images into `assets/viewer/`
- [x] V122 README: add "3D Replay Viewer" section
- [x] V123 README: embed screenshots + GIF
- [x] V124 README: one-line "how to open" (make viewer + double-click)
- [x] V125 README: label data source (honest)
- [x] V126 Run full gates (ruff, pytest ≥85%, lines, version sync)
- [x] V127 Bump version + CHANGELOG
- [x] V128 Commit + push
- [x] V129 **CHECKPOINT: report with screenshot; await go for SHOULD/COULD**

## VK — SHOULD (after checkpoint)
- [x] V130 `viewer/js/fog.js` — fog-of-war shroud outside vision radius
- [x] V131 fog: Chebyshev visibility from viewed agent
- [x] V132 fog: dim/hide tiles outside radius
- [x] V133 fog: hide opponent figure when out of view (partial obs!)
- [x] V134 fog: COP / THIEF / DIRECTOR toggle buttons
- [x] V135 fog: DIRECTOR = omniscient (no fog)
- [x] V136 fog: smooth transition on toggle
- [x] V137 fog: expose `PARLEY.fog` API
- [x] V138 `viewer/js/barriers.js` — neon wall mesh per barrier
- [x] V139 barriers: slam-down animation on placement frame
- [x] V140 barriers: block visual (both agents)
- [x] V141 `viewer/js/fx.js` — capture particle burst
- [x] V142 fx: camera zoom/punch on capture
- [x] V143 fx: bloom-like glow (additive sprites, no postprocessing dep)
- [x] V144 fx: neon trail behind moving agent
- [x] V145 SHOULD screenshots refresh (fog/view toggle/capture FX)
- [x] V146 README refresh with fog-of-war shots
- [x] V147 Gates green; bump version; commit/push

## VL — COULD (only if time)
- [ ] V148 MCP message-flow inset (two server nodes + animated messages)
- [ ] V149 Cinematic auto-follow camera mode
- [x] V150 Replay from a live Claude-CLI run (richer dialogue), labeled

## VM — gate safety (continuous)
- [x] V151 Confirm CI stays Python-only (no Node step)
- [x] V152 Confirm ruff/pytest/lines/version all green after each commit
- [x] V153 Confirm Three.js vendored (no CDN at runtime)
- [x] V154 Confirm no `fetch()` in app (file:// safe)
- [x] V155 Confirm no secrets added

## VN — finer-grained execution & QA (granularity to plan depth)

### Exporter robustness
- [x] V156 Handle a sub-game with zero moves (empty frames) gracefully
- [x] V157 Handle a thief-survive sub-game (no capture frame)
- [x] V158 Handle a sub-game ending exactly at max_moves
- [x] V159 Preserve move ordering stable across roles
- [x] V160 Clamp/validate positions within grid bounds in export
- [x] V161 Include per-frame running score snapshot
- [x] V162 Include `winner` mapped to a colour hint for the UI
- [x] V163 Include `total` cumulative scores in meta
- [x] V164 Round-trip: replay.json validates against an inline JSON-schema check (test)
- [x] V165 Export is idempotent (re-run overwrites identically) (test)

### Scene tuning
- [x] V166 Tune tile size + gap for a clean rooftop look
- [x] V167 Tune emissive intensity (neon but readable)
- [x] V168 Add fog/exponential depth haze for noir mood
- [x] V169 Add a faint reflective floor sheen
- [x] V170 Add tile hover/active highlight (current cells)
- [x] V171 Camera default angle frames the whole board
- [x] V172 Camera min/max zoom + polar limits (OrbitControls)
- [x] V173 Pixel-ratio cap for perf on hi-DPI
- [x] V174 Pause render loop when tab hidden
- [x] V175 Dispose geometries/materials on grid rebuild

### Agent motion polish
- [x] V176 Ease-in-out cubic for glide
- [x] V177 Arc height proportional to diagonal length
- [x] V178 Slight squash/stretch on landing
- [x] V179 Idle bob when stationary
- [x] V180 Point-light follows each agent
- [x] V181 Trail fade length tuned (SHOULD hook)
- [x] V182 Distinct silhouettes (cop taller / thief sleeker)
- [x] V183 Capture: agents converge to same tile cleanly
- [x] V184 No overlap z-fighting at capture

### Dialogue timing
- [x] V185 Bubble appears at frame start, holds during glide
- [x] V186 Bubble max width + wrap (2–3 lines)
- [x] V187 Bubble fade-out easing
- [x] V188 Long taunt truncation in bubble (full text in chat)
- [x] V189 Chat line timestamps (move number)
- [x] V190 Chat role icons/colours legible on dark
- [x] V191 Chat scroll preserves position when scrubbing back
- [x] V192 Empty-message frames skip bubble but keep chat marker
- [x] V193 Data-source banner persistent + unobtrusive

### Controls edge cases
- [x] V194 Step back at frame 0 is a no-op
- [x] V195 Step forward at last frame pauses
- [x] V196 Scrubber thumb reflects current frame
- [x] V197 Speed change mid-play stays smooth
- [x] V198 Sub-game buttons show winner colour
- [x] V199 Active sub-game button highlighted
- [x] V200 Keyboard shortcuts don't fire in inputs
- [x] V201 Replay-end shows "replay complete" state
- [x] V202 Restart button resets to sub-game 1 frame 0
- [x] V203 HUD totals accumulate across watched sub-games

### App robustness
- [x] V204 Guard: REPLAY missing → friendly overlay + instructions
- [x] V205 Guard: empty subgames → message
- [x] V206 dt-based animation (frame-rate independent)
- [x] V207 Resize keeps bubbles aligned
- [x] V208 No console errors on load (clean)
- [x] V209 No global leaks beyond `window.PARLEY`/`window.REPLAY`

### index/css
- [x] V210 Semantic layout (header/main/aside/footer)
- [x] V211 Accessible button labels (aria-label)
- [x] V212 Prefers-reduced-motion respected (snap, no arcs)
- [x] V213 Mobile-ish narrow layout doesn't break
- [x] V214 Favicon / title polish
- [x] V215 Footer credits + course line

### Serve/Make/QA
- [x] V216 serve_viewer prints the URL clearly
- [x] V217 serve_viewer graceful Ctrl-C
- [x] V218 serve_viewer binds 127.0.0.1 only
- [x] V219 Makefile help target lists commands
- [x] V220 `make replay` regenerates data then reminds to refresh
- [x] V221 QA: open served in Chromium → animates
- [x] V222 QA: open file:// in Chromium → animates (no CORS errors)
- [x] V223 QA: orbit/zoom works
- [x] V224 QA: all 6 sub-games selectable
- [x] V225 QA: capture highlight fires on cop-win sub-games
- [x] V226 QA: chat matches the committed transcript text
- [x] V227 QA: no network requests at runtime (offline proof)

### Docs/visuals
- [x] V228 Screenshot naming + alt text
- [x] V229 GIF under ~3–5 MB (trim/scale)
- [x] V230 README section ordering (prominent, near top)
- [x] V231 Link viewer from repo structure section
- [x] V232 Note "replay theater, not a playable game"
- [x] V233 Note vendored Three.js version + license
- [x] V234 docs/viewer index cross-links prd/Plan/Todo

### Gate safety / release
- [x] V235 Confirm ≤150 lines on every new Python file (raw+logical)
- [x] V236 Confirm ruff clean (Python only)
- [x] V237 Confirm pytest green + coverage ≥85%
- [x] V238 Confirm CI workflow unchanged (Python-only)
- [x] V239 Confirm .gitignore excludes any large temp capture frames
- [x] V240 Confirm no secrets / keys / tokens added
- [x] V241 Version bump mirrored (version.py + runtime.json)
- [x] V242 CHANGELOG entry for the viewer
- [x] V243 Continuous commits (one per component, not big-bang)
- [x] V244 Push; confirm CI green badge
- [x] V245 Final review vs PRD acceptance criteria
- [x] V246 Final review vs the two open-paths (served + file://)
- [x] V247 Tag the viewer milestone version

### SHOULD detail (post-checkpoint)
- [x] V248 Fog shader/material approach decided (opacity vs emissive)
- [x] V249 Fog edge softness tuned
- [x] V250 View toggle remembers per-sub-game
- [x] V251 Opponent ghost (faint) when last-known vs unknown
- [x] V252 "You can only infer from words" hint in fog views
- [x] V253 Barrier neon colour + height
- [x] V254 Barrier slam easing + impact flash
- [x] V255 Particle count/perf budget for capture burst
- [x] V256 Capture camera punch returns smoothly
- [x] V257 Additive glow sprites for bloom feel
- [x] V258 Neon trail ribbon length/opacity
- [x] V259 Fog/FX screenshots
- [x] V260 README fog-of-war showcase paragraph

### COULD detail
- [ ] V261 MCP inset: two server nodes + client node
- [ ] V262 MCP inset: animate message dot per send
- [ ] V263 MCP inset: label tools (observe/send_message/act)
- [ ] V264 Auto-follow camera lerps toward action
- [x] V265 Live-run replay export + label + commit
- [x] V266 Toggle between sample and live replay datasets
- [x] V267 Final polish pass + perf check
- [x] V268 Final docs + push

## VO — additional test cases & micro-tasks (depth to ≥300)
- [x] V269 Test: meta.grid_size matches config exactly
- [x] V270 Test: vision_radius propagated to every frame
- [x] V271 Test: scoring table copied verbatim into meta
- [x] V272 Test: subgame.scores sum into meta totals
- [x] V273 Test: capture only on the final cop-win frame
- [x] V274 Test: thief-survive subgame has no capture frame
- [x] V275 Test: frame count equals move count per subgame
- [x] V276 Test: roles alternate thief-first within a subgame
- [x] V277 Test: message field never contains a coordinate tuple
- [x] V278 Test: replay-data.js is syntactically `window.REPLAY = {…};`
- [x] V279 Test: export script writes both files to viewer/
- [x] V280 Test: build_replay pure (no file IO)
- [x] V281 Test: source label includes "sample" + "deterministic"
- [x] V282 Test: barriers list empty for the all-move sample
- [x] V283 Test: large message wraps without breaking JSON
- [x] V284 util test stub (lerp/clamp pure) — JS sanity via node (optional, non-CI)
- [x] V285 scene: handle 2x2 and 5x5 grids from replay
- [x] V286 agents: handle capture on move 1
- [x] V287 dialogue: handle 25-move subgame chat length
- [x] V288 controls: scrubber spans variable-length subgames
- [x] V289 app: switching dataset reloads cleanly
- [x] V290 css: chat panel max-height + overflow on small screens
- [x] V291 css: bubble contrast meets readability
- [x] V292 perf: cap total DOM bubbles to active speakers
- [x] V293 perf: reuse geometries across tiles
- [x] V294 a11y: focus ring on controls
- [x] V295 a11y: chat is a labelled live region
- [x] V296 serve: 404 page is friendly
- [x] V297 serve: mime types correct for .js/.css
- [x] V298 Makefile: `clean` removes generated replay artifacts
- [x] V299 docs: viewer README in viewer/ explaining structure
- [x] V300 QA: capture-to-GIF pipeline documented
- [x] V301 QA: verify offline (airplane mode style) double-click works
- [x] V302 Final: checkpoint screenshot attached in report
- [x] V303 Final: SHOULD/COULD gated on user go-ahead

---

## Status

**297 / 303 complete.** MUST + SHOULD tiers fully delivered, plus the live-LLM
replay (COULD). The 6 remaining open boxes are two **optional COULD features that
were deliberately not built** — the MCP message-flow inset (V148, V261–V263) and the
cinematic auto-follow camera (V149, V264). They are pure polish; the standout is
complete and shipped without them. Left unchecked on purpose, for honesty.
