// parley viewer — playback controls, sub-game selector, score HUD, capture banner.
(function (P) {
  var C = {};
  function byId(id) { return document.getElementById(id); }

  C.init = function (replay, app) {
    C.replay = replay;
    C.app = app;
    C.el = {
      play: byId('play'), back: byId('step-back'), fwd: byId('step-fwd'),
      speed: byId('speed'), scrub: byId('scrub'), sg: byId('subgames'),
      hud: byId('hud'), banner: byId('banner'),
    };
    C._buildSubgames();
    C._bind();
    return C;
  };

  C._buildSubgames = function () {
    C.replay.subgames.forEach(function (sg, i) {
      var b = document.createElement('button');
      b.textContent = i + 1;
      b.className = 'sg-btn ' + sg.winner;
      b.title = 'Sub-game ' + (i + 1) + ' — ' + sg.winner + ' wins';
      b.onclick = function () { C.app.selectSubgame(i); };
      C.el.sg.appendChild(b);
    });
  };

  C._bind = function () {
    C.el.play.onclick = function () { C.app.togglePlay(); };
    C.el.fwd.onclick = function () { C.app.step(1); };
    C.el.back.onclick = function () { C.app.step(-1); };
    C.el.speed.onchange = function () { C.app.setSpeed(parseFloat(C.el.speed.value)); };
    C.el.scrub.oninput = function () { C.app.scrubTo(parseInt(C.el.scrub.value, 10)); };
    document.addEventListener('keydown', function (e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
      if (e.code === 'Space') { e.preventDefault(); C.app.togglePlay(); }
      if (e.code === 'ArrowRight') C.app.step(1);
      if (e.code === 'ArrowLeft') C.app.step(-1);
    });
  };

  C.onSubgame = function (i, frameCount) {
    C.el.scrub.max = Math.max(0, frameCount - 1);
    C.el.scrub.value = 0;
    Array.prototype.forEach.call(C.el.sg.children, function (b, j) {
      b.classList.toggle('active', j === i);
    });
  };

  C.onFrame = function (sg, idx, frame) {
    C.el.scrub.value = idx;
    C.el.hud.innerHTML =
      'Sub-game <b>' + (sg.index + 1) + '</b>/' + C.replay.meta.num_subgames +
      ' · winner <b class="' + sg.winner + '">' + sg.winner + '</b>' +
      ' &nbsp;·&nbsp; running score &nbsp; COP <b class="cop">' + C.replay.meta.totals.cop + '</b>' +
      ' / THIEF <b class="thief">' + C.replay.meta.totals.thief + '</b>';
    C._banner(frame.capture ? 'CAPTURE' : '');
    C.el.play.textContent = C.app.playing ? '❚❚' : '▶';
  };

  C._banner = function (text) {
    C.el.banner.textContent = text;
    C.el.banner.style.opacity = text ? 1 : 0;
  };

  P.controls = C;
})(window.PARLEY);
