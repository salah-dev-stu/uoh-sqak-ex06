// parley viewer — cinematic auto-follow camera: the OrbitControls target eases
// toward the midpoint of the action (between cop and thief) so the chase stays
// framed. Toggleable; manual orbit still works while it's off.
(function (P) {
  var F = { on: false };

  F.init = function (button) {
    F.button = button;
    if (button) {
      button.onclick = function () { F.toggle(); };
      F._sync();
    }
    return F;
  };

  F.toggle = function () { F.on = !F.on; F._sync(); };

  F._sync = function () {
    if (F.button) {
      F.button.classList.toggle('active', F.on);
      F.button.textContent = F.on ? 'Auto-cam ●' : 'Auto-cam';
    }
  };

  F.update = function (dt) {
    if (!F.on || !P.app || !P.app.curFrame) return;
    var grid = P.app.replay.meta.grid_size;
    var c = P.util.tileToWorld(P.app.curFrame.cop[0], P.app.curFrame.cop[1], grid);
    var t = P.util.tileToWorld(P.app.curFrame.thief[0], P.app.curFrame.thief[1], grid);
    var mid = new THREE.Vector3((c.x + t.x) / 2, 0, (c.z + t.z) / 2);
    var k = Math.min(1, dt * 2.2);
    P.scene.controls.target.lerp(mid, k);
  };

  P.follow = F;
})(window.PARLEY);
