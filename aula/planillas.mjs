/* Planillas del panel docente. No se publican datos: el archivo se genera en el navegador del docente. */
const celda = valor => {
  let s = String(valor ?? "");
  // Excel y otras planillas pueden ejecutar fórmulas al abrir un CSV.
  if (typeof valor === "string" && /^[\s\uFEFF]*[=+\-@]/.test(s)) s = "'" + s;
  return `"${s.replace(/"/g, '""')}"`;
};

export function csvPlanilla(encabezados, filas) {
  return "\uFEFF" + [encabezados, ...filas].map(fila => fila.map(celda).join(",")).join("\r\n") + "\r\n";
}

export function planillaRegistros(alumnos) {
  const encabezados = ["uid", "apellidos", "nombres", "cedula", "fecha_nacimiento", "sexo", "nacionalidad", "departamento", "ciudad", "direccion", "telefono", "institucion", "profesion", "email", "cohorte", "consentimiento_fecha", "consentimiento_version"];
  const filas = alumnos.map(({ uid, perfil: p }) => [uid, p.apellidos, p.nombres, p.cedula, p.fechaNac, p.sexo, p.nacionalidad, p.departamento, p.ciudad, p.direccion, p.telefono, p.institucion, p.profesion, p.email, p.cohorte, p.consentimiento?.fecha, p.consentimiento?.version]);
  return csvPlanilla(encabezados, filas);
}

export function planillaQuizzes(alumnos, intentos) {
  const encabezados = ["uid", "apellidos", "nombres", "email", "sesion", "quiz", "intento_id", "fecha", "puntaje_%", "pregunta_numero", "pregunta", "respuesta", "respuesta_correcta", "acierto", "estado"];
  const porUid = new Map(alumnos.map(a => [a.uid, a.perfil]));
  const ids = new Set(intentos.map(i => i.id));
  const filas = [];
  for (const i of intentos) {
    const p = porUid.get(i.uid) || {};
    const base = [i.uid, p.apellidos, p.nombres, p.email, i.sesion, i.quizTitulo, i.id, i.fecha, i.pct];
    for (const [n, r] of (i.respuestas || []).entries()) filas.push([...base, n + 1, r.pregunta, r.respuesta, r.correcta, r.acierto ? "Sí" : "No", "detalle"]);
  }
  // Los intentos anteriores a esta función conservan fecha y nota, pero nunca guardaron respuestas.
  for (const a of alumnos) for (const [sesion, q] of Object.entries(a.progreso?.quiz || {})) {
    for (const i of q.intentos || []) {
      if (i.id && ids.has(i.id)) continue;
      filas.push([a.uid, a.perfil.apellidos, a.perfil.nombres, a.perfil.email, sesion, "", i.id || "", i.t, i.pct, "", "", "", "", "", "histórico sin detalle"]);
    }
  }
  filas.sort((a, b) => String(a[7] || "").localeCompare(String(b[7] || "")));
  return csvPlanilla(encabezados, filas);
}

export function planillaAutoevaluaciones(alumnos, actividades, rubricas) {
  const encabezados = ["uid", "apellidos", "nombres", "email", "sesion", "actividad", "rubrica", "criterio", "peso_%", "nivel", "descripcion_nivel"];
  const niveles = ["Sin responder", "Insuficiente", "En desarrollo", "Logrado", "Sobresaliente"];
  const filas = [];
  for (const a of alumnos) for (const act of actividades) {
    const valores = a.progreso?.auto?.[act.id], rubrica = rubricas[act.rubrica];
    if (!rubrica || !valores) continue;
    rubrica.criterios.forEach((c, n) => {
      const nivel = Number(valores[n]) || 0;
      if (nivel) filas.push([a.uid, a.perfil.apellidos, a.perfil.nombres, a.perfil.email, act.n, act.titulo, rubrica.titulo, c.n, c.w, nivel, niveles[nivel] || ""]);
    });
  }
  return csvPlanilla(encabezados, filas);
}
