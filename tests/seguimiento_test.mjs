import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { semanaDe, resumirParticipacion } from '../aula/seguimiento.mjs';

const semana = semanaDe(new Date('2026-11-26T15:00:00Z'));
assert.deepEqual(semana, { inicio: '2026-11-23', fin: '2026-11-29' });
const alumnos = [{ uid: 'a', perfil: { nombres: 'Ana' } }, { uid: 'b', perfil: { nombres: 'Beto' } }];
const resumen = resumirParticipacion(alumnos,
  [{ uid: 'a', fecha: '2026-11-25T14:00:00Z', pct: 80 }],
  [{ uid: 'a', tipo: 'tema', creado: '2026-11-26T15:00:00Z' },
    { uid: 'b', tipo: 'respuesta', creado: '2026-11-15T15:00:00Z' }], semana);
assert.equal(resumen[0].quizzes, 1);
assert.equal(resumen[0].mediaQuiz, 80);
assert.equal(resumen[0].temas, 1);
assert.equal(resumen[1].respuestas, 0);

const docs = new Map();
const fields = o => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, typeof v === 'boolean' ? { booleanValue: v } : typeof v === 'number' ? { integerValue: String(v) } : { stringValue: v }]));
const put = (path, data) => docs.set(path, { name: path, fields: fields(data) });
put('seguimiento/configuracion', { activo: true, fechaFin: '2026-12-31' });
put('usuarios/a', { nombres: 'Ana Gómez', cedula: '1111111', email: 'ana@universidad.edu.py', avisosSemanales: true });
put('usuarios/b', { nombres: 'Beto', cedula: '2222222', email: 'beto@universidad.edu.py', avisosSemanales: false });
put('usuarios/c', { nombres: 'Docente', cedula: '3333333', email: 'dmeza.py@gmail.com', avisosSemanales: true });
put('usuarios/d', { nombres: 'Ejemplo', cedula: '4444444', email: 'alumno@ejemplo.com', avisosSemanales: true });
put('usuarios/e', { nombres: 'Duplicado', cedula: '5555555', email: 'uno@universidad.edu.py', avisosSemanales: true });
put('usuarios/f', { nombres: 'Duplicado', cedula: '5555555', email: 'dos@universidad.edu.py', avisosSemanales: true });
put('docentes/dmeza.py@gmail.com', {});
put('respuestas_quiz/1', { uid: 'a', fecha: '2026-11-25T14:00:00Z', pct: 80 });
put('foros/7/mensajes/t1', { uid: 'a', tipo: 'tema', creado: '2026-11-26T15:00:00Z' });
const mails = [], triggers = [];
const fakeNow = new Date('2026-11-30T12:00:00Z');
class FakeDate extends Date { constructor(...args) { super(...(args.length ? args : [fakeNow])); } static now() { return +fakeNow; } }
const yyyyMmDd = (d, tz) => new Intl.DateTimeFormat('sv-SE', { timeZone: tz === 'GMT' ? 'UTC' : tz, year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
const ctx = {
  Date: FakeDate, JSON, String, Number, Object, Array, Math, Error, RegExp, encodeURIComponent,
  Utilities: { formatDate: (d, tz) => yyyyMmDd(d, tz) },
  ScriptApp: { getOAuthToken: () => 'fake-token', getProjectTriggers: () => triggers, deleteTrigger: () => {},
    WeekDay: { MONDAY: 1 }, newTrigger: name => ({ timeBased() { return this; }, onWeekDay() { return this; }, atHour() { return this; }, create() { triggers.push(name); } }) },
  LockService: { getScriptLock: () => ({ tryLock: () => true, releaseLock() {} }) },
  MailApp: { getRemainingDailyQuota: () => 100, sendEmail: m => mails.push(m) },
  UrlFetchApp: { fetch(url, opts) {
    const path = decodeURIComponent(url.split('/documents/')[1]).split('?')[0].replace(/^\//, '');
    const method = (opts.method || 'get').toLowerCase();
    let status = 200, data = {};
    if (method === 'get' && docs.has(path)) data = docs.get(path);
    else if (method === 'get' && path.split('/').length % 2 === 0) status = 404;
    else if (method === 'get') { const a = [...docs].filter(([k]) => k.startsWith(path + '/') && k.slice(path.length + 1).split('/').length === 1); data = { documents: a.map(([, v]) => v) }; }
    else if (method === 'post') {
      const id = decodeURIComponent(url.split('documentId=')[1]); const p = path + '/' + id;
      if (docs.has(p)) status = 409;
      else { data = { name: p, ...JSON.parse(opts.payload) }; docs.set(p, data); }
    } else if (method === 'patch') { data = docs.get(path); data.fields = { ...data.fields, ...JSON.parse(opts.payload).fields }; docs.set(path, data); }
    return { getResponseCode: () => status, getContentText: () => JSON.stringify(data) };
  } },
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(new URL('../appsscript_seguimiento/Seguimiento.gs', import.meta.url), 'utf8'), ctx);
const run = expr => vm.runInContext(expr, ctx);
assert.equal(run('diagnosticarSeguimiento().estudiantes'), 6);
assert.equal(run('verificarEscrituraSeguimiento().escrituraFirestore'), true);
assert.equal(docs.get('seguimiento_envios/verificacion_sistema').fields.estado.stringValue, 'verificado');
assert.equal(run('instalarSeguimientoSemanal().activadores'), 1);
assert.equal(triggers.length, 1);
const first = run('procesarSeguimientoSemanal()');
assert.equal(first.enviados, 1);
assert.equal(first.elegibles, 1);
assert.equal(mails.length, 1);
assert.equal(mails[0].to, 'ana@universidad.edu.py');
assert.match(mails[0].body, /80 %/);
assert.match(mails[0].body, /seguimiento semanal|resumen semanal/i);
const second = run('procesarSeguimientoSemanal()');
assert.equal(second.enviados, 0);
assert.equal(mails.length, 1);
assert.equal(docs.get('seguimiento_envios/2026-11-23_a').fields.estado.stringValue, 'enviado');
assert.equal(run('enviarPruebaSeguimiento().enviadoAlDocente'), true);
assert.equal(mails[1].to, 'dmeza.py@gmail.com');
assert.match(mails[1].subject, /^\[PRUEBA\]/);
console.log('Seguimiento semanal: resumen, exclusión voluntaria, trigger e idempotencia correctos.');
