import { RETOS_CODIGO } from "./codigo-retos.mjs";
import { RETOS_TALLERES } from "./codigo-talleres.mjs";

const idioma = new Map();
const pasoActivo = new Map();
const memoriaPorUsuario = new Map();
const memoriaId = uid => `cvd_codigo_sesion_${uid || "invitado"}`;
function memoriaDe(uid) {
  const id = uid || "invitado";
  if (!memoriaPorUsuario.has(id)) {
    let guardado = {};
    try { guardado = JSON.parse(sessionStorage.getItem(memoriaId(id)) || "{}"); } catch {}
    memoriaPorUsuario.set(id, { borradores: {}, resultados: {}, ayuda: {}, historialAbierto: {}, ...guardado });
  }
  return memoriaPorUsuario.get(id);
}
function guardarMemoria(uid) {
  try { sessionStorage.setItem(memoriaId(uid), JSON.stringify(memoriaDe(uid))); } catch {}
}
export function limpiarCodigoSesion(uid) {
  memoriaPorUsuario.delete(uid || "invitado");
  try { sessionStorage.removeItem(memoriaId(uid)); } catch {}
  idioma.clear(); pasoActivo.clear();
}
const esc = x => String(x ?? "").replace(/[&<>"']/g, s => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[s]));
const retosDe = n => (n >= 9 ? RETOS_TALLERES : RETOS_CODIGO).filter(r => r.n === n).sort((a, b) => a.paso - b.paso);
const lenguajesDe = n => n === 9 ? ["r"] : n === 10 ? ["python"] : ["r", "python"];
const idiomaDe = n => idioma.get(n) || (n === 9 ? "r" : "python");
const retoDe = n => retosDe(n).find(r => r.paso === (pasoActivo.get(n) || 1));
const clave = (reto, lang) => `${reto.id}_${lang}`;
const estado = (progreso, reto, lang) => progreso?.[clave(reto, lang)] || {};
export function codigoProgreso(progreso, n) {
  const retos = retosDe(n);
  return { done: retos.filter(r => lenguajesDe(n).some(lang => estado(progreso, r, lang).hecho)).length, items: retos.length };
}
let webR;
let webRPromesa;
let ggplotPromesa;
let pyWorker;
let pySecuencia = 0;
let ocupado = false;
let cancelarPython;
let ejecucion = 0;

async function obtenerR() {
  if (!webRPromesa) webRPromesa = import("https://webr.r-wasm.org/v0.6.1/webr.mjs").then(async ({ WebR }) => {
    const r = new WebR({ channelType: "PostMessage" });
    webR = r;
    await r.init();
    await r.evalRVoid("options(device = webr::canvas)");
    return r;
  }).catch(error => { webRPromesa = null; throw error; });
  return webRPromesa;
}

function detener() {
  cancelarPython?.();
  if (webR) { webR.close(); webR = null; webRPromesa = null; ggplotPromesa = null; }
  if (pyWorker) { pyWorker.terminate(); pyWorker = null; }
}

async function ejecutarR(codigo, csv) {
  const r = await obtenerR();
  if (/\b(?:library|require)\s*\(\s*["']?ggplot2\b/.test(codigo)) {
    if (!ggplotPromesa) ggplotPromesa = r.installPackages(["ggplot2"]).catch(error => { ggplotPromesa = null; throw error; });
    await ggplotPromesa;
  }
  if (csv != null) await r.FS.writeFile("/tmp/datos.csv", new TextEncoder().encode(csv));
  const shelter = await new r.Shelter();
  try {
    const preparado = `local({\nsetwd("/tmp")\n${codigo}\nif (!exists("respuesta", inherits = FALSE)) stop("Creá la variable respuesta.")\nrespuesta\n})`;
    const captura = await shelter.captureR(preparado);
    const respuesta = await captura.result.toJs();
    const salida = captura.output.filter(x => x.type === "stdout" || x.type === "stderr").map(x => String(x.data)).slice(0, 30).join("\n");
    return { respuesta, imagenes: captura.images, salida };
  } finally {
    await shelter.purge();
  }
}

function ejecutarPython(codigo, csv, grafico) {
  if (!pyWorker) pyWorker = new Worker(new URL("./codigo-python-worker.mjs", import.meta.url), { type: "module" });
  const worker = pyWorker, id = ++pySecuencia;
  return new Promise((resolve, reject) => {
    const mensaje = event => {
      if (event.data?.id !== id) return;
      limpiar();
      event.data.error ? reject(new Error(event.data.error)) : resolve(event.data);
    };
    const error = event => { limpiar(); reject(new Error(event.message || "No se pudo iniciar Python.")); };
    const cancelar = () => { limpiar(); reject(new Error("Ejecución detenida.")); };
    const limpiar = () => { worker.removeEventListener("message", mensaje); worker.removeEventListener("error", error); if (cancelarPython === cancelar) cancelarPython = null; };
    cancelarPython = cancelar;
    worker.addEventListener("message", mensaje);
    worker.addEventListener("error", error);
    worker.postMessage({ id, codigo, csv, grafico });
  });
}

export function comprobarRespuesta(obtenido, esperado) {
  if (obtenido && typeof obtenido === "object" && Object.hasOwn(obtenido, "values")) obtenido = obtenido.values;
  if (Array.isArray(obtenido) && !Array.isArray(esperado) && obtenido.length === 1) obtenido = obtenido[0];
  if (Array.isArray(esperado)) return Array.isArray(obtenido) && esperado.length === obtenido.length && esperado.every((v, i) => comprobarRespuesta(obtenido[i], v));
  return typeof esperado === "number" ? typeof obtenido === "number" && Number.isFinite(obtenido) && Math.abs(obtenido - esperado) < 0.001 : String(obtenido ?? "").trim() === esperado;
}
function mostrarRespuesta(valor) {
  if (valor && typeof valor === "object" && Object.hasOwn(valor, "values")) valor = valor.values;
  if (Array.isArray(valor) && valor.length === 1) valor = valor[0];
  try { return JSON.stringify(valor) ?? String(valor); } catch { return String(valor); }
}
const tipoRespuesta = valor => Array.isArray(valor) ? `una lista de ${valor.length} valores` : typeof valor === "number" ? "un número" : "un texto";
function ejemplosBreves(reto, n) {
  const fragmento = lang => {
    const lineas = reto.codigo[lang].split("\n");
    const graficas = lineas.filter(l => /^\s*#\s*(?:p <-|print\(p\)|plot\(|barplot\(|hist\(|plt\.|fig,|for |import matplotlib)/.test(l))
      .map(l => l.replace(/^\s*#\s?/, ""));
    const datos = lineas.filter(l => l.trim() && !/^\s*#/.test(l) && !/^\s*respuesta\s*(?:<-|=)/.test(l)).slice(0, 3);
    return [...datos, ...graficas.slice(0, 3)].join("\n").slice(0, 700);
  };
  const r = fragmento("r"), python = fragmento("python");
  return `<div class="codigo-ayuda-grid ${n >= 9 ? "solo" : ""}">${n !== 10 ? `<div><strong>Ejemplo en R</strong><pre><code>${esc(r)}</code></pre></div>` : ""}${n !== 9 ? `<div><strong>Ejemplo en Python</strong><pre><code>${esc(python)}</code></pre></div>` : ""}</div>`;
}
function animarResultado(raiz, feedback, correcto) {
  feedback.classList.remove("codigo-ok", "codigo-error", "codigo-sacudir");
  feedback.classList.add(correcto ? "codigo-ok" : "codigo-error");
  const boton = raiz.querySelector("[data-codigo-run]");
  boton.classList.remove("codigo-ejecutar-error");
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (correcto) {
    raiz.querySelector(".codigo-explosion")?.remove();
    const explosion = document.createElement("div"); explosion.className = "codigo-explosion"; explosion.setAttribute("aria-hidden", "true");
    explosion.style.left = `${boton.offsetLeft + boton.offsetWidth / 2}px`;
    explosion.style.top = `${boton.offsetTop + boton.offsetHeight - 4}px`;
    const trayectorias = [[-82, -92], [-69, -135], [-54, -108], [-40, -157], [-24, -119], [-11, -148], [5, -114], [20, -159], [34, -129], [49, -151], [64, -105], [79, -132], [-48, -79], [45, -84]];
    trayectorias.forEach(([x, y], i) => {
      const tira = document.createElement("span");
      tira.style.setProperty("--dx", `${x}px`); tira.style.setProperty("--dy", `${y}px`);
      tira.style.setProperty("--rot", `${i % 2 ? 230 : -230}deg`);
      tira.style.animationDelay = `${(i % 4) * 18}ms`;
      explosion.appendChild(tira);
    });
    raiz.querySelector(".codigo-actions").appendChild(explosion);
    setTimeout(() => explosion.remove(), 1300);
  } else {
    void boton.offsetWidth;
    boton.classList.add("codigo-ejecutar-error");
    feedback.classList.add("codigo-sacudir");
    setTimeout(() => { boton.classList.remove("codigo-ejecutar-error"); feedback.classList.remove("codigo-sacudir"); }, 500);
  }
}

function historialHtml(n, memoria) {
  const registros = retosDe(n).flatMap(reto => lenguajesDe(n).map(lang => ({ reto, lang, dato: memoria.resultados[clave(reto, lang)] }))).filter(x => x.dato);
  return `<details class="codigo-historial" ${memoria.historialAbierto[n] ? "open" : ""}><summary>Mis respuestas de esta unidad (${registros.length})</summary>
    ${registros.length ? `<ol>${registros.map(({ reto, lang, dato }) => `<li><details><summary>Paso ${reto.paso}: ${esc(reto.titulo)} · ${lang === "r" ? "R" : "Python"} · ${dato.correcto ? "✓ Correcta" : "↻ Para revisar"}</summary><p><b>Respuesta obtenida:</b> <code>${esc(dato.respuesta ?? "Sin resultado")}</code></p><pre><code>${esc(dato.codigo)}</code></pre></details></li>`).join("")}</ol>` : '<p class="muted">Tus ejecuciones aparecerán aquí mientras trabajes en esta pestaña.</p>'}</details>`;
}

export function codigoHtml(n, progreso = {}, usuarioId = "invitado") {
  const retos = retosDe(n), reto = retoDe(n); if (!reto) return "";
  const memoria = memoriaDe(usuarioId);
  const lang = idiomaDe(n), codigo = memoria.borradores[clave(reto, lang)] ?? reto.codigo[lang];
  const actual = estado(progreso, reto, lang), avance = codigoProgreso(progreso, n);
  const ultimo = memoria.resultados[clave(reto, lang)];
  const ayudaVisible = !!memoria.ayuda[n];
  const cambioPendiente = ultimo && ultimo.codigo !== codigo;
  const resuelto = lenguajesDe(n).some(l => estado(progreso, reto, l).hecho);
  const esTaller = n >= 9, nombre = n === 9 ? "R" : "Python";
  return `<section class="codigo-wrap" data-codigo-n="${n}" aria-labelledby="codigo-titulo-${n}">
    <h2 id="codigo-titulo-${n}">💻 ${esTaller ? `Prácticas guiadas de ${nombre}` : "Prácticas guiadas de código"}</h2>
    <div class="card codigo-card">
      <div class="codigo-head"><div><span class="tag" data-codigo-badge>${esTaller ? `Taller ${nombre}` : `Unidad ${n}`} · ${avance.done}/${avance.items} pasos resueltos</span><h3>${esTaller ? `Aprendé ${nombre}, paso a paso` : "Aprendé con R o Python, paso a paso"}</h3></div><span class="muted">${retos.length} pasos · reintentos ilimitados</span></div>
      <p class="codigo-intro">${esTaller ? "Cuatro bloques desde datos manuales hasta figuras analíticas. Resolvé cada consigna editando el código y ejecutándolo; podés repetir, pedir pistas y volver a tus respuestas." : "Elegí un paso y un lenguaje. Resolvé la consigna editando el código; podés repetir cada intento y pedir pistas. Completar un paso en cualquiera de los dos lenguajes suma al avance."}</p>
      <div class="codigo-stepper ${esTaller ? "taller" : ""}" role="group" aria-label="Pasos de ${esTaller ? `prácticas ${nombre}` : `la unidad ${n}`}">${retos.map(r => {
        const ok = lenguajesDe(n).some(l => estado(progreso, r, l).hecho);
        return `<button type="button" data-codigo-paso="${r.paso}" class="codigo-paso ${r.paso === reto.paso ? "activo" : ""} ${ok ? "hecho" : ""}" aria-label="Paso ${r.paso}: ${esc(r.titulo)}${ok ? ", resuelto" : ""}" aria-current="${r.paso === reto.paso ? "step" : "false"}">${r.paso}${ok ? " ✓" : ""}</button>`;
      }).join("")}</div>
      <div class="codigo-step-head"><span class="tag">${esTaller ? `${esc(reto.bloque)} · ` : ""}Paso ${reto.paso} de ${retos.length}</span><h3>${esc(reto.titulo)}</h3></div>
      <div class="codigo-consigna-box" role="group" aria-label="Consigna del paso ${reto.paso}"><strong class="codigo-consigna-etiqueta">🎯 Tu desafío</strong>
        <p class="codigo-consigna">${esc(reto.consigna)}</p>
        <p class="codigo-entrega"><strong>Para acertar:</strong> asigná ${tipoRespuesta(reto.esperado)} a <code>respuesta</code>${reto.grafico ? " y ejecutá el gráfico" : ""}. Podés volver a intentar cuantas veces necesites.</p>
      </div>
      ${reto.csv ? `<p class="muted">Datos de este paso: <a href="${esc(reto.csv)}" target="_blank" rel="noopener">${esc(reto.csv.split("/").pop())}</a>. Al ejecutar se cargan como <code>datos.csv</code>.</p>` : ""}
      ${esTaller ? "" : `<div class="codigo-tabs" role="tablist" aria-label="Lenguaje de programación"><button type="button" data-codigo-lang="python" role="tab" aria-selected="${lang === "python"}" class="btn ${lang === "python" ? "" : "sec"}">Python ${estado(progreso, reto, "python").hecho ? "✓" : ""}</button><button type="button" data-codigo-lang="r" role="tab" aria-selected="${lang === "r"}" class="btn ${lang === "r" ? "" : "sec"}">R ${estado(progreso, reto, "r").hecho ? "✓" : ""}</button></div>`}
      <div class="codigo-layout">
        <div class="codigo-editor-col"><label for="codigo-editor-${n}-${reto.paso}">Código ${lang === "r" ? "R" : "Python"} editable</label>
          <textarea id="codigo-editor-${n}-${reto.paso}" class="codigo-editor" spellcheck="false" autocapitalize="off" autocomplete="off" aria-describedby="codigo-ayuda-${n}">${esc(codigo)}</textarea>
          <p class="muted" id="codigo-ayuda-${n}">Reemplazá <code>${lang === "r" ? "NA" : "None"}</code> en la línea <code>respuesta</code>${reto.grafico ? " y activá el gráfico quitando # de sus líneas" : ""}. Después pulsá «Ejecutar y comprobar».</p>
          <div class="row codigo-actions"><button type="button" class="btn" data-codigo-run>▶ Ejecutar y comprobar</button><button type="button" class="btn sec" data-codigo-hint>💡 Pedir pista</button><button type="button" class="btn sec" data-codigo-help aria-expanded="${ayudaVisible}" aria-controls="codigo-mini-${n}-${reto.paso}">${ayudaVisible ? "Cerrar ayuda y ejemplos" : "📘 Ayuda y ejemplos"}</button><button type="button" class="btn sec" data-codigo-reset>Restaurar ejemplo</button><button type="button" class="btn sec" data-codigo-stop hidden>Detener</button></div>
          <div class="codigo-ayuda-panel" id="codigo-mini-${n}-${reto.paso}" data-codigo-help-panel ${ayudaVisible ? "" : "hidden"}><strong>Miniayuda · paso ${reto.paso}: ${esc(reto.titulo)}</strong>${reto.pistas?.[0] ? `<p><b>Orientación:</b> ${esc(reto.pistas[0])}</p>` : ""}${reto.pistas?.[1] ? `<p><b>Herramientas sugeridas:</b> ${esc(reto.pistas[1])}</p>` : ""}<p>Los fragmentos de este paso muestran cómo preparar los datos o activar la figura. Adaptá el cálculo y reemplazá <code>${lang === "r" ? "NA" : "None"}</code> en tu editor.</p>${ejemplosBreves(reto, n)}</div>
          <p class="muted" data-codigo-intentos>Intentos de comprobación: ${actual.intentos || 0}</p>
          <div class="codigo-pista" data-codigo-pista role="status" aria-live="polite">${actual.pistas ? `Pista ${actual.pistas}/3: ${esc(reto.pistas[actual.pistas - 1])}` : ""}</div>
        </div>
        <section class="codigo-resultados" aria-label="Resultados del código"><h4>Consola de resultados</h4>
          <pre class="codigo-salida" data-codigo-salida aria-live="polite">${ultimo ? esc(ultimo.salida) : "Ejecutá el código para ver aquí la respuesta y los mensajes."}</pre>
          <div class="codigo-feedback ${ultimo ? ultimo.correcto ? "codigo-ok" : "codigo-error" : actual.hecho ? "codigo-ok" : ""}" data-codigo-feedback role="status" aria-live="polite">${cambioPendiente ? "Modificaste el código desde la última ejecución. El resultado anterior sigue visible; ejecutá de nuevo para actualizarlo." : ultimo ? esc(ultimo.feedback) : actual.hecho ? `✓ Paso resuelto. ${esc(reto.explicacion)}` : "Esperando tu primer intento en este lenguaje."}</div>
          <h4>Gráfico</h4><div class="codigo-grafico" data-codigo-grafico><p class="muted">${reto.grafico ? ultimo ? "Volvé a ejecutar para recuperar el gráfico." : "Tu visualización aparecerá aquí." : "Este paso se resuelve sin gráfico."}</p></div>
        </section>
      </div>
      <p class="muted codigo-memoria-nota">El código y las últimas respuestas se conservan mientras esta pestaña esté abierta. Podés volver a cualquier paso para revisarlos.</p>
      <div data-codigo-historial>${historialHtml(n, memoria)}</div>
      <button type="button" class="btn sec codigo-next" data-codigo-next ${resuelto && reto.paso < retos.length ? "" : "hidden"}>Siguiente paso →</button>
      <p class="muted codigo-nota">La comprobación es formativa y no modifica la nota oficial. El código se ejecuta en tu navegador.</p>
    </div></section>`;
}

export function enlazarCodigo(n, progreso, guardar, usuarioId = "invitado") {
  const raiz = document.querySelector(`[data-codigo-n="${n}"]`); if (!raiz) return;
  const reto = retoDe(n), editor = raiz.querySelector(".codigo-editor"), feedback = raiz.querySelector("[data-codigo-feedback]"), pista = raiz.querySelector("[data-codigo-pista]"), salida = raiz.querySelector("[data-codigo-salida]"), grafico = raiz.querySelector("[data-codigo-grafico]"), run = raiz.querySelector("[data-codigo-run]"), stop = raiz.querySelector("[data-codigo-stop]"), siguiente = raiz.querySelector("[data-codigo-next]");
  const memoria = memoriaDe(usuarioId);
  const langActual = () => idiomaDe(n);
  const guardarBorrador = () => { memoria.borradores[clave(reto, langActual())] = editor.value; guardarMemoria(usuarioId); };
  const pintarHistorial = () => {
    raiz.querySelector("[data-codigo-historial]").innerHTML = historialHtml(n, memoria);
    enlazarHistorial();
  };
  const enlazarHistorial = () => raiz.querySelector(".codigo-historial")?.addEventListener("toggle", e => {
    memoria.historialAbierto[n] = e.target.open; guardarMemoria(usuarioId);
  });
  enlazarHistorial();
  const mostrarVacio = () => { grafico.replaceChildren(); const p = document.createElement("p"); p.className = "muted"; p.textContent = reto.grafico ? "Tu visualización aparecerá aquí." : "Este paso se resuelve sin gráfico."; grafico.appendChild(p); };
  const setOcupado = v => { ocupado = v; run.disabled = v; stop.hidden = !v; raiz.querySelectorAll("[data-codigo-paso], [data-codigo-lang], [data-codigo-next]").forEach(b => b.disabled = v); };
  const refrescarEstado = () => {
    const avance = codigoProgreso(progreso, n);
    raiz.querySelector("[data-codigo-badge]").textContent = `${n === 9 ? "Taller R" : n === 10 ? "Taller Python" : `Unidad ${n}`} · ${avance.done}/${avance.items} pasos resueltos`;
    raiz.querySelectorAll("[data-codigo-lang]").forEach(b => { const l = b.dataset.codigoLang; b.textContent = `${l === "r" ? "R" : "Python"}${estado(progreso, reto, l).hecho ? " ✓" : ""}`; });
    const botonPaso = raiz.querySelector(`[data-codigo-paso="${reto.paso}"]`);
    const pasoResuelto = lenguajesDe(n).some(l => estado(progreso, reto, l).hecho);
    botonPaso.textContent = `${reto.paso}${pasoResuelto ? " ✓" : ""}`;
    botonPaso.classList.toggle("hecho", pasoResuelto);
    botonPaso.setAttribute("aria-label", `Paso ${reto.paso}: ${reto.titulo}${pasoResuelto ? ", resuelto" : ""}`);
    siguiente.hidden = reto.paso >= retosDe(n).length || !lenguajesDe(n).some(l => estado(progreso, reto, l).hecho);
  };
  editor.addEventListener("input", guardarBorrador);
  raiz.querySelectorAll("[data-codigo-paso]").forEach(b => b.addEventListener("click", () => {
    guardarBorrador(); pasoActivo.set(n, Number(b.dataset.codigoPaso));
    raiz.outerHTML = codigoHtml(n, progreso, usuarioId); enlazarCodigo(n, progreso, guardar, usuarioId);
  }));
  raiz.querySelectorAll("[data-codigo-lang]").forEach(b => b.addEventListener("click", () => {
    guardarBorrador(); idioma.set(n, b.dataset.codigoLang);
    raiz.outerHTML = codigoHtml(n, progreso, usuarioId);
    enlazarCodigo(n, progreso, guardar, usuarioId);
  }));
  siguiente.addEventListener("click", () => { guardarBorrador(); pasoActivo.set(n, reto.paso + 1); raiz.outerHTML = codigoHtml(n, progreso, usuarioId); enlazarCodigo(n, progreso, guardar, usuarioId); document.querySelector(`[data-codigo-n="${n}"] .codigo-step-head`)?.scrollIntoView({ behavior: "smooth", block: "start" }); });
  raiz.querySelector("[data-codigo-reset]").addEventListener("click", () => {
    editor.value = reto.codigo[langActual()]; guardarBorrador(); feedback.textContent = "Ejemplo restaurado. Probá otra vez."; feedback.classList.remove("codigo-ok", "codigo-error", "codigo-sacudir"); raiz.querySelector("[data-codigo-run]").classList.remove("codigo-ejecutar-error"); raiz.querySelector(".codigo-explosion")?.remove(); salida.textContent = "Ejecutá el código para ver aquí la respuesta y los mensajes."; mostrarVacio();
  });
  const botonAyuda = raiz.querySelector("[data-codigo-help]"), panelAyuda = raiz.querySelector("[data-codigo-help-panel]");
  botonAyuda.addEventListener("click", () => { const abrir = panelAyuda.hidden; panelAyuda.hidden = !abrir; memoria.ayuda[n] = abrir; guardarMemoria(usuarioId); botonAyuda.setAttribute("aria-expanded", String(abrir)); botonAyuda.textContent = abrir ? "Cerrar ayuda y ejemplos" : "📘 Ayuda y ejemplos"; });
  raiz.querySelector("[data-codigo-hint]").addEventListener("click", () => {
    const k = clave(reto, langActual()), anterior = progreso[k] || {}, numeroPista = Math.min(3, (anterior.pistas || 0) + 1);
    progreso[k] = { ...anterior, pistas: numeroPista };
    pista.textContent = `Pista ${numeroPista}/3: ${reto.pistas[numeroPista - 1]}`;
    guardar(n, langActual(), progreso[k]);
  });
  stop.addEventListener("click", () => { ejecucion++; detener(); setOcupado(false); feedback.textContent = "Ejecución detenida. Podés corregir el código y volver a intentar."; salida.textContent = "Ejecución detenida por el estudiante."; });
  run.addEventListener("click", async () => {
    if (ocupado) return;
    const idEjecucion = ++ejecucion;
    const lang = langActual(), k = clave(reto, lang), codigo = editor.value;
    if (codigo.length > 12000) { feedback.textContent = "El ensayo admite hasta 12.000 caracteres."; return; }
    guardarBorrador(); setOcupado(true);
    feedback.textContent = `Cargando ${lang === "r" ? "R" : "Python"} y ejecutando el código…`; pista.textContent = ""; salida.textContent = "Ejecutando el código. La primera carga del motor puede tardar unos segundos…"; mostrarVacio();
    let reloj;
    try {
      let csv = null;
      if (reto.csv) {
        const respuesta = await fetch(new URL(reto.csv, import.meta.url));
        if (!respuesta.ok) throw new Error(`No se pudo cargar el CSV (${respuesta.status}).`);
        csv = await respuesta.text();
      }
      const tarea = lang === "r" ? ejecutarR(codigo, csv) : ejecutarPython(codigo, csv, reto.grafico);
      const limite = lang === "r" && reto.ggplot ? 90000 : 35000;
      const resultado = await Promise.race([tarea, new Promise((_, rechazar) => { reloj = setTimeout(() => { rechazar(new Error(`La ejecución excedió ${limite / 1000} segundos. Revisá posibles bucles y reintentá.`)); detener(); }, limite); })]);
      if (idEjecucion !== ejecucion) return;
      const imagenes = lang === "r" ? resultado.imagenes : resultado.imagen ? [resultado.imagen] : [];
      if (imagenes.length) grafico.replaceChildren();
      if (lang === "r") imagenes.forEach(img => { const canvas = document.createElement("canvas"); canvas.width = img.width; canvas.height = img.height; canvas.setAttribute("role", "img"); canvas.setAttribute("aria-label", `Gráfico creado con R: ${reto.titulo}`); canvas.getContext("2d").drawImage(img, 0, 0); grafico.appendChild(canvas); img.close?.(); });
      else if (imagenes.length) { const img = document.createElement("img"); img.src = `data:image/png;base64,${resultado.imagen}`; img.alt = `Gráfico creado con Python: ${reto.titulo}`; grafico.appendChild(img); }
      salida.textContent = `respuesta = ${mostrarRespuesta(resultado.respuesta)}${resultado.salida ? "\n\nSalida del programa:\n" + resultado.salida.slice(0, 2000) : ""}`;
      const previo = progreso[k] || {}, intentos = (previo.intentos || 0) + 1;
      const correcto = comprobarRespuesta(resultado.respuesta, reto.esperado) && (!reto.grafico || imagenes.length > 0);
      progreso[k] = { ...previo, intentos, hecho: previo.hecho || correcto };
      raiz.querySelector("[data-codigo-intentos]").textContent = `Intentos de comprobación: ${intentos}`;
      if (correcto) feedback.textContent = `✓ Correcto. ${reto.explicacion} ${reto.grafico ? "Podés cambiar el gráfico y ejecutar de nuevo." : "Podés explorar otros valores y ejecutar de nuevo."}`;
      else feedback.textContent = `↻ Todavía no. ${reto.grafico && !imagenes.length ? "Falta ejecutar el gráfico. " : ""}Compará tu resultado con la consigna y pedí una pista si la necesitás.`;
      memoria.resultados[k] = { codigo, respuesta: mostrarRespuesta(resultado.respuesta), salida: salida.textContent, feedback: feedback.textContent, correcto };
      guardarMemoria(usuarioId); pintarHistorial();
      animarResultado(raiz, feedback, correcto);
      refrescarEstado(); guardar(n, lang, progreso[k]);
    } catch (error) {
      if (idEjecucion === ejecucion) { const mensaje = String(error?.message || error).slice(0, 1000); salida.textContent = `Error de ejecución:\n${mensaje}`; feedback.textContent = "↻ Corregí el código y volvé a probar. Este error no cuenta como intento."; memoria.resultados[k] = { codigo, respuesta: null, salida: salida.textContent, feedback: feedback.textContent, correcto: false }; guardarMemoria(usuarioId); pintarHistorial(); animarResultado(raiz, feedback, false); }
    } finally { clearTimeout(reloj); if (idEjecucion === ejecucion) setOcupado(false); }
  });
}

export function cancelarCodigo() { ejecucion++; detener(); ocupado = false; }
