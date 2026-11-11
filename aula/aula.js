/* Aula virtual · Visualización de Datos (FACET-UNC). Sin servidor: el progreso vive en el navegador del estudiante
   y se entrega al docente mediante un reporte (.json) que el panel docente consolida. */
(() => {
"use strict";
const D = window.CURSO, C = D.config;
const KEY = "cvd_aula_v1", KEYD = "cvd_docente_v1", SAL = "cvd-aula-v1";
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
const mem = {};
const load = (k, d) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : (mem[k] ?? d); } catch { return mem[k] ?? d; } };
const save = (k, v) => { mem[k] = v; try { localStorage.setItem(k, JSON.stringify(v)); } catch {} };
const empty = () => ({ perfil: {}, done: {}, quiz: {}, auto: {}, oficial: {} });
let S = Object.assign(empty(), load(KEY, {}));
const persist = () => save(KEY, S);
const drive = id => `https://drive.google.com/drive/folders/${id}`;
const slug = s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "_").replace(/^_|_$/g, "");
const fmt = (x, d = 1) => Number.isFinite(x) ? x.toFixed(d).replace(/\.0+$/, "") : "–";
const ACTS = D.sesiones.flatMap(s => s.actividades.map(a => ({ ...a, n: s.n })));
const PRACT = ["s1_ej", "s2_ej", "s3_ej", "s4_mp1", "s5_mp2", "s6_ej", "s7_mp3"];
const actById = id => ACTS.find(a => a.id === id);
const LVL = ["", "Insuficiente", "En desarrollo", "Logrado", "Sobresaliente"];

/* ---------- cálculos compartidos (alumno y docente) ---------- */
function teoria(quiz) {
  const p = Object.keys(D.quizzes).map(n => quiz?.[n]?.mejor ?? 0).sort((a, b) => b - a).slice(0, 6);
  const pct = p.reduce((a, b) => a + b, 0) / 6;
  return { pct, pts: pct * 0.30 };
}
function calcular(quiz, oficial) {
  const t = teoria(quiz), o = oficial || {};
  const pr = Math.min(50, PRACT.reduce((s, id) => s + (+o[id] || 0), 0) + (+o.s8_red || 0));
  const it = (+o.s8_inf || 0) + (+o.s8_pres || 0);
  const total = t.pts + pr + it;
  return { teoria: t.pts, practica: pr, integ: it, total, escala: escala(total) };
}
const escala = t => { const r = Math.round(t); return r >= 91 ? 5 : r >= 81 ? 4 : r >= 70 ? 3 : r >= 60 ? 2 : 1; };
function autoPct(auto, act) {
  const r = D.rubricas[act.rubrica]; if (!r || !auto?.[act.id]) return null;
  const tot = r.criterios.reduce((s, c) => s + c.w, 0);
  return r.criterios.reduce((s, c, i) => s + ((auto[act.id][i] || 0) / 4) * c.w, 0) / tot;
}
function progSes(s, st = S) {
  const items = s.actividades.length + (s.quiz ? 1 : 0);
  let done = s.actividades.filter(a => st.done[a.id]).length;
  if (s.quiz && (st.quiz[s.n]?.mejor ?? -1) >= 60) done++;
  return { done, items, pct: items ? done / items : 0 };
}
const progTotal = (st = S) => { let d = 0, i = 0; D.sesiones.forEach(s => { const p = progSes(s, st); d += p.done; i += p.items; }); return i ? d / i : 0; };
const claveAlumno = p => (p.email || p.doc || p.nombre || "").trim().toLowerCase();
async function sha(txt) {
  try { const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(txt)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join(""); }
  catch { return ""; }
}
function descargar(nombre, texto, mime = "application/json") {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([texto], { type: mime + ";charset=utf-8" })); a.download = nombre;
  document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
const bar = (p, cls = "") => `<div class="bar ${cls}" role="progressbar" aria-valuenow="${Math.round(p * 100)}" aria-valuemin="0" aria-valuemax="100"><i style="width:${Math.round(p * 100)}%"></i></div>`;

/* ---------- navegación ---------- */
function navHtml(ruta) {
  const it = (h, t, extra = "") => `<a href="#${h}" ${ruta === h ? 'aria-current="page"' : ""}><span>${t}</span>${extra}</a>`;
  let h = it("/", "🏠 Inicio") + it("/notas", "📊 Mis notas") + it("/recursos", "📚 Recursos") + `<div class="grp">Módulos</div>`;
  D.sesiones.forEach(s => { const p = progSes(s); h += it(`/sesion/${s.n}`, `${s.n}. ${esc(s.corto)}`, `<span class="dot">${p.pct >= 1 ? "✅" : Math.round(p.pct * 100) + "%"}</span>`); });
  h += `<div class="grp">Cuenta</div>` + it("/perfil", "👤 Mi perfil") + it("/docente", "🧑‍🏫 Panel docente");
  $("#nav").innerHTML = h;
  $("#user").textContent = S.perfil.nombre ? S.perfil.nombre.split(" ")[0] : "Ingresar";
}

/* ---------- vistas ---------- */
function vInicio() {
  const reg = S.perfil.nombre;
  const sig = D.sesiones.find(s => progSes(s).pct < 1);
  const c = calcular(S.quiz, S.oficial);
  return `<h1>${reg ? "Hola, " + esc(S.perfil.nombre.split(" ")[0]) + " 👋" : "Bienvenido/a al aula virtual"}</h1>
  <p class="sub">${esc(C.curso)} · ${esc(C.programa)} · ${esc(C.semestre)}</p>
  ${reg ? "" : `<div class="card note"><b>Primero, completá tu perfil.</b> Tu nombre y documento identifican tu reporte de avance. <a class="btn" href="#/perfil" style="margin-left:.5rem">Ir a Mi perfil</a></div>`}
  <div class="kpis">
    <div class="card"><div class="muted">Avance del curso</div><div class="big">${Math.round(progTotal() * 100)}%</div>${bar(progTotal())}</div>
    <div class="card"><div class="muted">Teoría (quizzes) / 30</div><div class="big">${fmt(c.teoria)}</div><div class="muted">mejores 6 quizzes</div></div>
    <div class="card"><div class="muted">Nota provisoria / 100</div><div class="big">${fmt(c.total)}</div><div class="muted">escala sugerida: ${c.escala}</div></div>
  </div>
  ${sig ? `<h2>Próximo paso</h2><a class="card link" href="#/sesion/${sig.n}"><span class="tag">Módulo ${sig.n}</span><h3>${esc(sig.titulo)}</h3><p class="muted" style="margin:.3rem 0 0">${esc(sig.resumen)}</p></a>` : `<div class="card"><b>¡Completaste todos los módulos!</b> Descargá tu reporte en <a href="#/notas">Mis notas</a>.</div>`}
  <h2>Módulos</h2><div class="grid">${D.sesiones.map(s => { const p = progSes(s); return `<a class="card link" href="#/sesion/${s.n}">
    <div class="row" style="justify-content:space-between"><span class="tag">${s.unidad} · Sesión ${s.n}</span>${p.pct >= 1 ? '<span class="tag ok">Completo</span>' : ""}</div>
    <h3 style="margin-top:.5rem">${esc(s.titulo)}</h3>${bar(p.pct, p.pct >= 1 ? "ok" : "")}<span class="muted">${p.done}/${p.items} actividades${C.fechas?.[s.n] ? " · " + esc(C.fechas[s.n]) : ""}</span></a>`; }).join("")}</div>
  <h2>Cómo funciona esta aula</h2>
  <div class="card"><ol style="margin:0;padding-left:1.2rem">
   <li><b>Estudiá</b> cada módulo: guía, lecturas y laboratorio (se abre en Google Colab sin instalar nada).</li>
   <li><b>Practicá</b> con el quiz autocorregido y marcá tus actividades.</li>
   <li><b>Entregá</b> tus trabajos en la carpeta de Drive con el nombre sugerido (o por formulario si el docente lo habilita).</li>
   <li><b>Descargá tu reporte</b> en <a href="#/notas">Mis notas</a> y subilo a la carpeta de entregas: el docente lo consolida y te devuelve tu hoja de calificaciones.</li></ol>
   <p class="muted" style="margin-bottom:0">Tu progreso se guarda en este navegador. Usá “Copia de seguridad” en <a href="#/perfil">Mi perfil</a> para llevarlo a otro dispositivo.</p></div>`;
}

function vSesion(n) {
  const s = D.sesiones.find(x => x.n === n); if (!s) return vInicio();
  const p = progSes(s), prev = D.sesiones.find(x => x.n === n - 1), next = D.sesiones.find(x => x.n === n + 1);
  const ico = { guia: "📖", colab: "🚀", codigo: "💻", drive: "📁", lectura: "📄" };
  const q = S.quiz[n];
  const entregaNombre = id => `S${n}_${id}_${slug(S.perfil.apellido_nombre || S.perfil.nombre) || "Apellido_Nombre"}`;
  return `<span class="tag">${s.unidad} · Sesión ${s.n}</span>${s.n === 8 ? ' <span class="tag warn">Redes opcional</span>' : ""}
  <h1>${esc(s.titulo)}</h1><p class="sub">${esc(s.resumen)}${C.fechas?.[n] ? " · <b>" + esc(C.fechas[n]) + "</b>" : ""}</p>
  ${bar(p.pct, p.pct >= 1 ? "ok" : "")}<span class="muted">${p.done}/${p.items} completado</span>
  <h2>🎯 Objetivos</h2><div class="card"><ul style="margin:0;padding-left:1.2rem">${s.objetivos.map(o => `<li>${esc(o)}</li>`).join("")}</ul></div>
  <h2>🧰 Recursos</h2><div class="card"><ul class="res">${s.recursos.map(r => `<li><span class="ico">${ico[r.k] || "🔗"}</span>${r.u ? `<a href="${esc(r.u)}" target="${r.k === "guia" ? "_self" : "_blank"}" rel="noopener">${esc(r.t)}</a>` : esc(r.t)}</li>`).join("")}</ul>
   <p class="muted" style="margin:.5rem 0 0">Datasets del curso en <a href="#/recursos">Recursos</a>. En Colab: <i>Entorno de ejecución → Ejecutar todas</i>.</p></div>
  <h2>✅ Actividades y entregas</h2>
  ${s.actividades.map(a => { const r = D.rubricas[a.rubrica]; const ap = autoPct(S.auto, a); return `<div class="card"><div class="act">
    <input type="checkbox" id="chk_${a.id}" data-act="${a.id}" ${S.done[a.id] ? "checked" : ""} aria-label="Marcar como hecha">
    <div style="flex:1"><label for="chk_${a.id}" style="margin:0;font-weight:600">${esc(a.titulo)}</label>
    <div class="row" style="margin-top:.3rem">${a.pts ? `<span class="tag">${a.pts} pts</span>` : '<span class="tag warn">Hito sin nota</span>'}${a.rubrica ? `<span class="tag">Rúbrica ${a.rubrica}</span>` : ""}${(S.oficial[a.id] ?? "") !== "" ? `<span class="tag ok">Nota oficial: ${fmt(+S.oficial[a.id])}/${a.pts}</span>` : ""}</div>
    ${a.entrega ? `<details style="margin-top:.6rem"><summary>Cómo entregar</summary><div style="padding:.4rem 0">
      <p style="margin:.3rem 0">Nombrá tu archivo: <code>${esc(entregaNombre(a.id))}.ext</code></p>
      <div class="row"><a class="btn sec" target="_blank" rel="noopener" href="${drive(C.drive.entregas)}">📁 Abrir carpeta de entregas (Drive)</a>
      ${C.formulario_entregas ? `<a class="btn" target="_blank" rel="noopener" href="${esc(C.formulario_entregas)}">📝 Entregar por formulario</a>` : ""}</div></div></details>` : ""}
    ${r ? `<details style="margin-top:.4rem"><summary>Autoevaluación con rúbrica (${esc(r.titulo)})</summary><div style="padding:.5rem 0">
      <div class="tw"><table><thead><tr><th>Criterio</th><th>Peso</th><th>Tu nivel</th></tr></thead><tbody>${r.criterios.map((c, i) => `<tr><td>${esc(c.n)}</td><td>${c.w}%</td><td><select data-auto="${a.id}" data-i="${i}" aria-label="${esc(c.n)}"><option value="0">–</option>${[1, 2, 3, 4].map(v => `<option value="${v}" ${S.auto[a.id]?.[i] == v ? "selected" : ""}>${v} · ${LVL[v]}</option>`).join("")}</select></td></tr>`).join("")}</tbody></table></div>
      <p class="muted" id="ap_${a.id}" style="margin:.4rem 0 0">${ap == null ? "Completá los niveles para ver tu autoestimación." : `Autoestimación: <b>${fmt(ap * a.pts)}/${a.pts}</b> pts (${fmt(ap * 100, 0)}%) — referencial; la nota oficial la asigna el docente.`}</p></div></details>` : ""}
    </div></div></div>`; }).join("")}
  ${s.quiz ? `<h2>🧠 Quiz de teoría</h2><div class="card"><div class="row" style="justify-content:space-between"><div><b>${esc(D.quizzes[n].titulo)}</b><div class="muted">5 preguntas · retroalimentación inmediata · reintentos ilimitados (cuenta tu mejor resultado)</div>
    ${q ? `<div class="muted">Mejor: <b>${q.mejor}%</b> · Intentos: ${q.intentos.length}</div>` : ""}</div><a class="btn" href="#/quiz/${n}">${q ? "Reintentar" : "Comenzar quiz"}</a></div></div>` : ""}
  ${s.extra?.length ? `<h2>💡 Para profundizar</h2><div class="card"><ul style="margin:0;padding-left:1.2rem">${s.extra.map(e => `<li>${esc(e)}</li>`).join("")}</ul></div>` : ""}
  <div class="row" style="justify-content:space-between;margin-top:1.5rem">${prev ? `<a class="btn sec" href="#/sesion/${prev.n}">← Sesión ${prev.n}</a>` : "<span></span>"}${next ? `<a class="btn sec" href="#/sesion/${next.n}">Sesión ${next.n} →</a>` : ""}</div>`;
}

/* ---------- quiz ---------- */
const QZ = {};
const shuffle = a => { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
function nuevoQuiz(n) { QZ[n] = { preguntas: shuffle(D.quizzes[n].preguntas).map(p => ({ ...p, ops: shuffle(p.o.map((t, i) => ({ t, ok: i === p.c }))) })), resp: {}, hecho: false }; }
function vQuiz(n) {
  if (!D.quizzes[n]) return vInicio();
  if (!QZ[n]) nuevoQuiz(n);
  const z = QZ[n], total = z.preguntas.length;
  let html = `<a href="#/sesion/${n}">← Sesión ${n}</a><h1>Quiz · ${esc(D.quizzes[n].titulo)}</h1><p class="sub">Elegí una opción por pregunta. Al enviar verás la corrección y la explicación.</p>`;
  if (z.hecho) {
    const ok = z.preguntas.filter((p, i) => p.ops[z.resp[i]]?.ok).length, pct = Math.round(ok / total * 100);
    html += `<div class="card"><div class="big">${pct}%</div><div>${ok} de ${total} correctas · mejor resultado: <b>${S.quiz[n].mejor}%</b> ${pct >= 60 ? '<span class="tag ok">Aprobado</span>' : '<span class="tag bad">Repasá y reintentá</span>'}</div></div>`;
  }
  html += `<form id="qf">${z.preguntas.map((p, i) => `<fieldset class="q"><legend>${i + 1}. ${esc(p.q)}</legend>
    ${p.ops.map((o, j) => { const sel = z.resp[i] === j; const cls = z.hecho ? (o.ok ? "right" : sel ? "wrong" : "") : ""; return `<label class="opt ${cls}" style="font-weight:400;margin:.15rem 0"><input type="radio" name="q${i}" value="${j}" ${sel ? "checked" : ""} ${z.hecho ? "disabled" : ""}><span>${esc(o.t)} ${z.hecho && o.ok ? "✔" : z.hecho && sel ? "✘" : ""}</span></label>`; }).join("")}
    ${z.hecho ? `<div class="why"><b>${p.ops[z.resp[i]]?.ok ? "Correcto." : "Incorrecto."}</b> ${esc(p.why)}</div>` : ""}</fieldset>`).join("")}
    <div class="row">${z.hecho ? `<button type="button" class="btn" id="retry">Reintentar con orden distinto</button><a class="btn sec" href="#/sesion/${n}">Volver al módulo</a>` : `<button class="btn" type="submit" id="send">Enviar respuestas</button><span class="muted" id="qmsg"></span>`}</div></form>`;
  return html;
}
function bindQuiz(n) {
  const z = QZ[n], f = $("#qf"); if (!f) return;
  $("#retry")?.addEventListener("click", () => { nuevoQuiz(n); render(); });
  f.addEventListener("submit", e => {
    e.preventDefault();
    z.preguntas.forEach((_, i) => { const r = f.querySelector(`input[name=q${i}]:checked`); if (r) z.resp[i] = +r.value; });
    if (Object.keys(z.resp).length < z.preguntas.length) { $("#qmsg").textContent = `Faltan ${z.preguntas.length - Object.keys(z.resp).length} pregunta(s) por responder.`; return; }
    const ok = z.preguntas.filter((p, i) => p.ops[z.resp[i]].ok).length, pct = Math.round(ok / z.preguntas.length * 100);
    const q = S.quiz[n] || { mejor: 0, intentos: [] };
    q.intentos.push({ t: new Date().toISOString(), pct }); q.mejor = Math.max(q.mejor, pct); S.quiz[n] = q; persist();
    z.hecho = true; render(); window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ---------- notas del estudiante ---------- */
function vNotas() {
  const c = calcular(S.quiz, S.oficial), t = teoria(S.quiz);
  const filaQ = Object.keys(D.quizzes).map(n => { const q = S.quiz[n]; return `<tr><td>Quiz ${n} · ${esc(D.quizzes[n].titulo)}</td><td>${q ? q.mejor + "%" : "–"}</td><td>${q ? q.intentos.length : 0}</td></tr>`; }).join("");
  const filaA = ACTS.filter(a => a.pts).map(a => { const ap = autoPct(S.auto, a), of = S.oficial[a.id]; return `<tr><td>S${a.n} · ${esc(a.titulo)}</td><td>${a.pts}</td><td>${S.done[a.id] ? "✅" : "⬜"}</td><td>${ap == null ? "–" : fmt(ap * a.pts)}</td><td>${of === undefined || of === "" ? '<span class="muted">pendiente</span>' : "<b>" + fmt(+of) + "</b>"}</td></tr>`; }).join("");
  return `<h1>Mis notas y reporte</h1><p class="sub">Calificación estimada con lo que ya tiene nota oficial del docente. Teoría se calcula automáticamente con tus quizzes.</p>
  <div class="kpis"><div class="card"><div class="muted">Teoría / 30</div><div class="big">${fmt(c.teoria)}</div></div>
   <div class="card"><div class="muted">Práctica / 50</div><div class="big">${fmt(c.practica)}</div></div>
   <div class="card"><div class="muted">Integrador / 20</div><div class="big">${fmt(c.integ)}</div></div>
   <div class="card"><div class="muted">Total / 100</div><div class="big">${fmt(c.total)}</div><div class="muted">Escala sugerida: <b>${c.escala}</b></div></div></div>
  <h2>Quizzes (teoría 30 %)</h2><div class="card tw"><table><thead><tr><th>Quiz</th><th>Mejor</th><th>Intentos</th></tr></thead><tbody>${filaQ}</tbody></table><p class="muted">Se promedian los <b>6 mejores</b> de los quizzes (el de Redes es opcional y puede sustituir al más bajo). Promedio: ${fmt(t.pct)}%.</p></div>
  <h2>Práctica e integrador</h2><div class="card tw"><table><thead><tr><th>Actividad</th><th>Pts</th><th>Hecha</th><th>Autoestimación</th><th>Nota oficial</th></tr></thead><tbody>${filaA}</tbody></table></div>
  <h2>Reporte para el docente</h2><div class="card"><p style="margin-top:0">Descargá tu reporte y subilo a la carpeta de entregas. El docente lo importa en su panel, te asigna las notas y te devuelve una <b>hoja de calificaciones</b> que podés importar acá.</p>
   <div class="row noprint"><button class="btn" id="bRep">⬇ Descargar mi reporte (.json)</button><a class="btn sec" target="_blank" rel="noopener" href="${drive(C.drive.entregas)}">📁 Carpeta de entregas</a><button class="btn sec" onclick="window.print()">🖨 Imprimir constancia</button></div>
   <label for="impNotas" class="noprint">Importar hoja de calificaciones del docente</label><input type="file" id="impNotas" accept=".json" class="noprint"><div id="impMsg" class="muted"></div></div>`;
}
async function descargarReporte() {
  if (!S.perfil.nombre) { alert("Completá tu perfil antes de generar el reporte."); location.hash = "#/perfil"; return; }
  const payload = { v: 1, generado: new Date().toISOString(), perfil: S.perfil, done: S.done, quiz: S.quiz, auto: S.auto };
  const rep = { ...payload, sha: await sha(JSON.stringify(payload) + SAL) };
  descargar(`reporte_${slug(S.perfil.nombre)}.json`, JSON.stringify(rep, null, 1));
}
function bindNotas() {
  $("#bRep")?.addEventListener("click", descargarReporte);
  $("#impNotas")?.addEventListener("change", async e => {
    const f = e.target.files[0]; if (!f) return;
    try {
      const j = JSON.parse(await f.text()); if (j.tipo !== "calificaciones" || !j.oficial) throw 0;
      const mine = claveAlumno(S.perfil);
      if (j.clave && mine && j.clave !== mine && !confirm("La hoja es de otra persona (" + j.nombre + "). ¿Importar igual?")) return;
      S.oficial = { ...S.oficial, ...j.oficial }; persist(); $("#impMsg").textContent = "Calificaciones importadas ✔"; setTimeout(render, 600);
    } catch { $("#impMsg").textContent = "Archivo no válido."; }
  });
}

/* ---------- recursos ---------- */
function vRecursos() {
  return `<h1>Recursos del curso</h1><p class="sub">Todo el material en un solo lugar.</p>
  <h2>📁 Google Drive</h2><div class="card"><ul class="res">
   <li><span class="ico">📂</span><a target="_blank" rel="noopener" href="${drive(C.drive.raiz)}">Carpeta general del aula</a></li>
   <li><span class="ico">📘</span><a target="_blank" rel="noopener" href="${drive(C.drive.programa)}">Programa y guías</a></li>
   <li><span class="ico">🗂</span><a target="_blank" rel="noopener" href="${drive(C.drive.datos)}">Datasets</a></li>
   <li><span class="ico">📤</span><a target="_blank" rel="noopener" href="${drive(C.drive.entregas)}">Entregas de estudiantes</a></li>
   <li><span class="ico">🎓</span><a target="_blank" rel="noopener" href="${drive(C.drive.integrador)}">Proyecto integrador</a></li>
   ${D.sesiones.map(s => `<li><span class="ico">${s.n}</span><a target="_blank" rel="noopener" href="${drive(C.drive.sesiones[s.n])}">Sesión ${s.n}: materiales</a></li>`).join("")}</ul></div>
  <h2>🗃 Datasets (descarga directa)</h2><div class="card tw"><table><tbody>${D.datasets.map(([f, d]) => `<tr><td><a href="${C.raw}/datos/${f}" download>${f}</a></td><td class="muted">${esc(d)}</td></tr>`).join("")}</tbody></table><p class="muted">Sintéticos y reproducibles (<code>datos/generar_datos.py</code>). Para mini-proyectos e integrador usá datos reales (datos.gov.py, INE, BCP, Our World in Data).</p></div>
  <h2>📜 Documentos</h2><div class="card"><ul class="res">
   ${[["programa", "Programa de estudios"], ["cronograma", "Cronograma"], ["evaluacion", "Evaluación"], ["rubricas", "Rúbricas"], ["proyecto_integrador", "Proyecto integrador"], ["bibliografia", "Bibliografía y fuentes de datos"], ["banco_quizzes", "Banco de quizzes (con respuestas)"]].map(([f, t]) => `<li><span class="ico">📄</span><a href="../docs/${f}.html">${t}</a></li>`).join("")}</ul></div>
  <h2>⚙️ Entorno local (opcional)</h2><div class="card"><p style="margin-top:0">Podés trabajar sin instalar nada con Colab. Para trabajar en tu equipo:</p><pre style="overflow:auto;background:var(--bg);padding:.8rem;border-radius:8px"><code>git clone ${esc(C.repo)}.git
cd curso_visualiza_datos_UNC
python -m venv .venv &amp;&amp; source .venv/bin/activate
pip install -r requirements.txt
python tools/py2nb.py &amp;&amp; jupyter lab</code></pre></div>
  <h2>🔤 Glosario</h2><div class="card"><input type="text" id="gq" placeholder="Buscar término…" aria-label="Buscar en el glosario"><dl id="gl">${D.glosario.map(g => `<div data-t="${esc((g.t + " " + g.d).toLowerCase())}"><dt>${esc(g.t)}</dt><dd>${esc(g.d)}</dd></div>`).join("")}</dl></div>`;
}
function bindRecursos() { $("#gq")?.addEventListener("input", e => { const q = e.target.value.toLowerCase(); $$("#gl > div").forEach(d => d.hidden = !d.dataset.t.includes(q)); }); }

/* ---------- perfil ---------- */
function vPerfil() {
  const p = S.perfil;
  return `<h1>Mi perfil</h1><p class="sub">Estos datos identifican tu reporte. Se guardan solo en este navegador.</p>
  <form class="card" id="pf"><label for="pn">Nombre y apellido *</label><input type="text" id="pn" required value="${esc(p.nombre)}" autocomplete="name">
   <label for="pd">N.º de documento (C.I.) *</label><input type="text" id="pd" required value="${esc(p.doc)}">
   <label for="pe">Correo electrónico</label><input type="email" id="pe" value="${esc(p.email)}" autocomplete="email">
   <label for="pc">Cohorte / grupo</label><input type="text" id="pc" value="${esc(p.cohorte)}" placeholder="p. ej. MICD 2026">
   <div class="row" style="margin-top:1rem"><button class="btn" type="submit">Guardar</button><span id="pm" class="muted"></span></div></form>
  <h2>Copia de seguridad</h2><div class="card"><p style="margin-top:0">El progreso se guarda en este navegador. Exportá una copia para usarla en otro dispositivo.</p><div class="row"><button class="btn sec" id="bk">⬇ Exportar copia</button><label class="btn sec" style="margin:0;cursor:pointer">⬆ Importar copia<input type="file" id="bki" accept=".json" hidden></label><button class="btn sec" id="rs" style="color:var(--bad);border-color:var(--bad)">Borrar mis datos</button></div></div>`;
}
function bindPerfil() {
  $("#pf")?.addEventListener("submit", e => { e.preventDefault(); S.perfil = { nombre: $("#pn").value.trim(), doc: $("#pd").value.trim(), email: $("#pe").value.trim(), cohorte: $("#pc").value.trim() }; persist(); $("#pm").textContent = "Guardado ✔"; navHtml("/perfil"); });
  $("#bk")?.addEventListener("click", () => descargar(`copia_aula_${slug(S.perfil.nombre) || "estudiante"}.json`, JSON.stringify({ tipo: "copia", estado: S })));
  $("#bki")?.addEventListener("change", async e => { try { const j = JSON.parse(await e.target.files[0].text()); if (j.tipo !== "copia") throw 0; S = Object.assign(empty(), j.estado); persist(); render(); } catch { alert("Archivo no válido."); } });
  $("#rs")?.addEventListener("click", () => { if (confirm("¿Borrar tu perfil, progreso y quizzes de este navegador?")) { S = empty(); persist(); render(); } });
}

/* ---------- panel docente ---------- */
let DOC = Object.assign({ alumnos: {} }, load(KEYD, {}));
const persistDoc = () => save(KEYD, DOC);
const GRADED = ACTS.filter(a => a.pts);
function filaDoc(k) {
  const a = DOC.alumnos[k], r = a.reporte, c = calcular(r.quiz, a.notas), pg = progTotal({ done: r.done || {}, quiz: r.quiz || {} });
  return `<tr data-k="${esc(k)}"><td><b>${esc(r.perfil.nombre)}</b><div class="muted">${esc(r.perfil.doc || "")} ${esc(r.perfil.email || "")}</div></td>
   <td>${Math.round(pg * 100)}%</td><td title="Quizzes">${fmt(c.teoria)}</td>
   ${GRADED.map(g => `<td><input type="number" min="0" max="${g.pts}" step="0.5" data-k="${esc(k)}" data-id="${g.id}" value="${a.notas[g.id] ?? ""}" aria-label="${esc(r.perfil.nombre)} ${g.id}"></td>`).join("")}
   <td data-c="pr">${fmt(c.practica)}</td><td data-c="it">${fmt(c.integ)}</td><td data-c="tt"><b>${fmt(c.total)}</b></td><td data-c="es"><b>${c.escala}</b></td>
   <td>${a.ok === true ? "✔" : a.ok === false ? '<span title="El contenido no coincide con su huella: fue modificado">⚠</span>' : "?"}</td>
   <td class="row"><button class="btn sec" data-hoja="${esc(k)}">Hoja</button><button class="btn sec" data-del="${esc(k)}" aria-label="Quitar">✕</button></td></tr>`;
}
function vDocente() {
  const ks = Object.keys(DOC.alumnos);
  return `<h1>Panel docente</h1><p class="sub">Consolida los reportes de los estudiantes, registra las notas de práctica e integrador y calcula la nota final.</p>
  <div class="note">🔒 Todo se procesa <b>en tu navegador</b>: los reportes no se suben a ningún servidor. Los datos del panel se guardan localmente; usá “Exportar copia” para respaldarlos. La huella (✔/⚠) detecta ediciones accidentales del archivo, pero no es una firma criptográfica: para evaluaciones de alto impacto, tomá los quizzes de forma presencial/sincrónica.</div>
  <div class="card"><div class="drop" id="drop"><p style="margin:0 0 .5rem">Arrastrá aquí los <b>reportes (.json)</b> de los estudiantes o</p><input type="file" id="fin" accept=".json" multiple></div>
   <div class="row" style="margin-top:.8rem"><button class="btn" id="csv" ${ks.length ? "" : "disabled"}>⬇ Exportar calificaciones (CSV)</button><button class="btn sec" id="dbk">⬇ Exportar copia</button><label class="btn sec" style="margin:0;cursor:pointer">⬆ Importar copia<input type="file" id="dbi" accept=".json" hidden></label></div><div id="dm" class="muted"></div></div>
  <h2>Estudiantes (${ks.length})</h2>
  ${ks.length ? `<div class="card tw"><table><thead><tr><th>Estudiante</th><th>Avance</th><th>Teoría/30</th>${GRADED.map(g => `<th title="${esc(g.titulo)}">${g.id.replace("s", "S").replace("_", " ")}<br>/${g.pts}</th>`).join("")}<th>Práct./50</th><th>Integr./20</th><th>Total</th><th>Esc.</th><th>Huella</th><th></th></tr></thead><tbody>${ks.map(filaDoc).join("")}</tbody></table>
   <p class="muted">Escala sugerida: 1 (&lt;60) · 2 (60-69) · 3 (70-80) · 4 (81-90) · 5 (≥91). Ajustar al reglamento vigente de la Maestría. Práctica incluye hasta +3 por el ejercicio opcional de redes (tope 50).</p></div>` : `<div class="card muted">Aún no importaste reportes.</div>`}`;
}
async function importarReportes(files) {
  let ok = 0, bad = 0;
  for (const f of files) {
    try {
      const r = JSON.parse(await f.text()); if (!r.perfil?.nombre || !r.quiz) throw 0;
      const { sha: h, ...payload } = r; const calc = await sha(JSON.stringify(payload) + SAL);
      const k = claveAlumno(r.perfil), prev = DOC.alumnos[k];
      DOC.alumnos[k] = { reporte: r, notas: prev?.notas || {}, ok: h ? h === calc : null }; ok++;
    } catch { bad++; }
  }
  persistDoc(); render(); $("#dm") && ($("#dm").textContent = `${ok} reporte(s) importado(s)${bad ? `, ${bad} no válido(s)` : ""}.`);
}
function bindDocente() {
  const fin = $("#fin"), drop = $("#drop");
  fin?.addEventListener("change", e => importarReportes([...e.target.files]));
  ["dragover", "dragenter"].forEach(ev => drop?.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach(ev => drop?.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("over"); }));
  drop?.addEventListener("drop", e => importarReportes([...e.dataTransfer.files]));
  $$("input[data-id]").forEach(inp => inp.addEventListener("input", () => {
    const k = inp.dataset.k, id = inp.dataset.id, g = actById(id); let v = inp.value === "" ? "" : Math.max(0, Math.min(g.pts, +inp.value));
    DOC.alumnos[k].notas[id] = v; if (v === "") delete DOC.alumnos[k].notas[id]; persistDoc();
    const c = calcular(DOC.alumnos[k].reporte.quiz, DOC.alumnos[k].notas), tr = inp.closest("tr");
    tr.querySelector("[data-c=pr]").textContent = fmt(c.practica); tr.querySelector("[data-c=it]").textContent = fmt(c.integ);
    tr.querySelector("[data-c=tt]").innerHTML = `<b>${fmt(c.total)}</b>`; tr.querySelector("[data-c=es]").innerHTML = `<b>${c.escala}</b>`;
  }));
  $$("[data-del]").forEach(b => b.addEventListener("click", () => { if (confirm("¿Quitar este estudiante del panel?")) { delete DOC.alumnos[b.dataset.del]; persistDoc(); render(); } }));
  $$("[data-hoja]").forEach(b => b.addEventListener("click", () => { const a = DOC.alumnos[b.dataset.hoja];
    descargar(`calificaciones_${slug(a.reporte.perfil.nombre)}.json`, JSON.stringify({ tipo: "calificaciones", clave: b.dataset.hoja, nombre: a.reporte.perfil.nombre, fecha: new Date().toISOString(), oficial: a.notas }, null, 1)); }));
  $("#csv")?.addEventListener("click", () => {
    const qs = Object.keys(D.quizzes), head = ["nombre", "documento", "email", "cohorte", "avance_%", ...qs.map(n => "quiz" + n + "_%"), "teoria_30", ...GRADED.map(g => g.id), "practica_50", "integrador_20", "total_100", "escala", "huella"];
    const rows = Object.values(DOC.alumnos).map(a => { const r = a.reporte, c = calcular(r.quiz, a.notas);
      return [r.perfil.nombre, r.perfil.doc, r.perfil.email, r.perfil.cohorte, Math.round(progTotal({ done: r.done || {}, quiz: r.quiz }) * 100), ...qs.map(n => r.quiz[n]?.mejor ?? ""), fmt(c.teoria, 2), ...GRADED.map(g => a.notas[g.id] ?? ""), fmt(c.practica, 2), fmt(c.integ, 2), fmt(c.total, 2), c.escala, a.ok === true ? "ok" : a.ok === false ? "modificado" : "sin_huella"]; });
    descargar("calificaciones_curso.csv", "﻿" + [head, ...rows].map(r => r.map(x => `"${String(x ?? "").replace(/"/g, '""')}"`).join(",")).join("\n"), "text/csv");
  });
  $("#dbk")?.addEventListener("click", () => descargar("copia_panel_docente.json", JSON.stringify({ tipo: "copia_docente", DOC })));
  $("#dbi")?.addEventListener("change", async e => { try { const j = JSON.parse(await e.target.files[0].text()); if (j.tipo !== "copia_docente") throw 0; DOC = j.DOC; persistDoc(); render(); } catch { alert("Archivo no válido."); } });
}

/* ---------- router ---------- */
function render() {
  const ruta = (location.hash.replace(/^#/, "") || "/"), [, a, b] = ruta.split("/");
  const n = +b; let html, bind = () => {}, crumb = "Inicio";
  switch (a) {
    case "sesion": html = vSesion(n); crumb = `Módulo ${n}`; bind = () => bindSesion(); break;
    case "quiz": html = vQuiz(n); crumb = `Módulo ${n} › Quiz`; bind = () => bindQuiz(n); break;
    case "notas": html = vNotas(); crumb = "Mis notas"; bind = bindNotas; break;
    case "recursos": html = vRecursos(); crumb = "Recursos"; bind = bindRecursos; break;
    case "perfil": html = vPerfil(); crumb = "Mi perfil"; bind = bindPerfil; break;
    case "docente": html = vDocente(); crumb = "Panel docente"; bind = bindDocente; break;
    default: html = vInicio();
  }
  $("#main").innerHTML = html; $("#crumb").textContent = `${C.curso} › ${crumb}`;
  navHtml(ruta === "" ? "/" : "/" + [a, b].filter(Boolean).join("/")); bind();
  document.title = `${crumb} · Aula virtual · Visualización de Datos UNC`;
  $("#side").classList.remove("open"); $("#menu").setAttribute("aria-expanded", "false");
}
function bindSesion() {
  $$("[data-act]").forEach(c => c.addEventListener("change", () => { S.done[c.dataset.act] = c.checked; if (!c.checked) delete S.done[c.dataset.act]; persist(); navHtml(location.hash.replace(/^#/, "")); }));
  $$("[data-auto]").forEach(sel => sel.addEventListener("change", () => {
    const id = sel.dataset.auto; S.auto[id] = S.auto[id] || {}; S.auto[id][sel.dataset.i] = +sel.value; persist();
    const a = actById(id), ap = autoPct(S.auto, a);
    $("#ap_" + id).innerHTML = `Autoestimación: <b>${fmt(ap * a.pts)}/${a.pts}</b> pts (${fmt(ap * 100, 0)}%) — referencial; la nota oficial la asigna el docente.`;
  }));
}
window.addEventListener("hashchange", () => { if (!location.hash.startsWith("#/quiz/")) Object.keys(QZ).forEach(k => delete QZ[k]); render(); window.scrollTo(0, 0); });
$("#menu").addEventListener("click", () => { const o = $("#side").classList.toggle("open"); $("#menu").setAttribute("aria-expanded", o); });
$("#lnk-drive").href = drive(C.drive.raiz);
render();
})();
