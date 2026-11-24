const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const datos = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'site', 'aula', 'data.js'), 'utf8').replace(/^window\.CURSO=/, '').replace(/;$/, ''));
datos.config.firebase = {};
const URL_AULA = 'http://localhost:8765/aula/index.html';

async function registrar(page, email, cedula, nombre) {
  await page.goto(URL_AULA + '#/registro');
  const campos = { nombres: nombre, apellidos: 'Prueba', cedula, fechaNac: '1995-03-14', sexo: 'Femenino', nacionalidad: 'Paraguaya', departamento: 'Central', ciudad: 'Luque', email, clave: 'Clave1234', clave2: 'Clave1234' };
  for (const [k, v] of Object.entries(campos)) {
    const el = page.locator('#f_' + k);
    if (await el.evaluate(e => e.tagName) === 'SELECT') await el.selectOption(v); else await el.fill(v);
  }
  await page.locator('#f_ok').check();
  await page.locator('#rg button[type=submit]').click();
  await page.waitForSelector('h1:has-text("Hola")');
}

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.route('**/aula/data.js*', route => route.fulfill({ contentType: 'application/javascript', body: 'window.CURSO=' + JSON.stringify(datos) + ';' }));
  await registrar(page, 'foro1@ejemplo.test', '4567890', 'Ana');
  await page.goto(URL_AULA + '#/foro/prensa');
  await page.waitForSelector('#foroTema');
  assert.match(await page.locator('h1').innerText(), /Foro/);
  await page.locator('#foroTitulo').fill('Unidades en la tabla de exportación');
  await page.locator('#foroTexto').fill('La tabla no aclara US$ por tonelada. Propongo incluir la unidad en el encabezado. <img src=x onerror=alert(1)>');
  await page.locator('#foroTema button').click();
  await page.waitForSelector('.foro-tema');
  assert.equal(await page.locator('#foroTema').count(), 0);
  assert.equal(await page.locator('.foro-tema img').count(), 0);
  assert.match(await page.locator('.foro-tema').innerText(), /Unidades en la tabla/);
  await page.locator('.foro-responder textarea').fill('De acuerdo. También debe indicarse el período enero a abril y la fuente SENACSA.');
  await page.locator('.foro-responder button').click();
  await page.waitForSelector('.foro-respuesta');
  assert.match(await page.locator('.foro-respuesta').innerText(), /período enero a abril/);
  await page.reload();
  await page.waitForSelector('.foro-respuesta');
  assert.equal(await page.locator('.foro-tema').count(), 1);
  assert.deepEqual(errors, []);
  await browser.close();
})().catch(e => { console.error(e); process.exitCode = 1; });
