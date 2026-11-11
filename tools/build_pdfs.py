"""Genera los PDF de materiales (fichas, guía de inicio, hojas de referencia) en materiales/pdf/.
Requiere: python-markdown y Playwright con Chromium (node).  Uso: python tools/build_pdfs.py"""
import html, subprocess, sys, tempfile, json, re
from pathlib import Path
import markdown
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "materiales"))
import fichas as F

OUT = RAIZ / "materiales" / "pdf"; OUT.mkdir(parents=True, exist_ok=True)
TMP = Path(tempfile.mkdtemp())
CSS = """@page{size:A4;margin:15mm 15mm 16mm}
*{box-sizing:border-box}body{font:10.5pt/1.45 'Inter','Segoe UI',Arial,sans-serif;color:#1f2328;margin:0}
header{border-bottom:3px solid #0072B2;padding-bottom:6px;margin-bottom:12px}
header .k{font-size:8.5pt;color:#59636e;text-transform:uppercase;letter-spacing:.06em}
h1{font-size:19pt;margin:2px 0 0;color:#0b2e4a}h2{font-size:12pt;margin:14px 0 5px;color:#0072B2;border-bottom:1px solid #d1d9e0;padding-bottom:2px}
ul,ol{margin:4px 0 4px 18px;padding:0}li{margin:3px 0}
code{font-family:'JetBrains Mono',Consolas,monospace;font-size:8.6pt;background:#f1f4f7;padding:0 3px;border-radius:3px}
pre{background:#0d1b2a;color:#e6edf3;border-radius:6px;padding:8px 10px;font:8.3pt/1.4 Consolas,'DejaVu Sans Mono',monospace;margin:4px 0;white-space:pre-wrap;word-break:break-word}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:10px}.lab{font-size:8.5pt;font-weight:700;color:#59636e;text-transform:uppercase;letter-spacing:.05em}
.box{border:1px solid #d1d9e0;border-radius:6px;padding:6px 10px;background:#f8fafc}.err li::marker{content:'✗  ';color:#c2410c}.chk li::marker{content:'☐  '}
table{border-collapse:collapse;width:100%;font-size:9pt}th,td{border:1px solid #d1d9e0;padding:4px 6px;text-align:left;vertical-align:top}th{background:#eaf2f8}
.warn{border-left:4px solid #D55E00;background:#fff4ec;padding:5px 9px;border-radius:0 6px 6px 0}footer{margin-top:14px;font-size:8pt;color:#59636e;border-top:1px solid #d1d9e0;padding-top:4px}"""
def doc(titulo, kicker, cuerpo):
    return f"<!doctype html><html lang='es'><meta charset='utf-8'><style>{CSS}</style><body><header><div class='k'>{kicker}</div><h1>{titulo}</h1></header>{cuerpo}<footer>Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET – UNC · Material docente CC BY-NC-SA 4.0</footer></body></html>"
def ul(items, cls=""): return f"<ul class='{cls}'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
paginas = {}

for nombre, f in F.FICHAS.items():
    cuerpo = f"<h2>Ideas clave</h2>{ul(f['claves'])}<h2>Errores frecuentes</h2>{ul(f['errores'], 'err')}" \
             f"<h2>Receta rápida</h2><div class='cols'><div><div class='lab'>Python (Colab)</div><pre>{html.escape(f['py'])}</pre></div><div><div class='lab'>R (RStudio → RPubs)</div><pre>{html.escape(f['r'])}</pre></div></div>" \
             f"<div class='cols'><div><h2>Checklist</h2><div class='box'>{ul(f['check'], 'chk')}</div></div><div><h2>Para profundizar</h2>{ul(f['mas'])}</div></div>"
    paginas[nombre] = doc(f["titulo"], f"Ficha de estudio · Sesión {f['sesion']}", cuerpo)

g = F.GUIA_INICIO
paginas["00_guia_inicio"] = doc(g["titulo"], "Empezá acá", "".join(f"<h2>{t}</h2>{c}" for t, c in g["secciones"]))

cuerpo = "".join(f"<h2>{t}</h2><div class='box'>{ul(i, 'chk')}</div>" for t, i in F.CHECKLIST)
paginas["checklist_calidad_etica"] = doc("Checklist de calidad visual y ética", "Hoja de referencia · usar en todo entregable", cuerpo)

filas = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td style='color:#c2410c'>{e}</td></tr>" for a, b, c, d, e in F.ELEGIR)
paginas["elegir_grafico"] = doc("Hoja de ruta: elegir el gráfico", "Hoja de referencia · sesiones 1-2",
  f"<table><tr><th>Pregunta</th><th>Datos</th><th>Primera opción</th><th>Alternativas</th><th>Evitar</th></tr>{filas}</table>"
  "<p>Principio rector: <b>posición &gt; longitud &gt; ángulo &gt; área &gt; color</b>. Si dudás: data-to-viz.com.</p>")

md = lambda p: re.sub(r'href="(?!https?:)[^"]*"', "", markdown.markdown((RAIZ / p).read_text(encoding="utf-8"), extensions=["tables"]))
paginas["rubricas"] = doc("Rúbricas de comunicación visual", "Evaluación", md("docs/rubricas.md").replace("<h1>Rúbricas de comunicación visual</h1>", ""))
paginas["evaluacion"] = doc("Evaluación del curso", "Evaluación", md("docs/evaluacion.md").replace("<h1>Evaluación (100 puntos)</h1>", ""))

lista = []
for n, h in paginas.items():
    (TMP / f"{n}.html").write_text(h, encoding="utf-8"); lista.append(n)
js = f"""const {{chromium}}=require('playwright');
(async()=>{{const b=await chromium.launch();const p=await b.newPage();
for(const n of {json.dumps(lista)}){{await p.goto('file://{TMP}/'+n+'.html');await p.pdf({{path:'{OUT}/'+n+'.pdf',format:'A4',printBackground:true,preferCSSPageSize:true}});}}
await b.close()}})()"""
(TMP / "run.js").write_text(js)
subprocess.run(["node", str(TMP / "run.js")], check=True)
print("PDF generados:", len(lista), "→", OUT)
