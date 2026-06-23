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
    var geo = new THREE.BoxGeometry(0.84, 1.04, 0.84);
    var mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
      color: 0x10333f, emissive: P.util.colors.neon, emissiveIntensity: 1.0,
      transparent: true, opacity: 0.9, metalness: 0.5, roughness: 0.25,
    }));
    mesh.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(geo),
      new THREE.LineBasicMaterial({ color: 0x9ff6ee, transparent: true, opacity: 0.95 })
    ));
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
