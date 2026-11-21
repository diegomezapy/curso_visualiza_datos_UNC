"""Arma aula/media/unidad2_ggplot/presentacion.pptx con python-pptx a partir de ggplot_spec.py y las figuras de fuentes/figuras/.
Uso: python tools/ggplot_pptx.py   (antes: ggplot_pasos_a_archivos.py y Rscript tools/ggplot_figuras.R)"""
import re, sys, csv
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
sys.path.insert(0, str(Path(__file__).parent))
import ggplot_spec as S

RAIZ = Path(__file__).resolve().parents[1]
M = RAIZ / "aula" / "media" / "unidad2_ggplot"; FIG = M / "fuentes" / "figuras"; DAT = M / "fuentes" / "datos"
BG, DARK, ACC, ORA, GRN, TXT, MUT = "EAF1F8", "0B2E4A", "0072B2", "D55E00", "009E73", "1F2933", "4B5B6B"
SANS, MONO = "Inter", "DejaVu Sans Mono"
rgb = lambda h: RGBColor.from_string(h)

prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def rect(sl, x, y, w, h, fill, line=None, radius=0.03, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = sl.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: s.adjustments[0] = radius
    s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line: s.line.color.rgb = rgb(line); s.line.width = Pt(1)
    else: s.line.fill.background()
    s.shadow.inherit = False
    return s

def runs(par, texto, size, color, font=SANS, bold=False):
    """Mini-markdown: **negrita**, `código`, *cursiva*."""
    for parte in re.split(r"(\*\*.+?\*\*|`.+?`|\*[^*]+?\*)", texto):
        if not parte: continue
        r = par.add_run(); f = r.font; f.size = Pt(size); f.name = font; f.color.rgb = rgb(color); f.bold = bold
        if parte.startswith("**"): r.text = parte[2:-2]; f.bold = True
        elif parte.startswith("`"): r.text = parte[1:-1]; f.name = MONO; f.color.rgb = rgb("0B5E91"); f.size = Pt(size - 1)
        elif parte.startswith("*") and len(parte) > 2: r.text = parte[1:-1]; f.italic = True
        else: r.text = parte

def caja(sl, x, y, w, h, parrafos, size=14, color=TXT, bold=False, font=SANS, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, espacio=0.0, margen=0.0):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(margen); tf.margin_top = tf.margin_bottom = Inches(margen / 2)
    if isinstance(parrafos, str): parrafos = [parrafos]
    for i, t in enumerate(parrafos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        if espacio: p.space_after = Pt(espacio)
        runs(p, t, size, color, font, bold)
    return tb

def nueva(titulo, etiqueta=None, notas=""):
    sl = prs.slides.add_slide(BLANK); sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb(BG)
    caja(sl, 0.5, 0.38, 9.7, 0.7, [titulo], size=24, color=DARK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    ln = sl.shapes.add_connector(1, Inches(0.5), Inches(1.12), Inches(12.83), Inches(1.12)); ln.line.color.rgb = rgb("7FB0CF"); ln.line.width = Pt(1.2)
    if etiqueta:
        rect(sl, 10.35, 0.12, 2.48, 0.3, ACC, radius=0.5)
        caja(sl, 10.35, 0.12, 2.48, 0.3, [etiqueta], size=10, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    if notas: sl.notes_slide.notes_text_frame.text = notas
    return sl

def pie(sl, texto="Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión"):
    caja(sl, 0.5, 7.12, 12.3, 0.3, [texto], size=9, color=MUT)

def callout(sl, x, y, w, h, texto, color=ACC, size=14):
    rect(sl, x, y, w, h, "FFFFFF", line="C7D7E6"); rect(sl, x, y, 0.09, h, color, radius=0.0, shape=MSO_SHAPE.RECTANGLE)
    caja(sl, x + 0.25, y, w - 0.4, h, [texto], size=size, color=TXT, anchor=MSO_ANCHOR.MIDDLE)

def codigo(sl, x, y, w, h, lineas, size=11):
    rect(sl, x, y, w, h, "0D1B2A", radius=0.025)
    maxlen = max((len(l[1:] if l.startswith("§") else l) for l in lineas), default=10)
    size = min(size, round((w - 0.35) * 72 / (0.605 * maxlen), 1))   # que la línea más larga quepa sin cortarse
    tb = sl.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.12), Inches(w - 0.3), Inches(h - 0.2)); tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, l in enumerate(lineas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.line_spacing = 1.0; p.alignment = PP_ALIGN.LEFT
        nuevo = l.startswith("§"); l = l[1:] if nuevo else l
        r = p.add_run(); r.text = l if l else " "; f = r.font; f.name = MONO; f.size = Pt(size)
        if l.strip().startswith("#"): f.color.rgb = rgb("6E8AA6"); f.italic = True
        elif nuevo: f.color.rgb = rgb("7EE787"); f.bold = True
        else: f.color.rgb = rgb("A9B8C9")
    return tb

def imagen(sl, ruta, x, y, w, h=None, marco=True):
    if marco: rect(sl, x - 0.06, y - 0.06, w + 0.12, (h or 3.9 * w / 6.4) + 0.12, "FFFFFF", line="C7D7E6", radius=0.015)
    return sl.shapes.add_picture(str(ruta), Inches(x), Inches(y), width=Inches(w))

def viñetas(sl, x, y, w, h, puntos, size=14):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, t in enumerate(puntos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = Pt(5)
        runs(p, "▸ " + t, size, TXT)
    return tb

def tabla(sl, x, y, w, filas, anchos, size=12, alto_fila=0.34):
    shp = sl.shapes.add_table(len(filas), len(filas[0]), Inches(x), Inches(y), Inches(w), Inches(alto_fila * len(filas)))
    t = shp.table
    for j, a in enumerate(anchos): t.columns[j].width = Inches(a)
    for i, fila in enumerate(filas):
        t.rows[i].height = Inches(alto_fila)
        for j, v in enumerate(fila):
            c = t.cell(i, j); c.text = ""; p = c.text_frame.paragraphs[0]
            runs(p, str(v), size, "FFFFFF" if i == 0 else TXT, SANS if i == 0 or j < 2 else MONO, bold=(i == 0))
            c.fill.solid(); c.fill.fore_color.rgb = rgb(DARK if i == 0 else ("FFFFFF" if i % 2 else "F3F7FB"))
            c.margin_left = c.margin_right = Inches(0.1)
    return shp

# ====================== diapositivas ======================
def portada():
    sl = prs.slides.add_slide(BLANK); sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb(BG)
    caja(sl, 0.7, 2.0, 6.3, 2.2, ["Cómo se construye una figura en R con ggplot2"], size=38, color=DARK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(sl, 0.7, 4.3, 6.2, 0.9, ["Capa por capa, con datos reales de la Encuesta Permanente de Hogares Continua (INE)"], size=17, color=MUT)
    caja(sl, 0.7, 1.35, 6.3, 0.4, ["MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC"], size=11, color=ACC, bold=True)
    caja(sl, 0.7, 5.6, 6.2, 0.6, ["Sesión 4 · Visual analytics, KPIs y storytelling"], size=14, color=TXT)
    imagen(sl, FIG / "p12.png", 7.3, 1.9, 5.5)
    sl.notes_slide.notes_text_frame.text = "Presentación de la sesión 4 (Unidad 2): gramática de gráficos con ggplot2, construida en 12 pasos con datos de la EPHC de Concepción 2022–2025. El código de cada diapositiva es el que genera la figura."

def datos():
    sl = nueva("El ejemplo: ocupación en Concepción con la EPHC", "Punto de partida", "Mostrar el data frame antes de graficar: una fila por año y situación (formato largo).")
    rows = list(csv.DictReader(open(DAT / "ocup_concepcion.csv", encoding="utf-8")))
    filas = [["anio", "ocup", "personas", "casos_muestrales"]] + [[r["anio"], r["ocup"], r["personas"], r["casos_muestrales"]] for r in rows[:6]] + [["…", "…", "…", "…"]]
    tabla(sl, 0.5, 1.45, 6.6, filas, [1.2, 1.9, 1.7, 1.8], size=13, alto_fila=0.42)
    viñetas(sl, 7.5, 1.45, 5.3, 3.8, [
        "**Pregunta:** ¿cómo cambió entre 2022 y 2025 el número de personas ocupadas, desocupadas e inactivas en Concepción?",
        "**Fuente:** microdatos de la EPHC anual del INE (tabla de personas).",
        "`personas` = suma del **factor de expansión**; `casos_muestrales` = encuestados que respaldan cada cifra.",
        "El data frame está en **formato largo**: una fila por año y situación. Es lo que espera ggplot2."], size=15)
    callout(sl, 0.5, 5.6, 12.3, 1.0, "Antes de graficar, siempre mirá los datos: ¿qué representa una fila? ¿qué variable irá a cada atributo del gráfico?")
    pie(sl)

def gramatica():
    sl = nueva("La gramática de los gráficos: un gráfico son capas", "Idea central", "ggplot2 implementa la gramática de gráficos de Wilkinson, adaptada por Hadley Wickham. Cada geometría lleva detrás una estadística (stat) y una posición (position).")
    comp = [("1", "Datos", "`data`", "¿Qué se grafica?", "un data frame ordenado", ACC),
            ("2", "Estéticas", "`aes()`", "¿Qué variable controla qué atributo?", "x, y, color, size, shape, label, group", "0B7FA8"),
            ("3", "Geometrías", "`geom_*()`", "¿Con qué forma se dibuja?", "line, point, col, text, histogram", GRN),
            ("4", "Escalas", "`scale_*()`", "¿Cómo se traducen datos a ejes y colores?", "breaks, labels, paleta manual", "5B8C2A"),
            ("5", "Facetas", "`facet_*()`", "¿Un panel o varios?", "facet_wrap, facet_grid", "B8860B"),
            ("6", "Coordenadas", "`coord_*()`", "¿Qué sistema de ejes?", "cartesiano, coord_flip, polar", ORA),
            ("7", "Tema", "`theme_*()`", "¿Cómo se ve?", "theme_minimal, theme()", "8E5BA8")]
    y = 1.35
    for n, nombre, fn, preg, ej, col in comp:
        rect(sl, 0.5, y, 12.3, 0.62, "FFFFFF", line="C7D7E6", radius=0.1); rect(sl, 0.5, y, 0.62, 0.62, col, radius=0.1)
        caja(sl, 0.5, y, 0.62, 0.62, [n], size=20, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, 1.3, y, 2.1, 0.62, [f"**{nombre}**"], size=16, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 3.4, y, 1.9, 0.62, [fn], size=14, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 5.3, y, 4.2, 0.62, [preg], size=14, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 9.5, y, 3.2, 0.62, [ej], size=12, color=MUT, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.7
    callout(sl, 0.5, 6.3, 12.3, 0.7, "Las capas se suman con +, de a una, y se leen de arriba hacia abajo.", size=15)

def anatomia():
    sl = nueva("Anatomía de una llamada a ggplot()", "Idea central", "Los tres elementos mínimos: datos, estéticas y una capa geométrica.")
    codigo(sl, 0.5, 1.4, 7.4, 1.5, ["ggplot(data = ocup_larga,", "       mapping = aes(x = anio, y = personas)) +", "  geom_line()"], size=15)
    notas = [("①", "data", "El data frame con las filas a graficar.", ACC), ("②", "mapping = aes()", "Qué variable va a qué atributo visual.", GRN), ("③", "geom_*()", "La forma con la que se dibujan los datos.", ORA)]
    y = 3.2
    for n, k, d, col in notas:
        rect(sl, 0.5, y, 7.4, 0.85, "FFFFFF", line="C7D7E6", radius=0.08); rect(sl, 0.5, y, 0.75, 0.85, col, radius=0.08)
        caja(sl, 0.5, y, 0.75, 0.85, [n], size=22, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, 1.45, y, 6.3, 0.85, [f"`{k}`  ·  {d}"], size=15, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.98
    viñetas(sl, 8.4, 1.45, 4.4, 4.5, ["`ggplot()` crea el lienzo.", "El `+` **va al final** de la línea, nunca al inicio de la siguiente.", "Se puede escribir con los argumentos con nombre o en orden: `ggplot(ocup_larga, aes(anio, personas))`.", "Lo demás (escalas, títulos, temas) son capas opcionales que mejoran la lectura."], size=15)
    callout(sl, 0.5, 6.15, 12.3, 0.85, "Receta mínima: datos + estéticas + una geometría. Con eso ya hay un gráfico.", size=15)

def paso(p):
    sl = nueva(p["titulo"], p["tag"], p["nota"])
    codigo(sl, 0.5, 1.3, 5.75, 3.95, p["mostrar"], size=11 if len(p["mostrar"]) > 12 else 12)
    ruta = FIG / f"{p['id']}.png"
    ancho = 6.5 if p["id"] != "p06" else 6.5
    imagen(sl, ruta, 6.45, 1.3 + (0 if p["id"] != "p06" else 0.3), ancho, 3.9 * ancho / (7.4 if p["id"] == "p06" else 6.4))
    viñetas(sl, 0.5, 5.45, 8.2, 1.6, p["puntos"], size=13)
    callout(sl, 8.95, 5.45, 3.85, 1.55, p["mensaje"], size=13)
    pie(sl)

def figura_extra(titulo, etiqueta, fid, codigo_lin, puntos, mensaje, nota=""):
    sl = nueva(titulo, etiqueta, nota)
    codigo(sl, 0.5, 1.3, 5.75, 3.95, codigo_lin, size=10.5 if len(codigo_lin) > 12 else 12)
    imagen(sl, FIG / f"{fid}.png", 6.45, 1.3, 6.5)
    viñetas(sl, 0.5, 5.45, 8.2, 1.6, puntos, size=13)
    callout(sl, 8.95, 5.45, 3.85, 1.55, mensaje, size=13)
    pie(sl)

def receta():
    sl = nueva("Receta: de la pregunta a la figura", "Para recordar", "Pasos que se repiten en cualquier gráfico de ggplot2.")
    pasos = [("Pregunta o mensaje", "¿Qué querés que entienda el lector?"), ("Datos ordenados", "Una fila por observación (formato largo); `pivot_longer()` si hace falta."),
             ("Estéticas", "`aes()`: qué variable va a x, y, color…"), ("Geometría", "Elegida según la tarea perceptiva: posición y longitud antes que ángulo y área."),
             ("Escalas", "Marcas, formatos y colores accesibles (Okabe-Ito)."), ("Textos", "Título, ejes con unidades, leyenda y **fuente**."), ("Tema y revisión", "`theme_*()` y el checklist de calidad visual y ética.")]
    y = 1.35
    for i, (a, b) in enumerate(pasos, 1):
        rect(sl, 0.5, y, 12.3, 0.68, "FFFFFF", line="C7D7E6", radius=0.1); rect(sl, 0.5, y, 0.68, 0.68, ACC, radius=0.1)
        caja(sl, 0.5, y, 0.68, 0.68, [str(i)], size=20, color="FFFFFF", bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, 1.4, y, 3.1, 0.68, [f"**{a}**"], size=16, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
        caja(sl, 4.5, y, 8.2, 0.68, [b], size=14, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.78
    pie(sl, "Cada paso del gráfico se resuelve con una capa o un argumento: la receta es siempre la misma.")

def errores():
    sl = nueva("Errores frecuentes y cómo leerlos", "Para recordar", "Los mensajes de error de ggplot2 suelen apuntar al + mal ubicado o a una estética mal escrita.")
    filas = [["Síntoma", "Causa probable", "Arreglo"],
             ["Línea en zigzag", "Falta separar las series", "Mapear `color` o `group` a la variable"],
             ["`Error: Cannot add ggproto objects together`", "El `+` quedó al inicio de la línea", "Ponerlo al **final** de la línea anterior"],
             ["`Object 'x' not found`", "Variable mal escrita o fuera de `aes()`", "Revisar el nombre con `names(datos)`"],
             ["La leyenda dice «#D55E00»", "El color fijo quedó dentro de `aes()`", "Sacar `color = ...` de `aes()`"],
             ["Años como 2022,5", "`anio` es numérica continua", "`scale_x_continuous(breaks = ...)` o `factor(anio)`"],
             ["No se puede mapear 3 series", "Datos en formato ancho", "`tidyr::pivot_longer()` a formato largo"]]
    tabla(sl, 0.5, 1.4, 12.3, filas, [3.9, 3.9, 4.5], size=13, alto_fila=0.66)
    pie(sl, "Consejo: ejecutá el gráfico después de agregar cada capa; así el error aparece donde se lo cometió.")

def completo():
    sl = nueva("El código completo de la figura", "Resumen", "Código final tal como se ejecuta en el ejercicio de la EPHC.")
    p12 = S.sin_marcas(S.PASOS[-1]["codigo"])
    mitad = 17
    codigo(sl, 0.5, 1.3, 6.1, 5.0, p12[:mitad], size=10.5); codigo(sl, 6.75, 1.3, 6.1, 5.0, p12[mitad:], size=10.5)
    callout(sl, 0.5, 6.45, 12.3, 0.6, "Cada línea corresponde a una de las capas de los 12 pasos. Probá quitar una y mirá qué cambia.", size=14)

def practicar():
    sl = nueva("Para practicar", "Tu turno", "Cierre: conectar con el ejercicio guiado y el Quiz 4B.")
    viñetas(sl, 0.7, 1.5, 7.2, 4.5, ["Corré el ejercicio guiado **04_ejercicio_ephc_concepcion.Rmd**: usa estas mismas capas con los microdatos completos de la EPHC.", "Cambiá **un paso por vez** y observá qué ocurre: quitá `group`, mové `color` fuera de `aes()`, probá `geom_col()`.", "Reemplazá Concepción por otro departamento (`DPTO == 2`, 3…) y volvé a mirar el mensaje.", "Respondé el **Quiz 4B** del aula para comprobar lo aprendido."], size=18)
    imagen(sl, FIG / "f_facetas.png", 8.3, 1.6, 4.5)
    callout(sl, 0.7, 6.0, 12.1, 0.95, "ggplot2 no dibuja un gráfico: lo describe. Datos + estéticas + capas + escalas + textos + tema.", size=17)

def construir():
    portada(); datos(); gramatica(); anatomia()
    for p in S.PASOS: paso(p)
    figura_extra("Facetas: un panel por categoría", "Más componentes", "f_facetas", S.EXTRA["f_facetas"],
                 ["`facet_wrap(~ ocup)` divide el gráfico en **paneles pequeños** (*small multiples*).", "`scales = \"free_y\"` deja que cada panel tenga su propio eje y.", "Útil cuando las magnitudes son muy distintas: ahora se ve la forma de cada serie."],
                 "Cuidado: con ejes libres no se pueden comparar alturas entre paneles.", "Mostrar el costo y el beneficio de free_y.")
    figura_extra("Cambiar de geometría: barras agrupadas", "Más componentes", "f_barras", S.EXTRA["f_barras"],
                 ["Mismos datos y estéticas; cambia la **geometría**: `geom_col(position = \"dodge\")`.", "`position = \"dodge\"` pone las barras una al lado de la otra.", "`fill` pinta el interior; `color` es solo el borde."],
                 "Con una serie en el tiempo, las líneas muestran mejor la tendencia; las barras comparan valores puntuales.", "Relacionar con la jerarquía de Cleveland y McGill: ambas usan posición/longitud.")
    figura_extra("Coordenadas: la pirámide de población", "Más componentes", "f_piramide", S.EXTRA["f_piramide"],
                 ["Otro ejemplo de la EPHC: población estimada de Concepción en 2025 por sexo y grupo de edad.", "`coord_flip()` intercambia los ejes; los hombres se grafican con valores negativos.", "Cada barra suma el **factor de expansión**, no cuenta filas."],
                 "Las coordenadas cambian cómo se orientan los ejes sin tocar los datos ni las estéticas.", "La pirámide usa una escala con abs() para mostrar valores positivos en ambos lados.")
    receta(); errores(); completo(); practicar()
    salida = M / "fuentes" / "ggplot2_capa_por_capa.pptx"
    prs.save(salida); print("guardado", salida, len(prs.slides), "diapositivas")

if __name__ == "__main__":
    construir()
