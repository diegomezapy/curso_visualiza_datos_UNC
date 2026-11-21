"""Presentación «Dashboards: del dato al tablero» (sesión 5, Unidad 2) con la base de aduanas (DNIT), código Python ejecutado en RStudio (reticulate).
Uso: python tools/dashboards_datos.py <parquet> ; python tools/dashboards_figuras.py ; python tools/dashboards_pptx.py ;
     python tools/procesar_presentacion.py unidad5_dashboards"""
import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ggplot_pptx import *
import ggplot_pptx as G
import dashboards_spec as S
M = G.RAIZ / "aula" / "media" / "unidad5_dashboards"; FIG = M / "fuentes" / "figuras"; DAT = M / "fuentes" / "datos"
PIE = S.PIE
def pie2(sl, t=PIE): G.pie(sl, t)

def portada():
    sl = G.prs.slides.add_slide(G.BLANK); sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb(BG)
    caja(sl, 0.7, 1.35, 6.3, 0.4, ["MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC"], size=11, color=ACC, bold=True)
    caja(sl, 0.7, 2.0, 6.3, 2.2, ["Dashboards: del dato al tablero"], size=38, color=DARK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(sl, 0.7, 4.3, 6.2, 0.9, ["Cómo diseñar un tablero que responde preguntas, con datos reales de la base de aduanas (DNIT) y código Python en RStudio"], size=16, color=MUT)
    caja(sl, 0.7, 5.6, 6.2, 0.6, ["Sesión 5 · Unidad 2 · Visual analytics, KPIs y storytelling"], size=14, color=TXT)
    imagen(sl, FIG / "d1.png", 7.3, 1.9, 5.5)
    sl.notes_slide.notes_text_frame.text = "Presentación de la sesión 5: principios de diseño de tableros (jerarquía, KPI, interacción con propósito, anti-patrones) con importaciones de electrónica 2024–2025 de la base de aduanas. El código es Python y corre dentro de RStudio con reticulate."

def preguntas():
    sl = nueva("Un tablero responde preguntas de una audiencia", "Punto de partida", "Antes de dibujar: audiencia, decisión y frecuencia de uso.")
    items = [("1", "Audiencia", "¿Quién lo mira?", "Un jefe de aduanas, un analista de comercio exterior o una empresa importadora necesitan tableros distintos.", ACC),
             ("2", "Decisión", "¿Qué decisión apoya?", "«¿Dónde se concentra la importación y cómo evoluciona respecto del año anterior?»", GRN),
             ("3", "Frecuencia", "¿Cada cuánto se consulta?", "Una vista mensual de seguimiento; una exploración puntual de detalle. Cambia el nivel de detalle.", ORA)]
    y = 1.4
    for n, a, b, c, col in items:
        rect(sl, 0.5, y, 12.3, 1.4, "FFFFFF", line="C7D7E6", radius=0.06); rect(sl, 0.5, y, 0.9, 1.4, col, radius=0.06)
        caja(sl, 0.5, y, 0.9, 1.4, [n], size=30, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, 1.65, y + 0.12, 2.8, 1.16, [f"**{a}**"], size=22, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 4.6, y + 0.12, 8.0, 1.16, [b, c], size=15, anchor=MSO_ANCHOR.MIDDLE, espacio=4)
        y += 1.55
    callout(sl, 0.5, 6.1, 12.3, 0.85, "Un tablero es una pantalla única que reúne la información clave para un objetivo y se entiende de un vistazo (Few, 2013).", size=15)
    pie2(sl, "Few, S. (2013). Information Dashboard Design. Analytics Press.")

def datos():
    sl = nueva("Los datos: importaciones de electrónica en la base de aduanas", "Punto de partida", "Mostrar el código de carga y el data frame. Aclarar que el archivo viene de la DNIT con separador punto y coma y decimales con coma.")
    codigo(sl, 0.5, 1.3, 5.9, 4.3, S.SETUP, size=11)
    rows = list(csv.DictReader(open(DAT / "cubo_importaciones.csv", encoding="utf-8")))[:6]
    filas = [["anio", "mes", "aduana", "pais", "medio", "items", "fob_usd"]] + [[r["anio"], r["mes"], r["aduana"][:14], r["pais"][:10], r["medio"][:8], r["items"], f"{float(r['fob_usd']):,.0f}"] for r in rows] + [["…"] * 7]
    G.tabla(sl, 6.6, 1.3, 6.2, filas, [0.6, 0.5, 1.4, 1.1, 0.9, 0.6, 1.1], size=10, alto_fila=0.36)
    viñetas(sl, 6.6, 4.35, 6.2, 1.3, ["Datos **agregados** por año, mes, aduana, país y medio de transporte (3.304 filas).", "Sale de **141.816 filas** de subítems; el archivo original usa `;` y coma decimal.", "La base **no trae junio de 2025**: se excluye de ambos años."], size=12)
    callout(sl, 0.5, 5.85, 12.3, 1.05, "Antes de graficar: ¿qué representa una fila? ¿están todos los períodos? Un tablero hereda los problemas de sus datos.", size=15)
    pie2(sl)

def figura(f):
    sl = nueva(f["titulo"], f["tag"], f["nota"])
    n = len(f["codigo"])
    codigo(sl, 0.5, 1.3, 5.75, 3.95, f["codigo"], size=11 if n > 12 else 12)
    imagen(sl, FIG / f"{f['id']}.png", 6.45, 1.3, 6.5)
    viñetas(sl, 0.5, 5.45, 8.2, 1.6, f["puntos"], size=13)
    callout(sl, 8.95, 5.45, 3.85, 1.55, f["mensaje"], size=13)
    pie2(sl, f["pie"])

def jerarquia():
    sl = nueva("Anatomía de un tablero: qué va en cada zona", "Diseño", "El ojo lee en F/Z: arriba los KPI, en el centro la tendencia, al costado la comparación, abajo el detalle.")
    X0, Y0, W = 0.7, 1.45, 8.2
    for i in range(3):
        rect(sl, X0 + i * 2.8, Y0, 2.6, 1.05, "FFFFFF", line=ACC)
        caja(sl, X0 + i * 2.8, Y0, 2.6, 1.05, ["**KPI**", ["437 M USD", "15.813 ítems", "85 % China"][i]], size=14, color=DARK, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    rect(sl, X0, Y0 + 1.25, 5.0, 2.5, "FFFFFF", line=ORA); caja(sl, X0, Y0 + 1.25, 5.0, 2.5, ["**Tendencia**", "valor mensual 2024 vs 2025"], size=14, color=DARK, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    rect(sl, X0 + 5.2, Y0 + 1.25, 3.0, 2.5, "FFFFFF", line=GRN); caja(sl, X0 + 5.2, Y0 + 1.25, 3.0, 2.5, ["**Comparación**", "ranking de aduanas"], size=14, color=DARK, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    rect(sl, X0, Y0 + 3.95, W, 1.0, "FFFFFF", line="7FB0CF"); caja(sl, X0, Y0 + 3.95, W, 1.0, ["**Detalle bajo demanda**", "tabla filtrable · mapa de calor"], size=14, color=DARK, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    zonas = [("1", "Arriba: **KPI** con su comparación"), ("2", "Centro: **tendencia** en el tiempo"), ("3", "Costado: **comparación** entre categorías"), ("4", "Abajo: **detalle** para quien lo necesite")]
    y = 1.5
    for n, t in zonas:
        rect(sl, 9.3, y, 0.55, 0.55, ACC, radius=0.5); caja(sl, 9.3, y, 0.55, 0.55, [n], size=16, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, 10.0, y - 0.05, 2.9, 0.65, [t], size=13, anchor=MSO_ANCHOR.MIDDLE); y += 0.85
    callout(sl, 0.7, 6.55, 12.1, 0.5, "Lo más importante, arriba y a la izquierda; lo menos importante, abajo.", size=14)
    pie2(sl, "Cada zona responde una pregunta distinta; los valores de ejemplo son los de las diapositivas siguientes.")

def mantra():
    sl = nueva("El mantra de Shneiderman aplicado a este tablero", "Interacción", "Overview first, zoom and filter, then details on demand (Shneiderman, 1996).")
    pasos = [("Vista general primero", "KPI + tendencia + ranking de aduanas, todo visible sin hacer nada.", "Tarjetas y gráficos de las diapositivas 6–9", ACC),
             ("Zoom y filtros", "El lector acota por medio de transporte, año o aduana.", "Menú desplegable de la diapositiva 13", GRN),
             ("Detalles bajo demanda", "Al pasar el mouse aparece el valor exacto; la tabla muestra los registros.", "`hovertemplate` y mapa de calor", ORA)]
    y = 1.45
    for i, (a, b, c, col) in enumerate(pasos, 1):
        rect(sl, 0.5, y, 12.3, 1.35, "FFFFFF", line="C7D7E6", radius=0.06); rect(sl, 0.5, y, 0.9, 1.35, col, radius=0.06)
        caja(sl, 0.5, y, 0.9, 1.35, [str(i)], size=30, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, 1.65, y + 0.1, 3.4, 1.15, [f"**{a}**"], size=18, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 5.1, y + 0.1, 4.6, 1.15, [b], size=14, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 9.8, y + 0.1, 2.9, 1.15, [c], size=12, color=MUT, anchor=MSO_ANCHOR.MIDDLE)
        y += 1.5
    callout(sl, 0.5, 6.05, 12.3, 0.9, "Interactividad con propósito: cada filtro y cada hover debe ayudar a responder una pregunta concreta.", size=15)
    pie2(sl, "Shneiderman, B. (1996). The eyes have it: a task by data type taxonomy for information visualizations.")

def rstudio_python():
    sl = nueva("RStudio con código Python: el paquete reticulate", "Herramientas", "RStudio ejecuta chunks de Python dentro de un documento R Markdown; el HTML se publica en RPubs.")
    codigo(sl, 0.5, 1.3, 6.0, 2.2, ["# En la consola de R (una sola vez)", 'install.packages("reticulate")', "library(reticulate)", 'virtualenv_create("r-viz")', 'py_install(c("pandas", "plotly"), "r-viz")'], size=12)
    codigo(sl, 0.5, 3.7, 6.0, 2.5, ["---", 'title: "Tablero de aduanas"', "output: html_document", "---", "", "```{r}", 'reticulate::use_virtualenv("r-viz")', "```", "", "```{python}", "import pandas as pd", "```"], size=11)
    viñetas(sl, 6.9, 1.35, 5.9, 4.8, ["Un documento **R Markdown** puede mezclar chunks de R (` ```{r} `) y de **Python** (` ```{python} `).", "Los objetos de Python se leen desde R con `py$objeto`, y los de R desde Python con `r.objeto`.", "Los gráficos de **plotly** se incrustan como HTML interactivo en el documento.", "**Knit → Publish → RPubs**: el tablero queda en un enlace, sin servidor (los filtros corren en el navegador).", "Por qué: usamos el entorno de R que ya conocemos (editor, Knit, RPubs) con las librerías de Python."], size=14)
    callout(sl, 0.5, 6.4, 12.3, 0.6, "El código de esta presentación está en `r/05_tablero_aduanas_python.Rmd` listo para abrir en RStudio.", size=14)
    pie2(sl, "Documentación: rstudio.github.io/reticulate")

def checklist():
    sl = nueva("Checklist de calidad de un tablero", "Para recordar", "Úsenlo para evaluar el Mini-proyecto 2 (rúbrica R2).")
    filas = [["Pregunta de control", "Si la respuesta es no…"],
             ["¿Se sabe en 5 segundos cuál es el mensaje principal?", "Poner un título que enuncie la conclusión"],
             ["¿Los KPI están arriba y tienen una comparación?", "Agregar referencia: período anterior o meta"],
             ["¿Cada gráfico responde una pregunta distinta?", "Eliminar o fusionar los que se repiten"],
             ["¿Se usa el color con intención (énfasis, una gama)?", "Reducir a un color de énfasis y grises"],
             ["¿Cada control interactivo tiene un propósito?", "Quitar los filtros que nadie usa"],
             ["¿Están declaradas la fuente, los períodos y las limitaciones?", "Agregar pie con fuente y notas (p. ej. «sin junio 2025»)"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [6.3, 6.0], size=14, alto_fila=0.72)
    pie2(sl, "Basado en Few (2013) y en el mantra de Shneiderman.")

def practicar():
    sl = nueva("Para practicar: tu propio tablero", "Tu turno", "Cierre: Mini-proyecto 2 y Quiz 5A.")
    viñetas(sl, 0.7, 1.5, 7.3, 4.4, ["Abrí `05_tablero_aduanas_python.Rmd` en **RStudio** y ejecutalo con los datos agregados.", "Agregá un **filtro de año** y un indicador nuevo (por ejemplo, el valor por kilo).", "Corregí el tablero recargado aplicando el **checklist**.", "Resolvé el **Quiz 5A** del aula: evalúa lo visto en esta presentación."], size=16)
    imagen(sl, FIG / "b1.png", 8.3, 1.6, 4.5)
    callout(sl, 0.7, 6.0, 12.1, 0.95, "Un buen tablero no muestra todo: muestra lo que ayuda a decidir.", size=17)

def construir():
    portada(); preguntas(); datos()
    por = {f["id"]: f for f in S.FIGS}
    figura(por["k0"]); jerarquia()
    for k in ("k1", "l1", "b1", "t1", "h1", "a1", "d1", "i1"): figura(por[k])
    mantra(); rstudio_python(); checklist(); practicar()
    salida = M / "fuentes" / "dashboards_aduanas.pptx"; G.prs.save(salida); print("guardado", salida, len(G.prs.slides), "diapositivas")

if __name__ == "__main__": construir()
