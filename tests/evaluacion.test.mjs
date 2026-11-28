import test from "node:test";
import assert from "node:assert/strict";
import { PESOS, calcularNota, puntajeCuestionarios } from "../aula/evaluacion.mjs";

test("la ponderación vigente suma 100 y cada componente alcanza su máximo", () => {
  assert.equal(Object.values(PESOS).reduce((a, b) => a + b, 0), 100);
  const ids = ["1", "2", "3", "4", "5", "6"];
  const quiz = Object.fromEntries(ids.map(id => [id, { mejor: 100 }]));
  assert.deepEqual(calcularNota(quiz, { s8_foros: 25, s8_inf: 18, s8_pres: 12, s8_coed: 20 }, ids), {
    cuestionarios: 25, foros: 25, trabajoFinal: 30, coedicion: 20, total: 100, completo: true, escala: 5
  });
});

test("los cuestionarios usan los seis mejores porcentajes disponibles", () => {
  const ids = ["1", "2", "3", "4", "5", "6", "7"];
  const quiz = Object.fromEntries([100, 90, 80, 70, 60, 50, 0].map((mejor, i) => [ids[i], { mejor }]));
  assert.deepEqual(puntajeCuestionarios(quiz, ids), { pct: 75, pts: 18.75 });
});

test("las notas anteriores no se suman y los componentes no exceden sus topes", () => {
  const c = calcularNota({}, { s1_ej: 5, s4_mp1: 10, s8_red: 3, s8_foros: 40, s8_inf: 50, s8_pres: 30, s8_coed: 40 }, []);
  assert.equal(c.cuestionarios, 0);
  assert.equal(c.foros, 25);
  assert.equal(c.trabajoFinal, 30);
  assert.equal(c.coedicion, 20);
  assert.equal(c.total, 75);
  assert.equal(c.completo, false);
  assert.equal(c.escala, null);
  assert.equal(calcularNota({}, { s8_foros: -2, s8_inf: "", s8_pres: null, s8_coed: "error" }, []).total, 0);
});
