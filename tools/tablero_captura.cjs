// Captura la app Shiny en ejecución. Uso: node tablero_captura.cjs <paso> <puerto> <carpeta_salida>
const { chromium } = require('playwright');
const [paso, puerto, salida] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1280, height: 820 }, deviceScaleFactor: 1.5 })).newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://127.0.0.1:${puerto}/`); await p.waitForTimeout(paso === 'v1' ? 1500 : 4000);
  if (paso === 'v2') { await p.uncheck('input[name=medio][value=AVION]'); await p.waitForTimeout(1200); }
  await p.screenshot({ path: `${salida}/${paso}.png` });
  if (paso === 'v5' || paso === 'v6') {
    const barras = p.locator('#aduanas .barlayer .point path'); const n = await barras.count();
    if (n) { await barras.nth(0).click({ force: true }); await p.waitForTimeout(2500); }   // la barra superior = la aduana de mayor valor
    await p.screenshot({ path: `${salida}/${paso}_clic.png` });
    console.log(paso, 'barras:', n, 'seleccion:', await p.locator('#sel').innerText().catch(() => ''));
  }
  if (paso === 'v6') { await p.setViewportSize({ width: 1280, height: 1400 }); await p.waitForTimeout(1500); await p.screenshot({ path: `${salida}/${paso}_tabla.png`, clip: { x: 0, y: 500, width: 1280, height: 820 } }); }
  console.log(paso, 'ok', errs.length ? errs : '');
  await b.close();
})();
