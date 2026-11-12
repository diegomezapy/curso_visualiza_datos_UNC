"""Calendario real del módulo (datos de coordinación académica, 26/10/2026).
Clases virtuales: viernes 18:00-22:00 y sábados 08:00-12:00. Inicio: viernes 13/11/2026. 4 semanas, 32 h sincrónicas.
No se publican honorarios ni otros datos contractuales."""
import datetime as dt
VIE = ("18:00", "22:00"); SAB = ("08:00", "12:00")
CORTO = ["Principios y percepción", "Elección de gráficos", "Color, diseño y ética", "KPIs y storytelling", "Dashboards interactivos", "Reporting automatizado", "Estructuras complejas", "Redes e integrador"]
INICIO = dt.date(2026, 11, 13)  # viernes
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]

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
                   "descripcion": "Clase virtual sincrónica (4 h). El enlace de la videollamada lo envía el docente.", "asistencia": False, "mini": False})
    return ev

def fechas():
    return {str(n): f"{DIAS[f.weekday()]} {f.day:02d}/{f.month:02d} · {a}–{b}" for n, f, a, b in clases()}
