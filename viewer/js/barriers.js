// parley viewer — neon barriers slamming down onto the rooftop.
(function (P) {
  var B = { meshes: {}, grid: null };

  B.init = function (grid) {
    B.grid = grid;
    B._clear();
    return B;
  };

  B._clear = function () {
    Object.keys(B.meshes).forEach(function (k) {
      P.scene.scene.remove(B.meshes[k]);
    });
    B.meshes = {};
  };

  B.setFrame = function (frame, animate) {
    var present = {};
    frame.barriers.forEach(function (cell) {
      var key = cell[0] + ',' + cell[1];
      present[key] = true;
      if (!B.meshes[key]) B._add(cell, animate);
    });
    Object.keys(B.meshes).forEach(function (key) {
      if (!present[key]) {
        P.scene.scene.remove(B.meshes[key]);
        delete B.meshes[key];
      }
    });
  };

  B.REST_Y = 0.52;

  B._add = function (cell, animate) {
    var w = P.util.tileToWorld(cell[0], cell[1], B.grid);
    var geo = new THREE.BoxGeometry(0.86, 1.05, 0.86);
    // A translucent neon force-field, not a solid block: you can see through it,
    // and the bright wireframe + horizontal bars read as a shutter/wall.
    var mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
      color: 0x0c2630, emissive: P.util.colors.neon, emissiveIntensity: 0.35,
      transparent: true, opacity: 0.32, metalness: 0.3, roughness: 0.4, depthWrite: false,
    }));
    mesh.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(geo),
      new THREE.LineBasicMaterial({ color: 0x9ff6ee, transparent: true, opacity: 0.95 })
    ));
    for (var i = 1; i <= 3; i++) {  // horizontal shutter slats
      var bar = new THREE.Mesh(
        new THREE.BoxGeometry(0.9, 0.045, 0.9),
        new THREE.MeshBasicMaterial({ color: 0x6ff0e4, transparent: true, opacity: 0.5 })
      );
      bar.position.y = -0.52 + i * 0.26;
      mesh.add(bar);
    }
    mesh.position.set(w.x, animate ? 2.6 : B.REST_Y, w.z);
    if (animate) mesh.userData.slam = 0;
    P.scene.scene.add(mesh);
    B.meshes[cell[0] + ',' + cell[1]] = mesh;
  };

  B.update = function (dt) {
    Object.keys(B.meshes).forEach(function (key) {
      var m = B.meshes[key];
      if (m.userData.slam === undefined) return;
      m.userData.slam = Math.min(1, m.userData.slam + dt / 0.3);
      m.position.y = P.util.lerp(2.6, B.REST_Y, P.util.easeInOut(m.userData.slam));
      if (m.userData.slam >= 1) delete m.userData.slam;
    });
  };

  P.barriers = B;
})(window.PARLEY);
