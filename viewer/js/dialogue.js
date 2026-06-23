// parley viewer — the graded centrepiece: NL taunts as speech bubbles + chat feed.
(function (P) {
  var D = {};

  // Render the LLM's light markdown (**bold**, *italic*, line breaks) as real
  // formatting — HTML-escaped first so the text can never inject markup.
  function mdToHtml(text) {
    var s = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    s = s.replace(/\n+/g, '<br>');
    return s;
  }

  D.init = function (bubbleLayer, chatEl, sourceEl) {
    D.bubbleLayer = bubbleLayer;
    D.chatEl = chatEl;
    D.bubbles = { cop: D._bubble('cop'), thief: D._bubble('thief') };
    if (sourceEl && window.REPLAY) sourceEl.textContent = window.REPLAY.meta.source;
    return D;
  };

  D._bubble = function (role) {
    var b = document.createElement('div');
    b.className = 'bubble ' + role;
    b.style.opacity = 0;
    D.bubbleLayer.appendChild(b);
    return b;
  };

  D.reset = function () {
    D.chatEl.innerHTML = '';
    D.bubbles.cop.style.opacity = 0;
    D.bubbles.thief.style.opacity = 0;
  };

  D._append = function (frame) {
    var line = document.createElement('div');
    line.className = 'chat-line ' + frame.role;
    var msg = frame.message || '(moves in silence)';
    var html = mdToHtml(msg);
    line.innerHTML = '<span class="who">' + frame.role + '</span>' +
      '<span class="mv">m' + frame.move + '</span><span class="msg">' + html + '</span>';
    // Only auto-scroll if the user is already near the bottom — so they can
    // freely scroll up to re-read earlier dialogue without being yanked down.
    var atBottom = D.chatEl.scrollHeight - D.chatEl.scrollTop - D.chatEl.clientHeight < 60;
    D.chatEl.appendChild(line);
    if (atBottom) D.chatEl.scrollTop = D.chatEl.scrollHeight;

    // Only the active speaker's bubble shows, so two bubbles never overlap. It
    // carries the full taunt (formatted); the chat panel keeps the history.
    var other = frame.role === 'cop' ? 'thief' : 'cop';
    var b = D.bubbles[frame.role];
    b.innerHTML = html;
    b.style.opacity = 1;
    D.bubbles[other].style.opacity = 0;
  };

  // append=true streams one new line; otherwise rebuild chat history up to idx.
  D.setFrame = function (frames, idx, append) {
    if (append) { D._append(frames[idx]); return; }
    D.chatEl.innerHTML = '';
    for (var i = 0; i <= idx; i++) D._append(frames[i]);
  };

  D.updateBubbles = function (camera, dom) {
    ['cop', 'thief'].forEach(function (role) {
      var b = D.bubbles[role];
      if (parseFloat(b.style.opacity) < 0.05) { b.style.display = 'none'; return; }
      var pos = P.agents[role].position.clone();
      pos.y += 1.25;
      var s = P.util.projectToScreen(pos, camera, dom);
      b.style.display = s.behind ? 'none' : 'block';
      b.style.left = s.x + 'px';
      b.style.top = s.y + 'px';
    });
  };

  P.dialogue = D;
})(window.PARLEY);
