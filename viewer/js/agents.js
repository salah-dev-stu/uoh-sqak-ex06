// parley viewer — the Cop and Thief figures, gliding tile-to-tile (diagonals arc).
(function (P) {
  var A = {};

  function makeAgent(color, tall) {
    var g = new THREE.Group();
    var h = tall ? 0.8 : 0.66;
    var body = new THREE.Mesh(
      new THREE.CylinderGeometry(0.16, 0.3, h, 16),
      new THREE.MeshStandardMaterial({ color: color, emissive: color, emissiveIntensity: 0.65,
        metalness: 0.4, roughness: 0.3 })
    );
    body.position.y = h / 2 + 0.04;
    g.add(body);
    var head = new THREE.Mesh(
      new THREE.SphereGeometry(0.16, 18, 18),
      new THREE.MeshStandardMaterial({ color: color, emissive: color, emissiveIntensity: 0.95 })
    );
    head.position.y = h + 0.18;
    g.add(head);
    var light = new THREE.PointLight(color, 1.0, 4.0);
    light.position.y = 0.8;
    g.add(light);
    return g;
  }

  A.init = function (grid) {
    A.grid = grid;
    A.cop = makeAgent(P.util.colors.cop, true);
    A.thief = makeAgent(P.util.colors.thief, false);
    P.scene.scene.add(A.cop);
    P.scene.scene.add(A.thief);
    A.anim = { cop: { from: null, to: null, t: 1 }, thief: { from: null, to: null, t: 1 } };
    return A;
  };

  A.place = function (role, tile, off) {
    var w = P.util.tileToWorld(tile[0], tile[1], A.grid);
    w.x += off || 0;
    A[role].position.set(w.x, 0, w.z);
    A.anim[role] = { from: w.clone(), to: w.clone(), t: 1 };
  };

  A.moveTo = function (role, tile, animate, off) {
    var w = P.util.tileToWorld(tile[0], tile[1], A.grid);
    w.x += off || 0;
    if (!animate) { A.place(role, tile, off); return; }
    A.anim[role] = { from: A[role].position.clone(), to: w, t: 0 };
  };

  // When both land on the same cell (capture), stand them side-by-side instead
  // of clipping into each other, and mark the thief as caught.
  A.setFrame = function (frame, animate) {
    var same = frame.cop[0] === frame.thief[0] && frame.cop[1] === frame.thief[1];
    var off = same ? 0.26 : 0;
    A.moveTo('cop', frame.cop, animate, off);
    A.moveTo('thief', frame.thief, animate, -off);
    A.thief.scale.setScalar(same ? 0.78 : 1);
    A.thief.rotation.z = same ? 0.5 : 0;
  };

  A.update = function (dt) {
    ['cop', 'thief'].forEach(function (role) {
      var s = A.anim[role];
      if (s.t >= 1) return;
      s.t = Math.min(1, s.t + dt / 0.7);
      var e = P.util.easeInOut(s.t);
      var x = P.util.lerp(s.from.x, s.to.x, e);
      var z = P.util.lerp(s.from.z, s.to.z, e);
      var dist = s.from.distanceTo(s.to);
      var hop = Math.sin(e * Math.PI) * Math.min(0.55, dist * 0.28);
      A[role].position.set(x, hop, z);
    });
  };

  P.agents = A;
})(window.PARLEY);
