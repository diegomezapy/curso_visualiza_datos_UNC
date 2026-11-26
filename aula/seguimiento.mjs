/* Resumen de participación visible solo al docente autenticado. */
const ZONA = 'America/Asuncion';
export const fechaPy = valor => {
  const d = valor?.toDate?.() || new Date(valor || 0);
  return Number.isNaN(d.getTime()) ? '' : d.toLocaleDateString('sv-SE', { timeZone: ZONA });
};
export function semanaDe(fecha = new Date(), desfase = 0) {
  const hoy = fechaPy(fecha);
  const d = new Date(`${hoy}T12:00:00Z`);
  const lunes = (d.getUTCDay() + 6) % 7;
  d.setUTCDate(d.getUTCDate() - lunes + desfase * 7);
  const inicio = d.toISOString().slice(0, 10);
  d.setUTCDate(d.getUTCDate() + 6);
  return { inicio, fin: d.toISOString().slice(0, 10) };
}
export function resumirParticipacion(alumnos, intentos, mensajes, semana) {
  const dentro = v => { const f = fechaPy(v); return f >= semana.inicio && f <= semana.fin; };
  const m = new Map(alumnos.map(a => [a.uid, { uid: a.uid, perfil: a.perfil, quizzes: 0, mediaQuiz: null, temas: 0, respuestas: 0, ultimo: '' }]));
  const nota = new Map();
  for (const i of intentos) {
    const r = m.get(i.uid);
    if (!r || !dentro(i.fecha)) continue;
    r.quizzes++;
    if (Number.isFinite(+i.pct)) { const x = nota.get(i.uid) || { suma: 0, n: 0 }; x.suma += +i.pct; x.n++; nota.set(i.uid, x); }
    const f = fechaPy(i.fecha); if (f > r.ultimo) r.ultimo = f;
  }
  for (const p of mensajes) {
    const r = m.get(p.uid);
    if (!r || !dentro(p.creado)) continue;
    if (p.tipo === 'tema') r.temas++;
    else if (p.tipo === 'respuesta') r.respuestas++;
    const f = fechaPy(p.creado); if (f > r.ultimo) r.ultimo = f;
  }
  for (const [uid, x] of nota) m.get(uid).mediaQuiz = Math.round(x.suma / x.n);
  return [...m.values()];
}
