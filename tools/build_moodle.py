"""Genera moodle/: material listo para importar/pegar en Moodle (banco de preguntas XML, glosario XML, páginas HTML por sesión) + guía de montaje.
Uso: python tools/build_moodle.py"""
import sys, json, shutil, html
from pathlib import Path
from xml.sax.saxutils import escape
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "aula"))
import contenido as c, recursos as rc
sys.path.insert(0, str(RAIZ / "datos_reales"))
import catalogo as cat
cfg = json.loads((RAIZ / "aula" / "config.json").read_text(encoding="utf-8"))
OUT = RAIZ / "moodle"  # GUIA_MONTAJE.md es manual: no se borra
for sub in ("paginas", "preguntas"):
    shutil.rmtree(OUT / sub, ignore_errors=True); (OUT / sub).mkdir(parents=True)
(OUT / "glosario.xml").unlink(missing_ok=True)
WEB = "https://diegomezapy.github.io/curso_visualiza_datos_UNC"
DIR = {1: "01_principios", 2: "02_eleccion_graficos", 3: "03_color_diseno_etica", 4: "04_visual_analytics_kpis", 5: "05_dashboards_interactivos", 6: "06_reporting_automatizado", 7: "07_estructuras_complejas", 8: "08_redes_e_integrador"}
LAB = {1: "lab01_percepcion", 2: "lab02_eleccion_graficos", 3: "lab03_color_diseno_etica", 4: "lab04_kpis_storytelling", 5: "lab05_dashboards_plotly", 6: "lab06_reportes_automaticos", 7: "lab07_complejas", 8: "lab08_redes"}
RMD = {1: "01_percepcion", 2: "02_eleccion_graficos", 3: "03_color_diseno_etica", 4: "04_kpis_storytelling", 5: "05_dashboards_interactivos", 6: "06_reporting_automatizado", 7: "07_estructuras_complejas", 8: "08_redes"}
FICHA = {1: "ficha_01_percepcion", 2: "ficha_02_eleccion", 3: "ficha_03_color_etica", 4: "ficha_04_kpis_storytelling", 5: "ficha_05_dashboards", 6: "ficha_06_reporting", 7: "ficha_07_complejas", 8: "ficha_08_redes"}
cdata = lambda t: "<![CDATA[" + t.replace("]]>", "]]]]><![CDATA[>") + "]]>"

def moodle_safe(markup):
    """La instalación FACET rechaza caracteres fuera del plano básico Unicode."""
    return "".join(char for char in markup if ord(char) <= 0xFFFF and char not in "\ufe0e\ufe0f")

def xml_preguntas(sesiones):
    o = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    grupos = [(f"Sesión {n}", f"S{n}", c.QUIZZES[n][1]) for n in sesiones if n in c.QUIZZES]
    grupos += [(f"Sesión {e['sesion']} · {e['categoria']}", f"S{e['etiqueta']}", e["preguntas"]) for e in c.QUIZZES_EXTRA if e["etiqueta"] in sesiones or "extras" in sesiones]
    for cat, pref, preg in grupos:
        n = pref
        o.append(f'<question type="category"><category><text>$course$/top/Visualización de datos/{cat}</text></category></question>')
        for i, q in enumerate(preg, 1):
            o.append(f'<question type="multichoice"><name><text>{pref}-Q{i}</text></name><questiontext format="html"><text>{cdata("<p>" + html.escape(q["q"]) + "</p>")}</text></questiontext>'
                     f'<generalfeedback format="html"><text>{cdata("<p>" + html.escape(q["why"]) + "</p>")}</text></generalfeedback><defaultgrade>1</defaultgrade><penalty>0.3333333</penalty><hidden>0</hidden>'
                     '<single>true</single><shuffleanswers>true</shuffleanswers><answernumbering>abc</answernumbering>'
                     '<correctfeedback format="html"><text>Correcto.</text></correctfeedback><partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback><incorrectfeedback format="html"><text>Revisá la explicación y volvé a intentar.</text></incorrectfeedback>')
            for k, op in enumerate(q["o"]):
                o.append(f'<answer fraction="{100 if k == q["c"] else 0}" format="html"><text>{cdata(html.escape(op))}</text></answer>')
            o.append("</question>")
    o.append("</quiz>"); return "\n".join(o)

def pagina(s):
    n = s["n"]; d = DIR[n]
    li = lambda a, b: f'<li><a href="{a}" target="_blank" rel="noopener">{html.escape(b)}</a></li>'
    rec = [li(f"{cfg['colab']}/sesiones/{d}/{LAB[n]}.ipynb", "🐍 Python · Laboratorio en Google Colab"), li(f"{cfg['repo']}/blob/main/r/{RMD[n]}.Rmd", "📊 R · Documento R Markdown (.Rmd) para RStudio"),
           li(f"{cfg['raw']}/r/{RMD[n]}.Rmd", "⬇ Descargar el .Rmd"), li(f"{WEB}/materiales/pdf/{FICHA[n]}.pdf", "📄 Ficha de estudio (PDF)"), li(f"{WEB}/sesiones/{d}/index.html", "📖 Guía completa de la sesión"),
           li(f"{cfg['repo']}/blob/main/sesiones/{d}/{LAB[n]}.py", "🐍 Código Python del laboratorio (.py)"),
           li(f"https://drive.google.com/drive/folders/{cfg['drive']['sesiones'][str(n)]}", "📁 Carpeta de materiales de la sesión en Drive")]
    if n == 1:
        rec += [li(f"{cfg['colab']}/sesiones/01_principios/lab00_diagnostico.ipynb", "🐍 Lab 0: resultados del diagnóstico en Colab"),
                li(f"{cfg['repo']}/blob/main/r/00_diagnostico.Rmd", "📊 Lab 0: resultados del diagnóstico en R Markdown")]
    if n == 3:
        rec.append(li(f"{WEB}/aula/tareas/ejercicio_s3_prensa_paraguaya.html", "Ejercicio S3: consigna de auditoría de prensa"))
    if n == 5:
        rec.append(li(f"{cfg['repo']}/blob/main/sesiones/{d}/app_dash.py", "🐍 Código de la aplicación Dash de ejemplo"))
        rec += [li(f"{WEB}/aula/media/unidad5_dashboards/tablero_d1.html", "🌐 Tablero interactivo: evolución mensual y ranking de aduanas"),
                li(f"{cfg['raw']}/r/05_tablero_aduanas_python.Rmd", "⬇ Descargar el .Rmd del tablero de aduanas"),
                li(f"{cfg['raw']}/r/app_tablero_aduanas/app.R", "⬇ Descargar app.R del tablero Shiny"),
                li(f"{cfg['raw']}/aula/media/unidad5_looker/fuentes/datos/can2022_estratos.csv", "⬇ Datos del CAN 2022 por tamaño de finca (CSV)")]
    if n == 6:
        rec.append(li(f"{cfg['repo']}/blob/main/r/plantilla_reporte_sucursal.Rmd", "📊 Plantilla de informe parametrizado en R Markdown"))
    practicas = [p for p in cat.PRACTICAS if n in p[3] and p[4] != "docente"]
    reales = "".join(li(f"{cfg['colab']}/practicas_reales/{pid}.ipynb", f"🐍 {nombre} · Colab") +
                    (li(f"{cfg['repo']}/blob/main/r/{pid}.Rmd", f"📊 {nombre} · R Markdown") if pid in {"pr01_explorador", "pr02_dncp", "pr03_banco_mundial"} else "")
                    for pid, nombre, _, _, _ in practicas)
    vids = "".join(li(f"https://www.youtube.com/watch?v={v['id']}" if v.get("tipo") != "playlist" else f"https://www.youtube.com/playlist?list={v['id']}", v["t"] + (" · " + v["nota"] if v.get("nota") else "")) for v in rc.VIDEOS.get(n, []))
    lec = "".join(li(l["u"], f"{l['t']} ({l['tipo']}, {l['idioma']})") for l in rc.LECTURAS.get(n, []))
    acts = "".join(f"<li>{html.escape(a['titulo'])}" + (f" — <b>{a['pts']} pts</b>" if a["pts"] else "") + "</li>" for a in s["actividades"])
    return moodle_safe(f"""<h3>Sesión {n} · {html.escape(s['titulo'])}</h3>
<p><b>Sección del aula:</b> Unidad {n}.</p>
<p>{html.escape(s['resumen'])}</p>
<h4>🎯 Objetivos</h4><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in s['objetivos'])}</ul>
<h4>🧰 Materiales</h4><ul>{''.join(rec)}</ul>
{f'<h4>🗺️ Prácticas con datos reales</h4><ul>{reales}</ul>' if reales else ''}
{f'<h4>🎬 Videos</h4><ul>{vids}</ul>' if vids else ''}
{f'<h4>📚 Lecturas</h4><ul>{lec}</ul>' if lec else ''}
{('<h4>📑 Presentación: dashboards con datos de aduanas</h4><ul>' + li(WEB + '/aula/media/unidad5_dashboards/presentacion.pdf', '📑 Presentación (PDF, 17 diapositivas)') + li(WEB + '/aula/media/unidad5_dashboards/presentacion.pptx', '⬇ Presentación (PowerPoint)') + li(WEB + '/aula/media/unidad5_dashboards/tablero_i1.html', '🌐 Tablero interactivo (plotly)') + li(cfg['repo'] + '/blob/main/r/05_tablero_aduanas_python.Rmd', '📊 R · Tablero de aduanas con Python en RStudio (.Rmd)') + '</ul><p><i>Quiz 5A: evalúa la lectura de la presentación.</i></p><h4>📑 Presentación 2: tablero dinámico en RStudio (Shiny)</h4><ul>' + li(WEB + '/aula/media/unidad5_tablero_shiny/presentacion.pdf', '📑 Presentación (PDF, 14 diapositivas)') + li(WEB + '/aula/media/unidad5_tablero_shiny/presentacion.pptx', '⬇ Presentación (PowerPoint)') + li(cfg['repo'] + '/blob/main/r/app_tablero_aduanas/app.R', '📊 R · app.R del tablero Shiny') + '</ul><p><i>Quiz 5B: evalúa la lectura de la presentación 2.</i></p><h4>📑 Presentación 3: Looker Studio con el Censo Agropecuario 2022</h4><ul>' + li(WEB + '/aula/media/unidad5_looker/presentacion.pdf', '📑 Presentación (PDF, 17 diapositivas)') + li(WEB + '/aula/media/unidad5_looker/presentacion.pptx', '⬇ Presentación (PowerPoint)') + li(cfg['raw'] + '/aula/media/unidad5_looker/fuentes/datos/can2022_departamentos.csv', '⬇ Datos del CAN 2022 por departamento (CSV)') + li(cfg['repo'] + '/blob/main/docs/looker_studio_can2022.md', '📖 Guía paso a paso') + '</ul><p><i>Quiz 5C: evalúa la lectura de la presentación 3.</i></p>') if n == 5 else ''}
{('<h4>📑 Presentación: elección de gráficos</h4><ul>' + li(WEB + '/aula/media/unidad2_eleccion/presentacion.pdf', '📑 Presentación (PDF, 20 diapositivas)') + li(WEB + '/aula/media/unidad2_eleccion/presentacion.pptx', '⬇ Presentación (PowerPoint)') + '</ul><p><i>Quiz 2A: evalúa la lectura de la presentación.</i></p>') if n == 2 else ''}
{('<h4>📑 Presentación: ggplot2, capa por capa</h4><ul>' + li(WEB + '/aula/media/unidad2_ggplot/presentacion.pdf', '📑 Presentación (PDF, 24 diapositivas)') + li(WEB + '/aula/media/unidad2_ggplot/presentacion.pptx', '⬇ Presentación (PowerPoint)') + '</ul>') if n == 4 else ''}
{('<h4>📝 Ejercicio guiado (Quiz 4B)</h4><ul>' + li(cfg['repo'] + '/blob/main/r/04_ejercicio_ephc_concepcion.Rmd', '📊 R · Ejercicio: ocupación en Concepción con la EPHC (.Rmd)') + li(cfg['raw'] + '/r/04_ejercicio_ephc_concepcion.Rmd', '⬇ Descargar el .Rmd') + '</ul>') if n == 4 else ''}
{('<h4>📑 Presentación e infografía</h4><ul>' + li(WEB + '/aula/media/unidad1/presentacion.pdf', '📑 Presentación (PDF, 14 diapositivas)') + li(WEB + '/aula/media/unidad1/presentacion.pptx', '⬇ Presentación (PowerPoint)') + li(WEB + '/aula/media/unidad1/infografia.webp', '🗺️ Infografía: la ciencia de la percepción gráfica') + '</ul><p><i>Quiz 1B: evalúa la lectura de la presentación.</i></p>') if n == 1 else ''}
<h4>✅ Actividades</h4><ul>{acts}</ul>
<p><i>Python en Colab: Entorno de ejecución → Ejecutar todas. R: abrir el .Rmd en RStudio, Knit y Publish → RPubs.</i></p>""")

def recursos_generales():
    li = lambda a, b: f'<li><a href="{a}" target="_blank" rel="noopener">{html.escape(b)}</a></li>'
    raw = cfg["raw"]
    pdfs = [("00_guia_inicio", "Guía de inicio: Colab, RStudio y RPubs"), ("elegir_grafico", "Hoja de ruta: elegir el gráfico"),
            ("checklist_calidad_etica", "Checklist de calidad visual y ética"), ("rubricas", "Rúbricas de evaluación"), ("evaluacion", "Cómo se evalúa el curso")]
    docs = [("programa", "Programa de estudios"), ("cronograma", "Cronograma"), ("evaluacion", "Evaluación"),
            ("rubricas", "Rúbricas"), ("proyecto_integrador", "Proyecto integrador"), ("bibliografia", "Bibliografía y fuentes de datos")]
    datos = [("ventas_retail.csv", "Ventas diarias 2024-25"), ("notas_estudiantes.csv", "Horas de estudio, asistencia y notas"),
             ("demanda_energia.csv", "Demanda de energía"), ("departamentos_py.csv", "Indicadores sintéticos por departamento"),
             ("anscombe.csv", "Cuarteto de Anscombe"), ("wine.csv", "Vinos: 13 variables"),
             ("karate_aristas.csv", "Red Zachary Karate Club"), ("lesmis_aristas.csv", "Red Les Misérables")]
    enlaces = li(f"{WEB}/aula/index.html", "Aula Git: recursos y actividades") + li(f"{WEB}/diagnostico/index.html", "Diagnóstico inicial")
    enlaces += li(f"{WEB}/aula/index.html#/datos", "Catálogo y prácticas con datos reales")
    enlaces += li(f"https://drive.google.com/drive/folders/{cfg['drive']['raiz']}", "Carpeta general del curso en Drive")
    enlaces += li(f"https://drive.google.com/drive/folders/{cfg['drive']['datos']}", "Datasets en Drive")
    enlaces += li(f"https://drive.google.com/drive/folders/{cfg['drive']['integrador']}", "Proyecto integrador en Drive")
    return ("<h3>Recursos generales del curso</h3><p>Materiales de consulta y descarga de la asignatura.</p>"
            f"<h4>Accesos principales</h4><ul>{enlaces}</ul>"
            f"<h4>Fichas y guías PDF</h4><ul>{''.join(li(f'{WEB}/materiales/pdf/{f}.pdf', t) for f, t in pdfs)}</ul>"
            f"<h4>Documentos del curso</h4><ul>{''.join(li(f'{WEB}/docs/{f}.html', t) for f, t in docs)}</ul>"
            f"<h4>Datasets de práctica</h4><ul>{''.join(li(f'{raw}/datos/{f}', t) for f, t in datos)}</ul>"
            "<p>Los datasets de práctica son sintéticos o de dominio público. Para análisis de datos reales, consultar el catálogo del aula Git.</p>")

def glosario():
    e = "".join(f'<ENTRY><CONCEPT>{escape(a)}</CONCEPT><DEFINITION>{escape(b)}</DEFINITION><FORMAT>1</FORMAT><USEDYNALINK>1</USEDYNALINK><CASESENSITIVE>0</CASESENSITIVE><FULLMATCH>0</FULLMATCH><TEACHERENTRY>1</TEACHERENTRY></ENTRY>' for a, b in c.GLOSARIO)
    return f'<?xml version="1.0" encoding="UTF-8"?><GLOSSARY><INFO><NAME>Glosario de visualización de datos</NAME><INTRO>Términos clave del curso.</INTRO><INTROFORMAT>1</INTROFORMAT><ALLOWDUPLICATEDENTRIES>0</ALLOWDUPLICATEDENTRIES><DISPLAYFORMAT>dictionary</DISPLAYFORMAT><SHOWSPECIAL>1</SHOWSPECIAL><SHOWALPHABET>1</SHOWALPHABET><SHOWALL>1</SHOWALL><ALLOWCOMMENTS>0</ALLOWCOMMENTS><USEDYNALINK>1</USEDYNALINK><DEFAULTAPPROVAL>1</DEFAULTAPPROVAL><GLOBALGLOSSARY>0</GLOBALGLOSSARY><ENTBYPAGE>20</ENTBYPAGE><ENTRIES>{e}</ENTRIES></INFO></GLOSSARY>'

(OUT / "preguntas" / "banco_completo.xml").write_text(xml_preguntas(sorted(c.QUIZZES) + ["extras"]), encoding="utf-8")
for e in c.QUIZZES_EXTRA:
    (OUT / "preguntas" / f"quiz_{e['etiqueta']}.xml").write_text(xml_preguntas([e["etiqueta"]]), encoding="utf-8")
for n in sorted(c.QUIZZES): (OUT / "preguntas" / f"quiz_sesion_{n}.xml").write_text(xml_preguntas([n]), encoding="utf-8")
(OUT / "glosario.xml").write_text(glosario(), encoding="utf-8")
for s in c.SESIONES: (OUT / "paginas" / f"sesion_{s['n']}.html").write_text(pagina(s), encoding="utf-8")
(OUT / "paginas" / "recursos_generales.html").write_text(recursos_generales(), encoding="utf-8")
print("moodle/ generado:", len(list(OUT.rglob("*.*"))), "archivos")
