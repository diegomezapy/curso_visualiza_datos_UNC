"""Genera moodle/: material listo para importar/pegar en Moodle (banco de preguntas XML, glosario XML, páginas HTML por sesión) + guía de montaje.
Uso: python tools/build_moodle.py"""
import sys, json, shutil, html
from pathlib import Path
from xml.sax.saxutils import escape
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "aula"))
import contenido as c, recursos as rc, agenda as ag
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
fechas = ag.fechas()
cdata = lambda t: "<![CDATA[" + t.replace("]]>", "]]]]><![CDATA[>") + "]]>"

def xml_preguntas(sesiones):
    o = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    for n in sesiones:
        titulo, preg = c.QUIZZES[n]
        o.append(f'<question type="category"><category><text>$course$/top/Visualización de datos/Sesión {n}</text></category></question>')
        for i, q in enumerate(preg, 1):
            o.append(f'<question type="multichoice"><name><text>S{n}-Q{i}</text></name><questiontext format="html"><text>{cdata("<p>" + html.escape(q["q"]) + "</p>")}</text></questiontext>'
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
           li(f"{cfg['raw']}/r/{RMD[n]}.Rmd", "⬇ Descargar el .Rmd"), li(f"{WEB}/materiales/pdf/{FICHA[n]}.pdf", "📄 Ficha de estudio (PDF)"), li(f"{WEB}/sesiones/{d}/index.html", "📖 Guía completa de la sesión")]
    vids = "".join(li(f"https://www.youtube.com/watch?v={v['id']}" if v.get("tipo") != "playlist" else f"https://www.youtube.com/playlist?list={v['id']}", v["t"] + (" · " + v["nota"] if v.get("nota") else "")) for v in rc.VIDEOS.get(n, []))
    lec = "".join(li(l["u"], f"{l['t']} ({l['tipo']}, {l['idioma']})") for l in rc.LECTURAS.get(n, []))
    acts = "".join(f"<li>{html.escape(a['titulo'])}" + (f" — <b>{a['pts']} pts</b>" if a["pts"] else "") + "</li>" for a in s["actividades"])
    return f"""<h3>Sesión {n} · {html.escape(s['titulo'])}</h3>
<p><b>Cuándo:</b> {fechas[str(n)]} (clase virtual). <b>Unidad:</b> {s['unidad']}.</p>
<p>{html.escape(s['resumen'])}</p>
<h4>🎯 Objetivos</h4><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in s['objetivos'])}</ul>
<h4>🧰 Materiales</h4><ul>{''.join(rec)}</ul>
{f'<h4>🎬 Videos</h4><ul>{vids}</ul>' if vids else ''}
{f'<h4>📚 Lecturas</h4><ul>{lec}</ul>' if lec else ''}
<h4>✅ Actividades</h4><ul>{acts}</ul>
<p><i>Python en Colab: Entorno de ejecución → Ejecutar todas. R: abrir el .Rmd en RStudio, Knit y Publish → RPubs.</i></p>"""

def glosario():
    e = "".join(f'<ENTRY><CONCEPT>{escape(a)}</CONCEPT><DEFINITION>{escape(b)}</DEFINITION><FORMAT>1</FORMAT><USEDYNALINK>1</USEDYNALINK><CASESENSITIVE>0</CASESENSITIVE><FULLMATCH>0</FULLMATCH><TEACHERENTRY>1</TEACHERENTRY></ENTRY>' for a, b in c.GLOSARIO)
    return f'<?xml version="1.0" encoding="UTF-8"?><GLOSSARY><INFO><NAME>Glosario de visualización de datos</NAME><INTRO>Términos clave del curso.</INTRO><INTROFORMAT>1</INTROFORMAT><ALLOWDUPLICATEDENTRIES>0</ALLOWDUPLICATEDENTRIES><DISPLAYFORMAT>dictionary</DISPLAYFORMAT><SHOWSPECIAL>1</SHOWSPECIAL><SHOWALPHABET>1</SHOWALPHABET><SHOWALL>1</SHOWALL><ALLOWCOMMENTS>0</ALLOWCOMMENTS><USEDYNALINK>1</USEDYNALINK><DEFAULTAPPROVAL>1</DEFAULTAPPROVAL><GLOBALGLOSSARY>0</GLOBALGLOSSARY><ENTBYPAGE>20</ENTBYPAGE><ENTRIES>{e}</ENTRIES></INFO></GLOSSARY>'

(OUT / "preguntas" / "banco_completo.xml").write_text(xml_preguntas(sorted(c.QUIZZES)), encoding="utf-8")
for n in sorted(c.QUIZZES): (OUT / "preguntas" / f"quiz_sesion_{n}.xml").write_text(xml_preguntas([n]), encoding="utf-8")
(OUT / "glosario.xml").write_text(glosario(), encoding="utf-8")
for s in c.SESIONES: (OUT / "paginas" / f"sesion_{s['n']}.html").write_text(pagina(s), encoding="utf-8")
print("moodle/ generado:", len(list(OUT.rglob("*.*"))), "archivos")
