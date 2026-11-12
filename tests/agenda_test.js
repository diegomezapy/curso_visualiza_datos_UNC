// Prueba de appsscript/Agenda.gs (agenda, asistencia con ventana horaria, correos automáticos y mini-evaluación). node tests/agenda_test.js
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert'), crypto = require('crypto');
const R = path.join(__dirname, '..', 'appsscript');
const OFF = 3 * 3600e3;   // America/Asuncion = UTC-3 (hora oficial permanente)
const pad = n => String(n).padStart(2, '0');
const loc = d => new Date(d.getTime() - OFF);
const fmt = (d, tz, f) => { const l = loc(d); const o = { yyyy: l.getUTCFullYear(), MM: pad(l.getUTCMonth() + 1), dd: pad(l.getUTCDate()), HH: pad(l.getUTCHours()), mm: pad(l.getUTCMinutes()), ss: pad(l.getUTCSeconds()) };
  return f.replace("'T'", 'T').replace('XXX', '-03:00').replace(/yyyy|MM|dd|HH|mm|ss/g, k => o[k]); };
class Sheet { constructor(n) { this.n = n; this.rows = []; }
  getLastRow() { return this.rows.length; } appendRow(r) { this.rows.push(r.slice()); } setFrozenRows() {} clear() { this.rows = []; }
  getDataRange() { return { getValues: () => this.rows.map(r => r.slice()) }; }
  getRange(r, c, n, m) { const S = this; if (typeof r === 'string') return { setFormula() {} }; if (n === undefined) return { setNumberFormat() {}, setValue(v) { while (S.rows.length < r) S.rows.push([]); S.rows[r - 1][c - 1] = v; } };
    return { getValues: () => S.rows.slice(r - 1, r - 1 + n).map(f => Array.from({ length: m }, (_, i) => f[c - 1 + i] === undefined ? '' : f[c - 1 + i])),
      setValues: v => { v.forEach((f, i) => { while (S.rows.length < r + i) S.rows.push([]); f.forEach((x, j) => S.rows[r - 1 + i][c - 1 + j] = x); }); }, setValue(v) { S.rows[r - 1][c - 1] = v; }, setNumberFormat() {} }; }
  setName(n) { this.n = n; } getParent() { return ss; } }
const hojas = {}; const getSheet = n => hojas[n]; const ss = { getSheetByName: n => hojas[n] || null, insertSheet: n => (hojas[n] = new Sheet(n)), getSheets: () => Object.values(hojas), getUrl: () => 'https://sheet' };
const props = { CODIGO_CLASE: 'c' }; const mails = []; let cuota = 100; const triggers = [];
const ctx = {
  console, Logger: { log() {} },
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k], setProperty: (k, v) => props[k] = v }) },
  SpreadsheetApp: { getActive: () => ss, openById: () => ss },
  LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock() {}, releaseLock() {} }) },
  MailApp: { sendEmail: m => mails.push(m), getRemainingDailyQuota: () => cuota - mails.length },
  ScriptApp: { getService: () => ({ getUrl: () => 'https://script.google.com/macros/s/ID/exec' }), getProjectTriggers: () => triggers.slice(), deleteTrigger: t => triggers.splice(triggers.indexOf(t), 1),
    newTrigger: h => ({ timeBased() { return { everyMinutes: n => ({ create() { triggers.push({ getHandlerFunction: () => h, n }); } }) }; } }) },
  Session: { getActiveUser: () => ({ getEmail: () => 'docente@x.com' }) },
  ContentService: { createTextOutput: t => ({ _t: t, setMimeType() { return this; } }), MimeType: { JSON: 'j', CSV: 'c' } },
  HtmlService: { createHtmlOutputFromFile: n => ({ f: n, setTitle() { return this; }, addMetaTag() { return this; }, setXFrameOptionsMode() { return this; } }), createTemplateFromFile: n => ({ f: n, evaluate() { return { f: n, setTitle() { return this; }, addMetaTag() { return this; }, setXFrameOptionsMode() { return this; } }; } }), XFrameOptionsMode: { ALLOWALL: 1 } },
  Utilities: { formatDate: fmt, parseDate: (s, tz) => { const m = s.match(/(\d+)-(\d+)-(\d+) (\d+):(\d+)/); return new Date(Date.UTC(+m[1], m[2] - 1, +m[3], +m[4], +m[5]) + OFF); },
    computeHmacSha256Signature: (v, k) => crypto.createHmac('sha256', k).update(v).digest(), base64EncodeWebSafe: b => Buffer.from(b).toString('base64url'), getUuid: () => crypto.randomUUID() },
};
vm.createContext(ctx);
vm.runInContext(['Preguntas', 'Banco', 'Code', 'Agenda'].map(f => fs.readFileSync(path.join(R, f + '.gs'), 'utf8')).join('\n'), ctx);
const call = (fn, ...a) => { ctx.__a = a; return vm.runInContext(fn + '(...__a)', ctx); };
const at = (f, h) => new Date(Date.UTC(+f.slice(0, 4), +f.slice(5, 7) - 1, +f.slice(8, 10), +h.slice(0, 2), +h.slice(3, 5)) + OFF);

call('configurarTodo');
assert.ok(['Agenda', 'Estudiantes', 'Asistencia', 'MiniEval', 'Config'].every(n => hojas[n])); assert.ok(props.SECRETO && props.SECRETO.length > 30);
assert.strictEqual(triggers.length, 1); assert.strictEqual(triggers[0].getHandlerFunction(), 'procesarEnvios');
console.log('✔ configurarTodo: crea pestañas, secreto y activador de tiempo');
call('activarEnvios', 5); assert.strictEqual(triggers.length, 1); assert.strictEqual(triggers[0].n, 5); console.log('✔ activarEnvios reemplaza el activador (sin duplicarlo)');

[['ana@x.com', 'Ana Gómez', 'SI'], ['beto@x.com', 'Beto Ruiz', ''], ['carla@x.com', 'Carla Paz', 'SI'], ['baja@x.com', 'Baja', 'NO'], ['malmail', 'Error', 'SI']].forEach(r => hojas.Estudiantes.appendRow(r));
hojas.Agenda.appendRow(['clase-2', '2026-11-20', '19:00', '21:00', 'clase', 'Sesión 2 · Elección de gráficos', 2, 'https://meet.google.com/abc', '', 'SI', 'SI', '', '']);
hojas.Agenda.appendRow(['entrega-2', '2026-11-27', '23:00', '23:59', 'entrega', 'Entrega S2', 2, '', '', 'NO', 'NO', '', '']);
call('procesarEnvios', at('2026-11-20', '18:59')); assert.strictEqual(mails.length, 0); console.log('✔ antes de la hora no se envía nada');
call('procesarEnvios', at('2026-11-20', '19:00'));
assert.strictEqual(mails.length, 3); assert.ok(mails.every(m => /Asistencia/.test(m.subject))); assert.deepStrictEqual(mails.map(m => m.to), ['ana@x.com', 'beto@x.com', 'carla@x.com']);
console.log('✔ a las 19:00 se envía la solicitud de asistencia solo a los 3 estudiantes activos y válidos');
assert.ok(mails[0].htmlBody.includes('page=asistencia') && mails[0].htmlBody.includes('meet.google.com')); const links = mails.map(m => m.htmlBody.match(/href="(https:\/\/script[^"]+)"/)[1]); assert.strictEqual(new Set(links).size, 3);
console.log('✔ cada correo trae un enlace personal distinto');
call('procesarEnvios', at('2026-11-20', '19:01')); assert.strictEqual(mails.length, 3); console.log('✔ no se reenvía (envío único por evento)');
assert.ok(String(hojas.Agenda.rows[1][11]).includes('3/3')); console.log('✔ se registra el envío en la hoja:', hojas.Agenda.rows[1][11]);
call('procesarEnvios', at('2026-11-20', '20:59')); assert.strictEqual(mails.length, 3);
call('procesarEnvios', at('2026-11-20', '21:00')); assert.strictEqual(mails.length, 6); assert.ok(mails.slice(3).every(m => /Mini-evaluación \(sin nota\)/.test(m.subject) && /No suma puntos/.test(m.htmlBody)));
console.log('✔ al terminar la clase (21:00) se envía la mini-evaluación "sin nota"');
call('procesarEnvios', at('2026-11-21', '10:00')); assert.strictEqual(mails.length, 6);

const u = e => e.match(/[?&]u=([^&]+)/)[1], tk = h => h.match(/[?&]t=([^"&]+)/)[1];
const eAna = decodeURIComponent(u(links[0])), tAna = tk(links[0]);
assert.strictEqual(call('registrarAsistencia', 'clase-2', eAna, tAna, at('2026-11-20', '18:30')).ok, false); console.log('✔ asistencia antes de la clase → rechazada');
let r = call('registrarAsistencia', 'clase-2', eAna, tAna, at('2026-11-20', '19:20')); assert.ok(r.ok && !r.ya); console.log('✔ asistencia durante la clase → registrada');
r = call('registrarAsistencia', 'clase-2', eAna, tAna, at('2026-11-20', '19:25')); assert.ok(r.ok && r.ya); assert.strictEqual(hojas.Asistencia.rows.length, 2); console.log('✔ doble registro no duplica');
assert.strictEqual(call('registrarAsistencia', 'clase-2', 'beto@x.com', tAna, at('2026-11-20', '19:30')).ok, false); console.log('✔ el token de otra persona no sirve');
assert.strictEqual(call('registrarAsistencia', 'clase-2', 'baja@x.com', call('token_', 'clase-2', 'baja@x.com'), at('2026-11-20', '19:30')).ok, false); console.log('✔ correo fuera de la lista del curso → rechazado');
assert.strictEqual(call('registrarAsistencia', 'clase-2', 'carla@x.com', call('token_', 'clase-2', 'carla@x.com'), at('2026-11-20', '21:10')).ok, true); console.log('✔ tolerancia de 15 min después del fin (21:10 ok)');
assert.strictEqual(call('registrarAsistencia', 'clase-2', 'beto@x.com', call('token_', 'clase-2', 'beto@x.com'), at('2026-11-20', '21:30')).ok, false);
assert.strictEqual(call('registrarAsistencia', 'clase-2', 'beto@x.com', call('token_', 'clase-2', 'beto@x.com'), at('2026-11-21', '19:30')).ok, false); console.log('✔ fuera del día y horario → rechazado (21:30 y al día siguiente)');
assert.strictEqual(call('registrarAsistencia', 'entrega-2', 'ana@x.com', call('token_', 'entrega-2', 'ana@x.com'), at('2026-11-27', '23:10')).ok, false); console.log('✔ eventos sin asistencia (entrega) no registran asistencia');

const tm = call('token_', 'clase-2', 'ana@x.com'); const m1 = call('getMini', 'clase-2', 'ana@x.com', tm, at('2026-11-20', '21:05'));
assert.ok(m1.ok && m1.preguntas.length === 3 && m1.preguntas.every(p => p.c === undefined && p.why === undefined && p.o.length >= 2)); console.log('✔ mini-evaluación: 3 preguntas y sin respuestas correctas en el cliente');
const sol = {}; m1.preguntas.forEach((p, i) => sol[p.i] = i === 0 ? 0 : call('Object.keys', {}).length); // dummy
const banco = ctx.BANCO ? ctx.BANCO : vm.runInContext('BANCO', ctx); const resp = {}; m1.preguntas.forEach((p, i) => resp[p.i] = i < 2 ? banco['2'][p.i].c : (banco['2'][p.i].c + 1) % 4);
let ev = call('enviarMini', 'clase-2', 'ana@x.com', tm, resp, at('2026-11-20', '21:06')); assert.ok(ev.ok); assert.strictEqual(ev.aciertos, 2); assert.strictEqual(ev.total, 3); console.log('✔ se califica en el servidor: 2/3');
ev = call('enviarMini', 'clase-2', 'ana@x.com', tm, banco['2'].map((_, i) => 0), at('2026-11-20', '21:07')); assert.ok(ev.repetida); assert.strictEqual(hojas.MiniEval.rows.length, 2); console.log('✔ solo cuenta el primer intento');
assert.strictEqual(call('getMini', 'clase-2', 'ana@x.com', tm, at('2026-11-24', '00:00')).ok, false); console.log('✔ fuera del plazo de 72 h → cerrada');
assert.strictEqual(call('getMini', 'clase-2', 'ana@x.com', 'falso', at('2026-11-20', '21:05')).ok, false); console.log('✔ token falso en mini-evaluación → rechazado');

// cuota diaria
mails.length = 0; cuota = 2; hojas.Agenda.rows[1][11] = ''; hojas.Agenda.rows[1][12] = 'x';
call('procesarEnvios', at('2026-11-20', '19:30')); assert.strictEqual(mails.length, 2); assert.ok(String(hojas.Agenda.rows[1][11]).includes('2/3')); console.log('✔ cuota diaria agotada: envía 2 de 3 y lo deja registrado (' + hojas.Agenda.rows[1][11].split('·')[1].trim() + ')'); cuota = 100;

// agenda pública
let ag = JSON.parse(call('doGet', { parameter: { action: 'agenda' } })._t);
assert.strictEqual(ag.eventos.length, 2); assert.ok(ag.eventos.every(e => e.enlace === undefined)); assert.ok(ag.eventos[0].inicio_iso.endsWith('-03:00')); assert.strictEqual(ag.eventos[0].inicio_iso, '2026-11-20T19:00:00-03:00');
console.log('✔ agenda pública: ISO con zona -03:00 y sin enlaces de Meet (por defecto)');
hojas.Config.rows.forEach(f => { if (f[0] === 'PUBLICAR_ENLACES') f[1] = 'SI'; }); ag = JSON.parse(call('doGet', { parameter: { action: 'agenda' } })._t); assert.strictEqual(ag.eventos[0].enlace, 'https://meet.google.com/abc'); console.log('✔ con PUBLICAR_ENLACES=SI se incluye el enlace');
assert.strictEqual(call('doGet', { parameter: {} }).f, 'Tablero'); assert.strictEqual(call('doGet', { parameter: { page: 'asistencia', e: 'clase-2' } }).f, 'Asistencia'); assert.strictEqual(call('doGet', { parameter: { page: 'mini' } }).f, 'MiniEval'); console.log('✔ rutas: ?page=asistencia, ?page=mini y tablero por defecto');

call('calcularResumen'); const res = hojas.Resumen.rows; assert.strictEqual(res[0][2], 'clase-2'); const fAna = res.find(f => f[1] === 'ana@x.com'); assert.strictEqual(fAna[2], 1); assert.ok(res.some(f => f[0] === 'Mini-evaluación (sin nota)')); console.log('✔ resumen: asistencia por estudiante y % de aciertos de la mini-evaluación');
// generarAgendaBase
hojas.Config.rows.forEach(f => { if (f[0] === 'clase_1') f[1] = '2026-12-01'; }); call('generarAgendaBase'); const ids = hojas.Agenda.rows.map(f => f[0]); assert.ok(ids.includes('clase-1') && ids.includes('entrega-1')); assert.strictEqual(hojas.Agenda.rows.find(f => f[0] === 'entrega-1')[1], '2026-12-08'); console.log('✔ generarAgendaBase: clase + entrega a +7 días');
console.log('\nTodas las pruebas de Agenda pasaron.');
