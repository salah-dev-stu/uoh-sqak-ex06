// parley viewer — MCP message-flow inset: surfaces the orchestration layer.
// A small 2D overlay shows the Orchestrator (MCP client, holds the LLM) talking to
// the two FastMCP servers; a dot animates along the edge each turn in the direction
// of that turn's tool calls (observe → think → send_message/act).
(function (P) {
  var M = { dots: [] };

  M.init = function (canvas) {
    M.canvas = canvas;
    M.ctx = canvas.getContext('2d');
    M.nodes = {
      orch: { x: 0.5, y: 0.26, label: 'Orchestrator', sub: 'MCP client · LLM' },
      cop: { x: 0.2, y: 0.8, label: 'Cop server', sub: 'FastMCP' },
      thief: { x: 0.8, y: 0.8, label: 'Thief server', sub: 'FastMCP' },
    };
    M._resize();
    window.addEventListener('resize', M._resize);
    return M;
  };

  M._resize = function () {
    var r = M.canvas.getBoundingClientRect();
    M.canvas.width = r.width * (window.devicePixelRatio || 1);
    M.canvas.height = r.height * (window.devicePixelRatio || 1);
  };

  // Fire a message dot toward the server whose agent is acting this turn.
  M.onTurn = function (role) {
    var to = role === 'cop' ? 'cop' : 'thief';
    M.dots.push({ from: 'orch', to: to, t: 0, dir: 1 });   // push observation/prompt
    M.dots.push({ from: to, to: 'orch', t: -0.5, dir: -1 }); // reply: message + action
  };

  M.reset = function () { M.dots = []; };

  function lerp(a, b, t) { return a + (b - a) * t; }

  M._node = function (ctx, n, w, h, color) {
    var x = n.x * w, y = n.y * h;
    ctx.fillStyle = 'rgba(10,16,28,.95)';
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(x - 54, y - 17, 108, 34, 8);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#dfe8f6';
    ctx.font = '11px -apple-system, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(n.label, x, y - 2);
    ctx.fillStyle = '#7a89a6';
    ctx.font = '9px -apple-system, sans-serif';
    ctx.fillText(n.sub, x, y + 10);
  };

  M.update = function (dt) {
    var ctx = M.ctx, w = M.canvas.width, h = M.canvas.height;
    ctx.clearRect(0, 0, w, h);
    var col = { orch: P.util.colors.neon, cop: P.util.colors.cop, thief: P.util.colors.thief };

    Object.keys(M.nodes).forEach(function (k) {
      ['cop', 'thief'].forEach(function (s) {
        if (k !== 'orch') return;
        var a = M.nodes.orch, b = M.nodes[s];
        ctx.strokeStyle = 'rgba(120,140,180,.28)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(a.x * w, a.y * h + 17);
        ctx.lineTo(b.x * w, b.y * h - 17);
        ctx.stroke();
      });
    });

    M.dots = M.dots.filter(function (d) {
      d.t += dt / 0.9;
      if (d.t < 0) return true;
      if (d.t > 1) return false;
      var a = M.nodes[d.from], b = M.nodes[d.to];
      var x = lerp(a.x, b.x, d.t) * w, y = lerp(a.y, b.y, d.t) * h;
      ctx.fillStyle = d.dir > 0 ? col[d.to] : col[d.from];
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
      return true;
    });

    M._node(ctx, M.nodes.orch, w, h, col.orch);
    M._node(ctx, M.nodes.cop, w, h, col.cop);
    M._node(ctx, M.nodes.thief, w, h, col.thief);
  };

  P.mcpflow = M;
})(window.PARLEY);
