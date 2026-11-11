/* Aula virtual · Visualización de Datos (FACET-UNC).
   Autenticación y datos: Firebase (Auth + Firestore) o modo demo local (ver backend.js). */
import { crearBackend, msgError } from "./backend.js";
(async () => {
"use strict";
const D = window.CURSO, C = D.config;

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
const empty = () => ({ perfil: {}, done: {}, quiz: {}, auto: {}, oficial: {} });
let S = empty(), USER = null, PERFIL = null, ES_DOC = false, ocupado = false, B;
let tmr;
const persist = () => { if (!USER || !PERFIL || PERFIL.virtual) return; clearTimeout(tmr); tmr = setTimeout(flush, 500); };
const flush = () => { clearTimeout(tmr); if (USER && PERFIL && !PERFIL.virtual) B.guardarProgreso(USER.uid, { done: S.done, quiz: S.quiz, auto: S.auto }).catch(e => aviso(msgError(e), "bad")); };
addEventListener("pagehide", flush);
function aviso(msg, tipo = "ok") { const t = $("#toast"); t.textContent = msg; t.className = "show " + tipo; clearTimeout(aviso.t); aviso.t = setTimeout(() => t.className = "", 4500); }
const drive = id => `https://drive.google.com/drive/folders/${id}`;
const nombreCompleto = p => `${p.nombres || ""} ${p.apellidos || ""}`.trim();
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
  h += `<div class="grp">Cuenta</div>` + it("/perfil", "👤 Mi perfil") + (ES_DOC ? it("/docente", "🧑‍🏫 Panel docente") : "");
  $("#nav").innerHTML = h;
  $("#user").textContent = PERFIL ? (PERFIL.nombres || "").split(" ")[0] : "Ingresar";
}

/* ---------- vistas ---------- */
function vInicio() {
  const reg = PERFIL?.nombres;
  const sig = D.sesiones.find(s => progSes(s).pct < 1);
  const c = calcular(S.quiz, S.oficial);
  return `<h1>Hola, ${esc((reg || "").split(" ")[0])} 👋</h1>
  <p class="sub">${esc(C.curso)} · ${esc(C.programa)} · ${esc(C.semestre)}</p>
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
   <li><b>Consultá tus notas</b> en <a href="#/notas">Mis notas</a>: el docente carga las calificaciones oficiales y se actualizan acá.</li></ol>
   <p class="muted" style="margin-bottom:0">Tu progreso se guarda en tu cuenta: podés continuar desde cualquier dispositivo.</p></div>`;
}

function vSesion(n) {
  const s = D.sesiones.find(x => x.n === n); if (!s) return vInicio();
  const p = progSes(s), prev = D.sesiones.find(x => x.n === n - 1), next = D.sesiones.find(x => x.n === n + 1);
  const ico = { guia: "📖", colab: "🚀", codigo: "💻", drive: "📁", lectura: "📄" };
  const q = S.quiz[n];
  const entregaNombre = id => `S${n}_${id}_${`${slug(PERFIL.apellidos)}_${slug(PERFIL.nombres)}`}`;
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
  return `<h1>Mis notas y reporte</h1><p class="sub">Calificación estimada con lo que ya tiene nota oficial del docente. Teoría se calcula automáticamente con tus quizzes. Las notas oficiales se actualizan cuando el docente las carga.</p>
  <div class="kpis"><div class="card"><div class="muted">Teoría / 30</div><div class="big">${fmt(c.teoria)}</div></div>
   <div class="card"><div class="muted">Práctica / 50</div><div class="big">${fmt(c.practica)}</div></div>
   <div class="card"><div class="muted">Integrador / 20</div><div class="big">${fmt(c.integ)}</div></div>
   <div class="card"><div class="muted">Total / 100</div><div class="big">${fmt(c.total)}</div><div class="muted">Escala sugerida: <b>${c.escala}</b></div></div></div>
  <h2>Quizzes (teoría 30 %)</h2><div class="card tw"><table><thead><tr><th>Quiz</th><th>Mejor</th><th>Intentos</th></tr></thead><tbody>${filaQ}</tbody></table><p class="muted">Se promedian los <b>6 mejores</b> de los quizzes (el de Redes es opcional y puede sustituir al más bajo). Promedio: ${fmt(t.pct)}%.</p></div>
  <h2>Práctica e integrador</h2><div class="card tw"><table><thead><tr><th>Actividad</th><th>Pts</th><th>Hecha</th><th>Autoestimación</th><th>Nota oficial</th></tr></thead><tbody>${filaA}</tbody></table></div>
  <div class="row noprint" style="margin-top:1rem"><button class="btn sec" onclick="window.print()">🖨 Imprimir constancia de avance</button></div>
  <p class="muted">${esc(nombreCompleto(PERFIL))} · C.I. ${esc(PERFIL.cedula)} · generado ${new Date().toLocaleDateString("es-PY")}</p>`;
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



/* ---------- acceso, registro y cuenta ---------- */
const DEPTOS = ["Asunción", "Concepción", "San Pedro", "Cordillera", "Guairá", "Caaguazú", "Caazapá", "Itapúa", "Misiones", "Paraguarí", "Alto Paraná", "Central", "Ñeembucú", "Amambay", "Canindeyú", "Presidente Hayes", "Boquerón", "Alto Paraguay", "Fuera de Paraguay"];
const SEXOS = ["Femenino", "Masculino", "Otro", "Prefiero no decir"];
const CONSENT = "Autorizo el tratamiento de mis datos personales con fines exclusivamente académicos y administrativos de este curso (identificación, seguimiento y evaluación). Los datos se almacenan en un servicio de Google (Firebase), solo son visibles para mí y para el docente, no se comparten con terceros y puedo solicitar su corrección o eliminación al docente.";
const claveOk = c => c.length >= 8 && /[A-Za-z]/.test(c) && /\d/.test(c);
const demoBanner = () => B.modo === "demo" ? `<div class="note" style="margin-bottom:1rem"><b>MODO DEMOSTRACIÓN.</b> Este aula todavía no está conectada a un servidor: las cuentas y datos se guardan solo en este navegador. Ver <i>docs/configurar_firebase.md</i> para activar el modo real.</div>` : "";
const inp = (id, label, v = "", ex = "", req = true) => `<div><label for="${id}">${label}${req ? " *" : ""}</label><input type="text" id="${id}" value="${esc(v)}" ${req ? "required" : ""} ${ex}></div>`;
const sel = (id, label, opts, v = "", req = true) => `<div><label for="${id}">${label}${req ? " *" : ""}</label><select id="${id}" ${req ? "required" : ""}><option value="">Seleccioná…</option>${opts.map(o => `<option ${o === v ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></div>`;
function camposPerfil(p = {}, edit = false) {
  const hoy = new Date(), max = new Date(hoy.getFullYear() - 16, hoy.getMonth(), hoy.getDate()).toISOString().slice(0, 10);
  return `<div class="form-grid">
   ${inp("f_nombres", "Nombres", p.nombres, 'autocomplete="given-name"')}${inp("f_apellidos", "Apellidos", p.apellidos, 'autocomplete="family-name"')}
   ${inp("f_cedula", "N.º de cédula de identidad (solo números)", p.cedula, `inputmode="numeric" pattern="[0-9]{4,10}" maxlength="10" ${edit ? "readonly" : ""}`)}
   <div><label for="f_fechaNac">Fecha de nacimiento *</label><input type="date" id="f_fechaNac" required min="1930-01-01" max="${max}" value="${esc(p.fechaNac)}" autocomplete="bday"></div>
   ${sel("f_sexo", "Sexo", SEXOS, p.sexo)}${inp("f_nacionalidad", "Nacionalidad", p.nacionalidad || "Paraguaya")}
   ${sel("f_departamento", "Departamento de residencia", DEPTOS, p.departamento)}${inp("f_ciudad", "Ciudad / localidad", p.ciudad)}
   ${inp("f_direccion", "Dirección o barrio", p.direccion, "", false)}${inp("f_telefono", "Teléfono / WhatsApp", p.telefono, 'inputmode="tel" autocomplete="tel"', false)}
   ${inp("f_institucion", "Institución o empresa donde trabaja", p.institucion, "", false)}${inp("f_profesion", "Profesión", p.profesion, "", false)}
   ${inp("f_cohorte", "Cohorte / grupo", p.cohorte || "MICD 2026", "", false)}</div>`;
}
function leerPerfil() {
  const v = id => ($("#" + id)?.value || "").trim();
  const p = { nombres: v("f_nombres"), apellidos: v("f_apellidos"), cedula: v("f_cedula").replace(/[.\s]/g, ""), fechaNac: v("f_fechaNac"), sexo: v("f_sexo"), nacionalidad: v("f_nacionalidad"),
    departamento: v("f_departamento"), ciudad: v("f_ciudad"), direccion: v("f_direccion"), telefono: v("f_telefono"), institucion: v("f_institucion"), profesion: v("f_profesion"), cohorte: v("f_cohorte") };
  if (!p.nombres || !p.apellidos) return { error: "Completá tus nombres y apellidos." };
  if (!/^\d{4,10}$/.test(p.cedula)) return { error: "La cédula debe tener solo números (4 a 10 dígitos)." };
  if (!p.fechaNac || !p.sexo || !p.departamento || !p.ciudad) return { error: "Completá fecha de nacimiento, sexo, departamento y ciudad." };
  return { p };
}
const medidor = `<div class="muted" id="pwhint">Mínimo 8 caracteres, con letras y números.</div>`;

function vAcceso() {
  return `<div class="auth"><div class="brand-big"><span class="logo">VD</span><div><h1 style="margin:0">Aula virtual</h1><div class="muted">${esc(C.curso)} · MICD · FACET – UNC</div></div></div>${demoBanner()}
  <div class="card"><h2 style="margin-top:0">Ingresar</h2>
   <form id="lf"><label for="le">Correo electrónico</label><input type="email" id="le" required autocomplete="username"><label for="lp">Contraseña</label><input type="password" id="lp" required autocomplete="current-password">
   <div class="row" style="margin-top:1rem"><button class="btn" type="submit">Ingresar</button><button class="btn sec" type="button" id="gb">Ingresar con Google</button></div></form>
   <p style="margin:1rem 0 0"><a href="#" id="olv">¿Olvidaste tu contraseña?</a></p>
   <form id="rf" hidden style="margin-top:.6rem"><label for="re">Te enviaremos un enlace para restablecerla</label><input type="email" id="re" required placeholder="tu correo registrado"><div class="row" style="margin-top:.6rem"><button class="btn sec" type="submit">Enviar enlace</button></div></form><div id="rmsg" class="muted" role="status"></div></div>
  <div class="card"><b>¿Primera vez?</b> Creá tu cuenta con tus datos personales. <a class="btn" href="#/registro" style="margin-left:.5rem">Crear cuenta</a></div></div>`;
}
function bindAcceso() {
  $("#lf").addEventListener("submit", async e => { e.preventDefault(); const b = e.submitter; b.disabled = true;
    try { await B.ingresar($("#le").value.trim(), $("#lp").value); } catch (er) { aviso(msgError(er), "bad"); } b.disabled = false; });
  $("#gb").addEventListener("click", async () => { try { await B.ingresarGoogle(); } catch (er) { aviso(msgError(er), "bad"); } });
  $("#olv").addEventListener("click", e => { e.preventDefault(); $("#rf").hidden = !$("#rf").hidden; $("#re").value = $("#le").value; });
  $("#rf").addEventListener("submit", async e => { e.preventDefault();
    try { const r = await B.recuperar($("#re").value.trim()); $("#rmsg").textContent = r.demo || "Si el correo está registrado, te enviamos un enlace para restablecer tu contraseña. Revisá también la carpeta de spam."; }
    catch (er) { aviso(msgError(er), "bad"); } });
}

function vRegistro() {
  return `<div class="auth wide"><a href="#/acceso">← Volver a ingresar</a><h1>Crear cuenta · primer acceso</h1>${demoBanner()}
  <p class="sub">Completá tus datos una sola vez. Con tu correo y contraseña ingresarás a tu aula personal.</p>
  <form id="rg" class="card"><h2 style="margin-top:0">Datos personales</h2>${camposPerfil()}
   <h2>Cuenta de acceso</h2><div class="form-grid"><div><label for="f_email">Correo electrónico *</label><input type="email" id="f_email" required autocomplete="email"></div><div></div>
   <div><label for="f_clave">Contraseña *</label><input type="password" id="f_clave" required minlength="8" autocomplete="new-password">${medidor}</div>
   <div><label for="f_clave2">Repetir contraseña *</label><input type="password" id="f_clave2" required autocomplete="new-password"></div></div>
   <label class="chk"><input type="checkbox" id="f_ok" required> <span>${esc(CONSENT)}</span></label>
   <div class="row" style="margin-top:1rem"><button class="btn" type="submit">Crear mi cuenta</button><span class="muted" id="rgm"></span></div></form>
  <p class="muted">¿Preferís usar tu cuenta de Google? <a href="#" id="gb2">Continuar con Google</a> (luego completás tus datos).</p></div>`;
}
function bindRegistro() {
  $("#f_clave").addEventListener("input", e => { $("#pwhint").style.color = claveOk(e.target.value) ? "var(--ok)" : ""; });
  $("#gb2").addEventListener("click", async e => { e.preventDefault(); try { await B.ingresarGoogle(); } catch (er) { aviso(msgError(er), "bad"); } });
  $("#rg").addEventListener("submit", async e => { e.preventDefault();
    const r = leerPerfil(); if (r.error) return aviso(r.error, "bad");
    const email = $("#f_email").value.trim().toLowerCase(), c = $("#f_clave").value;
    if (!claveOk(c)) return aviso("La contraseña debe tener mínimo 8 caracteres, con letras y números.", "bad");
    if (c !== $("#f_clave2").value) return aviso("Las contraseñas no coinciden.", "bad");
    const b = e.submitter; b.disabled = true; ocupado = true; let u;
    try {
      u = await B.registrar(email, c);
      await B.guardarPerfil(u.uid, { ...r.p, email, consentimiento: { fecha: new Date().toISOString(), version: "v1" } }, true);
      aviso("¡Cuenta creada!");
    } catch (er) { aviso(msgError(er), "bad"); }
    ocupado = false; b.disabled = false; USER = B.actual(); await cargarSesion(); location.hash = "#/"; render();
  });
}

function vCompletar() {
  const nm = (USER.displayName || "").split(" ");
  return `<div class="auth wide"><h1>Completá tu registro</h1><p class="sub">Ingresaste como <b>${esc(USER.email)}</b>. Para continuar necesitamos tus datos personales (solo la primera vez).</p>${demoBanner()}
  <form id="cf" class="card">${camposPerfil({ nombres: nm.slice(0, -1).join(" ") || nm[0], apellidos: nm.length > 1 ? nm.slice(-1)[0] : "" })}
   <label class="chk"><input type="checkbox" id="f_ok" required> <span>${esc(CONSENT)}</span></label>
   <div class="row" style="margin-top:1rem"><button class="btn" type="submit">Guardar y entrar</button><button class="btn sec" type="button" id="out2">Salir</button></div></form></div>`;
}
function bindCompletar() {
  $("#out2").addEventListener("click", salir);
  $("#cf").addEventListener("submit", async e => { e.preventDefault(); const r = leerPerfil(); if (r.error) return aviso(r.error, "bad");
    const b = e.submitter; b.disabled = true;
    try { await B.guardarPerfil(USER.uid, { ...r.p, email: USER.email, consentimiento: { fecha: new Date().toISOString(), version: "v1" } }, true); await cargarSesion(); location.hash = "#/"; render(); }
    catch (er) { aviso(msgError(er), "bad"); b.disabled = false; } });
}

const necesitaVerificar = () => USER && USER.proveedor === "password" && !USER.emailVerified;
function vVerificar() {
  return `<div class="auth"><h1>Verificá tu correo</h1><div class="card"><p>Te enviamos un mensaje a <b>${esc(USER.email)}</b>. Hacé clic en el enlace y luego presioná el botón. Si no lo ves, revisá la carpeta de spam.</p>
  <div class="row"><button class="btn" id="vok">Ya verifiqué mi correo</button><button class="btn sec" id="vre">Reenviar correo</button><button class="btn sec" id="vout">Salir</button></div></div></div>`;
}
function bindVerificar() {
  $("#vok").addEventListener("click", async () => { try { USER = await B.recargar(); if (USER.emailVerified) { await cargarSesion(); render(); } else aviso("Todavía no figura como verificado.", "bad"); } catch (er) { aviso(msgError(er), "bad"); } });
  $("#vre").addEventListener("click", async () => { try { await B.reenviarVerificacion(); aviso("Correo reenviado."); } catch (er) { aviso(msgError(er), "bad"); } });
  $("#vout").addEventListener("click", salir);
}

const MOTIVOS = { ok: "Sos docente: se habilitó el Panel docente.", correo_no_verificado: "Tu correo no figura como verificado, y el rol docente lo exige.", no_figura_en_docentes: "No existe un documento en la colección «docentes» cuyo ID sea exactamente tu correo (en minúsculas, sin espacios).", };
const motivoTxt = m => MOTIVOS[m] || (m ? "No se pudo comprobar el rol (" + esc(m) + "). Revisá que las reglas de Firestore estén publicadas." : "");
function estadoCuenta() {
  return `<h2>Estado de la cuenta</h2><div class="card"><table><tbody>
   <tr><th>Correo</th><td><code>${esc(USER.email)}</code></td></tr>
   <tr><th>Correo verificado</th><td>${USER.emailVerified ? "Sí" : "No"}</td></tr>
   <tr><th>Rol</th><td><b>${ES_DOC ? "Docente" : "Estudiante"}</b></td></tr></tbody></table>
   ${ES_DOC ? "" : `<p class="muted" style="margin-bottom:0">¿Sos docente? ${motivoTxt(B.diag?.motivo)} Si lo acabás de crear, cerrá sesión y volvé a ingresar.</p>`}</div>`;
}
function vPerfil() {
  const p = PERFIL;
  if (p.virtual) return `<h1>Mi cuenta</h1><div class="card">Sesión docente: <b>${esc(USER.email)}</b>.<div class="row" style="margin-top:.8rem"><button class="btn sec" id="out3">Cerrar sesión</button></div></div>${estadoCuenta()}`;
  return `<h1>Mi perfil</h1><p class="sub">Tu cuenta: <b>${esc(USER.email)}</b> · ingreso con ${USER.proveedor === "google.com" ? "Google" : "correo y contraseña"}.</p>
  <form id="pf" class="card">${camposPerfil(p, true)}<p class="muted">La cédula no se puede modificar; si hay un error, pedí la corrección al docente.</p>
   <div class="row"><button class="btn" type="submit">Guardar cambios</button></div></form>
  ${USER.proveedor === "password" ? `<h2>Cambiar contraseña</h2><form id="cp" class="card"><div class="form-grid"><div><label for="p0">Contraseña actual</label><input type="password" id="p0" required autocomplete="current-password"></div><div></div>
   <div><label for="p1">Nueva contraseña</label><input type="password" id="p1" required minlength="8" autocomplete="new-password">${medidor}</div><div><label for="p2">Repetir nueva contraseña</label><input type="password" id="p2" required autocomplete="new-password"></div></div>
   <div class="row" style="margin-top:1rem"><button class="btn" type="submit">Cambiar contraseña</button></div></form>` : ""}
  ${estadoCuenta()}
  <h2>Sesión y datos</h2><div class="card row"><button class="btn sec" id="out3">Cerrar sesión</button><button class="btn sec" id="mydata">⬇ Descargar mis datos (JSON)</button></div>`;
}
function bindPerfil() {
  $("#out3")?.addEventListener("click", salir);
  $("#pf")?.addEventListener("submit", async e => { e.preventDefault(); const r = leerPerfil(); if (r.error) return aviso(r.error, "bad");
    try { const { cedula, ...resto } = r.p; await B.guardarPerfil(USER.uid, resto, false); await cargarSesion(); aviso("Perfil actualizado ✔"); render(); } catch (er) { aviso(msgError(er), "bad"); } });
  $("#p1")?.addEventListener("input", e => { $("#pwhint").style.color = claveOk(e.target.value) ? "var(--ok)" : ""; });
  $("#cp")?.addEventListener("submit", async e => { e.preventDefault(); const n = $("#p1").value;
    if (!claveOk(n)) return aviso("La nueva contraseña debe tener mínimo 8 caracteres, con letras y números.", "bad");
    if (n !== $("#p2").value) return aviso("Las contraseñas nuevas no coinciden.", "bad");
    try { await B.cambiarClave($("#p0").value, n); e.target.reset(); aviso("Contraseña actualizada ✔"); } catch (er) { aviso(msgError(er), "bad"); } });
  $("#mydata")?.addEventListener("click", () => descargar(`mis_datos_${slug(PERFIL.apellidos)}.json`, JSON.stringify({ cuenta: { email: USER.email }, perfil: PERFIL, progreso: { done: S.done, quiz: S.quiz, auto: S.auto }, calificaciones: S.oficial }, null, 1)));
}
async function salir() { flush(); await B.salir(); USER = null; PERFIL = null; ES_DOC = false; S = empty(); location.hash = "#/acceso"; render(); }

/* ---------- panel docente ---------- */
let ALUMNOS = [];
const GRADED = ACTS.filter(a => a.pts);
const timers = {};
function filaDoc(a) {
  const c = calcular(a.progreso.quiz, a.oficial), pg = progTotal({ done: a.progreso.done || {}, quiz: a.progreso.quiz || {} }), p = a.perfil;
  return `<tr data-u="${esc(a.uid)}" data-q="${esc((nombreCompleto(p) + " " + p.cedula + " " + p.email).toLowerCase())}"><td><b>${esc(nombreCompleto(p))}</b><div class="muted">C.I. ${esc(p.cedula)} · ${esc(p.email)}</div></td>
   <td>${Math.round(pg * 100)}%</td><td>${fmt(c.teoria)}</td>
   ${GRADED.map(g => `<td><input type="number" min="0" max="${g.pts}" step="0.5" data-u="${esc(a.uid)}" data-id="${g.id}" value="${a.oficial[g.id] ?? ""}" aria-label="${esc(nombreCompleto(p))} ${g.id}"></td>`).join("")}
   <td data-c="pr">${fmt(c.practica)}</td><td data-c="it">${fmt(c.integ)}</td><td data-c="tt"><b>${fmt(c.total)}</b></td><td data-c="es"><b>${c.escala}</b></td></tr>`;
}
async function vDocente() {
  if (!ES_DOC) return `<h1>Acceso restringido</h1><div class="card">Esta sección es solo para docentes. Si sos docente, pedí que agreguen tu correo verificado a la colección <code>docentes</code>.</div>`;
  try { ALUMNOS = await B.listarAlumnos(); } catch (e) { return `<h1>Panel docente</h1><div class="card note">No se pudieron leer los datos: ${esc(msgError(e))}</div>`; }
  ALUMNOS.sort((x, y) => (x.perfil.apellidos || "").localeCompare(y.perfil.apellidos || "", "es"));
  return `<h1>Panel docente</h1><p class="sub">${ALUMNOS.length} estudiante(s) registrados. Las notas que cargues se guardan al instante y el estudiante las ve en su aula.</p>${demoBanner()}
  <div class="card"><div class="row"><input type="text" id="dq" placeholder="Buscar por nombre, cédula o correo…" style="max-width:360px" aria-label="Buscar estudiante"><button class="btn" id="csv" ${ALUMNOS.length ? "" : "disabled"}>⬇ Exportar planilla (CSV)</button></div></div>
  ${ALUMNOS.length ? `<div class="card tw"><table><thead><tr><th>Estudiante</th><th>Avance</th><th>Teoría/30</th>${GRADED.map(g => `<th title="${esc(g.titulo)}">${g.id.replace("s", "S").replace("_", " ")}<br>/${g.pts}</th>`).join("")}<th>Práct./50</th><th>Integr./20</th><th>Total</th><th>Esc.</th></tr></thead><tbody>${ALUMNOS.map(filaDoc).join("")}</tbody></table>
  <p class="muted">Escala sugerida: 1 (&lt;60) · 2 (60-69) · 3 (70-80) · 4 (81-90) · 5 (≥91). Ajustar al reglamento vigente. Práctica incluye hasta +3 por el ejercicio opcional de redes (tope 50).</p></div>` : `<div class="card muted">Aún no hay estudiantes registrados.</div>`}`;
}
function bindDocente() {
  $("#dq")?.addEventListener("input", e => { const q = e.target.value.toLowerCase(); $$("tbody tr").forEach(tr => tr.hidden = !tr.dataset.q.includes(q)); });
  $$("input[data-id]").forEach(inp => inp.addEventListener("input", () => {
    const u = inp.dataset.u, id = inp.dataset.id, g = actById(id), a = ALUMNOS.find(x => x.uid === u);
    if (inp.value === "") delete a.oficial[id]; else a.oficial[id] = Math.max(0, Math.min(g.pts, +inp.value));
    const c = calcular(a.progreso.quiz, a.oficial), tr = inp.closest("tr");
    tr.querySelector("[data-c=pr]").textContent = fmt(c.practica); tr.querySelector("[data-c=it]").textContent = fmt(c.integ);
    tr.querySelector("[data-c=tt]").innerHTML = `<b>${fmt(c.total)}</b>`; tr.querySelector("[data-c=es]").innerHTML = `<b>${c.escala}</b>`;
    clearTimeout(timers[u]); timers[u] = setTimeout(() => B.guardarCalificaciones(u, a.oficial).then(() => aviso("Nota guardada ✔")).catch(e => aviso(msgError(e), "bad")), 700);
  }));
  $("#csv")?.addEventListener("click", () => {
    const qs = Object.keys(D.quizzes), head = ["apellidos", "nombres", "cedula", "fecha_nacimiento", "sexo", "departamento", "ciudad", "telefono", "email", "cohorte", "avance_%", ...qs.map(n => "quiz" + n + "_%"), "teoria_30", ...GRADED.map(g => g.id), "practica_50", "integrador_20", "total_100", "escala"];
    const rows = ALUMNOS.map(a => { const p = a.perfil, q = a.progreso.quiz || {}, c = calcular(q, a.oficial);
      return [p.apellidos, p.nombres, p.cedula, p.fechaNac, p.sexo, p.departamento, p.ciudad, p.telefono, p.email, p.cohorte, Math.round(progTotal({ done: a.progreso.done || {}, quiz: q }) * 100), ...qs.map(n => q[n]?.mejor ?? ""), fmt(c.teoria, 2), ...GRADED.map(g => a.oficial[g.id] ?? ""), fmt(c.practica, 2), fmt(c.integ, 2), fmt(c.total, 2), c.escala]; });
    descargar("calificaciones_curso.csv", "﻿" + [head, ...rows].map(r => r.map(x => `"${String(x ?? "").replace(/"/g, '""')}"`).join(",")).join("\n"), "text/csv");
  });
}

/* ---------- sesión y router ---------- */
async function cargarSesion() {
  PERFIL = null; ES_DOC = false; S = empty();
  if (!USER) return;
  try {
    ES_DOC = await B.esDocente(USER);
    PERFIL = await B.cargarPerfil(USER.uid);
    if (PERFIL) {
      const pr = (await B.cargarProgreso(USER.uid)) || {}, of = (await B.cargarCalificaciones(USER.uid)) || {};
      S = { perfil: { ...PERFIL, nombre: nombreCompleto(PERFIL), doc: PERFIL.cedula }, done: pr.done || {}, quiz: pr.quiz || {}, auto: pr.auto || {}, oficial: of };
    } else if (ES_DOC) PERFIL = { nombres: USER.displayName || USER.email, apellidos: "", cedula: "", virtual: true };
  } catch (e) { aviso(msgError(e), "bad"); }
}
async function refrescarNotas() { if (USER && PERFIL && !PERFIL.virtual) { try { S.oficial = (await B.cargarCalificaciones(USER.uid)) || {}; } catch {} } }
let renderTk = 0;
async function render() {
  const tk = ++renderTk, ruta = (location.hash.replace(/^#/, "") || "/"), [, a, b] = ruta.split("/"), n = +b;
  let html, bind = () => {}, crumb = "Inicio", guest = false;
  if (!USER) { guest = true; if (a === "registro") { html = vRegistro(); bind = bindRegistro; crumb = "Crear cuenta"; } else { html = vAcceso(); bind = bindAcceso; crumb = "Ingresar"; } }
  else if (necesitaVerificar()) { guest = true; html = vVerificar(); bind = bindVerificar; crumb = "Verificar correo"; }
  else if (!PERFIL) { guest = true; html = vCompletar(); bind = bindCompletar; crumb = "Completar registro"; }
  else {
    if (a === "acceso" || a === "registro") { location.hash = "#/"; return; }
    switch (a) {
      case "sesion": html = vSesion(n); crumb = `Módulo ${n}`; bind = bindSesion; break;
      case "quiz": html = vQuiz(n); crumb = `Módulo ${n} › Quiz`; bind = () => bindQuiz(n); break;
      case "notas": await refrescarNotas(); html = vNotas(); crumb = "Mis notas"; break;
      case "recursos": html = vRecursos(); crumb = "Recursos"; bind = bindRecursos; break;
      case "perfil": html = vPerfil(); crumb = "Mi perfil"; bind = bindPerfil; break;
      case "docente": html = await vDocente(); crumb = "Panel docente"; bind = bindDocente; break;
      default: await refrescarNotas(); html = vInicio();
    }
  }
  if (tk !== renderTk) return;
  document.body.classList.toggle("guest", guest);
  $("#main").innerHTML = html; $("#crumb").textContent = `${C.curso} › ${crumb}`;
  if (!guest) navHtml("/" + [a, b].filter(Boolean).join("/")); else $("#user").textContent = "";
  $("#logout").hidden = !USER; bind();
  document.title = `${crumb} · Aula virtual · Visualización de Datos UNC`;
  $("#side").classList.remove("open"); $("#menu").setAttribute("aria-expanded", "false");
}
function bindSesion() {
  $$("[data-act]").forEach(c => c.addEventListener("change", () => { S.done[c.dataset.act] = c.checked; if (!c.checked) delete S.done[c.dataset.act]; persist(); navHtml(location.hash.replace(/^#/, "")); }));
  $$("[data-auto]").forEach(sl => sl.addEventListener("change", () => {
    const id = sl.dataset.auto; S.auto[id] = S.auto[id] || {}; S.auto[id][sl.dataset.i] = +sl.value; persist();
    const a = actById(id), ap = autoPct(S.auto, a);
    $("#ap_" + id).innerHTML = `Autoestimación: <b>${fmt(ap * a.pts)}/${a.pts}</b> pts (${fmt(ap * 100, 0)}%) — referencial; la nota oficial la asigna el docente.`;
  }));
}
addEventListener("hashchange", () => { if (!location.hash.startsWith("#/quiz/")) Object.keys(QZ).forEach(k => delete QZ[k]); render(); window.scrollTo(0, 0); });
$("#menu").addEventListener("click", () => { const o = $("#side").classList.toggle("open"); $("#menu").setAttribute("aria-expanded", o); });
$("#logout").addEventListener("click", salir);
$("#lnk-drive").href = drive(C.drive.raiz);

/* ---------- arranque ---------- */
B = await crearBackend(C);
await B.listo;
USER = B.actual(); await cargarSesion(); render();
B.onAuth(async u => { if (ocupado || (u?.uid === USER?.uid && u?.uid)) return; USER = u; await cargarSesion(); render(); });
window.__aula = { get usuario() { return USER; }, modo: B.modo };
})();
