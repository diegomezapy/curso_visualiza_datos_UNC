/** Seguimiento semanal privado del aula FACET-UNC. Sin web app ni credenciales en código. */
const SEG_PROYECTO = 'cursovisualizadatosunc';
const SEG_ZONA = 'America/Asuncion';
const SEG_AULA = 'https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/index.html';
const SEG_DOCENTE_PRUEBA = 'dmeza.py@gmail.com';
const SEG_BASE = 'https://firestore.googleapis.com/v1/projects/' + SEG_PROYECTO + '/databases/(default)/documents';

function segRequest_(ruta, metodo, datos, aceptar) {
  const opciones = { method: metodo || 'get', muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() } };
  if (datos !== undefined) { opciones.contentType = 'application/json'; opciones.payload = JSON.stringify(datos); }
  const r = UrlFetchApp.fetch(SEG_BASE + ruta, opciones), codigo = r.getResponseCode();
  if (aceptar && codigo === aceptar) return null;
  if (codigo < 200 || codigo >= 300) throw new Error('Firestore: HTTP ' + codigo + ' en ' + ruta.split('?')[0]);
  return JSON.parse(r.getContentText() || '{}');
}
function segValor_(v) {
  if (!v) return null;
  if ('stringValue' in v) return v.stringValue;
  if ('integerValue' in v) return Number(v.integerValue);
  if ('doubleValue' in v) return v.doubleValue;
  if ('booleanValue' in v) return v.booleanValue;
  if ('timestampValue' in v) return v.timestampValue;
  if ('nullValue' in v) return null;
  if ('mapValue' in v) return segCampos_(v.mapValue.fields || {});
  if ('arrayValue' in v) return (v.arrayValue.values || []).map(segValor_);
  return null;
}
function segCampos_(fields) { const o = {}; Object.keys(fields || {}).forEach(k => o[k] = segValor_(fields[k])); return o; }
function segDoc_(d) { return { id: d.name.split('/').pop(), ...segCampos_(d.fields || {}) }; }
function segGet_(ruta) { const r = segRequest_('/' + ruta, 'get', undefined, 404); return r ? segDoc_(r) : null; }
function segList_(ruta) {
  const salida = []; let token = '';
  do {
    const sep = ruta.indexOf('?') >= 0 ? '&' : '?';
    const q = '/' + ruta + sep + 'pageSize=1000' + (token ? '&pageToken=' + encodeURIComponent(token) : '');
    const r = segRequest_(q) || {};
    (r.documents || []).forEach(d => salida.push(segDoc_(d)));
    token = r.nextPageToken || '';
  } while (token);
  return salida;
}
function segFields_(d) {
  const fields = {};
  Object.keys(d).forEach(k => {
    const v = d[k];
    if (typeof v === 'boolean') fields[k] = { booleanValue: v };
    else if (typeof v === 'number') fields[k] = { integerValue: String(v) };
    else fields[k] = { stringValue: String(v == null ? '' : v) };
  });
  return { fields };
}
function segCrearEnvio_(id, datos) {
  return segRequest_('/seguimiento_envios?documentId=' + encodeURIComponent(id), 'post', segFields_(datos), 409);
}
function segActualizarEnvio_(id, datos) {
  const query = Object.keys(datos).map(k => 'updateMask.fieldPaths=' + encodeURIComponent(k)).join('&');
  return segRequest_('/seguimiento_envios/' + encodeURIComponent(id) + '?' + query, 'patch', segFields_(datos));
}
function segFecha_(v) {
  if (!v) return '';
  const d = new Date(v);
  return isNaN(d.getTime()) ? '' : Utilities.formatDate(d, SEG_ZONA, 'yyyy-MM-dd');
}
function segSemanaAnterior_(ahora) {
  const hoy = Utilities.formatDate(ahora, SEG_ZONA, 'yyyy-MM-dd');
  const d = new Date(hoy + 'T12:00:00Z');
  d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7) - 7);
  const inicio = Utilities.formatDate(d, 'GMT', 'yyyy-MM-dd');
  d.setUTCDate(d.getUTCDate() + 6);
  return { inicio, fin: Utilities.formatDate(d, 'GMT', 'yyyy-MM-dd') };
}
function segResumen_(usuarios, intentos, mensajes, semana) {
  const m = {};
  usuarios.forEach(u => { m[u.id] = { uid: u.id, email: String(u.email || '').trim().toLowerCase(),
    nombre: String(u.nombres || '').trim(), avisos: u.avisosSemanales !== false,
    quizzes: 0, suma: 0, temas: 0, respuestas: 0 }; });
  const dentro = x => { const f = segFecha_(x); return f >= semana.inicio && f <= semana.fin; };
  intentos.forEach(i => {
    const r = m[i.uid]; if (!r || !dentro(i.fecha)) return;
    r.quizzes++; if (typeof i.pct === 'number' && i.pct >= 0 && i.pct <= 100) r.suma += i.pct;
  });
  mensajes.forEach(p => {
    const r = m[p.uid]; if (!r || !dentro(p.creado)) return;
    if (p.tipo === 'tema') r.temas++;
    else if (p.tipo === 'respuesta') r.respuestas++;
  });
  return Object.keys(m).map(k => m[k]).filter(r => r.avisos && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(r.email));
}
function segCorreo_(r, semana) {
  const nombre = r.nombre.split(/\s+/)[0] || 'estudiante';
  const media = r.quizzes ? Math.round(r.suma / r.quizzes) : null;
  const actividad = r.quizzes || r.temas || r.respuestas;
  const msg = actividad
    ? 'Completaste ' + r.quizzes + ' intento(s) de quiz y participaste con ' + r.temas + ' tema(s) y ' + r.respuestas + ' respuesta(s) en los foros.'
    : 'Esta semana no registramos intentos de quiz ni publicaciones en los foros. Podés retomar el curso con una actividad breve.';
  const sugerencia = actividad ? 'Seguí avanzando y elegí una actividad de la próxima unidad.' : 'Te invitamos a elegir un recurso, resolver un quiz o comentar en el foro de tu unidad.';
  const cuerpo = 'Hola ' + nombre + ':\n\nResumen de tu participación en el aula Git, del ' + semana.inicio + ' al ' + semana.fin + '.\n' + msg +
    (media === null ? '' : '\nPromedio de los intentos de quiz de la semana: ' + media + ' %. Este dato es formativo, no una nota oficial.') +
    '\n\n' + sugerencia + '\n\nIngresá a tu aula: ' + SEG_AULA +
    '\n\nSi preferís dejar de recibir este resumen, desactivá «Recibir el resumen semanal» en Mi perfil.\nVisualización de datos · FACET-UNC';
  return { subject: 'Tu avance semanal en Visualización de datos · ' + semana.inicio, body: cuerpo };
}
/** Comprobación de acceso de solo lectura, sin enviar correos ni registrar datos personales. */
function diagnosticarSeguimiento() {
  const config = segGet_('seguimiento/configuracion');
  return { accesoFirestore: true, programacionActiva: !!config?.activo, estudiantes: segList_('usuarios').length,
    activadores: ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'procesarSeguimientoSemanal').length };
}
/** Comprueba creación y actualización con un registro técnico sin datos personales ni correo. */
function verificarEscrituraSeguimiento() {
  const id = 'verificacion_sistema';
  segCrearEnvio_(id, { uid: id, semana: '0000-00-00', estado: 'prueba', creado: new Date().toISOString() });
  segActualizarEnvio_(id, { estado: 'verificado' });
  return { escrituraFirestore: segGet_('seguimiento_envios/' + id)?.estado === 'verificado' };
}
/** Crea un único activador del lunes por la mañana (la hora exacta puede variar dentro de la franja). */
function instalarSeguimientoSemanal() {
  diagnosticarSeguimiento();
  ScriptApp.getProjectTriggers().forEach(t => { if (t.getHandlerFunction() === 'procesarSeguimientoSemanal') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('procesarSeguimientoSemanal').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(8).create();
  return { activadores: 1 };
}
/** El activador procesa la semana anterior; el documento semana+uid impide envíos duplicados. */
function procesarSeguimientoSemanal() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return { estado: 'ocupado' };
  try {
    const ahora = new Date(), hoy = Utilities.formatDate(ahora, SEG_ZONA, 'yyyy-MM-dd');
    const cfg = segGet_('seguimiento/configuracion');
    if (!cfg?.activo || hoy > cfg.fechaFin) return { estado: 'inactivo' };
    if (new Date(hoy + 'T12:00:00Z').getUTCDay() !== 1) return { estado: 'fuera_de_lunes' };
    const semana = segSemanaAnterior_(ahora);
    const usuarios = segList_('usuarios'), intentos = segList_('respuestas_quiz');
    const mensajes = segList_('foro_prensa').concat([1, 2, 4, 5, 6, 7, 8].flatMap(n => segList_('foros/' + n + '/mensajes')));
    const resumenes = segResumen_(usuarios, intentos, mensajes, semana);
    let enviados = 0, omitidos = 0;
    for (const r of resumenes) {
      if (MailApp.getRemainingDailyQuota() < 1) break;
      const id = semana.inicio + '_' + r.uid;
      if (!segCrearEnvio_(id, { uid: r.uid, semana: semana.inicio, estado: 'preparando', creado: ahora.toISOString() })) { omitidos++; continue; }
      const correo = segCorreo_(r, semana);
      try {
        MailApp.sendEmail({ to: r.email, subject: correo.subject, body: correo.body, name: 'Visualización de datos · FACET-UNC' });
        segActualizarEnvio_(id, { estado: 'enviado', enviado: new Date().toISOString(), quizzes: r.quizzes, temas: r.temas, respuestas: r.respuestas });
        enviados++;
      } catch (e) {
        // Se conserva el estado previo para revisión manual: un reintento automático podría duplicar un correo incierto.
        throw new Error('Envío incompleto; revisar el registro ' + id + ' antes de volver a ejecutar.');
      }
    }
    return { estado: 'procesado', semana: semana.inicio, elegibles: resumenes.length, enviados, omitidos };
  } finally { lock.releaseLock(); }
}
/** Prueba del formato sin datos reales de estudiantes: correo solo a la cuenta que ejecuta el script. */
function enviarPruebaSeguimiento() {
  const s = segSemanaAnterior_(new Date()), c = segCorreo_({ nombre: 'Docente', quizzes: 2, suma: 160, temas: 1, respuestas: 1 }, s);
  MailApp.sendEmail({ to: SEG_DOCENTE_PRUEBA, subject: '[PRUEBA] ' + c.subject, body: c.body, name: 'Visualización de datos · FACET-UNC' });
  return { enviadoAlDocente: true };
}
