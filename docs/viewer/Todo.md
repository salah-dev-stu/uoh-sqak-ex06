# Todo — 3D Replay Viewer (MUST → SHOULD → COULD)

> `[x]` = done. MUST first → **checkpoint** → SHOULD/COULD. Python TDD; web kept
> modular. Every Python file ≤150 lines (raw+logical); gates stay green.

## VA — replay exporter (Python, tested)
- [ ] V001 `src/parley/viewer/__init__.py`
- [ ] V002 Define replay schema in `docs/viewer/Plan.md` (done)
- [ ] V003 Test: `build_replay` returns `meta` with grid_size/vision_radius/scoring
- [ ] V004 Test: `meta.source` labels the data origin (honesty)
- [ ] V005 Test: `meta.num_subgames` == len(subgames)
- [ ] V006 Test: each subgame has index/winner/start/scores/frames
- [ ] V007 Test: first frame's acting role moved from its start
- [ ] V008 Test: every frame carries both `cop` and `thief` positions
- [ ] V009 Test: positions reconstructed by replaying `after` onto acting role
- [ ] V010 Test: capture frame flagged when cop == thief
- [ ] V011 Test: non-capture frames have `capture=false`
- [ ] V012 Test: frame carries the NL `message` (taunt) verbatim
- [ ] V013 Test: frame carries `action`, `move`, `barriers_left`, `vision_radius`
- [ ] V014 Test: BARRIER action appends a barrier cell to `barriers`
- [ ] V015 Test: `start` inferred from first `before` per role
- [ ] V016 Test: deterministic — same report → identical replay
- [ ] V017 Implement `viewer/replay_export.py` (`build_replay`)
- [ ] V018 Ruff + line-check exporter
- [ ] V019 Test: `write_replay` writes `replay.json` (valid JSON)
- [ ] V020 Test: `write_replay` writes `replay-data.js` starting `window.REPLAY =`
- [ ] V021 Test: `replay-data.js` JSON payload parses back equal to replay.json
- [ ] V022 Implement `viewer/replay_io.py` (`write_replay`)
- [ ] V023 Ruff + line-check io
- [ ] V024 `scripts/export_replay.py` — load sample report + config → build + write
- [ ] V025 Test: export script wires sample_report + config (mocked write)
- [ ] V026 Run export → `viewer/replay.json` + `viewer/replay-data.js`
- [ ] V027 Verify replay has 6 subgames, capture flagged, NL messages present
- [ ] V028 Coverage check ≥85% after exporter
- [ ] V029 Commit VA

## VB — vendor Three.js (offline)
- [ ] V030 Download `three.min.js` r128 global build → `viewer/vendor/`
- [ ] V031 Download `OrbitControls.js` r128 classic → `viewer/vendor/`
- [ ] V032 Verify both are classic globals (no `import`/`export`)
- [ ] V033 Note vendored versions in `viewer/vendor/README.md`
- [ ] V034 Commit VB

## VC — scene (rooftop board)
- [ ] V035 `viewer/js/util.js` — `window.PARLEY` namespace
- [ ] V036 util: `lerp`, `clamp`, `tileToWorld(r,c,grid)`
- [ ] V037 util: `projectToScreen(vec3, camera, renderer)`
- [ ] V038 util: color constants (cop blue, thief amber, neon)
- [ ] V039 `viewer/js/scene.js` — create renderer (antialias, dark clear)
- [ ] V040 scene: perspective camera + initial framing
- [ ] V041 scene: ambient + key + rim lights (noir)
- [ ] V042 scene: ground/rooftop plane (dark)
- [ ] V043 scene: build N×M tile grid from `grid_size`
- [ ] V044 scene: emissive tile material + neon edges
- [ ] V045 scene: subtle tile glow / gap between tiles
- [ ] V046 scene: resize handler (devicePixelRatio)
- [ ] V047 scene: OrbitControls wired
- [ ] V048 scene: expose `PARLEY.scene` API (init, tileMeshAt, render)
- [ ] V049 scene: starfield / skyline backdrop (cheap)
- [ ] V050 Tidy scene.js

## VD — agents (animated)
- [ ] V051 `viewer/js/agents.js` — cop mesh (blue emissive + point light)
- [ ] V052 agents: thief mesh (amber emissive + point light)
- [ ] V053 agents: place at start tiles
- [ ] V054 agents: `moveTo(role, fromTile, toTile)` tween over ~0.6s
- [ ] V055 agents: diagonal arc (vertical sin hop)
- [ ] V056 agents: snap mode (scrubbing) vs animated (play)
- [ ] V057 agents: face direction of travel
- [ ] V058 agents: capture pose (overlap highlight)
- [ ] V059 agents: expose `PARLEY.agents` API (init, setFrame, update(dt))
- [ ] V060 Tidy agents.js

## VE — dialogue (the graded centrepiece)
- [ ] V061 `viewer/js/dialogue.js` — speech bubble DOM element per agent
- [ ] V062 dialogue: position bubble by projecting agent world pos each frame
- [ ] V063 dialogue: role-coloured bubble (cop/thief)
- [ ] V064 dialogue: show current taunt, fade after N seconds
- [ ] V065 dialogue: chat panel DOM list (scrolling)
- [ ] V066 dialogue: append a line per frame (role + message)
- [ ] V067 dialogue: auto-scroll chat to newest
- [ ] V068 dialogue: highlight active speaker line
- [ ] V069 dialogue: rebuild chat when sub-game / scrub changes
- [ ] V070 dialogue: data-source label rendered in the panel header (honesty)
- [ ] V071 dialogue: expose `PARLEY.dialogue` API (init, setFrame, reset)
- [ ] V072 Tidy dialogue.js

## VF — controls + HUD
- [ ] V073 `viewer/js/controls.js` — play/pause toggle
- [ ] V074 controls: step forward / step back
- [ ] V075 controls: speed selector (0.5x/1x/2x)
- [ ] V076 controls: timeline scrubber (range over active sub-game frames)
- [ ] V077 controls: scrubber updates board + chat without animation
- [ ] V078 controls: sub-game selector (buttons 1–6)
- [ ] V079 controls: switching sub-game resets frame index + chat
- [ ] V080 controls: score HUD (cop/thief current + running totals)
- [ ] V081 controls: winner badge per sub-game
- [ ] V082 controls: capture highlight banner on capture frame
- [ ] V083 controls: keyboard (space=play, arrows=step)
- [ ] V084 controls: expose `PARLEY.controls` API (init, onFrame)
- [ ] V085 Tidy controls.js

## VG — app wiring
- [ ] V086 `viewer/js/app.js` — read `window.REPLAY`, guard if missing
- [ ] V087 app: init scene/agents/dialogue/controls with replay
- [ ] V088 app: global frame clock (requestAnimationFrame)
- [ ] V089 app: advance frames on play at selected speed
- [ ] V090 app: `setFrame(subgame, idx)` fans out to all modules
- [ ] V091 app: capture frame → highlight (zoom hook for SHOULD)
- [ ] V092 app: end-of-subgame → pause + winner badge
- [ ] V093 app: error overlay if replay missing/invalid
- [ ] V094 Tidy app.js

## VH — index.html + css
- [ ] V095 `viewer/index.html` — canvas + HUD + chat + controls DOM
- [ ] V096 index: `<script>` load order (vendor → data → util → modules → app)
- [ ] V097 index: title + data-source caption
- [ ] V098 `viewer/css/theater.css` — neon-noir palette, dark bg
- [ ] V099 css: chat panel styling (scroll, role colours)
- [ ] V100 css: speech bubble styling (tail, glow)
- [ ] V101 css: HUD + controls bar styling
- [ ] V102 css: responsive layout (canvas + side panel)
- [ ] V103 css: buttons (active/hover/disabled)
- [ ] V104 Tidy html/css

## VI — serve + make
- [ ] V105 `scripts/serve_viewer.py` — SimpleHTTPRequestHandler over `viewer/`
- [ ] V106 serve: pick a free port
- [ ] V107 serve: auto-open browser to the URL
- [ ] V108 Test: serve handler serves from the viewer dir (no live bind)
- [ ] V109 Test: free-port helper returns an int
- [ ] V110 Ruff + line-check serve_viewer
- [ ] V111 `Makefile` — `viewer`, `replay`, `test`, `serve` targets
- [ ] V112 Verify `python scripts/serve_viewer.py` serves + opens
- [ ] V113 Verify double-click `viewer/index.html` works (file://)
- [ ] V114 Commit VI

## VJ — screenshots + README + CHECKPOINT
- [ ] V115 Launch served viewer in a headless browser
- [ ] V116 Screenshot: opening board + both agents
- [ ] V117 Screenshot: speech bubble + chat panel mid-chase
- [ ] V118 Screenshot: capture highlight
- [ ] V119 Screenshot: sub-game selector + score HUD
- [ ] V120 Capture a short GIF of playback → `assets/`
- [ ] V121 Optimize/trim images into `assets/viewer/`
- [ ] V122 README: add "3D Replay Viewer" section
- [ ] V123 README: embed screenshots + GIF
- [ ] V124 README: one-line "how to open" (make viewer + double-click)
- [ ] V125 README: label data source (honest)
- [ ] V126 Run full gates (ruff, pytest ≥85%, lines, version sync)
- [ ] V127 Bump version + CHANGELOG
- [ ] V128 Commit + push
- [ ] V129 **CHECKPOINT: report with screenshot; await go for SHOULD/COULD**

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
- [ ] V144 fx: neon trail behind moving agent
- [x] V145 SHOULD screenshots refresh (fog/view toggle/capture FX)
- [x] V146 README refresh with fog-of-war shots
- [x] V147 Gates green; bump version; commit/push

## VL — COULD (only if time)
- [ ] V148 MCP message-flow inset (two server nodes + animated messages)
- [ ] V149 Cinematic auto-follow camera mode
- [ ] V150 Replay from a live Claude-CLI run (richer dialogue), labeled

## VM — gate safety (continuous)
- [ ] V151 Confirm CI stays Python-only (no Node step)
- [ ] V152 Confirm ruff/pytest/lines/version all green after each commit
- [ ] V153 Confirm Three.js vendored (no CDN at runtime)
- [ ] V154 Confirm no `fetch()` in app (file:// safe)
- [ ] V155 Confirm no secrets added

## VN — finer-grained execution & QA (granularity to plan depth)

### Exporter robustness
- [ ] V156 Handle a sub-game with zero moves (empty frames) gracefully
- [ ] V157 Handle a thief-survive sub-game (no capture frame)
- [ ] V158 Handle a sub-game ending exactly at max_moves
- [ ] V159 Preserve move ordering stable across roles
- [ ] V160 Clamp/validate positions within grid bounds in export
- [ ] V161 Include per-frame running score snapshot
- [ ] V162 Include `winner` mapped to a colour hint for the UI
- [ ] V163 Include `total` cumulative scores in meta
- [ ] V164 Round-trip: replay.json validates against an inline JSON-schema check (test)
- [ ] V165 Export is idempotent (re-run overwrites identically) (test)

### Scene tuning
- [ ] V166 Tune tile size + gap for a clean rooftop look
- [ ] V167 Tune emissive intensity (neon but readable)
- [ ] V168 Add fog/exponential depth haze for noir mood
- [ ] V169 Add a faint reflective floor sheen
- [ ] V170 Add tile hover/active highlight (current cells)
- [ ] V171 Camera default angle frames the whole board
- [ ] V172 Camera min/max zoom + polar limits (OrbitControls)
- [ ] V173 Pixel-ratio cap for perf on hi-DPI
- [ ] V174 Pause render loop when tab hidden
- [ ] V175 Dispose geometries/materials on grid rebuild

### Agent motion polish
- [ ] V176 Ease-in-out cubic for glide
- [ ] V177 Arc height proportional to diagonal length
- [ ] V178 Slight squash/stretch on landing
- [ ] V179 Idle bob when stationary
- [ ] V180 Point-light follows each agent
- [ ] V181 Trail fade length tuned (SHOULD hook)
- [ ] V182 Distinct silhouettes (cop taller / thief sleeker)
- [ ] V183 Capture: agents converge to same tile cleanly
- [ ] V184 No overlap z-fighting at capture

### Dialogue timing
- [ ] V185 Bubble appears at frame start, holds during glide
- [ ] V186 Bubble max width + wrap (2–3 lines)
- [ ] V187 Bubble fade-out easing
- [ ] V188 Long taunt truncation in bubble (full text in chat)
- [ ] V189 Chat line timestamps (move number)
- [ ] V190 Chat role icons/colours legible on dark
- [ ] V191 Chat scroll preserves position when scrubbing back
- [ ] V192 Empty-message frames skip bubble but keep chat marker
- [ ] V193 Data-source banner persistent + unobtrusive

### Controls edge cases
- [ ] V194 Step back at frame 0 is a no-op
- [ ] V195 Step forward at last frame pauses
- [ ] V196 Scrubber thumb reflects current frame
- [ ] V197 Speed change mid-play stays smooth
- [ ] V198 Sub-game buttons show winner colour
- [ ] V199 Active sub-game button highlighted
- [ ] V200 Keyboard shortcuts don't fire in inputs
- [ ] V201 Replay-end shows "replay complete" state
- [ ] V202 Restart button resets to sub-game 1 frame 0
- [ ] V203 HUD totals accumulate across watched sub-games

### App robustness
- [ ] V204 Guard: REPLAY missing → friendly overlay + instructions
- [ ] V205 Guard: empty subgames → message
- [ ] V206 dt-based animation (frame-rate independent)
- [ ] V207 Resize keeps bubbles aligned
- [ ] V208 No console errors on load (clean)
- [ ] V209 No global leaks beyond `window.PARLEY`/`window.REPLAY`

### index/css
- [ ] V210 Semantic layout (header/main/aside/footer)
- [ ] V211 Accessible button labels (aria-label)
- [ ] V212 Prefers-reduced-motion respected (snap, no arcs)
- [ ] V213 Mobile-ish narrow layout doesn't break
- [ ] V214 Favicon / title polish
- [ ] V215 Footer credits + course line

### Serve/Make/QA
- [ ] V216 serve_viewer prints the URL clearly
- [ ] V217 serve_viewer graceful Ctrl-C
- [ ] V218 serve_viewer binds 127.0.0.1 only
- [ ] V219 Makefile help target lists commands
- [ ] V220 `make replay` regenerates data then reminds to refresh
- [ ] V221 QA: open served in Chromium → animates
- [ ] V222 QA: open file:// in Chromium → animates (no CORS errors)
- [ ] V223 QA: orbit/zoom works
- [ ] V224 QA: all 6 sub-games selectable
- [ ] V225 QA: capture highlight fires on cop-win sub-games
- [ ] V226 QA: chat matches the committed transcript text
- [ ] V227 QA: no network requests at runtime (offline proof)

### Docs/visuals
- [ ] V228 Screenshot naming + alt text
- [ ] V229 GIF under ~3–5 MB (trim/scale)
- [ ] V230 README section ordering (prominent, near top)
- [ ] V231 Link viewer from repo structure section
- [ ] V232 Note "replay theater, not a playable game"
- [ ] V233 Note vendored Three.js version + license
- [ ] V234 docs/viewer index cross-links prd/Plan/Todo

### Gate safety / release
- [ ] V235 Confirm ≤150 lines on every new Python file (raw+logical)
- [ ] V236 Confirm ruff clean (Python only)
- [ ] V237 Confirm pytest green + coverage ≥85%
- [ ] V238 Confirm CI workflow unchanged (Python-only)
- [ ] V239 Confirm .gitignore excludes any large temp capture frames
- [ ] V240 Confirm no secrets / keys / tokens added
- [ ] V241 Version bump mirrored (version.py + runtime.json)
- [ ] V242 CHANGELOG entry for the viewer
- [ ] V243 Continuous commits (one per component, not big-bang)
- [ ] V244 Push; confirm CI green badge
- [ ] V245 Final review vs PRD acceptance criteria
- [ ] V246 Final review vs the two open-paths (served + file://)
- [ ] V247 Tag the viewer milestone version

### SHOULD detail (post-checkpoint)
- [ ] V248 Fog shader/material approach decided (opacity vs emissive)
- [ ] V249 Fog edge softness tuned
- [ ] V250 View toggle remembers per-sub-game
- [ ] V251 Opponent ghost (faint) when last-known vs unknown
- [ ] V252 "You can only infer from words" hint in fog views
- [ ] V253 Barrier neon colour + height
- [ ] V254 Barrier slam easing + impact flash
- [ ] V255 Particle count/perf budget for capture burst
- [ ] V256 Capture camera punch returns smoothly
- [ ] V257 Additive glow sprites for bloom feel
- [ ] V258 Neon trail ribbon length/opacity
- [ ] V259 Fog/FX screenshots
- [ ] V260 README fog-of-war showcase paragraph

### COULD detail
- [ ] V261 MCP inset: two server nodes + client node
- [ ] V262 MCP inset: animate message dot per send
- [ ] V263 MCP inset: label tools (observe/send_message/act)
- [ ] V264 Auto-follow camera lerps toward action
- [ ] V265 Live-run replay export + label + commit
- [ ] V266 Toggle between sample and live replay datasets
- [ ] V267 Final polish pass + perf check
- [ ] V268 Final docs + push

## VO — additional test cases & micro-tasks (depth to ≥300)
- [ ] V269 Test: meta.grid_size matches config exactly
- [ ] V270 Test: vision_radius propagated to every frame
- [ ] V271 Test: scoring table copied verbatim into meta
- [ ] V272 Test: subgame.scores sum into meta totals
- [ ] V273 Test: capture only on the final cop-win frame
- [ ] V274 Test: thief-survive subgame has no capture frame
- [ ] V275 Test: frame count equals move count per subgame
- [ ] V276 Test: roles alternate thief-first within a subgame
- [ ] V277 Test: message field never contains a coordinate tuple
- [ ] V278 Test: replay-data.js is syntactically `window.REPLAY = {…};`
- [ ] V279 Test: export script writes both files to viewer/
- [ ] V280 Test: build_replay pure (no file IO)
- [ ] V281 Test: source label includes "sample" + "deterministic"
- [ ] V282 Test: barriers list empty for the all-move sample
- [ ] V283 Test: large message wraps without breaking JSON
- [ ] V284 util test stub (lerp/clamp pure) — JS sanity via node (optional, non-CI)
- [ ] V285 scene: handle 2x2 and 5x5 grids from replay
- [ ] V286 agents: handle capture on move 1
- [ ] V287 dialogue: handle 25-move subgame chat length
- [ ] V288 controls: scrubber spans variable-length subgames
- [ ] V289 app: switching dataset reloads cleanly
- [ ] V290 css: chat panel max-height + overflow on small screens
- [ ] V291 css: bubble contrast meets readability
- [ ] V292 perf: cap total DOM bubbles to active speakers
- [ ] V293 perf: reuse geometries across tiles
- [ ] V294 a11y: focus ring on controls
- [ ] V295 a11y: chat is a labelled live region
- [ ] V296 serve: 404 page is friendly
- [ ] V297 serve: mime types correct for .js/.css
- [ ] V298 Makefile: `clean` removes generated replay artifacts
- [ ] V299 docs: viewer README in viewer/ explaining structure
- [ ] V300 QA: capture-to-GIF pipeline documented
- [ ] V301 QA: verify offline (airplane mode style) double-click works
- [ ] V302 Final: checkpoint screenshot attached in report
- [ ] V303 Final: SHOULD/COULD gated on user go-ahead
