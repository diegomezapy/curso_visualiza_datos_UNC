import assert from "node:assert/strict";
import { csvPlanilla, planillaRegistros, planillaQuizzes, planillaAutoevaluaciones } from "../aula/planillas.mjs";

const alumno = { uid: "u1", perfil: { apellidos: "Benítez", nombres: "Ana", email: "ana@example.test", cedula: "4567890", ciudad: "=HYPERLINK(\"https://example.test\")", consentimiento: { fecha: "2026-11-14T12:00:00Z", version: "v1" } }, progreso: { quiz: { 1: { intentos: [{ t: "2026-11-13T12:00:00Z", pct: 60 }, { id: "nuevo", t: "2026-11-14T12:00:00Z", pct: 80 }] } }, auto: { s1_ej: { 0: 3 } } } };
const intento = { id: "nuevo", uid: "u1", sesion: 1, quizTitulo: "Percepción", fecha: "2026-11-14T12:00:00Z", pct: 80, respuestas: [{ pregunta: "¿Qué gráfico?", respuesta: "Barras", correcta: "Barras", acierto: true }] };

const registros = planillaRegistros([alumno]);
assert.match(registros, /consentimiento_fecha/);
assert.match(registros, /'\=HYPERLINK/);
assert.equal(registros.split("\r\n").length, 3);

const quizzes = planillaQuizzes([alumno], [intento]);
assert.match(quizzes, /"¿Qué gráfico\?","Barras","Barras","Sí","detalle"/);
assert.match(quizzes, /histórico sin detalle/);
assert.equal(quizzes.split("\r\n").length, 4); // encabezado, detalle, histórico y línea final

const auto = planillaAutoevaluaciones([alumno], [{ id: "s1_ej", n: 1, titulo: "Ejercicio 1", rubrica: "R1" }], { R1: { titulo: "Calidad", criterios: [{ n: "Claridad", w: 40 }] } });
assert.match(auto, /"Claridad","40","3","Logrado"/);

assert.equal(csvPlanilla(["valor"], [["\t+CMD()"]]).includes("\"'\t+CMD()\""), true);
