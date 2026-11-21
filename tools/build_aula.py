"""Genera site/aula/data.js a partir de aula/contenido.py + aula/config.json y copia el frontend.
Uso: python tools/build_aula.py  (después de tools/build_site.py)"""
import hashlib, json, shutil, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "aula"))
import contenido as c

SITE = RAIZ / "site" / "aula"
SITE.mkdir(parents=True, exist_ok=True)
cfg = json.loads((RAIZ / "aula" / "config.json").read_text(encoding="utf-8"))

SES_DIR = {1: "01_principios", 2: "02_eleccion_graficos", 3: "03_color_diseno_etica", 4: "04_visual_analytics_kpis",
           5: "05_dashboards_interactivos", 6: "06_reporting_automatizado", 7: "07_estructuras_complejas", 8: "08_redes_e_integrador"}
LABS = {1: "lab01_percepcion", 2: "lab02_eleccion_graficos", 3: "lab03_color_diseno_etica", 4: "lab04_kpis_storytelling",
        5: "lab05_dashboards_plotly", 6: "lab06_reportes_automaticos", 7: "lab07_complejas", 8: "lab08_redes"}

CORTO = {1: "Principios y percepción", 2: "Elección de gráficos", 3: "Color, diseño y ética", 4: "KPIs y storytelling", 5: "Dashboards", 6: "Reporting automatizado", 7: "Estructuras complejas", 8: "Redes e integrador"}
RMD = {1: "01_percepcion", 2: "02_eleccion_graficos", 3: "03_color_diseno_etica", 4: "04_kpis_storytelling",
       5: "05_dashboards_interactivos", 6: "06_reporting_automatizado", 7: "07_estructuras_complejas", 8: "08_redes"}
FICHA = {1: "ficha_01_percepcion", 2: "ficha_02_eleccion", 3: "ficha_03_color_etica", 4: "ficha_04_kpis_storytelling",
         5: "ficha_05_dashboards", 6: "ficha_06_reporting", 7: "ficha_07_complejas", 8: "ficha_08_redes"}
import recursos as rc
import tutor as tt
import agenda as ag
sys.path.insert(0, str(RAIZ / "datos_reales"))
import catalogo as cat
INFO_TXT = ("Tres bloques. Izquierda: procesamiento preatentivo (memoria icónica que procesa atributos antes de la cognición), jerarquía de la Gestalt (conexión y encierro superan a la proximidad) y contraste de accesibilidad WCAG de 3:1. "
  "Centro: jerarquía de tareas perceptivas, de mayor a menor precisión: posición en escala común, escalas no alineadas, longitud/dirección/ángulo, área, volumen y curvatura, sombreado y saturación. "
  "Derecha: los tres pilares del mapeo de datos (atributos del dato, codificación visual adecuada y claridad de propósito) y el rediseño de gráficos tradicionales: gráfico circular, barras divididas y mapa de coropletas se reemplazan por puntos agrupados, rectángulos enmarcados y diferencias representadas directamente.")
# Presentaciones incrustadas por sesión (los archivos se generan con tools/procesar_presentacion.py)
PRESENTACIONES = {1: {"dir": "unidad1", "titulo": "Presentación de la unidad", "infografia": True},
                  2: {"dir": "unidad2_eleccion", "titulo": "Presentación: elección de gráficos"},
                  4: {"dir": "unidad2_ggplot", "titulo": "Presentación: ggplot2, capa por capa"},
                  5: [{"dir": "unidad5_dashboards", "titulo": "Presentación 1: dashboards con datos de aduanas"},
                      {"dir": "unidad5_tablero_shiny", "titulo": "Presentación 2: tablero dinámico en RStudio (Shiny)"},
                      {"dir": "unidad5_looker", "titulo": "Presentación 3: Looker Studio con el Censo Agropecuario 2022"}]}
R_OK = {"pr01_explorador", "pr02_dncp", "pr03_banco_mundial"}
sesiones = []
for s in c.SESIONES:
    n, d = s["n"], SES_DIR[s["n"]]
    rec = [
        {"t": "Guía de la sesión (agenda y objetivos)", "u": f"../sesiones/{d}/index.html", "k": "guia"},
        {"t": "Ficha de estudio (PDF)", "u": f"../materiales/pdf/{FICHA[n]}.pdf", "k": "pdf"},
        {"t": "Python · Laboratorio en Google Colab", "u": f"{cfg['colab']}/sesiones/{d}/{LABS[n]}.ipynb", "k": "colab"},
        {"t": "R · Documento R Markdown para RStudio (.Rmd)", "u": f"{cfg['repo']}/blob/main/r/{RMD[n]}.Rmd", "k": "rmd"},
        {"t": "R · Descargar el .Rmd", "u": f"{cfg['raw']}/r/{RMD[n]}.Rmd", "k": "descarga"},
        {"t": "Código Python del laboratorio (.py)", "u": f"{cfg['repo']}/blob/main/sesiones/{d}/{LABS[n]}.py", "k": "codigo"},
        {"t": "Materiales en Google Drive", "u": f"https://drive.google.com/drive/folders/{cfg['drive']['sesiones'][str(n)]}", "k": "drive"},
    ]
    if n == 1:
        rec.insert(3, {"t": "Python · Lab 0 en Colab: resultados del diagnóstico", "u": f"{cfg['colab']}/sesiones/01_principios/lab00_diagnostico.ipynb", "k": "colab"})
        rec.insert(5, {"t": "R · 00_diagnostico.Rmd: resultados del diagnóstico (RPubs)", "u": f"{cfg['repo']}/blob/main/r/00_diagnostico.Rmd", "k": "rmd"})
    if n == 4:
        rec.insert(5, {"t": "R · Ejercicio guiado: ocupación en Concepción con la EPHC (.Rmd)", "u": f"{cfg['repo']}/blob/main/r/04_ejercicio_ephc_concepcion.Rmd", "k": "rmd"})
        rec.insert(6, {"t": "R · Descargar el .Rmd del ejercicio", "u": f"{cfg['raw']}/r/04_ejercicio_ephc_concepcion.Rmd", "k": "descarga"})
    if n == 5:
        rec.insert(5, {"t": "R · Tablero de aduanas con código Python en RStudio (reticulate, .Rmd)", "u": f"{cfg['repo']}/blob/main/r/05_tablero_aduanas_python.Rmd", "k": "rmd"})
        rec.insert(6, {"t": "R · Descargar el .Rmd del tablero de aduanas", "u": f"{cfg['raw']}/r/05_tablero_aduanas_python.Rmd", "k": "descarga"})
        rec.insert(7, {"t": "Tablero interactivo: valor mensual por medio de transporte (plotly)", "u": "media/unidad5_dashboards/tablero_i1.html", "k": "web"})
        rec.insert(8, {"t": "Tablero interactivo: evolución mensual y ranking de aduanas (plotly)", "u": "media/unidad5_dashboards/tablero_d1.html", "k": "web"})
        rec.insert(9, {"t": "R · Tablero dinámico Shiny de aduanas: app.R (abrir en RStudio y Run App)", "u": f"{cfg['repo']}/blob/main/r/app_tablero_aduanas/app.R", "k": "rmd"})
        rec.insert(10, {"t": "R · Descargar app.R del tablero Shiny", "u": f"{cfg['raw']}/r/app_tablero_aduanas/app.R", "k": "descarga"})
        rec.insert(11, {"t": "Datos del CAN 2022 por departamento (CSV) para Looker Studio", "u": f"{cfg['raw']}/aula/media/unidad5_looker/fuentes/datos/can2022_departamentos.csv", "k": "descarga"})
        rec.insert(12, {"t": "Datos del CAN 2022 por tamaño de finca (CSV)", "u": f"{cfg['raw']}/aula/media/unidad5_looker/fuentes/datos/can2022_estratos.csv", "k": "descarga"})
        rec.insert(13, {"t": "Guía paso a paso: informe de Looker Studio con el CAN 2022", "u": f"{cfg['repo']}/blob/main/docs/looker_studio_can2022.md", "k": "guia"})
    if n == 5: rec.append({"t": "App Dash de ejemplo (app_dash.py)", "u": f"{cfg['repo']}/blob/main/sesiones/{d}/app_dash.py", "k": "codigo"})
    if n == 6: rec.append({"t": "R · Plantilla de informe parametrizado", "u": f"{cfg['repo']}/blob/main/r/plantilla_reporte_sucursal.Rmd", "k": "rmd"})
    prs = [{"id": pid, "nombre": nm, "desc": ds, "rol": rol, "colab": f"{cfg['colab']}/practicas_reales/{pid}.ipynb", "rmd": (f"{cfg['repo']}/blob/main/r/{pid}.Rmd" if pid in R_OK else "")} for pid, nm, ds, ses, rol in cat.PRACTICAS if n in ses and rol != "docente"]
    qids = ([str(n)] if n in c.QUIZZES else []) + [e["id"] for e in c.QUIZZES_EXTRA if e["sesion"] == n]
    media = []
    mcs = PRESENTACIONES.get(n) or []
    for mc in (mcs if isinstance(mcs, list) else [mcs]):
        d_ = mc["dir"]
        if not (RAIZ / "aula" / "media" / d_ / "slides.json").exists(): continue
        sl = json.loads((RAIZ / "aula" / "media" / d_ / "slides.json").read_text(encoding="utf-8"))
        md = {"titulo": mc["titulo"], "base": f"media/{d_}/diapositivas", "slides": sl, "pdf": f"media/{d_}/presentacion.pdf", "pptx": f"media/{d_}/presentacion.pptx"}
        if mc.get("infografia"):
            md["infografia"] = {"src": f"media/{d_}/infografia.webp", "alt": "Infografía: La ciencia de la percepción gráfica. Jerarquía y principios de diseño visual", "descripcion": INFO_TXT}
        media.append(md)
    media = media or None
    s2 = {k: v for k, v in s.items() if k != "lecturas"}
    sesiones.append({**s2, "corto": CORTO[n], "quizIds": qids, "media": media, "practicas_reales": prs, "recursos": rec, "videos": rc.VIDEOS.get(n, []), "lecturas": rc.LECTURAS.get(n, []), "quiz": n in c.QUIZZES})

cfg["fechas"] = {**cfg.get("fechas", {}), **{k: v for k, v in ag.fechas().items() if not cfg.get("fechas", {}).get(k)}}
data = {
    "config": cfg,
    "agenda_base": {"eventos": ag.eventos(), "nota": "Calendario base cargado desde el aula."},
    "sesiones": sesiones,
    "quizzes": {**{str(k): {"titulo": v[0], "preguntas": v[1], "sesion": k, "etiqueta": str(k)} for k, v in c.QUIZZES.items()},
                **{e["id"]: {"titulo": e["titulo"], "preguntas": e["preguntas"], "sesion": e["sesion"], "etiqueta": e["etiqueta"], "ubicacion": e.get("ubicacion", "final"), "deck": e.get("deck", 0), "nota": e.get("nota", ""), "volver": e.get("volver", "")} for e in c.QUIZZES_EXTRA}},
    "rubricas": {k: {"titulo": v[0], "criterios": [{"n": a, "w": b} for a, b in v[1]]} for k, v in c.RUBRICAS.items()},
    "abiertos": {"fuentes": cat.FUENTES, "estados": {k: list(v) for k, v in cat.ESTADOS.items()},
                 "practicas": [{"id": pid, "nombre": nm, "desc": ds, "sesiones": ses, "rol": rol, "colab": f"{cfg['colab']}/practicas_reales/{pid}.ipynb", "rmd": (f"{cfg['repo']}/blob/main/r/{pid}.Rmd" if pid in R_OK else "")} for pid, nm, ds, ses, rol in cat.PRACTICAS]},
    "tutor": {**tt.TUTOR, "links": tt.LINKS + cfg.get("tutor_links", [])},
    "glosario": [{"t": a, "d": b} for a, b in c.GLOSARIO],
    "materiales": [("00_guia_inicio", "Guía de inicio: Colab, RStudio y RPubs"), ("elegir_grafico", "Hoja de ruta: elegir el gráfico"), ("checklist_calidad_etica", "Checklist de calidad visual y ética"), ("rubricas", "Rúbricas de evaluación"), ("evaluacion", "Cómo se evalúa el curso")],
    "datasets": [("ventas_retail.csv", "Ventas diarias 2024-25 (5 sucursales × 4 categorías)"), ("notas_estudiantes.csv", "Horas de estudio, asistencia y notas"),
                 ("demanda_energia.csv", "Serie diaria de demanda de energía"), ("departamentos_py.csv", "Departamentos de Paraguay (indicadores sintéticos)"),
                 ("anscombe.csv", "Cuarteto de Anscombe"), ("wine.csv", "Vinos: 13 variables y 3 clases (alta dimensionalidad)"), ("karate_aristas.csv", "Red Zachary Karate Club: aristas (+ karate_nodos.csv)"), ("lesmis_aristas.csv", "Red Les Misérables: aristas con peso")],
}
(SITE / "data.js").write_text("window.CURSO=" + json.dumps(data, ensure_ascii=False) + ";", encoding="utf-8")
for f in ("index.html", "aula.css", "aula.js", "backend.js", "planillas.mjs", "xlsx.mjs", "fx.js", "fxbg.js", "visibilidad.js"):
    shutil.copy(RAIZ / "aula" / f, SITE / f)

# Pages conserva archivos en caché; cada importación debe apuntar a la versión del archivo copiado.
def version(nombre):
    return hashlib.sha256((SITE / nombre).read_bytes()).hexdigest()[:12]

modulo = SITE / "aula.js"
codigo = modulo.read_text(encoding="utf-8")
for nombre in ("backend.js", "planillas.mjs", "xlsx.mjs", "fx.js", "visibilidad.js"):
    codigo = codigo.replace(f'"./{nombre}"', f'"./{nombre}?v={version(nombre)}"')
modulo.write_text(codigo, encoding="utf-8")

entrada = SITE / "index.html"
html = entrada.read_text(encoding="utf-8")
for nombre in ("aula.css", "data.js", "fxbg.js", "aula.js"):
    html = html.replace(f'"{nombre}"', f'"{nombre}?v={version(nombre)}"')
entrada.write_text(html, encoding="utf-8")

shutil.copytree(RAIZ / "aula" / "vendor", SITE / "vendor", dirs_exist_ok=True)
shutil.copytree(RAIZ / "aula" / "media", SITE / "media", dirs_exist_ok=True, ignore=shutil.ignore_patterns("fuentes"))
shutil.copytree(RAIZ / "materiales" / "pdf", SITE.parent / "materiales" / "pdf", dirs_exist_ok=True)
print("aula generada en", SITE)
