"""Calendario real del módulo (datos de coordinación académica, 26/10/2026).
Clases virtuales: viernes 18:00-22:00 y sábados 08:00-12:00. Inicio: viernes 13/11/2026. 4 semanas, 32 h sincrónicas.
No se publican honorarios ni otros datos contractuales."""
import datetime as dt
VIE = ("18:00", "22:00"); SAB = ("08:00", "12:00")
CORTO = ["Principios y percepción", "Elección de gráficos", "Color, diseño y ética", "KPIs y storytelling", "Dashboards interactivos", "Reporting automatizado", "Estructuras complejas", "Redes e integrador"]
INICIO = dt.date(2026, 11, 13)  # viernes
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
ENLACE_CLASE = "https://www.facet-unc.edu.py/moodle/mod/url/view.php?id=6792"
ENLACE_TAREA_S3 = "https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/index.html#/sesion/3"
ENLACE_FORO_S3 = "https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/index.html#/foro/prensa"

def clases():
    out = []
    for n in range(1, 9):
        semana, sab = divmod(n - 1, 2)
        f = INICIO + dt.timedelta(days=7 * semana + sab)
        a, b = SAB if sab else VIE
        out.append((n, f, a, b))
    return out

def eventos():
    ev = []
    for n, f, a, b in clases():
        ev.append({"id": f"clase-{n}", "tipo": "clase", "titulo": f"Sesión {n} · {CORTO[n-1]}", "sesion": n, "fecha": f.isoformat(), "inicio": a, "fin": b,
                   "inicio_iso": f"{f.isoformat()}T{a}:00-03:00", "fin_iso": f"{f.isoformat()}T{b}:00-03:00",
                   "descripcion": "Clase virtual sincrónica (4 h). Acceso mediante el recurso de reunión del aula Moodle FACET-UNC.",
                   "enlace": ENLACE_CLASE, "accion": "Entrar a la clase", "asistencia": False, "mini": False})
    # Son fechas de apertura confirmadas, no plazos de entrega. Se muestran como eventos de día completo.
    for id_, tipo, titulo, dia, sesion, descripcion, enlace, accion in [
        ("apertura-s3", "actividad", "Ejercicio S3 disponible", dt.date(2026, 11, 24), 3,
         "La entrega del ejercicio se registra en la Unidad 3 del aula Git. No tiene fecha de cierre fijada.", ENLACE_TAREA_S3, "Ir a la entrega"),
        ("foro-prensa-s3", "foro", "Foro de prensa disponible", dt.date(2026, 11, 24), 3,
         "El foro de discusión de prensa paraguaya está abierto en el aula Git, sin fecha de cierre fijada.", ENLACE_FORO_S3, "Participar en el foro"),
    ]:
        ev.append({"id": id_, "tipo": tipo, "titulo": titulo, "sesion": sesion, "fecha": dia.isoformat(),
                   "inicio": "", "fin": "", "inicio_iso": f"{dia.isoformat()}T00:00:00-03:00",
                   "fin_iso": f"{(dia + dt.timedelta(days=1)).isoformat()}T00:00:00-03:00",
                   "todo_el_dia": True, "descripcion": descripcion, "enlace": enlace, "accion": accion,
                   "asistencia": False, "mini": False})
    return sorted(ev, key=lambda e: e["inicio_iso"])

def fechas():
    return {str(n): f"{DIAS[f.weekday()]} {f.day:02d}/{f.month:02d} · {a}–{b}" for n, f, a, b in clases()}
