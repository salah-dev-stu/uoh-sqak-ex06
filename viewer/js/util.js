// parley viewer — shared helpers + the single global namespace.
window.PARLEY = window.PARLEY || {};
(function (P) {
  P.util = {
    lerp: function (a, b, t) { return a + (b - a) * t; },
    clamp: function (v, lo, hi) { return Math.max(lo, Math.min(hi, v)); },
    easeInOut: function (t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; },

    colors: { cop: 0x39a0ff, thief: 0xff9d3a, neon: 0x14e0d0, bg: 0x05060a, tile: 0x0c1424 },

    // grid (row, col) -> world (x = col, z = row), board centred at the origin.
    tileToWorld: function (r, c, grid, size) {
      size = size || 1;
      var rows = grid[0], cols = grid[1];
      return new THREE.Vector3((c - (cols - 1) / 2) * size, 0, (r - (rows - 1) / 2) * size);
    },

    projectToScreen: function (vec3, camera, dom) {
      var v = vec3.clone().project(camera);
      return {
        x: (v.x * 0.5 + 0.5) * dom.clientWidth,
        y: (-v.y * 0.5 + 0.5) * dom.clientHeight,
        behind: v.z > 1,
      };
    },
  };
})(window.PARLEY);
