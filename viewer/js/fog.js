// parley viewer — fog-of-war + view toggle: this IS the partial-observation (Dec-POMDP)
// showcase. In a player's view, tiles beyond the vision radius go dark AND the opponent
// figure vanishes — you only know where they are from the words in the chat.
(function (P) {
  var F = { mode: 'director' };

  function cheb(a, b) { return Math.max(Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1])); }

  F.init = function (buttons, hintEl, onChange) {
    F.buttons = buttons;
    F.hint = hintEl;
    F.onChange = onChange;
    Object.keys(buttons).forEach(function (mode) {
      buttons[mode].onclick = function () { F.setMode(mode); };
    });
    F.setMode('director');
    return F;
  };

  F.setMode = function (mode) {
    F.mode = mode;
    Object.keys(F.buttons).forEach(function (m) {
      F.buttons[m].classList.toggle('active', m === mode);
    });
    if (F.hint) {
      F.hint.style.opacity = mode === 'director' ? 0 : 1;
      F.hint.textContent = mode === 'director' ? '' :
        'Fog of war — you see only the ' + mode + "'s vision radius. " +
        'The opponent is hidden; infer them from the words.';
    }
    if (F.onChange) F.onChange();
  };

  F.apply = function (frame) {
    var grid = window.REPLAY.meta.grid_size, rows = grid[0], cols = grid[1];
    var vr = frame.vision_radius;
    var viewer = F.mode === 'cop' ? frame.cop : F.mode === 'thief' ? frame.thief : null;

    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var key = r + ',' + c;
        var vis = !viewer || cheb(viewer, [r, c]) <= vr;
        var tile = P.scene.tiles[key], edge = P.scene.edges[key];
        tile.material.emissiveIntensity = vis ? 0.62 : 0.03;
        tile.material.color.setHex(vis ? P.util.colors.tile : 0x05080f);
        edge.material.opacity = vis ? 0.75 : 0.05;
      }
    }

    if (viewer) {
      var oppRole = F.mode === 'cop' ? 'thief' : 'cop';
      var oppPos = F.mode === 'cop' ? frame.thief : frame.cop;
      P.agents[oppRole].visible = cheb(viewer, oppPos) <= vr;
      P.agents[F.mode].visible = true;
    } else {
      P.agents.cop.visible = true;
      P.agents.thief.visible = true;
    }
  };

  P.fog = F;
})(window.PARLEY);
