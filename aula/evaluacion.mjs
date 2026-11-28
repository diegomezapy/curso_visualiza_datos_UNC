/* Ponderación vigente del curso; las actividades anteriores conservan sus notas como registro. */
export const PESOS = Object.freeze({ cuestionarios: 25, foros: 25, trabajoFinal: 30, coedicion: 20 });

const acotar = (valor, maximo) => {
  if (valor === "" || valor == null) return 0;
  const numero = Number(valor);
  return Number.isFinite(numero) ? Math.max(0, Math.min(maximo, numero)) : 0;
};

export function puntajeCuestionarios(quiz = {}, ids = []) {
  const mejores = ids.map(id => acotar(quiz?.[id]?.mejor, 100)).sort((a, b) => b - a).slice(0, 6);
  const pct = mejores.reduce((suma, valor) => suma + valor, 0) / 6;
  return { pct, pts: pct * PESOS.cuestionarios / 100 };
}

export function calcularNota(quiz = {}, oficial = {}, ids = []) {
  const cuestionarios = puntajeCuestionarios(quiz, ids).pts;
  const foros = acotar(oficial?.s8_foros, PESOS.foros);
  const trabajoFinal = acotar(oficial?.s8_inf, 18) + acotar(oficial?.s8_pres, 12);
  const coedicion = acotar(oficial?.s8_coed, PESOS.coedicion);
  const total = cuestionarios + foros + trabajoFinal + coedicion;
  const completo = ids.filter(id => quiz?.[id]?.mejor != null).length >= 6 && ["s8_foros", "s8_inf", "s8_pres", "s8_coed"].every(id => oficial?.[id] !== "" && oficial?.[id] != null);
  const redondeado = Math.round(total);
  const escala = completo ? redondeado >= 91 ? 5 : redondeado >= 81 ? 4 : redondeado >= 70 ? 3 : redondeado >= 60 ? 2 : 1 : null;
  return { cuestionarios, foros, trabajoFinal, coedicion, total, completo, escala };
}
