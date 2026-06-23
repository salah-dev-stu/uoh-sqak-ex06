// parley viewer — main: read window.REPLAY, drive frames, wire the modules.
(function (P) {
  var App = { playing: false, speed: 1, sgIndex: 0, frameIdx: 0, _acc: 0 };
  function gid(id) { return document.getElementById(id); }

  App.start = function () {
    if (!window.REPLAY || !window.REPLAY.subgames) {
      gid('error').style.display = 'block';
      return;
    }
    App.replay = window.REPLAY;
    var grid = App.replay.meta.grid_size;
    P.scene.init(gid('stage'), grid);
    P.agents.init(grid);
    P.barriers.init(grid);
    P.dialogue.init(gid('bubbles'), gid('chat'), gid('source'));
    P.fog.init(
      { director: gid('view-director'), cop: gid('view-cop'), thief: gid('view-thief') },
      gid('fog-hint'),
      function () { if (App.curFrame) P.fog.apply(App.curFrame); }
    );
    P.controls.init(App.replay, App);
    App.selectSubgame(0);
    App._clock = performance.now();
    requestAnimationFrame(App._loop);
  };

  App.subgame = function () { return App.replay.subgames[App.sgIndex]; };

  App.selectSubgame = function (i) {
    App.sgIndex = i;
    App.frameIdx = 0;
    var sg = App.subgame();
    P.agents.place('cop', sg.start.cop);
    P.agents.place('thief', sg.start.thief);
    P.dialogue.reset();
    P.controls.onSubgame(i, sg.frames.length);
    App._apply(0, false, false);
    App.playing = true;
  };

  App._apply = function (idx, animate, append) {
    var sg = App.subgame();
    var frame = sg.frames[idx];
    P.agents.setFrame(frame, animate);
    P.barriers.setFrame(frame, animate);
    P.dialogue.setFrame(sg.frames, idx, append);
    P.controls.onFrame(sg, idx, frame);
    P.fog.apply(frame);
    App.curFrame = frame;
    if (animate && frame.capture) App._burst(frame);
  };

  App._burst = function (frame) {
    var key = App.sgIndex + ':' + App.frameIdx;
    if (App._burstKey === key) return;
    App._burstKey = key;
    P.fx.burst(P.util.tileToWorld(frame.cop[0], frame.cop[1], App.replay.meta.grid_size), 0xffd24a);
  };

  App.step = function (d) {
    App.playing = false;
    var n = App.subgame().frames.length;
    var ni = P.util.clamp(App.frameIdx + d, 0, n - 1);
    if (ni === App.frameIdx) return;
    App.frameIdx = ni;
    App._apply(ni, true, false);
  };

  App.scrubTo = function (idx) {
    App.playing = false;
    App.frameIdx = idx;
    App._apply(idx, false, false);
  };

  App.togglePlay = function () { App.playing = !App.playing; };
  App.setSpeed = function (s) { App.speed = s; };

  App._advance = function () {
    var sg = App.subgame();
    if (App.frameIdx >= sg.frames.length - 1) { App.playing = false; return; }
    App.frameIdx += 1;
    App._apply(App.frameIdx, true, true);
  };

  App._loop = function (now) {
    var dt = (now - App._clock) / 1000;
    App._clock = now;
    P.agents.update(dt);
    P.barriers.update(dt);
    P.fx.update(dt);
    if (App.playing) {
      App._acc += dt * App.speed;
      if (App._acc >= 0.85) { App._acc = 0; App._advance(); }
    }
    P.dialogue.updateBubbles(P.scene.camera, P.scene.renderer.domElement);
    P.scene.render();
    requestAnimationFrame(App._loop);
  };

  P.app = App;
  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', App.start);
  } else {
    App.start();
  }
})(window.PARLEY);
