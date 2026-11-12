/* Efectos de interfaz del aula: hero con gráficos animados, contadores, revelado al hacer scroll,
   brillo que sigue al puntero y transición entre vistas. Todo se desactiva con "Efectos" o prefers-reduced-motion. */
const fxOn = () => !document.documentElement.classList.contains("fx-off");
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* ---------- hero: gráficos que se dibujan solos; el anillo muestra el avance real ---------- */
export function heroHtml(pct = 0, nombre = "") {
  const bars = [38, 62, 45, 80, 58, 92, 70, 104], W = 28, G = 10, x0 = 12;
  const pts = [[12, 118], [52, 96], [92, 104], [132, 70], [172, 82], [212, 46], [252, 56], [292, 24]];
  const line = pts.map((p, i) => (i ? "L" : "M") + p.join(" ")).join(" "), area = line + " L292 140 L12 140 Z";
  const R = 46, C = +(2 * Math.PI * R).toFixed(1), off = +(C * (1 - Math.max(0, Math.min(1, pct)))).toFixed(1), mv = fxOn();
  return `<section class="hero" aria-label="Resumen visual" data-fx-mouse>
   <div class="hero-txt"><span class="hero-tag"><i></i> Visualización de datos · en vivo</span>
    <h1 class="hero-h">${nombre ? `Hola, ${nombre}.` : "Hola."}<br><span class="grad">Convertí datos en decisiones.</span></h1>
    <p class="hero-sub">Percepción, color, dashboards, redes y storytelling con Python y R, usando datos reales de Paraguay.</p>
    <div class="hero-chips" aria-hidden="true"><span>Python</span><span>R · RPubs</span><span>Plotly</span><span>ggplot2</span><span>Datos abiertos</span></div></div>
   <svg class="hero-viz" viewBox="0 0 420 170" role="img" aria-label="Ilustración: gráfico de barras, línea de tendencia y anillo con tu avance del ${Math.round(pct * 100)}%">
    <defs><linearGradient id="hg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--ac)" stop-opacity=".45"/><stop offset="1" stop-color="var(--ac)" stop-opacity="0"/></linearGradient></defs>
    <g class="hv-grid">${[30, 70, 110].map(y => `<line x1="8" x2="300" y1="${y}" y2="${y}"/>`).join("")}</g>
    <g class="hv-bars">${bars.map((h, i) => `<rect style="--i:${i}" x="${x0 + i * (W + G) - 4 + 4}" y="${140 - h}" width="${W - 6}" height="${h}" rx="3"/>`).join("")}</g>
    <path class="hv-area" d="${area}" fill="url(#hg)"/><path class="hv-line" d="${line}" pathLength="1"/>
    ${pts.map((p, i) => `<circle class="hv-pt" style="--i:${i}" cx="${p[0]}" cy="${p[1]}" r="3.6"/>`).join("")}
    ${mv ? `<circle class="hv-dot" r="5"><animateMotion dur="7s" repeatCount="indefinite" path="${line}"/></circle>` : ""}
    <g transform="translate(362 82)"><circle class="hv-ring0" r="${R}"/><circle class="hv-ring" r="${R}" stroke-dasharray="${C}" stroke-dashoffset="${mv ? C : off}" style="--c:${C};--o:${off}" transform="rotate(-90)"/>
     <text class="hv-pct" text-anchor="middle" y="6" data-count="${Math.round(pct * 100)}" data-suf="%">${Math.round(pct * 100)}%</text><text class="hv-lbl" text-anchor="middle" y="26">avance</text></g>
   </svg></section>`;
}

/* ---------- contadores ---------- */
function countUp(el) {
  const raw = el.dataset.count ?? el.textContent, m = String(raw).match(/-?\d+(?:[.,]\d+)?/); if (!m) return;
  const dec = (m[0].split(/[.,]/)[1] || "").length, to = parseFloat(m[0].replace(",", ".")), pre = String(raw).slice(0, m.index), suf = el.dataset.suf ?? String(raw).slice(m.index + m[0].length);
  const t0 = performance.now(), dur = 900;
  const step = t => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); el.textContent = pre + (to * e).toFixed(dec) + suf; if (k < 1) requestAnimationFrame(step); else el.textContent = pre + to.toFixed(dec) + suf; };
  requestAnimationFrame(step);
}

/* ---------- revelado al hacer scroll ---------- */
let io;
function reveal() {
  io?.disconnect(); const els = $$("#main .card, #main .vcard, #main .tl, #main .grid > *, #main h2").filter((e, i, a) => a.indexOf(e) === i);
  if (!fxOn() || !("IntersectionObserver" in window)) return;
  io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }), { rootMargin: "0px 0px -6% 0px", threshold: .05 });
  els.forEach((e, i) => { e.classList.add("fx-reveal"); e.style.setProperty("--d", Math.min(i % 8, 7) * 45 + "ms"); io.observe(e); });
  setTimeout(() => els.forEach(e => e.classList.add("in")), 1800); // red de seguridad: nada queda oculto
}

/* ---------- se llama después de cada render ---------- */
export function afterRender() {
  const main = document.getElementById("main"); if (!main) return;
  main.classList.remove("fx-enter"); void main.offsetWidth; if (fxOn()) main.classList.add("fx-enter");
  if (fxOn()) $$("#main .big, #main .hv-pct").forEach(countUp);
  reveal();
}

/* ---------- brillo que sigue al puntero + botón de efectos ---------- */
export function initFx() {
  document.addEventListener("pointermove", e => {
    const t = e.target.closest?.(".card.link, .vcard, .hero, .kpis .card, .grid > .card"); if (!t || !fxOn()) return;
    const r = t.getBoundingClientRect(); t.style.setProperty("--mx", e.clientX - r.left + "px"); t.style.setProperty("--my", e.clientY - r.top + "px"); t.classList.add("glow");
  }, { passive: true });
  const bar = document.querySelector(".topbar"), b = document.createElement("button");
  b.id = "fxbtn"; b.className = "user"; b.type = "button"; b.title = "Activar o desactivar las animaciones";
  const pintar = () => { b.textContent = fxOn() ? "✨ Efectos: sí" : "✨ Efectos: no"; b.setAttribute("aria-pressed", fxOn()); };
  b.addEventListener("click", () => { window.FXBG?.set(!fxOn()); pintar(); document.dispatchEvent(new Event("fx-change")); afterRender(); });
  bar?.insertBefore(b, document.getElementById("user")); pintar();
}
