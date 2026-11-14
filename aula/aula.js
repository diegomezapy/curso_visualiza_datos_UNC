/* Aula virtual · Visualización de Datos (FACET-UNC).
   Autenticación y datos: Firebase (Auth + Firestore) o modo demo local (ver backend.js). */
import { crearBackend, msgError } from "./backend.js";
import { heroHtml, afterRender, initFx } from "./fx.js";
import { csvPlanilla, planillaRegistros, planillaQuizzes, planillaAutoevaluaciones } from "./planillas.mjs";
(async () => {
"use strict";
const D = window.CURSO, C = D.config;

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
const empty = () => ({ perfil: {}, done: {}, quiz: {}, auto: {}, oficial: {}, enlaces: {} });
let S = empty(), USER = null, PERFIL = null, ES_DOC = false, ocupado = false, B;
let tmr;
const persist = () => { if (!USER || !PERFIL || PERFIL.virtual) return; clearTimeout(tmr); tmr = setTimeout(flush, 500); };
const flush = () => { clearTimeout(tmr); if (USER && PERFIL && !PERFIL.virtual) B.guardarProgreso(USER.uid, { done: S.done, quiz: S.quiz, auto: S.auto, enlaces: S.enlaces }).catch(e => aviso(msgError(e), "bad")); };
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
  let h = it("/", "🏠 Inicio") + it("/calendario", "📅 Calendario") + it("/clases", "🎥 Clases grabadas") + it("/datos", "🗺️ Datos abiertos") + it("/tutor", "👤 El tutor") + it("/notas", "📊 Mis notas") + it("/recursos", "📚 Recursos") + `<div class="grp">Módulos</div>`;
  D.sesiones.forEach(s => { const p = progSes(s); h += it(`/sesion/${s.n}`, `${s.n}. ${esc(s.corto)}`, `<span class="dot">${p.pct >= 1 ? "✅" : Math.round(p.pct * 100) + "%"}</span>`); });
  h += `<div class="grp">Cuenta</div>` + it("/perfil", "👤 Mi perfil") + (ES_DOC ? it("/docente", "🧑‍🏫 Panel docente") : "");
  $("#nav").innerHTML = h;
  $("#user").textContent = PERFIL ? (PERFIL.nombres || "").split(" ")[0] : "Ingresar";
}

/* ---------- vistas ---------- */
function proximosHtml() {
  if (!AGENDA || !AGENDA.eventos?.length) return "";
  const ev = AGENDA.eventos.filter(e => new Date(e.fin_iso) >= new Date()).slice(0, 3); if (!ev.length) return "";
  return `<h2>📅 Próximos eventos</h2><div class="card"><ul class="res">${ev.map(e => { const t = TIPO_EV[e.tipo] || TIPO_EV.otro; return `<li><span class="ico">${t[0]}</span><span><a href="#/calendario/${encodeURIComponent(e.id)}"><b>${esc(e.titulo)}</b></a><br><span class="muted">${esc(fmtF(e))} · ${esc(e.inicio)}–${esc(e.fin)}</span></span></li>`; }).join("")}</ul><a href="#/calendario">Ver el calendario completo →</a></div>`;
}
function vInicio() {
  const reg = PERFIL?.nombres;
  const sig = D.sesiones.find(s => progSes(s).pct < 1);
  const c = calcular(S.quiz, S.oficial);
  return `${heroHtml(progTotal(), esc((reg || "").split(" ")[0]))}
  <p class="sub">${esc(C.curso)} · ${esc(C.programa)} · ${esc(C.semestre)}</p>
  <div class="kpis">
    <div class="card"><div class="muted">Avance del curso</div><div class="big">${Math.round(progTotal() * 100)}%</div>${bar(progTotal())}</div>
    <div class="card"><div class="muted">Teoría (quizzes) / 30</div><div class="big">${fmt(c.teoria)}</div><div class="muted">mejores 6 quizzes</div></div>
    <div class="card"><div class="muted">Nota provisoria / 100</div><div class="big">${fmt(c.total)}</div><div class="muted">escala sugerida: ${c.escala}</div></div>
  </div>
  ${sig ? `<h2>Próximo paso</h2><a class="card link" href="#/sesion/${sig.n}"><span class="tag">Módulo ${sig.n}</span><h3>${esc(sig.titulo)}</h3><p class="muted" style="margin:.3rem 0 0">${esc(sig.resumen)}</p></a>` : `<div class="card"><b>¡Completaste todos los módulos!</b> Descargá tu reporte en <a href="#/notas">Mis notas</a>.</div>`}
  ${proximosHtml()}
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

const ytUrl = v => v.tipo === "playlist" ? `https://www.youtube.com/playlist?list=${v.id}` : `https://www.youtube.com/watch?v=${v.id}`;
const LEC_ICO = { pdf: "📄", libro: "📘", "artículo": "🧾", web: "🔗", datos: "🗂" };
const RE_ENL = { rpubs: /^https:\/\/(www\.)?rpubs\.com\/.+/i, colab: /^https:\/\/(colab\.research\.google\.com|drive\.google\.com|colab\.google)\/.+/i };
const ENL_TXT = { rpubs: ["📊 Enlace de tu publicación en RPubs", "https://rpubs.com/tu_usuario/titulo"], colab: ["🐍 Enlace de tu Colab (compartido: cualquiera con el enlace, Lector)", "https://colab.research.google.com/drive/..."] };
function videosHtml(s) {
  if (!s.videos?.length) return "";
  const vistos = s.videos.filter(v => S.done["vid_" + v.id]).length;
  return `<h2>🎬 Videos <span class="muted" style="font-weight:400;font-size:.9rem">· vistos ${vistos}/${s.videos.length}</span></h2>
  <p class="muted" style="margin-top:0">Selección en español. Marcá los que ya viste. Si alguno no se reproduce acá, usá “Abrir en YouTube”.</p>
  <div class="vgrid">${s.videos.map(v => `<div class="vcard"><div class="vbox" id="vb_${v.id}"><button class="vthumb ${v.tipo === "playlist" ? "pl" : ""}" data-play="${v.id}" data-tipo="${v.tipo}" data-t="${esc(v.t)}" aria-label="Reproducir: ${esc(v.t)}" ${v.tipo === "playlist" ? "" : `style="background-image:url(https://i.ytimg.com/vi/${v.id}/hqdefault.jpg)"`}><span>${v.tipo === "playlist" ? "▶ Lista de reproducción" : "▶"}</span></button></div>
   <div class="vinfo"><b>${esc(v.t)}</b>${v.nota ? `<div class="muted">${esc(v.nota)}</div>` : ""}
   <div class="row" style="justify-content:space-between;margin-top:.3rem"><label class="chk2"><input type="checkbox" data-vis="${v.id}" ${S.done["vid_" + v.id] ? "checked" : ""}> Visto</label><a target="_blank" rel="noopener" href="${ytUrl(v)}">Abrir en YouTube ↗</a></div></div></div>`).join("")}</div>`;
}
function lecturasHtml(s) {
  if (!s.lecturas?.length) return "";
  return `<h2>📚 Lecturas y documentos</h2><div class="card"><ul class="res">${s.lecturas.map(l => `<li><span class="ico">${LEC_ICO[l.tipo] || "🔗"}</span><span><a target="_blank" rel="noopener" href="${esc(l.u)}">${esc(l.t)}</a> <span class="tag">${esc(l.idioma)}</span>${l.nota ? ` <span class="muted">· ${esc(l.nota)}</span>` : ""}</span></li>`).join("")}</ul></div>`;
}
function enlacesHtml(a) {
  if (!a.ent?.length) return "";
  const e = S.enlaces[a.id] || {};
  return `<div style="margin-top:.6rem"><b style="font-size:.9rem">Entrega por enlace</b>${a.ent.map(t => `<label for="enl_${a.id}_${t}" style="font-weight:400">${ENL_TXT[t][0]} ${e[t] ? "✅" : ""}</label><input type="url" id="enl_${a.id}_${t}" data-enl="${a.id}" data-t="${t}" placeholder="${ENL_TXT[t][1]}" value="${esc(e[t] || "")}">`).join("")}
  <p class="muted" style="margin:.3rem 0 0">Al guardar todos los enlaces requeridos, la actividad se marca como entregada. Recordá: RPubs es público (sin datos personales).</p></div>`;
}
function rutaDatosHtml(s) {
  if (s.n !== 1) return "";
  const dg = C.diagnostico || {}, tablero = dg.tablero_url || "../diagnostico/tablero.html", looker = dg.looker_url || "", embed = dg.looker_embed || "";
  const colab = (s.recursos.find(r => r.k === "colab" && /lab00/.test(r.u)) || {}).u, rmd = (s.recursos.find(r => r.k === "rmd" && /00_diagnostico/.test(r.u)) || {}).u;
  const via = (ico, t, d, a) => `<div class="card" style="margin:0"><div style="font-size:1.6rem">${ico}</div><h3>${t}</h3><p class="muted" style="margin:.2rem 0 .6rem">${d}</p>${a}</div>`;
  return `<h2>📈 Del dato a la visualización: cuatro vías para los mismos datos</h2>
  <p class="muted" style="margin-top:0">Después del <b>diagnóstico</b>, los datos viajan: <b>cuestionario → Google Apps Script → hoja de Google Sheets</b>, y de ahí salen cuatro formas de mostrarlos. Elegí la que mejor sirve a tu audiencia.</p>
  <div class="grid">
   ${via("⚡", "Tablero en vivo", "Apps Script · se actualiza con cada respuesta, con filtros interactivos.", `<a class="btn" target="_blank" rel="noopener" href="${esc(tablero)}">Abrir el tablero</a>`)}
   ${via("📊", "Looker Studio", "Informe de Google conectado a la misma hoja (arrastrar y soltar).", looker ? `<a class="btn" target="_blank" rel="noopener" href="${esc(looker)}">Abrir en Looker Studio</a>` : `<span class="muted">El docente publicará el enlace aquí.</span>`)}
   ${via("📘", "R → RPubs", "Informe reproducible en R Markdown, publicado como página web.", rmd ? `<a class="btn" target="_blank" rel="noopener" href="${esc(rmd)}">Abrir el .Rmd</a>` : "")}
   ${via("🐍", "Python → Colab", "Notebook con matplotlib y plotly; compartís el enlace.", colab ? `<a class="btn" target="_blank" rel="noopener" href="${esc(colab)}">Abrir en Colab</a>` : "")}
  </div>
  ${embed ? `<details style="margin-top:.8rem"><summary><b>Ver el informe de Looker Studio aquí mismo</b></summary><iframe src="${esc(embed)}" style="width:100%;height:600px;border:1px solid var(--bd);border-radius:8px;margin-top:.5rem" loading="lazy" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups"></iframe></details>` : ""}`;
}
function vSesion(n) {
  const s = D.sesiones.find(x => x.n === n); if (!s) return vInicio();
  const p = progSes(s), prev = D.sesiones.find(x => x.n === n - 1), next = D.sesiones.find(x => x.n === n + 1);
  const ico = { guia: "📖", colab: "🐍", codigo: "💻", drive: "📁", pdf: "📄", rmd: "📊", descarga: "⬇️" };
  const q = S.quiz[n];
  const entregaNombre = id => `S${n}_${id}_${`${slug(PERFIL.apellidos)}_${slug(PERFIL.nombres)}`}`;
  return `<span class="tag">${s.unidad} · Sesión ${s.n}</span>${s.n === 8 ? ' <span class="tag warn">Redes opcional</span>' : ""}
  <h1>${esc(s.titulo)}</h1><p class="sub">${esc(s.resumen)}${C.fechas?.[n] ? " · <b>" + esc(C.fechas[n]) + "</b>" : ""}</p>
  ${bar(p.pct, p.pct >= 1 ? "ok" : "")}<span class="muted">${p.done}/${p.items} completado</span>
  <h2>🎯 Objetivos</h2><div class="card"><ul style="margin:0;padding-left:1.2rem">${s.objetivos.map(o => `<li>${esc(o)}</li>`).join("")}</ul></div>
  <p><a class="btn sm" href="#/clases/s${n}">🎥 Ver clases grabadas de esta sesión</a></p>
  <h2>🧰 Materiales de la sesión</h2><div class="card"><ul class="res">${s.recursos.map(r => `<li><span class="ico">${ico[r.k] || "🔗"}</span>${r.u ? `<a href="${esc(r.u)}" target="${r.k === "guia" ? "_self" : "_blank"}" rel="noopener">${esc(r.t)}</a>` : esc(r.t)}</li>`).join("")}</ul>
   <p class="muted" style="margin:.5rem 0 0">🐍 <b>Python</b> en Colab (<i>Entorno de ejecución → Ejecutar todas</i>) · 📊 <b>R</b> en RStudio: abrí el .Rmd, presioná <i>Knit</i> y publicá con <i>Publish → RPubs</i>. Datasets en <a href="#/recursos">Recursos</a>; guía en <a href="../materiales/pdf/00_guia_inicio.pdf" target="_blank">Guía de inicio (PDF)</a>.</p></div>
  ${videosHtml(s)}${lecturasHtml(s)}
  <h2>✅ Actividades y entregas</h2>
  ${s.actividades.map(a => { const r = D.rubricas[a.rubrica]; const ap = autoPct(S.auto, a); return `<div class="card"><div class="act">
    <input type="checkbox" id="chk_${a.id}" data-act="${a.id}" ${S.done[a.id] ? "checked" : ""} aria-label="Marcar como hecha">
    <div style="flex:1"><label for="chk_${a.id}" style="margin:0;font-weight:600">${esc(a.titulo)}</label>
    <div class="row" style="margin-top:.3rem">${a.pts ? `<span class="tag">${a.pts} pts</span>` : '<span class="tag warn">Hito sin nota</span>'}${a.rubrica ? `<span class="tag">Rúbrica ${a.rubrica}</span>` : ""}${(S.oficial[a.id] ?? "") !== "" ? `<span class="tag ok">Nota oficial: ${fmt(+S.oficial[a.id])}/${a.pts}</span>` : ""}</div>
    ${a.accion ? `<p style="margin:.6rem 0 0"><a class="btn" target="_blank" rel="noopener" href="${esc(a.accion.u)}">${esc(a.accion.t)} →</a></p>` : ""}
    ${a.entrega ? `<details style="margin-top:.6rem"><summary>Cómo entregar</summary><div style="padding:.4rem 0">
      <p style="margin:.3rem 0">Si entregás un archivo, nombralo: <code>${esc(entregaNombre(a.id))}.ext</code></p>
      <div class="row"><a class="btn sec" target="_blank" rel="noopener" href="${drive(C.drive.entregas)}">📁 Abrir carpeta de entregas (Drive)</a>
      ${C.formulario_entregas ? `<a class="btn" target="_blank" rel="noopener" href="${esc(C.formulario_entregas)}">📝 Entregar por formulario</a>` : ""}</div></div></details>` : ""}
    ${enlacesHtml(a)}
    ${r ? `<details style="margin-top:.4rem"><summary>Autoevaluación con rúbrica (${esc(r.titulo)})</summary><div style="padding:.5rem 0">
      <div class="tw"><table><thead><tr><th>Criterio</th><th>Peso</th><th>Tu nivel</th></tr></thead><tbody>${r.criterios.map((c, i) => `<tr><td>${esc(c.n)}</td><td>${c.w}%</td><td><select data-auto="${a.id}" data-i="${i}" aria-label="${esc(c.n)}"><option value="0">–</option>${[1, 2, 3, 4].map(v => `<option value="${v}" ${S.auto[a.id]?.[i] == v ? "selected" : ""}>${v} · ${LVL[v]}</option>`).join("")}</select></td></tr>`).join("")}</tbody></table></div>
      <p class="muted" id="ap_${a.id}" style="margin:.4rem 0 0">${ap == null ? "Completá los niveles para ver tu autoestimación." : `Autoestimación: <b>${fmt(ap * a.pts)}/${a.pts}</b> pts (${fmt(ap * 100, 0)}%) — referencial; la nota oficial la asigna el docente.`}</p></div></details>` : ""}
    </div></div></div>`; }).join("")}
  ${rutaDatosHtml(s)}
  ${(s.practicas_reales || []).length ? `<h2>🗺️ Práctica con datos reales</h2><div class="card">${s.practicas_reales.map(p => `<div class="row" style="justify-content:space-between;padding:.35rem 0;border-bottom:1px solid var(--bd)"><span><b>${esc(p.nombre)}</b><br><span class="muted">${esc(p.desc)}</span></span><span class="row"><a class="btn sec sm" target="_blank" rel="noopener" href="${esc(p.colab)}">🐍 Colab</a>${p.rmd ? `<a class="btn sec sm" target="_blank" rel="noopener" href="${esc(p.rmd)}">📊 R → RPubs</a>` : ""}</span></div>`).join("")}<p class="muted" style="margin:.5rem 0 0">Fuentes, estado y cuidados en <a href="#/datos">Datos abiertos</a>. Citá siempre la fuente y no publiques datos personales.</p></div>` : ""}
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
  f.addEventListener("submit", async e => {
    e.preventDefault();
    z.preguntas.forEach((_, i) => { const r = f.querySelector(`input[name=q${i}]:checked`); if (r) z.resp[i] = +r.value; });
    if (Object.keys(z.resp).length < z.preguntas.length) { $("#qmsg").textContent = `Faltan ${z.preguntas.length - Object.keys(z.resp).length} pregunta(s) por responder.`; return; }
    const ok = z.preguntas.filter((p, i) => p.ops[z.resp[i]].ok).length, pct = Math.round(ok / z.preguntas.length * 100);
    const intento = { id: crypto.randomUUID(), sesion: n, quizTitulo: D.quizzes[n].titulo, fecha: new Date().toISOString(), pct,
      respuestas: z.preguntas.map((p, i) => ({ pregunta: p.q, respuesta: p.ops[z.resp[i]].t, correcta: p.ops.find(o => o.ok).t, acierto: p.ops[z.resp[i]].ok })) };
    const boton = $("#send"); boton.disabled = true; $("#qmsg").textContent = "Guardando respuestas…";
    try { await B.guardarIntentoQuiz(USER.uid, intento); }
    catch (er) { boton.disabled = false; $("#qmsg").textContent = `No se guardaron las respuestas: ${msgError(er)}. Volvé a intentar.`; return; }
    const q = S.quiz[n] || { mejor: 0, intentos: [] };
    q.intentos.push({ id: intento.id, t: intento.fecha, pct }); q.mejor = Math.max(q.mejor, pct); S.quiz[n] = q; persist();
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
  <h2>📄 Fichas y hojas de referencia (PDF)</h2><div class="card"><ul class="res">
   ${D.materiales.map(([f, t]) => `<li><span class="ico">📄</span><a target="_blank" href="../materiales/pdf/${f}.pdf">${esc(t)}</a></li>`).join("")}
   ${D.sesiones.map(s => `<li><span class="ico">${s.n}</span><a target="_blank" href="../materiales/pdf/${["ficha_01_percepcion", "ficha_02_eleccion", "ficha_03_color_etica", "ficha_04_kpis_storytelling", "ficha_05_dashboards", "ficha_06_reporting", "ficha_07_complejas", "ficha_08_redes"][s.n - 1]}.pdf">Ficha de estudio · Sesión ${s.n}: ${esc(s.corto)}</a></li>`).join("")}</ul></div>
  <h2>🗃 Datasets (descarga directa)</h2><div class="card tw"><table><tbody>${D.datasets.map(([f, d]) => `<tr><td><a href="${C.raw}/datos/${f}" download>${f}</a></td><td class="muted">${esc(d)}</td></tr>`).join("")}</tbody></table><p class="muted">Sintéticos y reproducibles (<code>datos/generar_datos.py</code>). Para mini-proyectos e integrador usá datos reales (datos.gov.py, INE, BCP, Our World in Data).</p></div>
  <h2>📜 Documentos</h2><div class="card"><ul class="res">
   ${[["programa", "Programa de estudios"], ["cronograma", "Cronograma"], ["evaluacion", "Evaluación"], ["rubricas", "Rúbricas"], ["proyecto_integrador", "Proyecto integrador"], ["bibliografia", "Bibliografía y fuentes de datos"], ["banco_quizzes", "Banco de quizzes (con respuestas)"]].map(([f, t]) => `<li><span class="ico">📄</span><a href="../docs/${f}.html">${t}</a></li>`).join("")}</ul></div>
  <h2>⚙️ Entorno local (opcional)</h2><div class="card"><p style="margin-top:0">Podés trabajar sin instalar nada con Colab. Para trabajar en tu equipo:</p><pre style="overflow:auto;background:var(--bg);padding:.8rem;border-radius:8px"><code>git clone ${esc(C.repo)}.git
cd curso_visualiza_datos_UNC
python -m venv .venv &amp;&amp; source .venv/bin/activate
pip install -r requirements.txt
python tools/py2nb.py &amp;&amp; jupyter lab
# R: abrir r/01_percepcion.Rmd en RStudio y ejecutar antes r/instalar_paquetes.R</code></pre></div>
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
  $("#mydata")?.addEventListener("click", () => descargar(`mis_datos_${slug(PERFIL.apellidos)}.json`, JSON.stringify({ cuenta: { email: USER.email }, perfil: PERFIL, progreso: { done: S.done, quiz: S.quiz, auto: S.auto, enlaces: S.enlaces }, calificaciones: S.oficial }, null, 1)));
}
async function salir() { flush(); await B.salir(); USER = null; PERFIL = null; ES_DOC = false; S = empty(); location.hash = "#/acceso"; render(); }

/* ---------- panel docente ---------- */
let ALUMNOS = [], INTENTOS = [], PLANILLAS = {}, ERROR_INTENTOS = "";
const GRADED = ACTS.filter(a => a.pts);
const timers = {};
function chipsEnlaces(enl) {
  const items = Object.entries(enl || {}).flatMap(([id, o]) => Object.entries(o || {}).map(([t, u]) => ({ id, t, u }))).filter(x => /^https:\/\//.test(x.u));
  if (!items.length) return "";
  return `<div class="chips">${items.map(x => `<a target="_blank" rel="noopener noreferrer" href="${esc(x.u)}" title="${esc(x.u)}">S${actById(x.id)?.n ?? "?"}${x.id.includes("mp") ? " MP" + x.id.match(/mp(\d)/)[1] : ""} ${x.t === "rpubs" ? "📊" : "🐍"}</a>`).join("")}</div>`;
}
function filaDoc(a) {
  const c = calcular(a.progreso.quiz, a.oficial), pg = progTotal({ done: a.progreso.done || {}, quiz: a.progreso.quiz || {} }), p = a.perfil;
  return `<tr data-u="${esc(a.uid)}" data-q="${esc((nombreCompleto(p) + " " + p.cedula + " " + p.email).toLowerCase())}"><td><b>${esc(nombreCompleto(p))}</b><div class="muted">C.I. ${esc(p.cedula)} · ${esc(p.email)}</div>${chipsEnlaces(a.progreso.enlaces)}</td>
   <td>${Math.round(pg * 100)}%</td><td>${fmt(c.teoria)}</td>
   ${GRADED.map(g => `<td><input type="number" min="0" max="${g.pts}" step="0.5" data-u="${esc(a.uid)}" data-id="${g.id}" value="${a.oficial[g.id] ?? ""}" aria-label="${esc(nombreCompleto(p))} ${g.id}"></td>`).join("")}
   <td data-c="pr">${fmt(c.practica)}</td><td data-c="it">${fmt(c.integ)}</td><td data-c="tt"><b>${fmt(c.total)}</b></td><td data-c="es"><b>${c.escala}</b></td></tr>`;
}
async function vDocente() {
  if (!ES_DOC) return `<h1>Acceso restringido</h1><div class="card">Esta sección es solo para docentes. Si sos docente, pedí que agreguen tu correo verificado a la colección <code>docentes</code>.</div>`;
  try { ALUMNOS = await B.listarAlumnos(); } catch (e) { return `<h1>Panel docente</h1><div class="card note">No se pudieron leer los datos: ${esc(msgError(e))}</div>`; }
  const [rIntentos, rPlanillas] = await Promise.allSettled([B.listarIntentosQuiz(), B.cargarPlanillasDocente(USER.email)]);
  INTENTOS = rIntentos.status === "fulfilled" ? rIntentos.value : [];
  ERROR_INTENTOS = rIntentos.status === "rejected" ? msgError(rIntentos.reason) : "";
  PLANILLAS = rPlanillas.status === "fulfilled" ? rPlanillas.value?.planillas || {} : {};
  ALUMNOS.sort((x, y) => (x.perfil.apellidos || "").localeCompare(y.perfil.apellidos || "", "es"));
  const hayQuiz = INTENTOS.length || ALUMNOS.some(a => Object.values(a.progreso.quiz || {}).some(q => q.intentos?.length));
  const hayAuto = ALUMNOS.some(a => Object.keys(a.progreso.auto || {}).length);
  const links = [["diagnostico", "Diagnóstico inicial"], ["agenda", "Asistencia y mini evaluaciones"], ["entregas", "Otros formularios"]];
  const enlaceSeguro = u => /^https:\/\/docs\.google\.com\/spreadsheets\/d\/[\w-]+(?:\/|$)/.test(u || "");
  return `<h1>Panel docente</h1><p class="sub">${ALUMNOS.length} estudiante(s) registrados. Las notas que cargues se guardan al instante y el estudiante las ve en su aula.</p>${demoBanner()}
  <h2>Planillas del aula</h2><div class="card"><div class="row">
    <button type="button" class="btn" id="csvRegistro" ${ALUMNOS.length ? "" : "disabled"}>⬇ Registro de usuarios</button>
    <button type="button" class="btn" id="csvRespuestas" ${hayQuiz && !ERROR_INTENTOS ? "" : "disabled"}>⬇ Respuestas de quizzes</button>
    <button type="button" class="btn" id="csvAuto" ${hayAuto ? "" : "disabled"}>⬇ Autoevaluaciones</button>
    <button type="button" class="btn sec" id="csv" ${ALUMNOS.length ? "" : "disabled"}>⬇ Calificaciones</button></div>
    <p class="muted" style="margin-bottom:0">Los quizzes de práctica nuevos incluyen cada respuesta. Los intentos anteriores conservan solo fecha y puntaje. Las evaluaciones formales y sus respuestas se administran en Moodle.</p>
    ${ERROR_INTENTOS ? `<p class="note">No se pudieron leer los intentos de quizzes: ${esc(ERROR_INTENTOS)}</p>` : ""}</div>
  <h2>Hojas externas del curso</h2><div class="card"><ul class="res">${links.map(([clave, titulo]) => `<li>${enlaceSeguro(PLANILLAS[clave]) ? `<a href="${esc(PLANILLAS[clave])}" target="_blank" rel="noopener noreferrer">${titulo} ↗</a>` : `${titulo}: <span class="muted">hoja no configurada</span>`}</li>`).join("")}</ul><p class="muted">Estas hojas se abren con los permisos de tu cuenta de Google. Sus enlaces se guardan en tu documento privado de docente en Firebase.</p></div>
  <div class="card"><input type="text" id="dq" placeholder="Buscar por nombre, cédula o correo…" style="max-width:360px" aria-label="Buscar estudiante"></div>
  ${ALUMNOS.length ? `<div class="card tw"><table><thead><tr><th>Estudiante</th><th>Avance</th><th>Teoría/30</th>${GRADED.map(g => `<th title="${esc(g.titulo)}">${g.id.replace("s", "S").replace("_", " ")}<br>/${g.pts}</th>`).join("")}<th>Práct./50</th><th>Integr./20</th><th>Total</th><th>Esc.</th></tr></thead><tbody>${ALUMNOS.map(filaDoc).join("")}</tbody></table>
  <p class="muted">Escala sugerida: 1 (&lt;60) · 2 (60-69) · 3 (70-80) · 4 (81-90) · 5 (≥91). Ajustar al reglamento vigente. Práctica incluye hasta +3 por el ejercicio opcional de redes (tope 50).</p></div>` : `<div class="card muted">Aún no hay estudiantes registrados.</div>`}`;
}
function bindDocente() {
  $("#dq")?.addEventListener("input", e => { const q = e.target.value.toLowerCase(); $$("tbody tr").forEach(tr => tr.hidden = !tr.dataset.q.includes(q)); });
  $("#csvRegistro")?.addEventListener("click", () => descargar("registro_usuarios.csv", planillaRegistros(ALUMNOS), "text/csv"));
  $("#csvRespuestas")?.addEventListener("click", () => descargar("respuestas_quizzes.csv", planillaQuizzes(ALUMNOS, INTENTOS), "text/csv"));
  $("#csvAuto")?.addEventListener("click", () => descargar("autoevaluaciones.csv", planillaAutoevaluaciones(ALUMNOS, ACTS, D.rubricas), "text/csv"));
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
    descargar("calificaciones_curso.csv", csvPlanilla(head, rows), "text/csv");
  });
}

/* ---------- clases grabadas ---------- */
let CLASES = [], CL_FILTRO = "todas", CL_EDIT = null;
// Acepta YouTube, Google Drive o cualquier https (se abre en pestaña nueva). Devuelve {tipo, id, embed(inicio)}.
function parseVideo(u) {
  let x; try { x = new URL(String(u).trim()); } catch { return null; }
  if (x.protocol !== "https:") return null;
  const h = x.hostname.replace(/^www\./, "");
  let id = null;
  if (h === "youtu.be") id = x.pathname.slice(1);
  else if (h === "youtube.com" || h === "m.youtube.com" || h === "youtube-nocookie.com") id = x.searchParams.get("v") || (x.pathname.match(/^\/(?:embed|live|shorts)\/([\w-]{11})/) || [])[1];
  if (id && /^[\w-]{11}$/.test(id)) return { tipo: "yt", id, embed: t => `https://www.youtube-nocookie.com/embed/${id}?rel=0${t ? `&start=${t}&autoplay=1` : ""}` };
  if (h === "drive.google.com") { const m = x.pathname.match(/\/file\/d\/([\w-]+)/) || (x.searchParams.get("id") ? [0, x.searchParams.get("id")] : null); if (m) return { tipo: "drive", id: m[1], embed: () => `https://drive.google.com/file/d/${m[1]}/preview` }; }
  return { tipo: "ext", id: null, url: x.href };
}
const hms = t => t.split(":").reverse().reduce((a, v, i) => a + (+v || 0) * 60 ** i, 0);
function capitulos(txt) { return String(txt || "").split("\n").map(l => l.trim().match(/^((?:\d{1,2}:)?\d{1,2}:\d{2})\s+(.+)$/)).filter(Boolean).map(m => ({ t: m[1], s: hms(m[1]), n: m[2] })); }
async function vClases() {
  try { CLASES = await B.listarClases(); } catch (e) { return `<h1>🎥 Clases grabadas</h1><div class="card note">No se pudieron leer las clases: ${esc(msgError(e))}</div>`; }
  CLASES = CLASES.filter(c => ES_DOC || c.visible !== false).sort((a, b) => (b.fecha || "").localeCompare(a.fecha || ""));
  const lista = CLASES.filter(c => CL_FILTRO === "todas" || String(c.sesion) === CL_FILTRO.slice(1));
  const chips = [["todas", "Todas"], ...D.sesiones.map(s => ["s" + s.n, "Sesión " + s.n])];
  const vistas = CLASES.filter(c => S.done["rec_" + c.id]).length;
  const form = ES_DOC ? `<details class="card" id="clform" ${CL_EDIT ? "open" : ""}><summary><b>${CL_EDIT ? "✏️ Editar clase" : "➕ Cargar una clase grabada"}</b> <span class="muted">(solo docentes)</span></summary>
   <p class="muted">Subí la grabación a Google Drive (carpeta con acceso solo para el grupo) o a YouTube como <b>no listado</b>, y pegá acá el enlace. El aula no almacena el video.</p>
   <form id="clf" class="form-grid">
    <div><label for="cl_t">Título</label><input id="cl_t" type="text" required maxlength="150" value="${esc(CL_EDIT?.titulo || "")}"></div>
    <div><label for="cl_u">Enlace del video (https)</label><input id="cl_u" type="url" required placeholder="https://drive.google.com/file/d/…/view  ·  https://youtu.be/…" value="${esc(CL_EDIT?.url || "")}"></div>
    <div><label for="cl_s">Sesión</label><select id="cl_s">${D.sesiones.map(s => `<option value="${s.n}" ${+CL_EDIT?.sesion === s.n ? "selected" : ""}>${s.n}. ${esc(s.corto)}</option>`).join("")}</select></div>
    <div><label for="cl_f">Fecha de la clase</label><input id="cl_f" type="date" required value="${esc(CL_EDIT?.fecha || new Date().toISOString().slice(0, 10))}"></div>
    <div style="grid-column:1/-1"><label for="cl_n">Notas / resumen (opcional)</label><textarea id="cl_n" rows="2" maxlength="600">${esc(CL_EDIT?.notas || "")}</textarea></div>
    <div style="grid-column:1/-1"><label for="cl_c">Capítulos (opcional; uno por línea: <code>12:40 Color y daltonismo</code>)</label><textarea id="cl_c" rows="3" maxlength="1500">${esc(CL_EDIT?.capitulos || "")}</textarea></div>
    <label class="chk" style="grid-column:1/-1;margin-top:0"><input id="cl_v" type="checkbox" ${CL_EDIT && CL_EDIT.visible === false ? "" : "checked"}> Visible para los estudiantes</label>
    <div style="grid-column:1/-1" class="row"><button class="btn" type="submit">${CL_EDIT ? "Guardar cambios" : "Publicar clase"}</button>${CL_EDIT ? '<button class="btn sm" type="button" id="cl_x">Cancelar</button>' : ""}</div>
   </form></details>` : "";
  const card = c => { const v = parseVideo(c.url) || {}, caps = capitulos(c.capitulos), visto = !!S.done["rec_" + c.id];
    const player = v.tipo === "ext" ? `<div class="vbox" style="display:grid;place-items:center"><a class="btn" target="_blank" rel="noopener" href="${esc(v.url)}">▶ Abrir grabación</a></div>`
      : `<div class="vbox" id="cb_${esc(c.id)}"><button class="vthumb ${v.tipo === "drive" ? "pl" : ""}" data-cplay="${esc(c.id)}" aria-label="Reproducir: ${esc(c.titulo)}" ${v.tipo === "yt" ? `style="background-image:url(https://i.ytimg.com/vi/${v.id}/hqdefault.jpg)"` : ""}><span>▶</span></button></div>`;
    return `<div class="vcard">${player}<div class="vinfo"><div class="row" style="justify-content:space-between"><span class="tag">Sesión ${esc(c.sesion)} · ${esc(c.fecha)}</span>${c.visible === false ? '<span class="tag warn">Oculta</span>' : ""}</div>
     <b>${esc(c.titulo)}</b>${c.notas ? `<div class="muted">${esc(c.notas)}</div>` : ""}
     ${caps.length ? `<div class="chips">${caps.map(k => v.tipo === "yt" ? `<a href="#" data-cseek="${esc(c.id)}" data-s="${k.s}">${esc(k.t)} ${esc(k.n)}</a>` : `<span class="chip" style="font-size:.75rem">${esc(k.t)} ${esc(k.n)}</span>`).join("")}</div>` : ""}
     <div class="row" style="margin-top:.5rem;justify-content:space-between"><label class="chk2"><input type="checkbox" data-cvis="${esc(c.id)}" ${visto ? "checked" : ""}> Ya la vi</label>
     <span><a class="btn sm" href="#/sesion/${esc(c.sesion)}">Ir a la sesión</a>${ES_DOC ? ` <button class="btn sm" data-cedit="${esc(c.id)}">Editar</button> <button class="btn sm" data-chide="${esc(c.id)}">${c.visible === false ? "Mostrar" : "Ocultar"}</button>` : ""}</span></div></div></div>`; };
  return `<h1>🎥 Clases grabadas</h1><p class="sub">Si faltaste o querés repasar: mirá la clase y marcá <i>Ya la vi</i>. ${CLASES.length ? `Viste <b>${vistas}</b> de <b>${CLASES.length}</b>.` : ""}</p>${demoBanner()}
  ${form}<div class="chips2" style="margin:.8rem 0">${chips.map(([k, t]) => `<a class="chip ${CL_FILTRO === k ? "on" : ""}" href="#/clases/${k}">${t}</a>`).join("")}</div>
  ${lista.length ? `<div class="vgrid">${lista.map(card).join("")}</div>` : `<div class="card muted">Todavía no hay clases grabadas${CL_FILTRO !== "todas" ? " para esta sesión" : ""}.${ES_DOC ? " Cargá la primera con el formulario de arriba." : " El docente las publicará acá."}</div>`}
  <p class="muted">Las grabaciones son material del curso: no las descargues ni compartas fuera del grupo.</p>`;
}
function bindClases() {
  const por = id => CLASES.find(c => c.id === id);
  const play = (id, t) => { const c = por(id), v = c && parseVideo(c.url); if (!v || v.tipo === "ext") return;
    $("#cb_" + id).innerHTML = `<iframe src="${v.embed(t)}" title="${esc(c.titulo)}" loading="lazy" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>`; };
  $$("[data-cplay]").forEach(b => b.addEventListener("click", () => play(b.dataset.cplay)));
  $$("[data-cseek]").forEach(a => a.addEventListener("click", e => { e.preventDefault(); play(a.dataset.cseek, a.dataset.s); }));
  $$("[data-cvis]").forEach(c => c.addEventListener("change", () => { const k = "rec_" + c.dataset.cvis; if (c.checked) S.done[k] = true; else delete S.done[k]; persist(); }));
  $$("[data-cedit]").forEach(b => b.addEventListener("click", () => { CL_EDIT = por(b.dataset.cedit); render().then(() => $("#clform")?.scrollIntoView()); }));
  $$("[data-chide]").forEach(b => b.addEventListener("click", async () => { const c = por(b.dataset.chide); try { await B.guardarClase({ ...c, visible: c.visible === false }); aviso("Listo ✔"); render(); } catch (e) { aviso(msgError(e), "bad"); } }));
  $("#cl_x")?.addEventListener("click", () => { CL_EDIT = null; render(); });
  $("#clf")?.addEventListener("submit", async e => { e.preventDefault();
    const url = $("#cl_u").value.trim(), v = parseVideo(url); if (!v) return aviso("El enlace debe empezar con https://", "bad");
    const c = { id: CL_EDIT?.id || "c" + Date.now().toString(36), titulo: $("#cl_t").value.trim(), url, sesion: +$("#cl_s").value, fecha: $("#cl_f").value, notas: $("#cl_n").value.trim(), capitulos: $("#cl_c").value.trim(), visible: $("#cl_v").checked };
    try { await B.guardarClase(c); aviso(CL_EDIT ? "Clase actualizada ✔" : "Clase publicada ✔"); CL_EDIT = null; render(); } catch (er) { aviso(msgError(er), "bad"); } });
}

/* ---------- El tutor ---------- */
function vTutor() {
  const T = D.tutor, ini = T.nombre.split(" ").filter((_, i) => i === 0 || i === 2).map(x => x[0]).join("");
  const fila = ([a, b, c]) => `<div class="tl"><div class="tl-y">${esc(a)}</div><div><b>${esc(b)}</b>${c ? `<div class="mut">${esc(c)}</div>` : ""}</div></div>`;
  const links = (T.links || []).map(l => `<a class="chip" target="_blank" rel="noopener" href="${esc(l.u)}">${esc(l.t)}</a>`).join("");
  return `<h1>👤 El tutor</h1>
  <div class="card"><div class="row" style="gap:1rem;align-items:center"><div class="logo" style="width:64px;height:64px;font-size:1.5rem;flex:none">${esc(ini)}</div>
   <div><h2 style="margin:0">${esc(T.nombre)}</h2><div class="mut">${esc(T.rol)}</div></div></div>
   <p>${esc(T.resumen)}</p>
   <div class="chips2">${T.areas.map(a => `<span class="chip">${esc(a)}</span>`).join("")}</div>
   <p style="margin:.8rem 0 0">${links ? `<b>Perfiles y producción:</b> <span class="chips2" style="display:inline-flex">${links}</span>` : '<span class="mut"></span>'}</p>
   <p class="mut" style="margin:.5rem 0 0">Citar como: ${esc(T.cita)} · Idiomas: ${esc(T.idiomas)}${C.contacto_docente ? ` · Contacto: <a href="mailto:${esc(C.contacto_docente)}">${esc(C.contacto_docente)}</a>` : ""}</p></div>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(340px,1fr))">
   <div class="card" style="margin:0"><h3>🎓 Formación</h3>${T.formacion.map(fila).join("")}</div>
   <div class="card" style="margin:0"><h3>💼 Experiencia</h3>${T.experiencia.map(fila).join("")}</div></div>
  <div class="card"><h3>📄 Producción</h3>${T.produccion.map(([k, t, u]) => `<div class="tl"><div class="tl-y"><span class="tag ok">${esc(k)}</span></div><div>${esc(t)}${u ? ` <a target="_blank" rel="noopener" href="${esc(u)}">Ver ↗</a>` : ""}</div></div>`).join("")}</div>
  <div class="card"><h3>✍️ Divulgación en LinkedIn</h3><p class="muted">Artículos sobre R, Python, datos abiertos y enseñanza de la estadística: varios sirven como lectura complementaria del curso.</p>${(T.divulgacion || []).map(([f, t, u]) => `<div class="tl"><div class="tl-y">${esc(f)}</div><div><a target="_blank" rel="noopener" href="${esc(u)}">${esc(t)}</a></div></div>`).join("")}</div>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(340px,1fr))">
   <div class="card" style="margin:0"><h3>🏅 Reconocimientos</h3><ul>${T.premios.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>
   <div class="card" style="margin:0"><h3>🧭 Tutorías</h3><ul>${T.docencia_inv.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div></div>`;
}

/* ---------- datos abiertos reales ---------- */
let DA_FILTRO = "todas";
const ESTADO_CLS = { verificado: "ok", documentado: "ok", verificar: "warn", incierto: "bad" };
function vDatos() {
  const A = D.abiertos, fs = A.fuentes.filter(f => DA_FILTRO === "todas" || (DA_FILTRO === "personales" ? f.sensible : DA_FILTRO.startsWith("s") ? f.sesiones.includes(+DA_FILTRO.slice(1)) : f.estado === DA_FILTRO));
  const chips = [["todas", "Todas"], ["verificado", "🟢 Verificadas"], ["documentado", "✅ Documentadas"], ["verificar", "🔎 Verificar"], ["incierto", "⚠️ Inciertas"], ["personales", "🔒 Datos personales"], ...D.sesiones.map(s => ["s" + s.n, "Sesión " + s.n])];
  const prac = id => A.practicas.find(p => p.id === id);
  return `<h1>🗺️ Datos abiertos reales</h1><p class="sub">Las prácticas usan datos reales de Paraguay y fuentes globales: compras públicas, encuestas de hogares, nómina estatal, imágenes satelitales, comercio exterior…</p>
  <div class="card note"><b>Leé esto primero.</b> Solo la <b>EPHC (INE)</b> y la <b>recaudación de la DNIT</b> están 🟢 <b>verificadas</b>: se descargaron e inspeccionaron archivos reales. El resto se armó con búsquedas y <b>no se pudo abrir ni inspeccionar filas</b>. Cada fuente tiene un <b>estado</b>; los nombres de columnas se toman del <b>diccionario oficial</b> (o se detectan automáticamente). Todas las prácticas funcionan <b>sin conexión con datos sintéticos rotulados</b> y pasan a datos reales al pegar la URL.
   El docente debe correr antes <a target="_blank" rel="noopener" href="${esc(prac("pr00_verificar_fuentes").colab)}">pr00 · Verificar fuentes</a> en Colab.</div>
  <div class="chips2" style="margin:.8rem 0">${chips.map(([k, t]) => `<a class="chip ${DA_FILTRO === k ? "on" : ""}" href="#/datos/${k}">${t}</a>`).join("")}</div>
  <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr))">${fs.map(f => { const pr = prac(f.practica), ic = A.estados[f.estado];
   return `<div class="card" style="margin:0"><div class="row" style="justify-content:space-between"><span class="tag ${ESTADO_CLS[f.estado]}">${ic[0]} ${ic[1]}</span>${f.sensible ? '<span class="tag bad">🔒 datos personales</span>' : ""}</div>
    <h3 style="margin:.5rem 0 .1rem">${esc(f.nombre)}</h3><div class="muted">${esc(f.inst)}</div>
    <p style="margin:.5rem 0">${esc(f.contiene)}</p>
    <div class="muted" style="font-size:.82rem">${esc(f.tipo)} · ${esc(f.formato)}</div>
    <details style="margin:.5rem 0"><summary>Ideas y cuidados</summary><ul style="margin:.3rem 0;padding-left:1.1rem">${f.ideas.map(i => `<li>${esc(i)}</li>`).join("")}</ul><p class="muted" style="margin:.3rem 0 0">⚠ ${esc(f.aviso)}</p></details>
    <div class="row"><a target="_blank" rel="noopener" href="${esc(f.url)}">Portal ↗</a><a target="_blank" rel="noopener" href="${esc(f.doc)}">Documentación ↗</a></div>
    <div class="row" style="margin-top:.5rem"><span class="tag">Sesiones ${f.sesiones.join(", ")}</span>${pr ? `<a class="btn sec sm" target="_blank" rel="noopener" href="${esc(pr.colab)}">🐍 ${esc(f.titulo_practica.length > 30 ? "Práctica en Colab" : f.titulo_practica)}</a>${pr.rmd ? `<a class="btn sec sm" target="_blank" rel="noopener" href="${esc(pr.rmd)}">📊 R → RPubs</a>` : ""}` : ""}</div></div>`; }).join("")}</div>
  <h2>Ruta de prácticas por sesión</h2><div class="card tw"><table><thead><tr><th>Sesión</th><th>Práctica</th><th>Qué se aprende</th><th>Abrir</th></tr></thead><tbody>${A.practicas.map(p => `<tr><td>${p.sesiones.join(", ")}</td><td><b>${esc(p.nombre)}</b>${p.rol === "docente" ? ' <span class="tag warn">docente</span>' : ""}</td><td>${esc(p.desc)}</td><td><a target="_blank" rel="noopener" href="${esc(p.colab)}">🐍 Colab</a>${p.rmd ? ` · <a target="_blank" rel="noopener" href="${esc(p.rmd)}">📊 R</a>` : ""}</td></tr>`).join("")}</tbody></table></div>
  <h2>Reglas de oro con datos reales</h2><div class="card"><ol style="margin:0;padding-left:1.2rem">
   <li><b>Citá</b> la fuente, la URL y la <b>fecha de descarga</b>; completá la <i>ficha del dataset</i> (práctica 1).</li>
   <li><b>Oficial no es sinónimo de limpio:</b> perfilá, buscá nulos, duplicados y cambios de definición.</li>
   <li><b>Datos personales:</b> solo agregados; descartá nombres y documentos al cargar; suprimí grupos pequeños. <b>Lo que publicás en RPubs es público.</b></li>
   <li><b>Encuestas:</b> usá el factor de expansión. <b>Mapas:</b> tasas o densidades, no conteos.</li>
   <li><b>Licencias:</b> verificá las condiciones de uso de cada fuente.</li>
   <li>Si una fuente cae o cambia, el código usa datos <b>sintéticos</b> rotulados: nunca los presentes como reales.</li></ol>
   <p class="muted" style="margin:.6rem 0 0">Guía completa y lista de verificación del docente: <a target="_blank" rel="noopener" href="../docs/datos_abiertos_reales.html">datos_abiertos_reales</a>.</p></div>`;
}

/* ---------- calendario y agenda ---------- */
const TIPO_EV = { clase: ["🎓", "Clase", "#0072B2"], tutoria: ["💬", "Tutoría", "#009E73"], entrega: ["📤", "Entrega", "#D55E00"], evaluacion: ["📝", "Evaluación", "#CC79A7"], otro: ["📌", "Otro", "#8C8C8C"] };
let AGENDA = null, AGENDA_ERR = "", calMes = new Date(), calFiltro = "todos", calEjemplo = false;
const agendaUrl = () => (C.agenda?.endpoint || C.diagnostico?.endpoint || "");
function agendaEjemplo() {
  const hoy = new Date(); hoy.setHours(0, 0, 0, 0); const d = n => { const x = new Date(hoy); x.setDate(x.getDate() + n); return x; };
  const f = x => x.toISOString().slice(0, 10), iso = (x, h) => `${f(x)}T${h}:00-03:00`, mk = (id, tipo, titulo, n, a, b, extra = {}) => ({ id, tipo, titulo, fecha: f(d(n)), inicio: a, fin: b, inicio_iso: iso(d(n), a), fin_iso: iso(d(n), b), sesion: null, descripcion: "", asistencia: false, mini: false, ...extra });
  return { eventos: [mk("ej1", "clase", "Sesión 1 · Principios y percepción", 2, "19:00", "21:00", { sesion: 1, asistencia: true, mini: true }), mk("ej2", "tutoria", "Tutoría virtual · Dudas de la sesión 1", 5, "18:00", "19:00", { asistencia: true }),
    mk("ej3", "entrega", "Entrega de actividades · Sesión 1", 9, "23:00", "23:59", { sesion: 1, descripcion: "Publicar en RPubs/Colab y pegar el enlace en el aula" }), mk("ej4", "clase", "Sesión 2 · Elección de gráficos", 9, "19:00", "21:00", { sesion: 2, asistencia: true, mini: true })] };
}
async function cargarAgenda(forzar) {
  if (AGENDA && !forzar) return;
  const ep = agendaUrl(); AGENDA_ERR = "";
  const base = () => ({ eventos: D.agenda_base?.eventos || [], estatica: true });
  if (!ep) { AGENDA = base(); return; }
  try { const r = await fetch(ep + (ep.includes("?") ? "&" : "?") + "action=agenda"); AGENDA = await r.json(); if (!AGENDA.eventos?.length) AGENDA = base(); }
  catch (e) { AGENDA = base(); AGENDA_ERR = "No se pudo leer la agenda del servidor; se muestra el calendario base de clases."; }
}
const evFecha = e => new Date(e.inicio_iso), pad2 = n => String(n).padStart(2, "0");
const hoyZ = () => new Date().toLocaleDateString("sv-SE", { timeZone: "America/Asuncion" });
const fmtF = e => new Date(e.inicio_iso).toLocaleDateString("es-PY", { weekday: "long", day: "numeric", month: "long", timeZone: "America/Asuncion" });
function ics(evs) {
  const z = d => new Date(d).toISOString().replace(/[-:]/g, "").replace(/\.\d+Z/, "Z"), esc2 = t => String(t || "").replace(/([,;\\])/g, "\\$1").replace(/\n/g, "\\n");
  return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Visualizacion de Datos UNC//Aula//ES", "CALSCALE:GREGORIAN"].concat(evs.flatMap(e => ["BEGIN:VEVENT", `UID:${e.id}@aula-vd-unc`, `DTSTAMP:${z(new Date())}`, `DTSTART:${z(e.inicio_iso)}`, `DTEND:${z(e.fin_iso)}`,
    `SUMMARY:${esc2((TIPO_EV[e.tipo] || TIPO_EV.otro)[0] + " " + e.titulo)}`, `DESCRIPTION:${esc2(e.descripcion || "")}`, ...(e.enlace ? [`URL:${e.enlace}`] : []), "END:VEVENT"])).concat("END:VCALENDAR").join("\r\n");
}
function vCalendario() {
  const A = calEjemplo ? agendaEjemplo() : AGENDA, evs = (A?.eventos || []).filter(e => calFiltro === "todos" || e.tipo === calFiltro);
  const y = calMes.getFullYear(), m = calMes.getMonth(), primero = new Date(y, m, 1), nDias = new Date(y, m + 1, 0).getDate(), off = (primero.getDay() + 6) % 7;
  const porDia = {}; evs.forEach(e => { (porDia[e.fecha] = porDia[e.fecha] || []).push(e); });
  const celdas = []; for (let i = 0; i < off; i++) celdas.push('<div class="cd off"></div>');
  for (let d = 1; d <= nDias; d++) { const k = `${y}-${pad2(m + 1)}-${pad2(d)}`, lista = porDia[k] || [];
    celdas.push(`<div class="cd ${k === hoyZ() ? "hoy" : ""}"><div class="dn">${d}</div>${lista.map(e => `<a href="#/calendario/${encodeURIComponent(e.id)}" class="ev" style="--c:${(TIPO_EV[e.tipo] || TIPO_EV.otro)[2]}" title="${esc(e.titulo)} · ${e.inicio}–${e.fin}">${(TIPO_EV[e.tipo] || TIPO_EV.otro)[0]} <span>${esc(e.inicio)} ${esc(e.titulo)}</span></a>`).join("")}</div>`); }
  const proximos = (A?.eventos || []).filter(e => new Date(e.fin_iso) >= new Date()).filter(e => calFiltro === "todos" || e.tipo === calFiltro).slice(0, 8);
  const mes0 = primero.toLocaleDateString("es-PY", { month: "long", year: "numeric" }).replace(" de ", " "), mes = mes0.charAt(0).toUpperCase() + mes0.slice(1);
  return `<h1>📅 Calendario del curso</h1><p class="sub">Clases, tutorías virtuales y fechas de entrega. Horario de Paraguay (UTC−3).</p>
  ${calEjemplo ? '<div class="card note"><b>Ejemplo.</b> Esta agenda es ilustrativa. La agenda real aparecerá aquí cuando el docente la publique.</div>' : ""}
  ${AGENDA_ERR ? `<div class="card note">${esc(AGENDA_ERR)}</div>` : ""}
  ${AGENDA?.estatica && !calEjemplo ? `<div class="card note"><b>Calendario base de clases.</b> Clases virtuales los viernes de 18:00 a 22:00 y los sábados de 08:00 a 12:00. Las tutorías, las fechas de entrega y los correos de asistencia se suman acá cuando el docente los publique.</div>` : ""}
  ${!agendaUrl() && !calEjemplo && !AGENDA?.eventos?.length ? `<div class="card note"><b>La agenda todavía no está publicada.</b> El docente la carga en la hoja de cálculo del curso (pestaña <i>Agenda</i>) y se muestra aquí automáticamente. <button class="btn sec" id="ejCal" style="margin-left:.5rem">Ver un ejemplo</button></div>` : ""}
  <div class="row" style="margin:.6rem 0"><button class="btn sec" id="cPrev" aria-label="Mes anterior">←</button><b style="min-width:11rem;text-align:center">${esc(mes)}</b><button class="btn sec" id="cNext" aria-label="Mes siguiente">→</button>
   <select id="cFil" aria-label="Filtrar por tipo" style="width:auto"><option value="todos">Todos los tipos</option>${Object.entries(TIPO_EV).map(([k, v]) => `<option value="${k}" ${calFiltro === k ? "selected" : ""}>${v[0]} ${v[1]}</option>`).join("")}</select>
   <button class="btn sec" id="cRef">↻ Actualizar</button><button class="btn sec" id="cIcs" ${evs.length ? "" : "disabled"}>⬇ Agregar a mi calendario (.ics)</button></div>
  <div class="cal"><div class="ch">Lun</div><div class="ch">Mar</div><div class="ch">Mié</div><div class="ch">Jue</div><div class="ch">Vie</div><div class="ch">Sáb</div><div class="ch">Dom</div>${celdas.join("")}</div>
  <div class="leg">${Object.values(TIPO_EV).map(v => `<span style="--c:${v[2]}">${v[0]} ${v[1]}</span>`).join("")}</div>
  <h2>Próximos eventos</h2>${proximos.length ? `<div class="card"><ul class="res">${proximos.map(e => { const t = TIPO_EV[e.tipo] || TIPO_EV.otro;
    return `<li><span class="ico">${t[0]}</span><span><a href="#/calendario/${encodeURIComponent(e.id)}"><b>${esc(e.titulo)}</b></a><br><span class="muted">${esc(fmtF(e))} · ${esc(e.inicio)}–${esc(e.fin)}</span>${e.asistencia ? ' <span class="tag">asistencia</span>' : ""}${e.mini ? ' <span class="tag">mini-evaluación sin nota</span>' : ""}</span></li>`; }).join("")}</ul></div>` : '<div class="card muted">No hay eventos próximos.</div>'}
  <div class="card"><b>¿Cómo funcionan la asistencia y la mini-evaluación?</b><ul style="margin:.4rem 0 0;padding-left:1.2rem">
   <li>📍 <b>Asistencia:</b> a la hora de cada clase o tutoría con registro recibís un <b>correo con tu enlace personal</b>. El formulario solo funciona durante el horario del evento (con 15 min de tolerancia).</li>
   <li>📝 <b>Mini-evaluación:</b> al terminar cada clase recibís otro correo con 3 preguntas sobre lo visto. <b>No suma puntos</b> para la certificación.</li>
   <li>Revisá tu bandeja de entrada y la carpeta de spam; los correos salen del sistema del curso.</li></ul></div>`;
}
function vEvento(id) {
  const A = calEjemplo ? agendaEjemplo() : AGENDA, e = (A?.eventos || []).find(x => x.id === id), t = e && (TIPO_EV[e.tipo] || TIPO_EV.otro);
  if (!e) return `<a href="#/calendario">← Calendario</a><h1>Evento no encontrado</h1>`;
  return `<a href="#/calendario">← Calendario</a><h1>${t[0]} ${esc(e.titulo)}</h1><p class="sub">${esc(fmtF(e))} · ${esc(e.inicio)}–${esc(e.fin)} (hora de Paraguay)</p>
  <div class="card">${e.descripcion ? `<p style="margin-top:0">${esc(e.descripcion)}</p>` : ""}
   <div class="row"><span class="tag">${t[1]}</span>${e.sesion ? `<a href="#/sesion/${e.sesion}">Ir al módulo ${e.sesion}</a>` : ""}${e.enlace ? `<a class="btn" target="_blank" rel="noopener" href="${esc(e.enlace)}">Unirme a la sesión</a>` : ""}
   <button class="btn sec" id="evIcs">⬇ Agregar a mi calendario</button></div>
   ${e.asistencia ? '<p class="muted" style="margin:.8rem 0 0">📍 Recibirás por correo, a la hora de inicio, el enlace personal para registrar tu asistencia (solo funciona durante el horario).</p>' : ""}
   ${e.mini ? '<p class="muted" style="margin:.4rem 0 0">📝 Al terminar recibirás una mini-evaluación de 3 preguntas. No suma puntos.</p>' : ""}
   ${!e.enlace && (e.tipo === "clase" || e.tipo === "tutoria") ? '<p class="muted" style="margin:.4rem 0 0">El enlace de la sesión llega en el correo de asistencia.</p>' : ""}</div>`;
}
function bindCalendario(id) {
  $("#cPrev")?.addEventListener("click", () => { calMes = new Date(calMes.getFullYear(), calMes.getMonth() - 1, 1); render(); });
  $("#cNext")?.addEventListener("click", () => { calMes = new Date(calMes.getFullYear(), calMes.getMonth() + 1, 1); render(); });
  $("#cFil")?.addEventListener("change", e => { calFiltro = e.target.value; render(); });
  $("#cRef")?.addEventListener("click", async () => { await cargarAgenda(true); render(); });
  $("#ejCal")?.addEventListener("click", () => { calEjemplo = true; calMes = new Date(); render(); });
  $("#cIcs")?.addEventListener("click", () => descargar("calendario_visualizacion_datos.ics", ics((calEjemplo ? agendaEjemplo() : AGENDA).eventos), "text/calendar"));
  $("#evIcs")?.addEventListener("click", () => descargar(`evento_${id}.ics`, ics([(calEjemplo ? agendaEjemplo() : AGENDA).eventos.find(x => x.id === id)]), "text/calendar"));
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
      S = { perfil: { ...PERFIL, nombre: nombreCompleto(PERFIL), doc: PERFIL.cedula }, done: pr.done || {}, quiz: pr.quiz || {}, auto: pr.auto || {}, enlaces: pr.enlaces || {}, oficial: of };
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
      case "clases": CL_FILTRO = b || "todas"; html = await vClases(); bind = bindClases; crumb = "Clases grabadas"; break;
      case "tutor": html = vTutor(); crumb = "El tutor"; break;
      case "datos": DA_FILTRO = b || "todas"; html = vDatos(); crumb = "Datos abiertos"; break;
      case "calendario": await cargarAgenda(); html = b ? vEvento(decodeURIComponent(b)) : vCalendario(); crumb = "Calendario"; bind = () => bindCalendario(b ? decodeURIComponent(b) : ""); break;
      case "recursos": html = vRecursos(); crumb = "Recursos"; bind = bindRecursos; break;
      case "perfil": html = vPerfil(); crumb = "Mi perfil"; bind = bindPerfil; break;
      case "docente": html = await vDocente(); crumb = "Panel docente"; bind = bindDocente; break;
      default: await refrescarNotas(); await cargarAgenda(); html = vInicio();
    }
  }
  if (tk !== renderTk) return;
  document.body.classList.toggle("guest", guest);
  $("#main").innerHTML = html; $("#crumb").textContent = `${C.curso} › ${crumb}`;
  if (!guest) navHtml("/" + [a, b].filter(Boolean).join("/")); else $("#user").textContent = "";
  $("#logout").hidden = !USER; bind(); afterRender();
  document.title = `${crumb} · Aula virtual · Visualización de Datos UNC`;
  $("#side").classList.remove("open"); $("#menu").setAttribute("aria-expanded", "false");
}
function bindSesion() {
  $$("[data-play]").forEach(b => b.addEventListener("click", () => {
    const id = b.dataset.play, pl = b.dataset.tipo === "playlist";
    const src = pl ? `https://www.youtube-nocookie.com/embed/videoseries?list=${id}&autoplay=1` : `https://www.youtube-nocookie.com/embed/${id}?rel=0&autoplay=1`;
    $("#vb_" + id).innerHTML = `<iframe src="${src}" title="${esc(b.dataset.t)}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>`;
  }));
  $$("[data-vis]").forEach(c => c.addEventListener("change", () => { const k = "vid_" + c.dataset.vis; if (c.checked) S.done[k] = true; else delete S.done[k]; persist(); }));
  $$("[data-enl]").forEach(inp => inp.addEventListener("change", () => {
    const id = inp.dataset.enl, t = inp.dataset.t, v = inp.value.trim(), a = actById(id);
    S.enlaces[id] = S.enlaces[id] || {};
    if (v && !RE_ENL[t].test(v)) { aviso(t === "rpubs" ? "El enlace debe ser de rpubs.com (https://rpubs.com/...)." : "El enlace debe ser de Google Colab o Drive (https://colab.research.google.com/...).", "bad"); return; }
    if (v) S.enlaces[id][t] = v; else delete S.enlaces[id][t];
    const completo = a.ent.every(x => S.enlaces[id][x]);
    if (completo) S.done[id] = true; else if (!v) delete S.done[id];
    persist(); aviso(v ? (completo ? "Entrega registrada ✔" : "Enlace guardado ✔") : "Enlace quitado"); render();
  }));
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
initFx();
B = await crearBackend(C);
await B.listo;
USER = B.actual(); await cargarSesion(); render();
B.onAuth(async u => { if (ocupado || (u?.uid === USER?.uid && u?.uid)) return; USER = u; await cargarSesion(); render(); });
window.__aula = { get usuario() { return USER; }, modo: B.modo };
})();
