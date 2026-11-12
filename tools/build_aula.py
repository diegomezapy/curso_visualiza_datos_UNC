"""Genera site/aula/data.js a partir de aula/contenido.py + aula/config.json y copia el frontend.
Uso: python tools/build_aula.py  (después de tools/build_site.py)"""
import json, shutil, sys
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
    if n == 5: rec.append({"t": "App Dash de ejemplo (app_dash.py)", "u": f"{cfg['repo']}/blob/main/sesiones/{d}/app_dash.py", "k": "codigo"})
    if n == 6: rec.append({"t": "R · Plantilla de informe parametrizado", "u": f"{cfg['repo']}/blob/main/r/plantilla_reporte_sucursal.Rmd", "k": "rmd"})
    s2 = {k: v for k, v in s.items() if k != "lecturas"}
    sesiones.append({**s2, "corto": CORTO[n], "recursos": rec, "videos": rc.VIDEOS.get(n, []), "lecturas": rc.LECTURAS.get(n, []), "quiz": n in c.QUIZZES})

data = {
    "config": cfg,
    "sesiones": sesiones,
    "quizzes": {str(k): {"titulo": v[0], "preguntas": v[1]} for k, v in c.QUIZZES.items()},
    "rubricas": {k: {"titulo": v[0], "criterios": [{"n": a, "w": b} for a, b in v[1]]} for k, v in c.RUBRICAS.items()},
    "glosario": [{"t": a, "d": b} for a, b in c.GLOSARIO],
    "materiales": [("00_guia_inicio", "Guía de inicio: Colab, RStudio y RPubs"), ("elegir_grafico", "Hoja de ruta: elegir el gráfico"), ("checklist_calidad_etica", "Checklist de calidad visual y ética"), ("rubricas", "Rúbricas de evaluación"), ("evaluacion", "Cómo se evalúa el curso")],
    "datasets": [("ventas_retail.csv", "Ventas diarias 2024-25 (5 sucursales × 4 categorías)"), ("notas_estudiantes.csv", "Horas de estudio, asistencia y notas"),
                 ("demanda_energia.csv", "Serie diaria de demanda de energía"), ("departamentos_py.csv", "Departamentos de Paraguay (indicadores sintéticos)"),
                 ("anscombe.csv", "Cuarteto de Anscombe"), ("wine.csv", "Vinos: 13 variables y 3 clases (alta dimensionalidad)"), ("karate_aristas.csv", "Red Zachary Karate Club: aristas (+ karate_nodos.csv)"), ("lesmis_aristas.csv", "Red Les Misérables: aristas con peso")],
}
(SITE / "data.js").write_text("window.CURSO=" + json.dumps(data, ensure_ascii=False) + ";", encoding="utf-8")
for f in ("index.html", "aula.css", "aula.js", "backend.js"):
    shutil.copy(RAIZ / "aula" / f, SITE / f)
shutil.copytree(RAIZ / "aula" / "vendor", SITE / "vendor", dirs_exist_ok=True)
shutil.copytree(RAIZ / "materiales" / "pdf", SITE.parent / "materiales" / "pdf", dirs_exist_ok=True)
print("aula generada en", SITE)
