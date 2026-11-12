/**
 * Agenda, asistencia con ventana horaria y mini-evaluaciones por correo.
 * Pestañas de la hoja: Agenda · Estudiantes · Asistencia · MiniEval · Config · Resumen
 * Envíos automáticos mediante un activador de tiempo (procesarEnvios, cada minuto).
 * Instrucciones: docs/agenda_asistencia_appsscript.md
 */

const HOJA_AGENDA = 'Agenda', HOJA_EST = 'Estudiantes', HOJA_ASIST = 'Asistencia', HOJA_MINI = 'MiniEval', HOJA_CFG = 'Config', HOJA_RES = 'Resumen';
const COL_AGENDA = ['id', 'fecha', 'inicio', 'fin', 'tipo', 'titulo', 'sesion', 'enlace', 'descripcion', 'asistencia', 'mini', 'enviado_asistencia', 'enviado_mini'];
const COL_EST = ['email', 'nombre', 'activo'];
const COL_ASIST = ['ts', 'evento_id', 'email', 'nombre', 'titulo'];
const COL_MINI = ['ts', 'evento_id', 'email', 'sesion', 'aciertos', 'total', 'respuestas'];
const TIPOS = ['clase', 'tutoria', 'entrega', 'evaluacion', 'otro'];
const GRACIA_MIN = 15;            // minutos después del fin en que todavía se acepta la asistencia
const MINI_HORAS_EXTRA = 12;      // el correo de mini-evaluación se envía hasta N horas después del fin
const MINI_VALIDEZ_HORAS = 72;    // la mini-evaluación se puede responder hasta N horas después del fin
const N_MINI = 3;                 // preguntas por mini-evaluación

function ss_() { const id = prop_('SHEET_ID'); return id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActive(); }
function tab_(nombre, cols) {
  const ss = ss_(); let sh = ss.getSheetByName(nombre);
  if (!sh) sh = ss.insertSheet(nombre);
  if (sh.getLastRow() === 0 && cols) { sh.appendRow(cols); sh.setFrozenRows(1); }
  return sh;
}

/* ---------- configuración inicial (ejecutar UNA vez desde el editor) ---------- */
function configurarTodo() {
  configurar();
  const ag = tab_(HOJA_AGENDA, COL_AGENDA); tab_(HOJA_EST, COL_EST); tab_(HOJA_ASIST, COL_ASIST); tab_(HOJA_MINI, COL_MINI);
  const cfg = tab_(HOJA_CFG, ['clave', 'valor']);
  if (cfg.getLastRow() < 2) {
    [['PUBLICAR_ENLACES', 'NO'], ['hora_inicio', '18:00'], ['hora_fin', '22:00'], ['dias_entrega', '7'],
      ['clase_1', '2026-11-13'], ['clase_2', '2026-11-14'], ['hora_inicio_2', '08:00'], ['hora_fin_2', '12:00'],
      ['clase_3', '2026-11-20'], ['clase_4', '2026-11-21'], ['hora_inicio_4', '08:00'], ['hora_fin_4', '12:00'],
      ['clase_5', '2026-11-27'], ['clase_6', '2026-11-28'], ['hora_inicio_6', '08:00'], ['hora_fin_6', '12:00'],
      ['clase_7', '2026-12-04'], ['clase_8', '2026-12-05'], ['hora_inicio_8', '08:00'], ['hora_fin_8', '12:00']].forEach(function (r) { cfg.appendRow(r); });
  }
  try { ag.getRange('B2:D500').setNumberFormat('@'); } catch (e) {}          // fecha y horas como texto
  if (!prop_('SECRETO')) PropertiesService.getScriptProperties().setProperty('SECRETO', Utilities.getUuid() + Utilities.getUuid());
  activarEnvios(1);
  Logger.log('Listo. Cargue Estudiantes y Agenda (o use generarAgendaBase) y publique la aplicación web.');
}

/** Crea el activador que revisa la agenda cada N minutos (1, 5, 10, 15 o 30). */
function activarEnvios(minutos) {
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'procesarEnvios') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('procesarEnvios').timeBased().everyMinutes(minutos || 1).create();
}

/** Genera la agenda base: una clase por sesión (en Config: clase_1 … clase_8 = fechas yyyy-mm-dd) + su entrega. */
function generarAgendaBase() {
  const cfg = {}; tab_(HOJA_CFG).getDataRange().getValues().forEach(function (r) { cfg[r[0]] = r[1]; });
  const ag = tab_(HOJA_AGENDA, COL_AGENDA);
  const titulos = ['Principios y percepción', 'Elección de gráficos', 'Color, diseño y ética', 'KPIs y storytelling', 'Dashboards interactivos', 'Reporting automatizado', 'Estructuras complejas', 'Redes e integrador'];
  const existentes = ag.getLastRow() > 1 ? ag.getRange(2, 1, ag.getLastRow() - 1, 1).getValues().map(function (r) { return r[0]; }) : [];
  for (var n = 1; n <= 8; n++) {
    var f = txtFecha_(cfg['clase_' + n]); if (!f) continue;
    if (existentes.indexOf('clase-' + n) < 0) ag.appendRow(['clase-' + n, f, cfg['hora_inicio_' + n] || cfg.hora_inicio || '18:00', cfg['hora_fin_' + n] || cfg.hora_fin || '22:00', 'clase', 'Sesión ' + n + ' · ' + titulos[n - 1], n, '', '', 'SI', 'SI', '', '']);
    if (existentes.indexOf('entrega-' + n) < 0) ag.appendRow(['entrega-' + n, sumarDias_(f, +cfg.dias_entrega || 7), '23:00', '23:59', 'entrega', 'Entrega de actividades · Sesión ' + n, n, '', 'Publicar en RPubs/Colab y pegar el enlace en el aula', 'NO', 'NO', '', '']);
  }
}
function sumarDias_(fechaTxt, dias) { const d = Utilities.parseDate(fechaTxt + ' 12:00', ZONA, 'yyyy-MM-dd HH:mm'); d.setTime(d.getTime() + dias * 86400000); return Utilities.formatDate(d, ZONA, 'yyyy-MM-dd'); }

/* ---------- utilidades de fecha y token ---------- */
function txtFecha_(v) { return v instanceof Date ? Utilities.formatDate(v, ZONA, 'yyyy-MM-dd') : String(v || '').trim().slice(0, 10); }
function txtHora_(v) { return v instanceof Date ? Utilities.formatDate(v, ZONA, 'HH:mm') : String(v || '').trim().slice(0, 5); }
function aDate_(f, h) { return Utilities.parseDate(f + ' ' + h, ZONA, 'yyyy-MM-dd HH:mm'); }
function isoZona_(d) { return Utilities.formatDate(d, ZONA, "yyyy-MM-dd'T'HH:mm:ssXXX"); }

function token_(eventoId, email) {
  const sig = Utilities.computeHmacSha256Signature(String(eventoId) + '|' + String(email).toLowerCase(), prop_('SECRETO'));
  return Utilities.base64EncodeWebSafe(sig).replace(/=+$/, '').slice(0, 22);
}
function tokenValido_(eventoId, email, t) { return !!t && !!email && token_(eventoId, email) === t; }

function leerAgenda_() {
  const sh = tab_(HOJA_AGENDA, COL_AGENDA), n = sh.getLastRow();
  if (n < 2) return [];
  return sh.getRange(2, 1, n - 1, COL_AGENDA.length).getValues().map(function (r, i) {
    var o = { fila: i + 2 }; COL_AGENDA.forEach(function (c, k) { o[c] = r[k]; });
    o.fecha = txtFecha_(o.fecha); o.inicio = txtHora_(o.inicio); o.fin = txtHora_(o.fin);
    o.asistencia = String(o.asistencia || '').toUpperCase() === 'SI'; o.mini = String(o.mini || '').toUpperCase() === 'SI';
    try { o.t0 = aDate_(o.fecha, o.inicio || '00:00'); o.t1 = aDate_(o.fecha, o.fin || o.inicio || '23:59'); } catch (e) { o.t0 = o.t1 = null; }
    return o;
  }).filter(function (o) { return o.id && o.t0 && o.t1; });
}
function estudiantes_() {
  const sh = tab_(HOJA_EST, COL_EST), n = sh.getLastRow();
  if (n < 2) return [];
  return sh.getRange(2, 1, n - 1, 3).getValues().map(function (r) { return { email: String(r[0] || '').trim().toLowerCase(), nombre: String(r[1] || '').trim(), activo: String(r[2] || 'SI').toUpperCase() !== 'NO' }; })
    .filter(function (e) { return e.email && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e.email) && e.activo; });
}
function marcar_(e, col, valor) { tab_(HOJA_AGENDA).getRange(e.fila, COL_AGENDA.indexOf(col) + 1).setValue(valor); }

/* ---------- envíos automáticos ---------- */
function urlApp_() { return ScriptApp.getService().getUrl(); }
function enlaceEvento_(pagina, e, est) { return urlApp_() + '?page=' + pagina + '&e=' + encodeURIComponent(e.id) + '&u=' + encodeURIComponent(est.email) + '&t=' + token_(e.id, est.email); }
function saludo_(est) { return est.nombre ? 'Hola ' + est.nombre.split(' ')[0] + ',' : 'Hola,'; }
function boton_(url, texto) { return '<p><a href="' + url + '" style="background:#0072B2;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:bold;display:inline-block">' + texto + '</a></p>'; }

function correoAsistencia_(e, est) {
  const cuerpo = '<div style="font-family:Arial,sans-serif;max-width:520px"><p>' + saludo_(est) + '</p>' +
    '<p>Comenzó <b>' + e.titulo + '</b> (' + e.inicio + '–' + e.fin + ').</p>' +
    (e.enlace ? '<p>Enlace de la sesión: <a href="' + e.enlace + '">' + e.enlace + '</a></p>' : '') +
    '<p>Registrá tu <b>asistencia de hoy</b>. El formulario solo funciona durante el horario de la clase (hasta ' + GRACIA_MIN + ' minutos después de que termine).</p>' +
    boton_(enlaceEvento_('asistencia', e, est), 'Registrar mi asistencia') +
    '<p style="color:#666;font-size:12px">Este enlace es personal; no lo compartas. Visualización de Datos · MICD · FACET – UNC</p></div>';
  return { asunto: '📍 Asistencia: ' + e.titulo, cuerpo: cuerpo };
}
function correoMini_(e, est) {
  const cuerpo = '<div style="font-family:Arial,sans-serif;max-width:520px"><p>' + saludo_(est) + '</p>' +
    '<p>Gracias por participar en <b>' + e.titulo + '</b>. Respondé una <b>mini-evaluación de ' + N_MINI + ' preguntas (2 minutos)</b> sobre lo visto hoy.</p>' +
    '<p><b>No suma puntos</b> para la certificación: es solo para que vos y el docente sepan qué reforzar.</p>' +
    boton_(enlaceEvento_('mini', e, est), 'Responder la mini-evaluación') +
    '<p style="color:#666;font-size:12px">Disponible durante ' + MINI_VALIDEZ_HORAS + ' horas. Visualización de Datos · MICD · FACET – UNC</p></div>';
  return { asunto: '📝 Mini-evaluación (sin nota): ' + e.titulo, cuerpo: cuerpo };
}

/** Envía un correo a cada estudiante hasta agotar la cuota diaria. Devuelve {enviados, total}. */
function enviarLote_(e, lista, armar) {
  var enviados = 0;
  for (var i = 0; i < lista.length; i++) {
    if (MailApp.getRemainingDailyQuota() < 1) break;
    var c = armar(e, lista[i]);
    try { MailApp.sendEmail({ to: lista[i].email, subject: c.asunto, htmlBody: c.cuerpo, name: 'Visualización de Datos · UNC' }); enviados++; } catch (x) { Logger.log('Fallo ' + lista[i].email + ': ' + x); }
  }
  return { enviados: enviados, total: lista.length };
}

/** Lo ejecuta el activador de tiempo. Cada envío ocurre una sola vez por evento (se marca en la hoja). */
function procesarEnvios(ahoraOpc) {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return;
  try {
    const ahora = (ahoraOpc && typeof ahoraOpc.getTime === 'function') ? ahoraOpc : new Date(), lista = estudiantes_();
    leerAgenda_().forEach(function (e) {
      if (e.asistencia && !e.enviado_asistencia && ahora >= e.t0 && ahora <= new Date(e.t1.getTime() + GRACIA_MIN * 60000)) {
        marcar_(e, 'enviado_asistencia', 'enviando ' + isoZona_(ahora));
        var r = enviarLote_(e, lista, correoAsistencia_);
        marcar_(e, 'enviado_asistencia', isoZona_(ahora) + ' · ' + r.enviados + '/' + r.total);
      }
      if (e.mini && !e.enviado_mini && ahora >= e.t1 && ahora <= new Date(e.t1.getTime() + MINI_HORAS_EXTRA * 3600000)) {
        marcar_(e, 'enviado_mini', 'enviando ' + isoZona_(ahora));
        var r2 = enviarLote_(e, lista, correoMini_);
        marcar_(e, 'enviado_mini', isoZona_(ahora) + ' · ' + r2.enviados + '/' + r2.total);
      }
    });
  } finally { lock.releaseLock(); }
}

/** Prueba: envía los dos correos del primer evento a la cuenta del docente. */
function enviarPrueba() {
  const yo = Session.getActiveUser().getEmail(), e = leerAgenda_()[0];
  if (!e) throw new Error('No hay eventos en la pestaña Agenda.');
  const est = { email: yo, nombre: 'Docente' };
  [correoAsistencia_, correoMini_].forEach(function (f) { var c = f(e, est); MailApp.sendEmail({ to: yo, subject: '[PRUEBA] ' + c.asunto, htmlBody: c.cuerpo }); });
}

/* ---------- asistencia (la invoca la página Asistencia.html con google.script.run) ---------- */
function registrarAsistencia(eventoId, email, t, ahoraOpc) {
  email = String(email || '').toLowerCase();
  if (!tokenValido_(eventoId, email, t)) return { ok: false, msg: 'El enlace no es válido. Usá el enlace del correo que recibiste.' };
  const e = leerAgenda_().filter(function (x) { return x.id === eventoId; })[0];
  if (!e || !e.asistencia) return { ok: false, msg: 'Este evento no tiene registro de asistencia.' };
  const est = estudiantes_().filter(function (x) { return x.email === email; })[0];
  if (!est) return { ok: false, msg: 'Tu correo no figura en la lista del curso. Avisá al docente.' };
  const ahora = ahoraOpc || new Date(), cierre = new Date(e.t1.getTime() + GRACIA_MIN * 60000);
  if (ahora < e.t0) return { ok: false, msg: 'Todavía no comenzó. El registro se abre a las ' + e.inicio + ' (' + e.fecha + ').' };
  if (ahora > cierre) return { ok: false, msg: 'El registro de asistencia ya cerró (era para el ' + e.fecha + ' de ' + e.inicio + ' a ' + e.fin + ').' };
  const sh = tab_(HOJA_ASIST, COL_ASIST), n = sh.getLastRow();
  if (n > 1) {
    var previos = sh.getRange(2, 2, n - 1, 2).getValues();
    for (var i = 0; i < previos.length; i++) if (previos[i][0] === e.id && String(previos[i][1]).toLowerCase() === email) return { ok: true, ya: true, msg: 'Tu asistencia ya estaba registrada. ¡Gracias!' };
  }
  sh.appendRow([isoZona_(ahora), e.id, email, est.nombre, e.titulo]);
  return { ok: true, msg: '✅ Asistencia registrada: ' + e.titulo + '.' };
}

/* ---------- mini-evaluación ---------- */
function preguntasMini_(e) {
  const banco = BANCO[String(e.sesion)] || [];
  if (!banco.length) return [];
  var semilla = 0; String(e.id).split('').forEach(function (ch) { semilla = (semilla * 31 + ch.charCodeAt(0)) % 997; });
  var out = []; for (var i = 0; i < Math.min(N_MINI, banco.length); i++) out.push((semilla + i) % banco.length);
  return out;
}
function eventoMini_(eventoId, email, t, ahoraOpc) {
  email = String(email || '').toLowerCase();
  if (!tokenValido_(eventoId, email, t)) return { error: 'El enlace no es válido. Usá el enlace del correo que recibiste.' };
  const e = leerAgenda_().filter(function (x) { return x.id === eventoId; })[0];
  if (!e || !e.mini) return { error: 'Este evento no tiene mini-evaluación.' };
  const ahora = ahoraOpc || new Date();
  if (ahora < e.t0) return { error: 'Todavía no está disponible.' };
  if (ahora > new Date(e.t1.getTime() + MINI_VALIDEZ_HORAS * 3600000)) return { error: 'La mini-evaluación ya cerró.' };
  return { e: e, email: email };
}
/** Devuelve las preguntas SIN la respuesta correcta. */
function getMini(eventoId, email, t, ahoraOpc) {
  const r = eventoMini_(eventoId, email, t, ahoraOpc); if (r.error) return { ok: false, msg: r.error };
  const banco = BANCO[String(r.e.sesion)] || [];
  return { ok: true, titulo: r.e.titulo, preguntas: preguntasMini_(r.e).map(function (i) { return { i: i, q: banco[i].q, o: banco[i].o }; }) };
}
/** resp = { "<índice de pregunta>": <índice de opción>, ... } → corrige en el servidor y guarda. No suma puntos. */
function enviarMini(eventoId, email, t, resp, ahoraOpc) {
  const r = eventoMini_(eventoId, email, t, ahoraOpc); if (r.error) return { ok: false, msg: r.error };
  const banco = BANCO[String(r.e.sesion)] || [], idx = preguntasMini_(r.e);
  var aciertos = 0, detalle = [];
  idx.forEach(function (i) { var sel = resp && resp[i], ok = sel === banco[i].c; if (ok) aciertos++; detalle.push({ i: i, ok: ok, correcta: banco[i].c, why: banco[i].why }); });
  const sh = tab_(HOJA_MINI, COL_MINI), n = sh.getLastRow();
  var ya = false;
  if (n > 1) sh.getRange(2, 2, n - 1, 2).getValues().forEach(function (f) { if (f[0] === r.e.id && String(f[1]).toLowerCase() === r.email) ya = true; });
  if (!ya) sh.appendRow([isoZona_(ahoraOpc || new Date()), r.e.id, r.email, r.e.sesion, aciertos, idx.length, JSON.stringify(resp || {})]);
  return { ok: true, aciertos: aciertos, total: idx.length, detalle: detalle, repetida: ya, msg: ya ? 'Ya habías respondido: se conserva tu primera respuesta.' : '' };
}

/* ---------- agenda pública para el calendario del aula ---------- */
function agendaPublica_() {
  const conEnlace = String((tab_(HOJA_CFG).getDataRange().getValues().filter(function (r) { return r[0] === 'PUBLICAR_ENLACES'; })[0] || [])[1]).toUpperCase() === 'SI';
  return { zona: ZONA, actualizado: new Date().toISOString(), eventos: leerAgenda_().map(function (e) {
    var o = { id: e.id, tipo: e.tipo, titulo: e.titulo, sesion: e.sesion || null, fecha: e.fecha, inicio: e.inicio, fin: e.fin, inicio_iso: isoZona_(e.t0), fin_iso: isoZona_(e.t1), descripcion: e.descripcion || '', asistencia: e.asistencia, mini: e.mini };
    if (conEnlace && e.enlace) o.enlace = e.enlace;
    return o;
  }).sort(function (a, b) { return a.inicio_iso < b.inicio_iso ? -1 : 1; }) };
}
function getAgenda() { return agendaPublica_(); }

/* ---------- resumen para el docente (pestaña "Resumen") ---------- */
function calcularResumen() {
  const ev = leerAgenda_().filter(function (e) { return e.asistencia; }), est = estudiantes_();
  const sh = tab_(HOJA_RES); sh.clear();
  const asis = {}, n = tab_(HOJA_ASIST, COL_ASIST).getLastRow();
  if (n > 1) tab_(HOJA_ASIST).getRange(2, 2, n - 1, 2).getValues().forEach(function (f) { asis[f[0] + '|' + String(f[1]).toLowerCase()] = 1; });
  const filas = [['Estudiante', 'Correo'].concat(ev.map(function (e) { return e.id; })).concat(['Asistencias', '% asistencia'])];
  est.forEach(function (s) {
    var marcas = ev.map(function (e) { return asis[e.id + '|' + s.email] ? 1 : 0; }), tot = marcas.reduce(function (a, b) { return a + b; }, 0);
    filas.push([s.nombre, s.email].concat(marcas).concat([tot, ev.length ? Math.round(tot / ev.length * 100) + '%' : '']));
  });
  sh.getRange(1, 1, filas.length, filas[0].length).setValues(filas);
  // mini-evaluaciones: promedio de aciertos por evento
  const m = tab_(HOJA_MINI, COL_MINI), nm = m.getLastRow(), acum = {};
  if (nm > 1) m.getRange(2, 2, nm - 1, 5).getValues().forEach(function (f) { var k = f[0]; acum[k] = acum[k] || { a: 0, t: 0, n: 0 }; acum[k].a += +f[3]; acum[k].t += +f[4]; acum[k].n++; });
  const base = filas.length + 2, fm = [['Mini-evaluación (sin nota)', 'Respuestas', '% de aciertos']];
  Object.keys(acum).forEach(function (k) { fm.push([k, acum[k].n, acum[k].t ? Math.round(acum[k].a / acum[k].t * 100) + '%' : '']); });
  sh.getRange(base, 1, fm.length, 3).setValues(fm);
}

/** Menú en la hoja (solo si el script está vinculado a la hoja de cálculo). */
function onOpen() {
  try {
    SpreadsheetApp.getUi().createMenu('Curso').addItem('1 · Configurar todo', 'configurarTodo').addItem('2 · Generar agenda base', 'generarAgendaBase')
      .addItem('3 · Enviar correos de prueba', 'enviarPrueba').addItem('4 · Calcular resumen de asistencia', 'calcularResumen').addToUi();
  } catch (e) {}
}
