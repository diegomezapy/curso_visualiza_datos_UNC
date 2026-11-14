const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const origen = fs.readFileSync(path.join(__dirname, '..', 'site', 'aula', 'data.js'), 'utf8');
const datos = JSON.parse(origen.replace(/^window\.CURSO=/, '').replace(/;$/, ''));
datos.config.firebase = {};
datos.config.demo.planillas = { diagnostico: 'https://docs.google.com/spreadsheets/d/PRUEBA/edit' };

async function perfil(page, correo, cedula, nombre) {
  const campos = { nombres: nombre, apellidos: 'Prueba', cedula, fechaNac: '1995-03-14', sexo: 'Femenino', nacionalidad: 'Paraguaya', departamento: 'Central', ciudad: 'Luque', email: correo, clave: 'Clave1234', clave2: 'Clave1234' };
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
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.route('**/aula/data.js*', route => route.fulfill({ contentType: 'application/javascript', body: 'window.CURSO=' + JSON.stringify(datos) + ';' }));

  await page.goto('http://localhost:8765/aula/index.html#/registro');
  await perfil(page, 'alumna@ejemplo.test', '4567890', 'Alumna');
  await page.goto('http://localhost:8765/aula/index.html#/quiz/1');
  for (let i = 0; i < 5; i++) await page.locator(`input[name=q${i}]`).first().check();
  await page.locator('#send').click();
  await page.waitForSelector('#retry');
  await page.goto('http://localhost:8765/aula/index.html#/sesion/1');
  await page.locator('details:has(select[data-auto="s1_ej"]) summary').click();
  await page.locator('select[data-auto="s1_ej"][data-i="0"]').selectOption('3');
  await page.waitForTimeout(800);
  await page.locator('#logout').click();
  await page.waitForSelector('#lf');

  await page.goto('http://localhost:8765/aula/index.html#/registro');
  await perfil(page, 'docente@demo.local', '1111111', 'Docente');
  await page.goto('http://localhost:8765/aula/index.html#/docente');
  await page.waitForSelector('#csvRegistro');
  assert.equal(await page.locator('#csvRegistro').isEnabled(), true);
  assert.equal(await page.locator('#csvRespuestas').isEnabled(), true);
  assert.equal(await page.locator('#csvAuto').isEnabled(), true);
  assert.equal(await page.locator('a:has-text("Diagnóstico inicial")').count(), 1);
  await page.screenshot({ path: '/tmp/aula_planillas_docente.png', fullPage: true });
  for (const [boton, muestra] of [['csvRegistro', 'alumna@ejemplo.test'], ['csvRespuestas', 'detalle'], ['csvAuto', 'Logrado']]) {
    const evento = page.waitForEvent('download');
    await page.locator('#' + boton).click();
    const descarga = await evento;
    const texto = fs.readFileSync(await descarga.path(), 'utf8');
    assert.ok(texto.includes(muestra), `${boton} no contiene ${muestra}`);
  }
  await page.locator('#logout').click();
  await page.waitForSelector('#lf');
  await page.waitForTimeout(300);
  await page.locator('#le').fill('alumna@ejemplo.test');
  await page.locator('#lp').fill('Clave1234');
  await page.locator('#lf button[type=submit]').click();
  await page.waitForSelector('h1:has-text("Hola")');
  await page.goto('http://localhost:8765/aula/index.html#/docente');
  await page.waitForSelector('h1:has-text("Acceso restringido")');
  assert.equal(await page.locator('h1').innerText(), 'Acceso restringido');
  assert.deepEqual(errors, []);
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
