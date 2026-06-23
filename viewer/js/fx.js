// parley viewer — capture FX: a gold particle burst at the moment of arrest.
(function (P) {
  var FX = { active: null };

  FX.burst = function (worldPos, color) {
    var N = 70;
    var positions = new Float32Array(N * 3);
    var vel = [];
    for (var i = 0; i < N; i++) {
      positions[i * 3] = worldPos.x;
      positions[i * 3 + 1] = 0.45;
      positions[i * 3 + 2] = worldPos.z;
      var a = Math.random() * Math.PI * 2;
      var up = 0.6 + Math.random() * 2.2;
      var s = 1.6 + Math.random() * 2.4;
      vel.push(new THREE.Vector3(Math.cos(a) * s, up, Math.sin(a) * s));
    }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var mat = new THREE.PointsMaterial({
      color: color || 0xffd24a, size: 0.14, transparent: true, opacity: 1,
      blending: THREE.AdditiveBlending, depthWrite: false,
    });
    var pts = new THREE.Points(geo, mat);
    P.scene.scene.add(pts);
    if (FX.active) FX._dispose();
    FX.active = { pts: pts, geo: geo, mat: mat, vel: vel, life: 0 };
  };

  FX.update = function (dt) {
    var a = FX.active;
    if (!a) return;
    a.life += dt;
    var arr = a.geo.attributes.position.array;
    for (var i = 0; i < a.vel.length; i++) {
      arr[i * 3] += a.vel[i].x * dt;
      arr[i * 3 + 1] += (a.vel[i].y - a.life * 4.5) * dt;
      arr[i * 3 + 2] += a.vel[i].z * dt;
    }
    a.geo.attributes.position.needsUpdate = true;
    a.mat.opacity = Math.max(0, 1 - a.life / 1.15);
    if (a.life > 1.15) FX._dispose();
  };

  FX._dispose = function () {
    if (!FX.active) return;
    P.scene.scene.remove(FX.active.pts);
    FX.active.geo.dispose();
    FX.active.mat.dispose();
    FX.active = null;
  };

  P.fx = FX;
})(window.PARLEY);
