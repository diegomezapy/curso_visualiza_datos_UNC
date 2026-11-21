"""Presentación «Elección de gráficos según objetivo, audiencia y dato» (sesión 2, Unidad 1) con datos reales de la EPHC.
Uso:  python tools/eleccion_pptx.py pasos   → escribe fuentes/pasos/*.R (el código que ejecuta R)
      Rscript tools/eleccion_datos.R <carpeta_csv> ; Rscript tools/eleccion_figuras.R
      python tools/eleccion_pptx.py pptx    → arma fuentes/eleccion_de_graficos.pptx (luego: python tools/procesar_presentacion.py unidad2_eleccion)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ggplot_pptx as G
from ggplot_pptx import *   # helpers de dibujo compartidos con la presentación de ggplot2
import eleccion_spec as S   # (después del import *: ggplot_pptx también define S)

M = G.RAIZ / "aula" / "media" / "unidad2_eleccion"; FIG = M / "fuentes" / "figuras"

def pasos():
    d = M / "fuentes" / "pasos"; d.mkdir(parents=True, exist_ok=True)
    for f in S.FIGS: (d / f"{f['id']}.R").write_text("\n".join(S.sin_marcas(f["codigo"])) + "\n", encoding="utf-8")
    print(len(S.FIGS), "archivos de código")

def pie2(sl, t): G.pie(sl, t)

def portada():
    sl = G.prs.slides.add_slide(G.BLANK); sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb(BG)
    caja(sl, 0.7, 1.35, 6.3, 0.4, ["MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC"], size=11, color=ACC, bold=True)
    caja(sl, 0.7, 2.0, 6.3, 2.2, ["Elección de gráficos según objetivo, audiencia y dato"], size=36, color=DARK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(sl, 0.7, 4.3, 6.2, 0.9, ["Cinco preguntas, cinco familias de gráficos; ejemplos reales de la Encuesta Permanente de Hogares Continua (INE)"], size=16, color=MUT)
    caja(sl, 0.7, 5.6, 6.2, 0.6, ["Sesión 2 · Unidad 1 · Fundamentos de la visualización"], size=14, color=TXT)
    imagen(sl, FIG / "r4.png", 7.3, 1.9, 5.5)
    sl.notes_slide.notes_text_frame.text = "Presentación de la sesión 2: cómo elegir el gráfico según la tarea (distribución, cantidad, proporción, relación y tiempo), cómo resolver overplotting, binning y orden, y cómo tomar la decisión con una matriz. Todas las figuras se generan con el código que se muestra, con datos de la EPHC 2025."

def tres_preguntas():
    sl = nueva("Antes de elegir un gráfico: tres preguntas", "Punto de partida", "El tipo de gráfico es la última decisión, no la primera.")
    items = [("1", "Objetivo", "¿Qué quiero que el lector **haga o entienda**?", "Comparar, ver una distribución, seguir una evolución, descubrir una relación, mostrar una composición.", ACC),
             ("2", "Audiencia", "¿**Quién** lo va a leer y cuánto tiempo tiene?", "Un equipo técnico tolera un boxplot; un directivo necesita un mensaje y un gráfico simple.", GRN),
             ("3", "Dato", "¿Qué **tipo de variables** tengo y cuántas observaciones?", "Categórica, numérica, temporal; pocas o millones de filas; una o varias series.", ORA)]
    y = 1.4
    for n, a, b, c, col in items:
        rect(sl, 0.5, y, 12.3, 1.4, "FFFFFF", line="C7D7E6", radius=0.06); rect(sl, 0.5, y, 0.9, 1.4, col, radius=0.06)
        caja(sl, 0.5, y, 0.9, 1.4, [n], size=30, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, 1.65, y + 0.12, 3.0, 1.16, [f"**{a}**"], size=22, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 4.6, y + 0.12, 8.0, 1.16, [b, c], size=15, anchor=MSO_ANCHOR.MIDDLE, espacio=4)
        y += 1.55
    callout(sl, 0.5, 6.1, 12.3, 0.85, "Primero la pregunta; después el gráfico. Un mismo dato admite muchos gráficos, pero solo algunos responden la pregunta.", size=15)
    pie2(sl, "Resumen de la matriz de decisión: objetivo + audiencia + dato → gráfico.")

def cinco_tareas():
    sl = nueva("Cinco tareas, cinco familias de gráficos", "Mapa de la sesión", "Este es el hilo de la clase: cada tarea con un ejemplo real de la EPHC.")
    filas = [["Tarea", "Pregunta con la EPHC", "Gráfico adecuado", "Cuidado con…"],
             ["Distribución", "¿Cómo se reparten los ingresos?", "Histograma, densidad, boxplot", "Ancho de bins, escala, atípicos"],
             ["Cantidad", "¿Qué departamento tiene mayor ingreso mediano?", "Barras ordenadas", "Nombres largos, orden alfabético"],
             ["Proporción", "¿Qué parte de la población está ocupada, desocupada, inactiva?", "Barras apiladas al 100 %", "Tortas con muchas partes"],
             ["Relación", "¿Cómo se relacionan educación e ingreso?", "Dispersión, bin2d, tendencia", "Overplotting, causalidad"],
             ["Tiempo", "¿Cómo cambió la tasa de ocupación 2022–2025?", "Líneas con etiquetas directas", "Ejes truncados en barras"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [1.8, 4.7, 3.1, 2.7], size=13, alto_fila=0.72)
    callout(sl, 0.5, 6.0, 12.3, 0.9, "Cada fila se desarrolla en las siguientes diapositivas: primero el gráfico que no funciona, después el que sí.", size=15)
    pie2(sl, "Todos los ejemplos usan el microdato público de la EPHC anual 2022–2025 del INE.")

def jerarquia():
    sl = nueva("Elegir bien: qué tarea perceptiva le pedimos al lector", "Fundamento", "Cleveland y McGill (1984): la precisión con la que se juzgan los atributos visuales. Se vio en la sesión 1.")
    niveles = [("Posición en una escala común", 11.0, GRN), ("Posición en escalas no alineadas", 10.0, "5B8C2A"), ("Longitud", 9.0, ACC), ("Ángulo y pendiente", 8.0, "B8860B"), ("Área", 7.0, ORA), ("Volumen, color y saturación", 6.2, "A04000")]
    y = 1.45
    for i, (t, w, col) in enumerate(niveles):
        rect(sl, 0.5, y, w * 0.62, 0.6, col, radius=0.3)
        caja(sl, 0.75, y, 8.5, 0.6, [f"**{t}**"], size=15, color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE)
        y += 0.72
    caja(sl, 8.9, 1.5, 3.9, 2.6, ["**Más preciso** ↑", "", "Barras, puntos y líneas se leen con posición y longitud.", "", "**Menos preciso** ↓"], size=14, color=MUT)
    viñetas(sl, 0.5, 5.9, 12.3, 1.0, ["Por eso comparamos con **barras ordenadas** antes que con tortas, y mostramos la tendencia con **líneas**."], size=15)
    pie2(sl, "Cleveland, W. y McGill, R. (1984). Graphical perception. Journal of the American Statistical Association.")

def figura(f):
    sl = nueva(f["titulo"], f["tag"], f["nota"])
    codigo(sl, 0.5, 1.3, 5.75, 3.95, f["codigo"], size=11 if len(f["codigo"]) > 12 else 12)
    imagen(sl, FIG / f"{f['id']}.png", 6.45, 1.3, 6.5)
    viñetas(sl, 0.5, 5.45, 8.2, 1.6, f["puntos"], size=13)
    callout(sl, 8.95, 5.45, 3.85, 1.55, f["mensaje"], size=13)
    pie2(sl, f["pie"])

def matriz():
    sl = nueva("Matriz de decisión: del dato al gráfico", "Para decidir", "Esta es la herramienta del Lab 2: cruzar la tarea con el tipo de dato.")
    filas = [["Quiero mostrar…", "Con estos datos", "Primera opción", "Alternativa", "Evitar"],
             ["Distribución", "1 variable numérica", "Histograma / densidad", "Boxplot por grupo", "Barras de promedios"],
             ["Cantidad", "Categoría + valor", "Barras horizontales ordenadas", "Puntos (lollipop)", "Torta, 3D"],
             ["Proporción", "Partes de un todo", "Barras apiladas al 100 %", "Barra única segmentada", "Torta con 6+ partes"],
             ["Relación", "2 variables numéricas", "Dispersión (con alpha / bins)", "Dispersión + tendencia", "Doble eje y"],
             ["Tiempo", "Serie temporal", "Líneas", "Barras (pocos periodos, base 0)", "Barras con eje truncado"],
             ["Muchos datos", "Miles de puntos", "Binning (bin2d / hex)", "Muestreo + alpha", "Puntos opacos"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [1.9, 2.4, 3.1, 2.7, 2.2], size=12, alto_fila=0.66)
    callout(sl, 0.5, 6.15, 12.3, 0.8, "La matriz orienta, no obliga: el objetivo y la audiencia pueden cambiar la elección.", size=15)
    pie2(sl, "Esta tabla es la base del Laboratorio 2 (matriz de decisión) y del chart clinic.")

def clinica():
    sl = nueva("Chart clinic: diagnosticá y corregí", "Para practicar", "Chart clinic: la audiencia trae un gráfico defectuoso y lo corrige entre todos.")
    filas = [["Síntoma", "Diagnóstico", "Corrección en ggplot2"],
             ["Barras apretadas y nombres superpuestos", "Eje con categorías largas", "Categorías en el eje y; `forcats::fct_reorder()`"],
             ["Histograma con una sola barra alta", "Cola larga de valores extremos", "`scale_x_log10()` y `bins` explícitos"],
             ["Nube de puntos opaca", "Overplotting", "`alpha`, `geom_jitter()`, `geom_bin2d()`"],
             ["Torta con varias partes parecidas", "Ángulos difíciles de comparar", "`geom_col(position = \"fill\")`"],
             ["Barras con la base recortada", "Eje y que no empieza en 0", "Quitar `coord_cartesian(ylim=)` o usar líneas"],
             ["Leyenda lejos de los datos", "Búsqueda visual costosa", "Etiquetas directas con `geom_text()`"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [4.3, 3.5, 4.5], size=13, alto_fila=0.68)
    pie2(sl, "Consejo: antes de entregar un gráfico, leelo como si no conocieras los datos.")

def practicar():
    sl = nueva("Para practicar: de cinco preguntas a cinco gráficos", "Tu turno", "Actividad asincrónica: 5 preguntas de negocio, 5 gráficos justificados, y el Quiz 2A.")
    viñetas(sl, 0.7, 1.5, 7.3, 4.4, ["Para cada una de las **cinco tareas**, formulá una pregunta con datos de la EPHC o de tu propio trabajo.", "Elegí el gráfico con la **matriz de decisión** y justificá en una línea: *objetivo, audiencia, dato*.", "Escribí el código con ggplot2 capa por capa (ver la presentación de la sesión 4) y revisá el **checklist**.", "Resolvé el **Quiz 2A** del aula: evalúa lo visto en esta presentación."], size=16)
    imagen(sl, FIG / "c2.png", 8.3, 1.6, 4.5)
    callout(sl, 0.7, 6.0, 12.1, 0.95, "No existe «el mejor gráfico»: existe el más adecuado para esta pregunta, esta audiencia y estos datos.", size=17)

def construir():
    portada(); tres_preguntas(); cinco_tareas(); jerarquia()
    for f in S.FIGS: figura(f)
    matriz(); clinica(); practicar()
    salida = M / "fuentes" / "eleccion_de_graficos.pptx"; G.prs.save(salida); print("guardado", salida, len(G.prs.slides), "diapositivas")

if __name__ == "__main__":
    {"pasos": pasos, "pptx": construir}[sys.argv[1] if len(sys.argv) > 1 else "pptx"]()
