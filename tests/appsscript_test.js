// Prueba de appsscript/Code.gs con mocks de los servicios de Google. Uso: node tests/appsscript_test.js
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert');
const R = path.join(__dirname, '..', 'appsscript');
const filas = [];                                   // "hoja" simulada
const sheet = {
  getLastRow: () => filas.length, appendRow: r => filas.push(r), setFrozenRows() {},
  getRange: (r, c, n, m) => typeof r === 'string' ? ({ setFormula(f) { sheet.formula = f; } }) : ({ getValues: () => filas.slice(r - 1, r - 1 + n).map(f => f.slice(c - 1, c - 1 + m)) }),
  getParent: () => ({ getUrl: () => 'https://sheet' }),
};
const props = {};
const out = o => ({ _t: o, setMimeType(m) { this.mime = m; return this; } });
const ctx = {
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k] }) },
  SpreadsheetApp: { getActive: () => ({ getSheetByName: () => sheet, insertSheet: () => sheet }), openById: () => ({ getSheetByName: () => sheet }) },
  LockService: { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) },
  ContentService: { createTextOutput: t => out(t), MimeType: { JSON: 'json', CSV: 'csv', JAVASCRIPT: 'javascript' } },
  HtmlService: { createHtmlOutputFromFile: n => ({ f: n, setTitle() { return this; }, addMetaTag() { return this; }, setXFrameOptionsMode() { return this; } }), XFrameOptionsMode: { ALLOWALL: 1 } },
  Logger: { log() {} }, console,
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(R, 'Preguntas.gs'), 'utf8') + '\n' + fs.readFileSync(path.join(R, 'Code.gs'), 'utf8'), ctx);
Object.assign(ctx, vm.runInContext('({CLAVE_IDS, CLAVE, AUTO_IDS, AREAS, EXPERIENCIA, COLUMNAS, PUBLICAS})', ctx));
const call = (fn, ...a) => vm.runInContext(fn + '(...__a)', Object.assign(ctx, { __a: a }));
const post = p => JSON.parse(call('doPost', { postData: { contents: typeof p === 'string' ? p : JSON.stringify(p) } })._t);

const resp = {}; ctx.CLAVE_IDS.forEach(id => resp[id] = ctx.CLAVE[id].c);          // todas correctas
const auto = {}; ctx.AUTO_IDS.forEach(id => auto[id] = 3);
const base = { pid: 'P-AB12CD34EF', area: ctx.AREAS[0], cohorte: 'MICD 2026', experiencia: ctx.EXPERIENCIA[1], herramientas: ['Python'], auto, resp, comentario: '' };

assert.deepStrictEqual(post(base), { ok: true });                         console.log('✔ envío válido se guarda');
assert.strictEqual(filas.length, 2);                                       console.log('✔ crea encabezado + 1 fila');
const f = Object.fromEntries(ctx.COLUMNAS.map((c, i) => [c, filas[1][i]]));
assert.strictEqual(f.score_total, 12); assert.strictEqual(f.nivel, 'Avanzado'); assert.strictEqual(f.score_py, 4);
console.log('✔ puntaje calculado en el servidor: 12/12 · Avanzado');
assert.deepStrictEqual(post(base), { ok: true, duplicado: true });         assert.strictEqual(filas.length, 2); console.log('✔ pid repetido no duplica filas');
assert.strictEqual(post({ ...base, pid: 'P-ZZ99ZZ99ZZ', web: 'http://spam' }).error, 'formato'); console.log('✔ campo trampa lleno (bot) → rechazado');
assert.strictEqual(post({ ...base, pid: 'P-ZZ99ZZ99ZZ', area: 'Hackeo' }).error, 'area');   console.log('✔ área no válida → rechazada');
assert.strictEqual(post({ ...base, pid: 'bad' }).error, 'pid');             console.log('✔ pid mal formado → rechazado');
assert.strictEqual(post({ ...base, pid: 'P-ZZ99ZZ99ZZ', auto: { ...auto, au_r: 9 } }).error, 'auto'); console.log('✔ autoevaluación fuera de rango → rechazada');
assert.strictEqual(post({ ...base, pid: 'P-ZZ99ZZ99ZZ', resp: { ...resp, V1: 'Z' } }).error, 'resp'); console.log('✔ respuesta inválida → rechazada');
assert.strictEqual(post({ ...base, pid: 'P-ZZ99ZZ99ZZ', comentario: 'x'.repeat(300) }).error, 'comentario'); console.log('✔ comentario > 280 caracteres → rechazado');
assert.strictEqual(post('no es json').error, 'formato');                    console.log('✔ cuerpo no JSON → rechazado');
const sinNs = { ...resp }; ctx.CLAVE_IDS.forEach((id, i) => { sinNs[id] = i < 3 ? 'NS' : ctx.CLAVE[id].c; });
post({ ...base, pid: 'P-NS000NS000', resp: sinNs, comentario: '=HYPERLINK("http://x")' });
const g = Object.fromEntries(ctx.COLUMNAS.map((c, i) => [c, filas[2][i]]));
assert.strictEqual(g.score_total, 9); assert.ok(String(g.comentario).startsWith("'=")); console.log('✔ "No sé" puntúa 0 y la fórmula en comentarios se neutraliza');
assert.strictEqual(post({ ...base, pid: 'P-NOC00NOC00' }).ok, true); console.log('✔ el servidor acepta envíos sin código de clase');
const d = JSON.parse(call('doGet', { parameter: { action: 'datos' } })._t);
assert.ok(!d.columnas.includes('pid') && !d.columnas.includes('comentario')); assert.strictEqual(d.filas.length, 3); console.log('✔ API de datos: sin pid ni comentario,', d.filas.length, 'filas');
const csv = call('doGet', { parameter: { action: 'csv' } })._t; assert.ok(csv.split('\n').length === 4 && csv.startsWith('"ts"')); console.log('✔ API CSV');
const estado = call('doGet', { parameter: { action: 'estado', pid: base.pid, callback: 'cvdEstado_abcdef123456' } });
assert.strictEqual(estado.mime, 'javascript'); assert.ok(estado._t.includes('"registrado":true'));
assert.strictEqual(call('doGet', { parameter: { action: 'estado', pid: 'P-ZZZZZZZZZZ', callback: 'cvdEstado_abcdef123456' } })._t.includes('"registrado":false'), true);
assert.strictEqual(call('doGet', { parameter: { action: 'estado', pid: base.pid, callback: 'alert' } }).mime, 'json');
assert.strictEqual(call('doGet', { parameter: {} }).f, 'Tablero'); console.log('✔ sin parámetros sirve el tablero');
call('prepararLooker'); assert.ok(sheet.formula.startsWith('=QUERY(Respuestas!A:'));
const colsFormula = sheet.formula.match(/select ([A-Z,]+)"/)[1].split(','); const letraDe = c => { let n = ctx.COLUMNAS.indexOf(c) + 1, s = ''; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; };
assert.ok(!colsFormula.includes(letraDe('pid')) && !colsFormula.includes(letraDe('comentario')) && colsFormula.length === ctx.PUBLICAS.length); console.log('✔ vista para Looker Studio: sin pid ni comentario (' + sheet.formula.slice(0, 60) + '…)');
console.log('\nTodas las pruebas de Apps Script pasaron.');
