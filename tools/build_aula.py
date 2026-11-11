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
sesiones = []
for s in c.SESIONES:
    n, d = s["n"], SES_DIR[s["n"]]
    rec = [
        {"t": "Guía de la sesión (agenda, lecturas)", "u": f"../sesiones/{d}/index.html", "k": "guia"},
        {"t": "Laboratorio en Google Colab", "u": f"{cfg['colab']}/sesiones/{d}/{LABS[n]}.ipynb", "k": "colab"},
        {"t": "Código del laboratorio (.py)", "u": f"{cfg['repo']}/blob/main/sesiones/{d}/{LABS[n]}.py", "k": "codigo"},
        {"t": "Materiales en Google Drive", "u": f"https://drive.google.com/drive/folders/{cfg['drive']['sesiones'][str(n)]}", "k": "drive"},
    ]
    if n == 5: rec.append({"t": "App Dash de ejemplo (app_dash.py)", "u": f"{cfg['repo']}/blob/main/sesiones/{d}/app_dash.py", "k": "codigo"})
    for t, u in s["lecturas"]: rec.append({"t": "Lectura: " + t, "u": u, "k": "lectura"})
    sesiones.append({**s, "corto": CORTO[n], "recursos": rec, "quiz": n in c.QUIZZES})

data = {
    "config": cfg,
    "sesiones": sesiones,
    "quizzes": {str(k): {"titulo": v[0], "preguntas": v[1]} for k, v in c.QUIZZES.items()},
    "rubricas": {k: {"titulo": v[0], "criterios": [{"n": a, "w": b} for a, b in v[1]]} for k, v in c.RUBRICAS.items()},
    "glosario": [{"t": a, "d": b} for a, b in c.GLOSARIO],
    "datasets": [("ventas_retail.csv", "Ventas diarias 2024-25 (5 sucursales × 4 categorías)"), ("notas_estudiantes.csv", "Horas de estudio, asistencia y notas"),
                 ("demanda_energia.csv", "Serie diaria de demanda de energía"), ("departamentos_py.csv", "Departamentos de Paraguay (indicadores sintéticos)"),
                 ("anscombe.csv", "Cuarteto de Anscombe")],
}
(SITE / "data.js").write_text("window.CURSO=" + json.dumps(data, ensure_ascii=False) + ";", encoding="utf-8")
for f in ("index.html", "aula.css", "aula.js", "backend.js"):
    shutil.copy(RAIZ / "aula" / f, SITE / f)
shutil.copytree(RAIZ / "aula" / "vendor", SITE / "vendor", dirs_exist_ok=True)
print("aula generada en", SITE)
