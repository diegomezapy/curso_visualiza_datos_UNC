/**
 * Diagnóstico inicial · Visualización de Datos (MICD · FACET – UNC)
 * Google Apps Script: recibe las respuestas del cuestionario, las guarda en una hoja de cálculo
 * y publica (1) un tablero interactivo y (2) una API de datos anonimizados (JSON/CSV).
 *
 * Archivos del proyecto: Code.gs (este), Preguntas.gs (generado), Tablero.html (generado), appsscript.json
 * Instrucciones paso a paso: docs/diagnostico_appsscript.md
 */

const HOJA = 'Respuestas';
const MAX_FILAS = 3000;          // tope de seguridad
const ZONA = 'America/Asuncion';

/** Propiedades del script (Configuración del proyecto → Propiedades del script):
 *  CODIGO_CLASE  → código que el docente anuncia en clase (obligatorio)
 *  SHEET_ID      → ID de la hoja de cálculo (opcional si el script está vinculado a la hoja) */
const CODIGO_POR_DEFECTO = '';      // (opcional) código de clase si no se define la propiedad CODIGO_CLASE
const SHEET_ID_POR_DEFECTO = '';   // (opcional) ID de la hoja si el script no está vinculado a ella
function prop_(k) {
  const v = PropertiesService.getScriptProperties().getProperty(k) || '';
  return v || (k === 'CODIGO_CLASE' ? CODIGO_POR_DEFECTO : k === 'SHEET_ID' ? SHEET_ID_POR_DEFECTO : '');
}

function hoja_() {
  const id = prop_('SHEET_ID');
  const ss = id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(HOJA);
  if (!sh) {   // reutiliza la hoja en blanco recién creada si existe
    const hojas = ss.getSheets();
    if (hojas.length === 1 && hojas[0].getLastRow() === 0) { sh = hojas[0]; sh.setName(HOJA); } else sh = ss.insertSheet(HOJA);
  }
  if (sh.getLastRow() === 0) { sh.appendRow(COLUMNAS); sh.setFrozenRows(1); }
  return sh;
}

/** Ejecutar UNA vez desde el editor (autoriza permisos y deja la hoja lista). */
function configurar() {
  const sh = hoja_();
  prepararLooker();
  Logger.log('Hoja lista: ' + sh.getParent().getUrl());
  Logger.log('CODIGO_CLASE ' + (prop_('CODIGO_CLASE') ? 'configurado' : 'FALTA: defínalo en Propiedades del script'));
}

/** Crea la pestaña "Looker": vista anonimizada (sin pid ni comentario) para conectar Looker Studio.
 *  Looker Studio → Crear → Fuente de datos → Hojas de cálculo de Google → pestaña "Looker". */
function prepararLooker() {
  const id = prop_('SHEET_ID');
  const ss = id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActive();
  const sh = ss.getSheetByName('Looker') || ss.insertSheet('Looker');
  const letras = PUBLICAS.map(function (c) { return letra_(COLUMNAS.indexOf(c) + 1); }).join(',');
  sh.getRange('A1').setFormula('=QUERY(' + HOJA + '!A:' + letra_(COLUMNAS.length) + ',"select ' + letras + '",1)');
}
function letra_(n) { var s = ''; while (n > 0) { var m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; }

/* ---------- recepción de respuestas ---------- */
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    const p = JSON.parse(e.postData.contents);
    const err = validar_(p, prop_('CODIGO_CLASE'));
    if (err) return json_({ ok: false, error: err });
    lock.waitLock(20000);
    const sh = hoja_();
    const n = sh.getLastRow();
    if (n > MAX_FILAS) return json_({ ok: false, error: 'limite' });
    if (n > 1) {
      const pids = sh.getRange(2, COLUMNAS.indexOf('pid') + 1, n - 1, 1).getValues().map(function (r) { return r[0]; });
      if (pids.indexOf(p.pid) >= 0) return json_({ ok: true, duplicado: true });
    }
    sh.appendRow(construirFila_(p, new Date()));
    return json_({ ok: true });
  } catch (x) {
    return json_({ ok: false, error: 'formato' });
  } finally {
    try { lock.releaseLock(); } catch (_) {}
  }
}

/** Valida el envío. Devuelve '' si es válido o un código de error. (Función pura: probada fuera de Google.) */
function validar_(p, codigoClase) {
  if (!codigoClase) return 'servidor_sin_codigo';
  if (!p || typeof p !== 'object') return 'formato';
  if (p.codigo !== codigoClase) return 'codigo';
  if (!/^P-[A-Z0-9]{5}$/.test(p.pid || '')) return 'pid';
  if (AREAS.indexOf(p.area) < 0) return 'area';
  if (EXPERIENCIA.indexOf(p.experiencia) < 0) return 'experiencia';
  if (!Array.isArray(p.herramientas) || p.herramientas.some(function (h) { return HERRAMIENTAS.indexOf(h) < 0; })) return 'herramientas';
  if (typeof p.cohorte !== 'string' || p.cohorte.length > 40) return 'cohorte';
  for (var i = 0; i < AUTO_IDS.length; i++) {
    var v = p.auto && p.auto[AUTO_IDS[i]];
    if (!(v === 1 || v === 2 || v === 3 || v === 4 || v === 5)) return 'auto';
  }
  for (var j = 0; j < CLAVE_IDS.length; j++) {
    if (['A', 'B', 'C', 'D', 'NS'].indexOf(p.resp && p.resp[CLAVE_IDS[j]]) < 0) return 'resp';
  }
  if (p.comentario != null && (typeof p.comentario !== 'string' || p.comentario.length > 280)) return 'comentario';
  return '';
}

/** Evita que un texto sea interpretado como fórmula en la hoja. */
function limpiar_(s) { s = String(s == null ? '' : s).trim(); return /^[=+\-@]/.test(s) ? "'" + s : s; }

function fechaTxt_(d) {
  if (typeof Utilities !== 'undefined') return Utilities.formatDate(d, ZONA, 'yyyy-MM-dd HH:mm:ss');
  return d.toISOString().replace('T', ' ').slice(0, 19);
}

/** Construye la fila en el orden de COLUMNAS; el puntaje se calcula aquí (no se confía en el navegador). */
function construirFila_(p, ahora) {
  const fila = { ts: fechaTxt_(ahora), pid: p.pid, area: p.area, cohorte: limpiar_(p.cohorte), experiencia: p.experiencia,
                 herramientas: p.herramientas.join('; '), comentario: limpiar_(p.comentario) };
  AUTO_IDS.forEach(function (id) { fila[id] = p.auto[id]; });
  const sc = { viz: 0, py: 0, r: 0 };
  CLAVE_IDS.forEach(function (id) {
    var letra = p.resp[id], ok = letra === CLAVE[id].c ? 1 : 0;
    fila['a_' + id] = letra; fila['ok_' + id] = ok; sc[CLAVE[id].t] += ok;
  });
  const total = sc.viz + sc.py + sc.r;
  fila.score_viz = sc.viz; fila.score_py = sc.py; fila.score_r = sc.r; fila.score_total = total;
  fila.nivel = total <= 4 ? 'Inicial' : total <= 8 ? 'Intermedio' : 'Avanzado';
  return COLUMNAS.map(function (c) { return fila[c] === undefined ? '' : fila[c]; });
}

/* ---------- lectura: tablero y API ---------- */
function doGet(e) {
  const p = (e && e.parameter) || {}, a = p.action || '', pg = p.page || '';
  if (a === 'datos') return json_(datos_());
  if (a === 'agenda') return json_(agendaPublica_());
  if (pg === 'asistencia' || pg === 'mini') {
    const t = HtmlService.createTemplateFromFile(pg === 'asistencia' ? 'Asistencia' : 'MiniEval');
    t.e = p.e || ''; t.u = p.u || ''; t.t = p.t || '';
    return t.evaluate().setTitle(pg === 'asistencia' ? 'Registro de asistencia' : 'Mini-evaluación')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1').setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }
  if (a === 'csv') return ContentService.createTextOutput(csv_()).setMimeType(ContentService.MimeType.CSV);
  return HtmlService.createHtmlOutputFromFile('Tablero')
    .setTitle('Tablero · Diagnóstico inicial')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/** Datos anonimizados (sin pid ni comentario). También lo invoca el tablero con google.script.run. */
function getDatos() { return datos_(); }
function datos_() {
  const sh = hoja_(), n = sh.getLastRow();
  const idx = PUBLICAS.map(function (c) { return COLUMNAS.indexOf(c); });
  var filas = [];
  if (n > 1) {
    filas = sh.getRange(2, 1, n - 1, COLUMNAS.length).getValues().map(function (r) {
      return idx.map(function (i) { var v = r[i]; return v instanceof Date ? fechaTxt_(v) : v; });
    });
  }
  return { columnas: PUBLICAS, filas: filas, actualizado: new Date().toISOString() };
}
function csv_() {
  const d = datos_();
  const esc = function (v) { return '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"'; };
  return [d.columnas.map(esc).join(',')].concat(d.filas.map(function (f) { return f.map(esc).join(','); })).join('\n');
}
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
