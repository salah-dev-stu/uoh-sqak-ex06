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
    var geo = new THREE.BoxGeometry(0.84, 1.02, 0.84);
    // A neon CAGE: a faint glowing core framed by bright wireframe edges and a ring
    // of vertical bars around the cell — clearly "this cell is blocked" from any angle.
    var mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
      color: 0x0c2a34, emissive: P.util.colors.neon, emissiveIntensity: 0.45,
      transparent: true, opacity: 0.22, metalness: 0.3, roughness: 0.4, depthWrite: false,
    }));
    mesh.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(geo),
      new THREE.LineBasicMaterial({ color: 0x9ff6ee, transparent: true, opacity: 1 })
    ));
    var barMat = new THREE.MeshBasicMaterial({ color: 0x8ff7ec });
    var h = 0.38;
    var ring = [[-h, -h], [0, -h], [h, -h], [h, 0], [h, h], [0, h], [-h, h], [-h, 0]];
    ring.forEach(function (p) {
      var bar = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.02, 8), barMat);
      bar.position.set(p[0], 0, p[1]);
      mesh.add(bar);
    });
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
