import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { RETOS_CODIGO } from "../aula/codigo-retos.mjs";
import { codigoHtml, codigoProgreso, comprobarRespuesta } from "../aula/codigo.mjs";

test("hay diez pasos progresivos por unidad, en R y Python", () => {
  assert.equal(RETOS_CODIGO.length, 80);
  assert.equal(new Set(RETOS_CODIGO.map(r => r.id)).size, 80);
  for (let n = 1; n <= 8; n++) {
    const unidad = RETOS_CODIGO.filter(r => r.n === n);
    assert.deepEqual(unidad.map(r => r.paso), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    assert.equal(unidad[9].id, String(n)); // conserva el avance del ensayo anterior
    for (let paso = 1; paso <= 9; paso++) assert.equal(unidad[paso - 1].id, `${n}_${String(paso).padStart(2, "0")}`);
  }
  for (const reto of RETOS_CODIGO) {
    assert.equal(reto.pistas.length, 3);
    assert.ok(reto.consigna.length >= 30);
    assert.ok(reto.explicacion?.length >= 12);
    assert.match(reto.codigo.r, /respuesta\s*<-/);
    assert.match(reto.codigo.python, /respuesta\s*=/);
    if (reto.paso >= 7 && reto.paso <= 9) assert.equal(reto.grafico, true);
    if (reto.csv) {
      const csv = readFileSync(fileURLToPath(new URL(`../aula/${reto.csv}`, import.meta.url)), "utf8");
      assert.ok(csv.includes("\n"));
      assert.ok(csv.split("\n").length >= 3);
    }
  }
});

test("la comprobación usa resultados, no coincidencia textual ni coerción de tipos", () => {
  assert.equal(comprobarRespuesta(2, 2), true);
  assert.equal(comprobarRespuesta([2], 2), true); // salida escalar de webR
  assert.equal(comprobarRespuesta("2", 2), false);
  assert.equal(comprobarRespuesta([25, 50], [25, 50]), true);
  assert.equal(comprobarRespuesta([25, 49], [25, 50]), false);
  assert.equal(comprobarRespuesta(null, "B"), false);
  assert.equal(comprobarRespuesta("B", "B"), true);
});

test("el editor conserva comillas y caracteres especiales del código inicial", () => {
  const html = codigoHtml(6);
  assert.match(html, /Consola de resultados/);
  assert.match(html, /codigo-layout/);
  assert.match(html, /data-codigo-paso="10"/);
  assert.doesNotMatch(html, /undefined/);
});

test("cada paso cuenta una vez y se conserva el progreso del ensayo anterior", () => {
  assert.deepEqual(codigoProgreso({}, 6), { done: 0, items: 10 });
  assert.deepEqual(codigoProgreso({ "6_r": { hecho: true } }, 6), { done: 1, items: 10 });
  assert.deepEqual(codigoProgreso({ "6_01_r": { hecho: true }, "6_01_python": { hecho: true }, "6_r": { hecho: true } }, 6), { done: 2, items: 10 });
});
