import { RETOS_CODIGO } from "./codigo-retos.mjs";

const borradores = new Map();
const idioma = new Map();
const pasoActivo = new Map();
const esc = x => String(x ?? "").replace(/[&<>"']/g, s => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[s]));
const retosDe = n => RETOS_CODIGO.filter(r => r.n === n).sort((a, b) => a.paso - b.paso);
const retoDe = n => retosDe(n).find(r => r.paso === (pasoActivo.get(n) || 1));
const clave = (reto, lang) => `${reto.id}_${lang}`;
const estado = (progreso, reto, lang) => progreso?.[clave(reto, lang)] || {};
export function codigoProgreso(progreso, n) {
  const retos = retosDe(n);
  return { done: retos.filter(r => ["r", "python"].some(lang => estado(progreso, r, lang).hecho)).length, items: retos.length };
}
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
function mostrarRespuesta(valor) {
  if (valor && typeof valor === "object" && Object.hasOwn(valor, "values")) valor = valor.values;
  if (Array.isArray(valor) && valor.length === 1) valor = valor[0];
  try { return JSON.stringify(valor) ?? String(valor); } catch { return String(valor); }
}
const tipoRespuesta = valor => Array.isArray(valor) ? `una lista de ${valor.length} valores` : typeof valor === "number" ? "un número" : "un texto";
function ejemplosBreves(grafico) {
  const r = grafico ? 'muestra <- c(3, 5, 7)\nrespuesta <- sum(muestra)\nbarplot(muestra, names.arg = c("A", "B", "C"))' : 'muestra <- c(3, 5, 7)\nrespuesta <- sum(muestra)';
  const python = grafico ? 'muestra = [3, 5, 7]\nrespuesta = sum(muestra)\nimport matplotlib.pyplot as plt\nplt.bar(["A", "B", "C"], muestra)' : 'muestra = [3, 5, 7]\nrespuesta = sum(muestra)';
  return `<div class="codigo-ayuda-grid"><div><strong>Ejemplo en R</strong><pre><code>${esc(r)}</code></pre></div><div><strong>Ejemplo en Python</strong><pre><code>${esc(python)}</code></pre></div></div>`;
}
function animarResultado(raiz, feedback, correcto) {
  feedback.classList.remove("codigo-ok", "codigo-error", "codigo-sacudir");
  feedback.classList.add(correcto ? "codigo-ok" : "codigo-error");
  const boton = raiz.querySelector("[data-codigo-run]");
  boton.classList.remove("codigo-ejecutar-error");
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (correcto) {
    const anterior = raiz.querySelector(".codigo-serpentina"); anterior?.remove();
    const serpentina = document.createElement("div"); serpentina.className = "codigo-serpentina"; serpentina.setAttribute("aria-hidden", "true");
    for (let i = 0; i < 12; i++) { const tira = document.createElement("span"); tira.style.left = `${5 + i * 8}%`; tira.style.animationDelay = `${i * 30}ms`; serpentina.appendChild(tira); }
    raiz.querySelector(".codigo-actions").appendChild(serpentina);
    setTimeout(() => serpentina.remove(), 1700);
  } else {
    void boton.offsetWidth;
    boton.classList.add("codigo-ejecutar-error");
    feedback.classList.add("codigo-sacudir");
    setTimeout(() => { boton.classList.remove("codigo-ejecutar-error"); feedback.classList.remove("codigo-sacudir"); }, 500);
  }
}

export function codigoHtml(n, progreso = {}) {
  const retos = retosDe(n), reto = retoDe(n); if (!reto) return "";
  const lang = idioma.get(n) || "python", codigo = borradores.get(clave(reto, lang)) ?? reto.codigo[lang];
  const actual = estado(progreso, reto, lang), avance = codigoProgreso(progreso, n);
  const resuelto = ["r", "python"].some(l => estado(progreso, reto, l).hecho);
  return `<section class="codigo-wrap" data-codigo-n="${n}" aria-labelledby="codigo-titulo-${n}">
    <h2 id="codigo-titulo-${n}">💻 Prácticas guiadas de código</h2>
    <div class="card codigo-card">
      <div class="codigo-head"><div><span class="tag" data-codigo-badge>Unidad ${n} · ${avance.done}/${avance.items} pasos resueltos</span><h3>Aprendé con R o Python, paso a paso</h3></div><span class="muted">10 pasos · reintentos ilimitados</span></div>
      <p class="codigo-intro">Elegí un paso y un lenguaje. Resolvé la consigna editando el código; podés repetir cada intento y pedir pistas. Completar un paso en cualquiera de los dos lenguajes suma al avance.</p>
      <div class="codigo-stepper" role="group" aria-label="Pasos de la unidad ${n}">${retos.map(r => {
        const ok = ["r", "python"].some(l => estado(progreso, r, l).hecho);
        return `<button type="button" data-codigo-paso="${r.paso}" class="codigo-paso ${r.paso === reto.paso ? "activo" : ""} ${ok ? "hecho" : ""}" aria-label="Paso ${r.paso}: ${esc(r.titulo)}${ok ? ", resuelto" : ""}" aria-current="${r.paso === reto.paso ? "step" : "false"}">${r.paso}${ok ? " ✓" : ""}</button>`;
      }).join("")}</div>
      <div class="codigo-step-head"><span class="tag">Paso ${reto.paso} de ${retos.length}</span><h3>${esc(reto.titulo)}</h3></div>
      <div class="codigo-consigna-box" role="group" aria-label="Consigna del paso ${reto.paso}"><strong class="codigo-consigna-etiqueta">🎯 Tu desafío</strong>
        <p class="codigo-consigna">${esc(reto.consigna)}</p>
        <p class="codigo-entrega"><strong>Para acertar:</strong> asigná ${tipoRespuesta(reto.esperado)} a <code>respuesta</code>${reto.grafico ? " y ejecutá el gráfico" : ""}. Podés volver a intentar cuantas veces necesites.</p>
      </div>
      ${reto.csv ? `<p class="muted">Datos de este paso: <a href="${esc(reto.csv)}" target="_blank" rel="noopener">${esc(reto.csv.split("/").pop())}</a>. Al ejecutar se cargan como <code>datos.csv</code>.</p>` : ""}
      <div class="codigo-tabs" role="tablist" aria-label="Lenguaje de programación"><button type="button" data-codigo-lang="python" role="tab" aria-selected="${lang === "python"}" class="btn ${lang === "python" ? "" : "sec"}">Python ${estado(progreso, reto, "python").hecho ? "✓" : ""}</button><button type="button" data-codigo-lang="r" role="tab" aria-selected="${lang === "r"}" class="btn ${lang === "r" ? "" : "sec"}">R ${estado(progreso, reto, "r").hecho ? "✓" : ""}</button></div>
      <div class="codigo-layout">
        <div class="codigo-editor-col"><label for="codigo-editor-${n}-${reto.paso}">Código ${lang === "r" ? "R" : "Python"} editable</label>
          <textarea id="codigo-editor-${n}-${reto.paso}" class="codigo-editor" spellcheck="false" autocapitalize="off" autocomplete="off" aria-describedby="codigo-ayuda-${n}">${esc(codigo)}</textarea>
          <p class="muted" id="codigo-ayuda-${n}">Reemplazá <code>${lang === "r" ? "NA" : "None"}</code> en la línea <code>respuesta</code>${reto.grafico ? " y activá el gráfico quitando # de sus líneas" : ""}. Después pulsá «Ejecutar y comprobar».</p>
          <div class="row codigo-actions"><button type="button" class="btn" data-codigo-run>▶ Ejecutar y comprobar</button><button type="button" class="btn sec" data-codigo-hint>💡 Pedir pista</button><button type="button" class="btn sec" data-codigo-help aria-expanded="false" aria-controls="codigo-mini-${n}-${reto.paso}">📘 Ayuda y ejemplos</button><button type="button" class="btn sec" data-codigo-reset>Restaurar ejemplo</button><button type="button" class="btn sec" data-codigo-stop hidden>Detener</button></div>
          <div class="codigo-ayuda-panel" id="codigo-mini-${n}-${reto.paso}" data-codigo-help-panel hidden><strong>Miniayuda: así se escribe una respuesta</strong>${reto.pistas?.[0] ? `<p><b>Orientación para este paso:</b> ${esc(reto.pistas[0])}</p>` : ""}<p>Estos ejemplos usan otros datos. Adaptá la idea a la consigna de arriba y reemplazá <code>${lang === "r" ? "NA" : "None"}</code> en tu editor.</p>${ejemplosBreves(reto.grafico)}</div>
          <p class="muted" data-codigo-intentos>Intentos de comprobación: ${actual.intentos || 0}</p>
          <div class="codigo-pista" data-codigo-pista role="status" aria-live="polite"></div>
        </div>
        <section class="codigo-resultados" aria-label="Resultados del código"><h4>Consola de resultados</h4>
          <pre class="codigo-salida" data-codigo-salida aria-live="polite">Ejecutá el código para ver aquí la respuesta y los mensajes.</pre>
          <div class="codigo-feedback ${actual.hecho ? "codigo-ok" : ""}" data-codigo-feedback role="status" aria-live="polite">${actual.hecho ? `✓ Paso resuelto. ${esc(reto.explicacion)}` : "Esperando tu primer intento en este lenguaje."}</div>
          <h4>Gráfico</h4><div class="codigo-grafico" data-codigo-grafico><p class="muted">${reto.grafico ? "Tu visualización aparecerá aquí." : "Este paso se resuelve sin gráfico."}</p></div>
        </section>
      </div>
      <button type="button" class="btn sec codigo-next" data-codigo-next ${resuelto && reto.paso < retos.length ? "" : "hidden"}>Siguiente paso →</button>
      <p class="muted codigo-nota">La comprobación es formativa y no modifica la nota oficial. El código se ejecuta en tu navegador.</p>
    </div></section>`;
}

export function enlazarCodigo(n, progreso, guardar) {
  const raiz = document.querySelector(`[data-codigo-n="${n}"]`); if (!raiz) return;
  const reto = retoDe(n), editor = raiz.querySelector(".codigo-editor"), feedback = raiz.querySelector("[data-codigo-feedback]"), pista = raiz.querySelector("[data-codigo-pista]"), salida = raiz.querySelector("[data-codigo-salida]"), grafico = raiz.querySelector("[data-codigo-grafico]"), run = raiz.querySelector("[data-codigo-run]"), stop = raiz.querySelector("[data-codigo-stop]"), siguiente = raiz.querySelector("[data-codigo-next]");
  const langActual = () => idioma.get(n) || "python";
  const guardarBorrador = () => borradores.set(clave(reto, langActual()), editor.value);
  const mostrarVacio = () => { grafico.replaceChildren(); const p = document.createElement("p"); p.className = "muted"; p.textContent = reto.grafico ? "Tu visualización aparecerá aquí." : "Este paso se resuelve sin gráfico."; grafico.appendChild(p); };
  const setOcupado = v => { ocupado = v; run.disabled = v; stop.hidden = !v; raiz.querySelectorAll("[data-codigo-paso], [data-codigo-lang], [data-codigo-next]").forEach(b => b.disabled = v); };
  const refrescarEstado = () => {
    const avance = codigoProgreso(progreso, n);
    raiz.querySelector("[data-codigo-badge]").textContent = `Unidad ${n} · ${avance.done}/${avance.items} pasos resueltos`;
    raiz.querySelectorAll("[data-codigo-lang]").forEach(b => { const l = b.dataset.codigoLang; b.textContent = `${l === "r" ? "R" : "Python"}${estado(progreso, reto, l).hecho ? " ✓" : ""}`; });
    const botonPaso = raiz.querySelector(`[data-codigo-paso="${reto.paso}"]`);
    const pasoResuelto = ["r", "python"].some(l => estado(progreso, reto, l).hecho);
    botonPaso.textContent = `${reto.paso}${pasoResuelto ? " ✓" : ""}`;
    botonPaso.classList.toggle("hecho", pasoResuelto);
    botonPaso.setAttribute("aria-label", `Paso ${reto.paso}: ${reto.titulo}${pasoResuelto ? ", resuelto" : ""}`);
    siguiente.hidden = reto.paso >= 10 || !["r", "python"].some(l => estado(progreso, reto, l).hecho);
  };
  editor.addEventListener("input", guardarBorrador);
  raiz.querySelectorAll("[data-codigo-paso]").forEach(b => b.addEventListener("click", () => {
    guardarBorrador(); pasoActivo.set(n, Number(b.dataset.codigoPaso));
    raiz.outerHTML = codigoHtml(n, progreso); enlazarCodigo(n, progreso, guardar);
  }));
  raiz.querySelectorAll("[data-codigo-lang]").forEach(b => b.addEventListener("click", () => {
    guardarBorrador(); idioma.set(n, b.dataset.codigoLang);
    raiz.outerHTML = codigoHtml(n, progreso);
    enlazarCodigo(n, progreso, guardar);
  }));
  siguiente.addEventListener("click", () => { guardarBorrador(); pasoActivo.set(n, reto.paso + 1); raiz.outerHTML = codigoHtml(n, progreso); enlazarCodigo(n, progreso, guardar); document.querySelector(`[data-codigo-n="${n}"] .codigo-step-head`)?.scrollIntoView({ behavior: "smooth", block: "start" }); });
  raiz.querySelector("[data-codigo-reset]").addEventListener("click", () => {
    editor.value = reto.codigo[langActual()]; guardarBorrador(); feedback.textContent = "Ejemplo restaurado. Probá otra vez."; feedback.classList.remove("codigo-ok", "codigo-error", "codigo-sacudir"); raiz.querySelector("[data-codigo-run]").classList.remove("codigo-ejecutar-error"); raiz.querySelector(".codigo-serpentina")?.remove(); salida.textContent = "Ejecutá el código para ver aquí la respuesta y los mensajes."; mostrarVacio();
  });
  const botonAyuda = raiz.querySelector("[data-codigo-help]"), panelAyuda = raiz.querySelector("[data-codigo-help-panel]");
  botonAyuda.addEventListener("click", () => { const abrir = panelAyuda.hidden; panelAyuda.hidden = !abrir; botonAyuda.setAttribute("aria-expanded", String(abrir)); botonAyuda.textContent = abrir ? "Cerrar ayuda y ejemplos" : "📘 Ayuda y ejemplos"; });
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
      const resultado = await Promise.race([tarea, new Promise((_, rechazar) => { reloj = setTimeout(() => { rechazar(new Error("La ejecución excedió 35 segundos. Revisá posibles bucles y reintentá.")); detener(); }, 35000); })]);
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
      animarResultado(raiz, feedback, correcto);
      refrescarEstado(); guardar(n, lang, progreso[k]);
    } catch (error) {
      if (idEjecucion === ejecucion) { const mensaje = String(error?.message || error).slice(0, 1000); salida.textContent = `Error de ejecución:\n${mensaje}`; feedback.textContent = "↻ Corregí el código y volvé a probar. Este error no cuenta como intento."; animarResultado(raiz, feedback, false); }
    } finally { clearTimeout(reloj); if (idEjecucion === ejecucion) setOcupado(false); }
  });
}

export function cancelarCodigo() { ejecucion++; detener(); ocupado = false; }
