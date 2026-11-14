/* Visibilidad de contenidos: el docente oculta o muestra cualquier elemento del aula.
   Por defecto todo está visible. La lista de ocultos vive en Firestore (ajustes/visibilidad) y se aplica al dibujar cada vista.
   OJO: es un control de interfaz, no de seguridad: el contenido sigue estando en los archivos del sitio. */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
const slug = s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 48);
const KED = "cvd_edicion";

export const VIS = { ocultos: {}, edicion: false, t: 0 };
let ctx = { B: null, esDoc: () => false, aviso: () => {}, repintar: () => {} };
export const iniciarVis = c => { ctx = { ...ctx, ...c }; try { VIS.edicion = localStorage.getItem(KED) === "1"; } catch {} };
export const cuantos = () => Object.keys(VIS.ocultos).length;

/* Rutas del menú que se pueden ocultar (Inicio, Mi perfil y Panel docente nunca). */
export const NAV_OCULTABLES = ["calendario", "clases", "datos", "tutor", "notas", "recursos", "sesion"];
export const claveRuta = (a, n) => NAV_OCULTABLES.includes(a) ? "nav:/" + a + (a === "sesion" ? "/" + n : "") : null;
export const rutaOculta = (a, n) => { const k = claveRuta(a, n); return !!(k && VIS.ocultos[k]); };

export async function cargarVis(forzar = false) {
  if (!ctx.B?.cargarVisibilidad) return;
  if (!forzar && Date.now() - VIS.t < 60000) return;
  try { VIS.ocultos = (await ctx.B.cargarVisibilidad()) || {}; VIS.t = Date.now(); } catch { VIS.ocultos = VIS.ocultos || {}; }
}

async function guardar(nuevo, previo) {
  VIS.ocultos = nuevo;
  try { await ctx.B.guardarVisibilidad(nuevo); VIS.t = Date.now(); return true; }
  catch (e) { VIS.ocultos = previo; ctx.aviso("No se pudo guardar el cambio: " + (e?.message || "error") + ". Revisá que las reglas de Firestore incluyan «ajustes».", "bad"); return false; }
}
async function alternar(clave, etiqueta) {
  const previo = VIS.ocultos, nuevo = { ...previo };
  if (nuevo[clave]) delete nuevo[clave]; else nuevo[clave] = String(etiqueta).slice(0, 120);
  if (await guardar(nuevo, previo)) { ctx.aviso(nuevo[clave] ? "Oculto para los estudiantes" : "Visible para los estudiantes"); ctx.repintar(); }
}
export async function mostrarTodo() { const previo = VIS.ocultos; if (await guardar({}, previo)) { ctx.aviso("Todo visible otra vez"); ctx.repintar(); } }
export function ponerEdicion(v) { VIS.edicion = !!v; try { localStorage.setItem(KED, v ? "1" : "0"); } catch {} }

/* ---------- menú lateral ---------- */
const PROTEGIDOS = new Set(["#/", "#/perfil", "#/docente"]);
export function aplicarNav() {
  const doc = ctx.esDoc();
  $$("#nav .vz-nav").forEach(w => { const a = w.querySelector("a"); w.replaceWith(a); });
  $$("#nav a").forEach(a => {
    a.classList.remove("vz-off"); a.hidden = false;
    const h = a.getAttribute("href"); if (!h || PROTEGIDOS.has(h)) return;
    const clave = "nav:" + h.replace(/^#/, ""), etiqueta = "Menú · " + a.textContent.replace(/\s+/g, " ").trim().replace(/\d+%|✅/g, "").trim();
    const off = !!VIS.ocultos[clave];
    if (off && !doc) { a.hidden = true; return; }
    if (off) a.classList.add("vz-off");
    if (doc && VIS.edicion) {
      const w = document.createElement("div"); w.className = "vz-nav"; a.replaceWith(w); w.appendChild(a); w.appendChild(boton(clave, etiqueta, off));
    }
  });
}

function boton(clave, etiqueta, off, tipo = "") {
  const b = document.createElement("button"); b.type = "button"; b.className = "vz-b " + tipo; b.dataset.vk = clave;
  b.title = off ? "Oculto para estudiantes: tocá para mostrar" : "Visible: tocá para ocultar a los estudiantes";
  b.setAttribute("aria-label", (off ? "Mostrar: " : "Ocultar: ") + etiqueta); b.textContent = off ? "🚫" : "👁";
  b.addEventListener("click", e => { e.preventDefault(); e.stopPropagation(); alternar(clave, etiqueta); });
  return b;
}

/* ---------- contenido de la vista ---------- */
const EDITABLES = new Set(["", "sesion", "calendario", "clases", "datos", "tutor", "recursos", "notas"]);
function agrupar(main) {
  if (main.querySelector(":scope > section.vz")) return;
  let cur = null;
  for (const k of [...main.children]) {
    if (k.hasAttribute("data-novis")) { cur = null; continue; }
    if (k.tagName === "H2") { cur = document.createElement("section"); cur.className = "vz"; main.insertBefore(cur, k); cur.appendChild(k); }
    else if (cur) cur.appendChild(k);
  }
}
function etiquetaDe(el) {
  const h = el.matches("section.vz") ? el.querySelector(":scope > h2") : el.querySelector("h1,h2,h3,b,strong");
  return (h?.textContent || el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 60) || "elemento";
}
export function aplicarMain(ruta) {
  const main = $("#main"); if (!main) return;
  $$(".vz-b, .vz-bar", main).forEach(x => x.parentNode.removeChild(x));
  $$(".vz-off, .vz-ed", main).forEach(x => x.classList.remove("vz-off", "vz-ed"));
  $$("[data-vk-hide]", main).forEach(x => { x.hidden = false; x.removeAttribute("data-vk-hide"); });
  const a = ruta.split("/")[1] || "", doc = ctx.esDoc();
  if (!EDITABLES.has(a)) return;
  agrupar(main);
  const cand = new Set($$("section.vz, .hero, .card, .grid > *, .vgrid > *, .kpis > *, .res > li", main));
  const usados = {};
  for (const el of cand) {
    if (el.closest(".deck-thumbs, #qf, .cal, .lb")) continue;
    const tipo = el.matches("section.vz") ? "sec" : el.matches("li") ? "li" : "bloque", et = etiquetaDe(el);
    const base = `${ruta || "/"}|${tipo}|${slug(et)}`; usados[base] = (usados[base] || 0) + 1;
    const clave = usados[base] > 1 ? `${base}~${usados[base]}` : base, off = !!VIS.ocultos[clave];
    if (off && !doc) { el.hidden = true; el.setAttribute("data-vk-hide", "1"); continue; }
    if (off) el.classList.add("vz-off");
    if (doc && VIS.edicion) { el.classList.add("vz-ed"); el.appendChild(boton(clave, et, off, tipo === "sec" ? "sec" : "")); }
  }
  if (doc && VIS.edicion) {
    const barra = document.createElement("div"); barra.className = "vz-bar card"; barra.setAttribute("role", "region"); barra.setAttribute("aria-label", "Modo edición de visibilidad");
    const lista = Object.entries(VIS.ocultos);
    barra.innerHTML = `<b>👁 Modo edición</b> · Tocá 👁 junto a cualquier sección, tarjeta o ítem para ocultarlo o mostrarlo a los estudiantes (vos siempre lo ves; lo oculto aparece atenuado con 🚫). Por defecto todo está visible.
      <div class="row" style="margin-top:.4rem"><span class="tag ${lista.length ? "warn" : "ok"}">${lista.length} oculto(s)</span><button type="button" class="btn sec sm" id="vzall" ${lista.length ? "" : "disabled"}>Mostrar todo</button></div>
      ${lista.length ? `<details><summary>Ver lista de ocultos</summary><ul class="res">${lista.map(([k, t]) => `<li><span>${esc(t || k)}</span><button type="button" class="btn sec sm" data-vzun="${esc(k)}">Mostrar</button></li>`).join("")}</ul></details>` : ""}`;
    main.insertBefore(barra, main.firstChild);
    $("#vzall", barra)?.addEventListener("click", () => mostrarTodo());
    $$("[data-vzun]", barra).forEach(b => b.addEventListener("click", () => alternar(b.dataset.vzun, "")));
  }
}

/* ---------- botón de la barra superior (solo docentes) ---------- */
export function botonEdicion() {
  let b = $("#edbtn"); const doc = ctx.esDoc();
  if (!doc) { b?.parentNode.removeChild(b); return; }
  if (!b) { b = document.createElement("button"); b.id = "edbtn"; b.type = "button"; b.className = "user"; b.title = "Ocultar o mostrar elementos del aula a los estudiantes";
    b.addEventListener("click", () => { ponerEdicion(!VIS.edicion); ctx.repintar(); }); $(".topbar")?.insertBefore(b, $("#fxbtn") || $("#user")); }
  b.textContent = VIS.edicion ? "👁 Edición: sí" : "👁 Edición: no"; b.setAttribute("aria-pressed", VIS.edicion);
}
