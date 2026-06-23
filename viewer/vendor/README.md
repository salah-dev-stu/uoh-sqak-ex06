# Vendored libraries (offline, no CDN at grade time)

| File | Library | Version | License |
|---|---|---|---|
| `three.min.js` | [Three.js](https://threejs.org) — **global build** (`window.THREE`) | r128 (0.128.0) | MIT |
| `OrbitControls.js` | Three.js example control (classic, attaches `THREE.OrbitControls`) | r128 | MIT |

These are the **classic global builds** (not ES modules) on purpose: ES modules are
blocked by the browser over `file://` (CORS), so vendoring the global build lets the
viewer open by **double-clicking `viewer/index.html`** with no server and no network.
