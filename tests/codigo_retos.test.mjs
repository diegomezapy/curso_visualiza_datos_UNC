import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { RETOS_CODIGO } from "../aula/codigo-retos.mjs";
import { codigoHtml, comprobarRespuesta } from "../aula/codigo.mjs";

test("hay un reto progresivo para cada unidad, en R y Python", () => {
  assert.deepEqual(RETOS_CODIGO.map(r => r.n), [1, 2, 3, 4, 5, 6, 7, 8]);
  for (const reto of RETOS_CODIGO) {
    assert.equal(reto.pistas.length, 3);
    assert.match(reto.codigo.r, /respuesta\s*<-/);
    assert.match(reto.codigo.python, /respuesta\s*=/);
    if (reto.n > 1) assert.equal(reto.grafico, true);
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
  assert.match(html, /&quot;Caso 1&quot;/);
  assert.doesNotMatch(html, /undefinedCaso/);
});
