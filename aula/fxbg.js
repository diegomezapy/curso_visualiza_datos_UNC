/* Fondo animado "campo de datos": nodos que derivan, se unen por proximidad (red) y reaccionan al puntero.
   Canvas 2D sin dependencias. Se pausa en pestañas ocultas, limita DPR y respeta prefers-reduced-motion. */
(function () {
  var KEY = "cvd_fx", cv = document.getElementById("fx-bg"); if (!cv) return;
  var ctx = cv.getContext("2d"), reduce = matchMedia("(prefers-reduced-motion: reduce)");
  var on = true, raf = 0, W = 0, H = 0, dpr = 1, N = [], mx = -999, my = -999, col = [0, 114, 178], last = 0, tCol = 0;
  try { var s = localStorage.getItem(KEY); on = s ? s === "on" : !reduce.matches; } catch (e) { on = !reduce.matches; }
  function rgb() { var v = getComputedStyle(document.documentElement).getPropertyValue("--ac").trim(), m;
    if ((m = /^#([0-9a-f]{6})$/i.exec(v))) col = [parseInt(m[1].slice(0, 2), 16), parseInt(m[1].slice(2, 4), 16), parseInt(m[1].slice(4), 16)]; }
  function size() { dpr = Math.min(devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight; cv.width = W * dpr; cv.height = H * dpr; cv.style.width = W + "px"; cv.style.height = H + "px"; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var n = Math.round(Math.min(70, Math.max(22, W * H / 22000))); while (N.length < n) N.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .25, vy: (Math.random() - .5) * .25, r: 1 + Math.random() * 1.8, p: Math.random() * 6.28 }); N.length = n; }
  function frame(t) {
    raf = 0; if (!on) return;
    var dt = Math.min(50, t - last || 16); last = t; if (t - tCol > 2000) { rgb(); tCol = t; }
    ctx.clearRect(0, 0, W, H);
    var c = col.join(","), D = 130, i, j, a, b;
    for (i = 0; i < N.length; i++) { a = N[i]; a.x += a.vx * dt / 16; a.y += a.vy * dt / 16;
      var dx = a.x - mx, dy = a.y - my, d2 = dx * dx + dy * dy; if (d2 < 14000 && d2 > 1) { var f = (1 - d2 / 14000) * .6; a.x += dx / Math.sqrt(d2) * f; a.y += dy / Math.sqrt(d2) * f; }
      if (a.x < -10) a.x = W + 10; else if (a.x > W + 10) a.x = -10; if (a.y < -10) a.y = H + 10; else if (a.y > H + 10) a.y = -10; }
    ctx.lineWidth = 1;
    for (i = 0; i < N.length; i++) { a = N[i];
      for (j = i + 1; j < N.length; j++) { b = N[j]; var ddx = a.x - b.x, ddy = a.y - b.y, dd = ddx * ddx + ddy * ddy;
        if (dd < D * D) { ctx.strokeStyle = "rgba(" + c + "," + (0.30 * (1 - Math.sqrt(dd) / D)).toFixed(3) + ")"; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); } }
      var pulse = .5 + .3 * Math.sin(t / 900 + a.p); ctx.fillStyle = "rgba(" + c + "," + pulse.toFixed(3) + ")"; ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fill(); }
    // línea de "serie temporal" muy tenue que ondula al pie de la ventana
    ctx.strokeStyle = "rgba(" + c + ",.16)"; ctx.lineWidth = 1.5; ctx.beginPath();
    for (var x = 0; x <= W; x += 14) { var y = H - 60 - 22 * Math.sin(x / 120 + t / 1800) - 10 * Math.sin(x / 37 + t / 700); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
    raf = requestAnimationFrame(frame);
  }
  function start() { if (!raf && on && !document.hidden) { last = 0; raf = requestAnimationFrame(frame); } }
  function stop() { if (raf) cancelAnimationFrame(raf); raf = 0; ctx.clearRect(0, 0, W, H); }
  function apply() { document.documentElement.classList.toggle("fx-off", !on); cv.hidden = !on; on ? (rgb(), start()) : stop(); }
  addEventListener("resize", function () { size(); }, { passive: true });
  addEventListener("pointermove", function (e) { mx = e.clientX; my = e.clientY; }, { passive: true });
  addEventListener("pointerleave", function () { mx = my = -999; });
  document.addEventListener("visibilitychange", function () { document.hidden ? (raf && cancelAnimationFrame(raf), raf = 0) : start(); });
  reduce.addEventListener && reduce.addEventListener("change", function () { try { if (localStorage.getItem(KEY)) return; } catch (e) {} on = !reduce.matches; apply(); });
  window.FXBG = { get enabled() { return on; }, set: function (v) { on = !!v; try { localStorage.setItem(KEY, on ? "on" : "off"); } catch (e) {} apply(); } };
  size(); apply();
})();
