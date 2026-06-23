// parley viewer — the neon-noir rooftop: renderer, camera, lights, tile grid.
(function (P) {
  var S = {};

  S.init = function (container, grid) {
    S.grid = grid;
    S.renderer = new THREE.WebGLRenderer({ antialias: true });
    S.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    S.renderer.setClearColor(P.util.colors.bg, 1);
    container.appendChild(S.renderer.domElement);

    S.scene = new THREE.Scene();
    S.scene.fog = new THREE.FogExp2(P.util.colors.bg, 0.03);

    var rows = grid[0], cols = grid[1], span = Math.max(rows, cols);
    S.camera = new THREE.PerspectiveCamera(50, 1, 0.1, 200);
    S.camera.position.set(span * 0.85, span * 1.25, span * 1.35);

    S.controls = new THREE.OrbitControls(S.camera, S.renderer.domElement);
    S.controls.target.set(0, 0, 0);
    S.controls.enableDamping = true;
    S.controls.dampingFactor = 0.08;
    S.controls.maxPolarAngle = Math.PI * 0.48;
    S.controls.minDistance = span * 0.8;
    S.controls.maxDistance = span * 4;

    S.scene.add(new THREE.AmbientLight(0x223044, 0.75));
    var key = new THREE.DirectionalLight(0x9fb4ff, 0.55);
    key.position.set(6, 14, 7);
    S.scene.add(key);

    var base = new THREE.Mesh(
      new THREE.BoxGeometry(cols + 1.4, 0.4, rows + 1.4),
      new THREE.MeshStandardMaterial({ color: 0x070b14, metalness: 0.65, roughness: 0.45 })
    );
    base.position.y = -0.28;
    S.scene.add(base);

    S.tiles = {};
    S.edges = {};
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var p = P.util.tileToWorld(r, c, grid);
        var geo = new THREE.BoxGeometry(0.9, 0.08, 0.9);
        var tile = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
          color: P.util.colors.tile, emissive: 0x0a2740, emissiveIntensity: 0.55,
          metalness: 0.3, roughness: 0.6,
        }));
        tile.position.copy(p);
        var edges = new THREE.LineSegments(
          new THREE.EdgesGeometry(geo),
          new THREE.LineBasicMaterial({ color: P.util.colors.neon, transparent: true, opacity: 0.5 })
        );
        edges.position.copy(p);
        S.scene.add(tile); S.scene.add(edges);
        S.tiles[r + ',' + c] = tile;
        S.edges[r + ',' + c] = edges;
      }
    }

    S.resize(container);
    window.addEventListener('resize', function () { S.resize(container); });
    return S;
  };

  S.resize = function (container) {
    var w = container.clientWidth, h = container.clientHeight;
    S.renderer.setSize(w, h);
    S.camera.aspect = w / h;
    S.camera.updateProjectionMatrix();
  };

  S.render = function () { S.controls.update(); S.renderer.render(S.scene, S.camera); };

  P.scene = S;
})(window.PARLEY);
