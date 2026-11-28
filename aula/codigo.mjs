import { RETOS_CODIGO } from "./codigo-retos.mjs";

const borradores = new Map();
const idioma = new Map();
const esc = x => String(x ?? "").replace(/[&<>"']/g, s => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[s]));
const clave = (n, lang) => `${n}_${lang}`;
const retoDe = n => RETOS_CODIGO.find(r => r.n === n);
let webR;
let webRPromesa;
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
  if (webR) { webR.close(); webR = null; webRPromesa = null; }
  if (pyWorker) { pyWorker.terminate(); pyWorker = null; }
}

async function ejecutarR(codigo, csv) {
  const r = await obtenerR();
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

export function codigoHtml(n, progreso = {}) {
  const reto = retoDe(n); if (!reto) return "";
  const lang = idioma.get(n) || "python", codigo = borradores.get(clave(n, lang)) ?? reto.codigo[lang];
  const hechos = ["r", "python"].filter(l => progreso?.[clave(n, l)]?.hecho).length;
  const actual = progreso?.[clave(n, lang)] || {};
  return `<section class="codigo-wrap" data-codigo-n="${n}" aria-labelledby="codigo-titulo-${n}">
    <h2 id="codigo-titulo-${n}">💻 Ensayo de código · R y Python</h2>
    <div class="card codigo-card"><div class="codigo-head"><div><span class="tag" data-codigo-badge>Unidad ${n} · ${hechos}/2 lenguajes resueltos</span><h3>${esc(reto.titulo)}</h3></div><span class="muted">Práctica formativa · reintentos ilimitados</span></div>
    <p>${esc(reto.consigna)}</p>
    ${reto.csv ? `<p class="muted">Archivo CSV sintético: <a href="${esc(reto.csv)}" target="_blank" rel="noopener">${esc(reto.csv.split("/").pop())}</a>. Se descarga al ejecutar y se monta como <code>datos.csv</code>.</p>` : ""}
    <div class="codigo-tabs" role="tablist" aria-label="Lenguaje de programación"><button type="button" data-codigo-lang="python" role="tab" aria-selected="${lang === "python"}" class="btn ${lang === "python" ? "" : "sec"}">Python ${progreso?.[clave(n, "python")]?.hecho ? "✓" : ""}</button><button type="button" data-codigo-lang="r" role="tab" aria-selected="${lang === "r"}" class="btn ${lang === "r" ? "" : "sec"}">R ${progreso?.[clave(n, "r")]?.hecho ? "✓" : ""}</button></div>
    <label for="codigo-editor-${n}">Editá el código ${lang === "r" ? "R" : "Python"}</label>
    <textarea id="codigo-editor-${n}" class="codigo-editor" spellcheck="false" autocapitalize="off" autocomplete="off" aria-describedby="codigo-ayuda-${n}">${esc(codigo)}</textarea>
    <p class="muted" id="codigo-ayuda-${n}">Reemplazá el valor pendiente de <code>respuesta</code>${reto.grafico ? " y descomentá las líneas del gráfico" : ""}. Se comprueba el resultado, no el texto del código.</p>
    <div class="row codigo-actions"><button type="button" class="btn" data-codigo-run>▶ Ejecutar y comprobar</button><button type="button" class="btn sec" data-codigo-hint>💡 Pedir pista</button><button type="button" class="btn sec" data-codigo-reset>Restaurar ejemplo</button><button type="button" class="btn sec" data-codigo-stop hidden>Detener</button></div>
    <p class="muted" data-codigo-intentos>Intentos de comprobación: ${actual.intentos || 0}</p>
    <div class="codigo-feedback" data-codigo-feedback role="status" aria-live="polite">${actual.hecho ? `✓ Resuelto. ${esc(reto.explicacion)}` : "Preparado para probar tu solución."}</div>
    <div class="codigo-pista" data-codigo-pista role="status" aria-live="polite"></div>
    <pre class="codigo-salida" data-codigo-salida hidden></pre><div class="codigo-grafico" data-codigo-grafico></div>
    <p class="muted codigo-nota">El código se ejecuta en tu navegador. La comprobación es orientativa y no modifica la nota oficial.</p>
    </div></section>`;
}

export function enlazarCodigo(n, progreso, guardar) {
  const raiz = document.querySelector(`[data-codigo-n="${n}"]`); if (!raiz) return;
  const reto = retoDe(n), editor = raiz.querySelector(".codigo-editor"), feedback = raiz.querySelector("[data-codigo-feedback]"), pista = raiz.querySelector("[data-codigo-pista]"), salida = raiz.querySelector("[data-codigo-salida]"), grafico = raiz.querySelector("[data-codigo-grafico]"), run = raiz.querySelector("[data-codigo-run]"), stop = raiz.querySelector("[data-codigo-stop]");
  const langActual = () => idioma.get(n) || "python";
  const guardarBorrador = () => borradores.set(clave(n, langActual()), editor.value);
  const refrescarEstado = () => {
    const hechos = ["r", "python"].filter(l => progreso[clave(n, l)]?.hecho).length;
    raiz.querySelector("[data-codigo-badge]").textContent = `Unidad ${n} · ${hechos}/2 lenguajes resueltos`;
    raiz.querySelectorAll("[data-codigo-lang]").forEach(b => { const l = b.dataset.codigoLang; b.textContent = `${l === "r" ? "R" : "Python"}${progreso[clave(n, l)]?.hecho ? " ✓" : ""}`; });
  };
  editor.addEventListener("input", guardarBorrador);
  raiz.querySelectorAll("[data-codigo-lang]").forEach(b => b.addEventListener("click", () => {
    guardarBorrador(); idioma.set(n, b.dataset.codigoLang);
    raiz.outerHTML = codigoHtml(n, progreso);
    enlazarCodigo(n, progreso, guardar);
  }));
  raiz.querySelector("[data-codigo-reset]").addEventListener("click", () => {
    editor.value = reto.codigo[langActual()]; guardarBorrador(); feedback.textContent = "Ejemplo restaurado. Probá otra vez."; salida.hidden = true; grafico.replaceChildren();
  });
  raiz.querySelector("[data-codigo-hint]").addEventListener("click", () => {
    const k = clave(n, langActual()), anterior = progreso[k] || {}, siguiente = Math.min(3, (anterior.pistas || 0) + 1);
    progreso[k] = { ...anterior, pistas: siguiente };
    pista.textContent = `Pista ${siguiente}/3: ${reto.pistas[siguiente - 1]}`;
    guardar(n, langActual(), progreso[k]);
  });
  stop.addEventListener("click", () => { ejecucion++; detener(); ocupado = false; run.disabled = false; stop.hidden = true; feedback.textContent = "Ejecución detenida. Podés corregir el código y volver a intentar."; });
  run.addEventListener("click", async () => {
    if (ocupado) return;
    const idEjecucion = ++ejecucion;
    const lang = langActual(), k = clave(n, lang), codigo = editor.value;
    if (codigo.length > 12000) { feedback.textContent = "El ensayo admite hasta 12.000 caracteres."; return; }
    guardarBorrador(); ocupado = true; run.disabled = true; stop.hidden = false;
    feedback.textContent = `Cargando ${lang === "r" ? "R" : "Python"} y ejecutando el código…`; pista.textContent = ""; salida.hidden = true; grafico.replaceChildren();
    let reloj;
    try {
      let csv = null;
      if (reto.csv) {
        const respuesta = await fetch(new URL(reto.csv, import.meta.url));
        if (!respuesta.ok) throw new Error(`No se pudo cargar el CSV (${respuesta.status}).`);
        csv = await respuesta.text();
      }
      const tarea = lang === "r" ? ejecutarR(codigo, csv) : ejecutarPython(codigo, csv, reto.grafico);
      const resultado = await Promise.race([tarea, new Promise((_, rechazar) => { reloj = setTimeout(() => { rechazar(new Error("La ejecución excedió 35 segundos. Revisá posibles bucles y reintentá.")); detener(); }, 35000); })]);
      if (idEjecucion !== ejecucion) return;
      const imagenes = lang === "r" ? resultado.imagenes : resultado.imagen ? [resultado.imagen] : [];
      if (lang === "r") imagenes.forEach(img => { const canvas = document.createElement("canvas"); canvas.width = img.width; canvas.height = img.height; canvas.setAttribute("role", "img"); canvas.setAttribute("aria-label", `Gráfico creado con R: ${reto.titulo}`); canvas.getContext("2d").drawImage(img, 0, 0); grafico.appendChild(canvas); img.close?.(); });
      else if (imagenes.length) { const img = document.createElement("img"); img.src = `data:image/png;base64,${resultado.imagen}`; img.alt = `Gráfico creado con Python: ${reto.titulo}`; grafico.appendChild(img); }
      if (resultado.salida) { salida.textContent = resultado.salida.slice(0, 2000); salida.hidden = false; }
      const previo = progreso[k] || {}, intentos = (previo.intentos || 0) + 1;
      const correcto = comprobarRespuesta(resultado.respuesta, reto.esperado) && (!reto.grafico || imagenes.length > 0);
      progreso[k] = { ...previo, intentos, hecho: previo.hecho || correcto };
      raiz.querySelector("[data-codigo-intentos]").textContent = `Intentos de comprobación: ${intentos}`;
      if (correcto) feedback.textContent = `✓ Correcto. ${reto.explicacion} ${reto.grafico ? "Podés cambiar el gráfico y ejecutar de nuevo." : "Podés explorar otros valores y ejecutar de nuevo."}`;
      else feedback.textContent = `Todavía no. ${reto.grafico && !imagenes.length ? "Falta ejecutar el gráfico. " : ""}Revisá la variable respuesta y pedí una pista si la necesitás.`;
      refrescarEstado(); guardar(n, lang, progreso[k]);
    } catch (error) {
      if (idEjecucion === ejecucion) feedback.textContent = `Error de ejecución: ${String(error?.message || error).slice(0, 1000)} Corregí el código y volvé a probar; este error no cuenta como intento.`;
    } finally { clearTimeout(reloj); if (idEjecucion === ejecucion) { ocupado = false; run.disabled = false; stop.hidden = true; } }
  });
}

export const codigosPorSesion = n => ["r", "python"].map(lang => clave(n, lang));
