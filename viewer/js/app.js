// parley viewer — main: read window.REPLAY, drive frames, wire the modules.
(function (P) {
  var App = { playing: false, speed: 0.5, sgIndex: 0, frameIdx: 0, _acc: 0 };
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
    App.playing = false;   // start paused at the very beginning — press Play to watch all 6
    App._clock = performance.now();
    requestAnimationFrame(App._loop);
  };

  App.subgame = function () { return App.replay.subgames[App.sgIndex]; };

  App.restart = function () {
    App._chain = undefined;
    App.selectSubgame(0);
    App.playing = true;
  };

  App.selectSubgame = function (i) {
    App._chain = undefined;
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
    App._chain = undefined;
    var n = App.subgame().frames.length;
    var ni = P.util.clamp(App.frameIdx + d, 0, n - 1);
    if (ni === App.frameIdx) return;
    App.frameIdx = ni;
    App._apply(ni, true, false);
  };

  App.scrubTo = function (idx) {
    App.playing = false;
    App._chain = undefined;
    App.frameIdx = idx;
    App._apply(idx, false, false);
  };

  // From the last frame of the last sub-game, play restarts the whole game.
  App.togglePlay = function () {
    var last = App.sgIndex === App.replay.subgames.length - 1 &&
      App.frameIdx >= App.subgame().frames.length - 1;
    if (!App.playing && last) { App.restart(); return; }
    App.playing = !App.playing;
  };

  App.setSpeed = function (s) { App.speed = s; };

  // At a sub-game's end, pause briefly then auto-advance to the next one — so a
  // single Play runs the whole game (all 6 sub-games) start to end.
  App._advance = function () {
    var sg = App.subgame();
    if (App.frameIdx >= sg.frames.length - 1) {
      if (App.sgIndex < App.replay.subgames.length - 1) App._chain = 0;
      else App.playing = false;
      return;
    }
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
      if (App._chain !== undefined) {
        App._chain += dt;
        if (App._chain > 2.0) { App._chain = undefined; App.selectSubgame(App.sgIndex + 1); }
      } else {
        App._acc += dt * App.speed;
        // ~1.7s per move at 1x — time to read the taunt and watch the glide.
        if (App._acc >= 1.7) { App._acc = 0; App._advance(); }
      }
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
