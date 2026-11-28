import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { RETOS_TALLERES } from "../aula/codigo-talleres.mjs";
import { codigoHtml, codigoProgreso } from "../aula/codigo.mjs";

test("dos talleres de doce pasos, con cuatro bloques y ambos lenguajes", () => {
  assert.equal(RETOS_TALLERES.length, 24);
  for (const n of [9, 10]) {
    const retos = RETOS_TALLERES.filter(r => r.n === n);
    assert.deepEqual(retos.map(r => r.paso), Array.from({ length: 12 }, (_, i) => i + 1));
    assert.equal(new Set(retos.map(r => r.bloque)).size, 4);
    assert.deepEqual(codigoProgreso({}, n), { done: 0, items: 12 });
    assert.ok(retos.some(r => r.titulo.includes("regresión")));
    assert.ok(retos.some(r => r.titulo.includes("Likert")));
    assert.ok(retos.some(r => r.titulo.includes("calor")));
    for (const reto of retos) {
      assert.equal(reto.pistas.length, 3);
      assert.ok(reto.codigo[n === 9 ? "r" : "python"].includes("respuesta"));
      if (reto.csv) {
        const csv = readFileSync(fileURLToPath(new URL(`../aula/${reto.csv}`, import.meta.url)), "utf8");
        assert.ok(csv.split("\n").length >= 4);
      }
    }
  }
});

test("el módulo R queda dedicado a R y el de Python a Python", () => {
  const r = codigoHtml(9, {}, "prueba-r");
  const python = codigoHtml(10, {}, "prueba-python");
  assert.match(r, /Prácticas guiadas de R/);
  assert.match(r, /Código R editable/);
  assert.doesNotMatch(r, /data-codigo-lang=/);
  assert.doesNotMatch(r, /Ejemplo en Python/);
  assert.match(python, /Prácticas guiadas de Python/);
  assert.match(python, /Código Python editable/);
  assert.doesNotMatch(python, /data-codigo-lang=/);
  assert.doesNotMatch(python, /Ejemplo en R/);
});
