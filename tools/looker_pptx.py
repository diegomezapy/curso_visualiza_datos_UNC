"""Presentación «Looker Studio (ex Data Studio) con el Censo Agropecuario Nacional 2022» (sesión 5, Unidad 2).
Datos reales del Volumen I del CAN 2022 (MAG). Las figuras son maquetas con esos datos (no capturas de Looker Studio).
Uso: python tools/can_datos.py <Volumen I> ; python tools/looker_figuras.py ; python tools/looker_pptx.py ; python tools/procesar_presentacion.py unidad5_looker"""
import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ggplot_pptx import *
import ggplot_pptx as G
M = G.RAIZ / "aula" / "media" / "unidad5_looker"; FIG = M / "fuentes" / "figuras"; DAT = M / "fuentes" / "datos"
PIE = "Fuente: MAG, Censo Agropecuario Nacional 2022, Volumen I · maqueta con los datos reales (no es una captura de Looker Studio)"
pie2 = lambda sl, t=PIE: G.pie(sl, t)
ASP = 3.9 / 6.4
from PIL import Image as _Im
def ajustada(sl, n, x, y, w, h):
    """Imagen escalada para entrar completa en el recuadro w×h (sin deformar) y centrada."""
    iw, ih = _Im.open(FIG / f"{n}.png").size; k = min(w / iw, h / ih); ww, hh = iw * k, ih * k
    ox, oy = x + (w - ww) / 2, y + (h - hh) / 2
    G.rect(sl, ox - 0.06, oy - 0.06, ww + 0.12, hh + 0.12, "FFFFFF", line="C7D7E6", radius=0.015)
    sl.shapes.add_picture(str(FIG / f"{n}.png"), G.Inches(ox), G.Inches(oy), width=G.Inches(ww))

def figura(titulo, tag, fig, pasos, puntos, mensaje, nota=""):
    sl = nueva(titulo, tag, nota)
    caja(sl, 0.5, 1.3, 5.75, 0.35, ["**En Looker Studio**"], size=13, color=ACC)
    viñetas(sl, 0.5, 1.75, 5.75, 3.5, pasos, size=13)
    ajustada(sl, fig, 6.5, 1.35, 6.3, 3.85)
    viñetas(sl, 0.5, 5.45, 8.2, 1.6, puntos, size=13)
    callout(sl, 8.95, 5.45, 3.85, 1.55, mensaje, size=13)
    pie2(sl)

def portada():
    sl = G.prs.slides.add_slide(G.BLANK); sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb(BG)
    caja(sl, 0.7, 1.35, 6.3, 0.4, ["MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC"], size=11, color=ACC, bold=True)
    caja(sl, 0.7, 2.0, 6.3, 2.2, ["Looker Studio, paso a paso, con el Censo Agropecuario 2022"], size=34, color=DARK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(sl, 0.7, 4.3, 6.2, 0.9, ["Cómo armar un informe interactivo gratuito en la nube (antes Google Data Studio) con datos oficiales del MAG"], size=16, color=MUT)
    caja(sl, 0.7, 5.6, 6.2, 0.6, ["Sesión 5 · Unidad 2 · Dashboards interactivos"], size=14, color=TXT)
    ajustada(sl, "l7", 7.1, 1.6, 5.9, 4.2)
    sl.notes_slide.notes_text_frame.text = "Parte 3 de la sesión 5: herramienta de BI gratuita. Los datos son el Volumen I del CAN 2022 (MAG). Las imágenes son maquetas con los datos reales; las pantallas de Looker Studio las muestra el docente en vivo."

def que_es():
    sl = nueva("Looker Studio: informes interactivos en la nube", "Herramienta", "Looker Studio es el nuevo nombre de Google Data Studio. Gratuito con cuenta Google.")
    filas = [["Característica", "Qué significa"],
             ["Gratuito y en la nube", "Se usa desde el navegador con una cuenta de Google; no hay que instalar nada."],
             ["Conectores", "Hojas de cálculo de Google, archivos CSV, BigQuery, Google Analytics y más."],
             ["Se comparte como un documento", "Permisos de lector o editor, enlace público o por correo; se puede incrustar en una web."],
             ["Interacción sin programar", "Filtros, controles, filtrado cruzado entre gráficos y mapas."],
             ["Límites", "No es para análisis estadístico complejo; los datos se preparan antes y viven en la fuente."]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [3.4, 8.9], size=14, alto_fila=0.78)
    callout(sl, 0.5, 6.15, 12.3, 0.8, "Sirve para tableros de seguimiento con datos ya ordenados: lo que cambia respecto de Shiny es que no requiere código ni servidor.", size=14)
    pie2(sl, "Documentación: support.google.com/looker-studio")

def datos():
    sl = nueva("Los datos: Censo Agropecuario Nacional 2022 (MAG)", "Punto de partida", "Fuente: Volumen I del CAN 2022. Cuadros usados: 1 (fincas y superficie), 5 (productores por sexo), 19 (uso de la tierra), 27 (soja) y 52 (ganadería).")
    rows = list(csv.DictReader(open(DAT / "can2022_departamentos.csv", encoding="utf-8")))
    f = lambda v: f"{float(v):,.0f}".replace(",", ".")
    filas = [["departamento", "iso_3166_2", "region", "fincas_2022", "superficie_2022_ha", "var_fincas_pct"]] + [[r["departamento"], r["iso_3166_2"], r["region"], f(r["fincas_2022"]), f(r["superficie_2022_ha"]), f"{float(r['var_fincas_pct']):.1f}".replace(".", ",")] for r in rows[:6]] + [["…"] * 6]
    G.tabla(sl, 0.5, 1.35, 7.6, filas, [1.7, 1.1, 1.1, 1.2, 1.6, 0.9], size=10.5, alto_fila=0.4)
    viñetas(sl, 8.4, 1.35, 4.4, 3.4, ["**291.497 fincas** y **30,4 millones de hectáreas** en 17 departamentos.", "**Volumen I** del CAN 2022: 78 cuadros por tamaño de finca y departamento.", "Se extrajeron 5 cuadros y se armó **una fila por departamento** (`can2022_departamentos.csv`) y una tabla por estratos de tamaño."], size=13)
    callout(sl, 0.5, 5.0, 12.3, 0.9, "Los totales de nuestra tabla coinciden con el censo: 291.497 fincas, 30.401.660 ha, 13.221.039 cabezas de vacunos y 245.002 productores residentes.", size=14)
    caja(sl, 0.5, 6.05, 12.3, 0.8, ["Verificá siempre que tu tabla preparada reproduzca los totales oficiales antes de graficar."], size=13, color=MUT)
    pie2(sl, "MAG (2024). Censo Agropecuario Nacional 2022, Volumen I. Archivos: can2022_departamentos.csv y can2022_estratos.csv.")

def preparar():
    sl = nueva("Preparar la tabla: una fila por departamento", "Preparación", "Los conectores esperan tablas ordenadas: una fila por observación, una columna por variable, encabezado único.")
    filas = [["Campo", "Ejemplo", "Tipo en Looker Studio"],
             ["departamento", "Concepción", "Dimensión · texto"],
             ["iso_3166_2", "PY-1", "Dimensión · Geografía (región/subregión de país)"],
             ["region", "Oriental", "Dimensión · texto (para filtros y colores)"],
             ["fincas_2022 · superficie_2022_ha", "16.670 · 1.521.325", "Métrica · número (suma)"],
             ["var_fincas_pct", "−4,1", "Métrica · número (se muestra como %)"],
             ["pct_productoras_mujeres", "45,8", "Métrica · número (promedio, no suma)"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [4.2, 3.0, 5.1], size=13, alto_fila=0.62)
    viñetas(sl, 0.5, 5.9, 12.3, 1.2, ["Nombres de columna **sin espacios ni tildes**; números **sin separador de miles** en la hoja.", "Los porcentajes y promedios **no se suman**: elegí la agregación correcta de cada métrica."], size=13)
    pie2(sl, "Resultado: Hoja de cálculo de Google con la pestaña «departamentos» (17 filas) y la pestaña «estratos» (12 filas).")

def conectar():
    sl = nueva("Paso 1: crear el informe y conectar la fuente", "Paso 1 de 8", "Flujo de conexión. Mostrar en vivo en lookerstudio.google.com.")
    pasos = ["lookerstudio.google.com", "Crear → Informe", "Agregar datos", "Conector: Hojas de cálculo de Google", "Elegir el archivo y la pestaña", "Agregar al informe"]
    x = 0.5
    for i, t in enumerate(pasos):
        rect(sl, x, 1.7, 1.9, 1.5, "FFFFFF", line=ACC, radius=0.08); rect(sl, x, 1.7, 1.9, 0.4, ACC, radius=0.15)
        caja(sl, x, 1.7, 1.9, 0.4, [f"**{i + 1}**"], size=13, color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, x + 0.08, 2.15, 1.74, 1.0, [t], size=12, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        if i < 5: caja(sl, x + 1.9, 2.1, 0.12, 0.6, ["›"], size=20, color=MUT, anchor=MSO_ANCHOR.MIDDLE)
        x += 2.07
    viñetas(sl, 0.5, 3.7, 12.3, 2.4, ["Conectá la pestaña **departamentos** como primera fuente de datos.", "Looker Studio **lee la hoja en vivo**: si actualizás la hoja, el informe se actualiza.", "Podés agregar más fuentes (por ejemplo, la pestaña **estratos**) y combinarlas por gráfico.", "La cuenta que conecta la hoja debe tener acceso de lectura al archivo."], size=15)
    callout(sl, 0.5, 6.1, 12.3, 0.85, "Se conecta una tabla ordenada: el trabajo de preparación del dato se hizo antes, no dentro de Looker.", size=14)
    pie2(sl, "Documentación: support.google.com/looker-studio/answer/6283323")

def tipos():
    sl = nueva("Paso 2: revisar los campos antes de graficar", "Paso 2 de 8", "En el editor de la fuente de datos se revisan tipo, agregación y formato de cada campo.")
    viñetas(sl, 0.6, 1.5, 7.0, 4.6, ["**Dimensiones** (categorías): departamento, región. **Métricas** (números): fincas, hectáreas.", "Cambiá el tipo de `iso_3166_2` a **Geografía → Región de país** (ISO 3166-2) para habilitar el mapa.", "Revisá la **agregación** por defecto: suma para fincas y hectáreas; promedio para porcentajes.", "Usá **campos calculados** para indicadores nuevos, por ejemplo hectáreas por finca: `superficie_2022_ha / fincas_2022`."], size=15)
    codigo(sl, 7.9, 1.5, 4.9, 2.0, ["# Campo calculado (ejemplo)", "Superficie promedio por finca", "=", "SUM(superficie_2022_ha)", "  / SUM(fincas_2022)"], size=13)
    codigo(sl, 7.9, 3.7, 4.9, 2.1, ["# Campo calculado (ejemplo)", "Porcentaje de fincas que cayeron", "=", "(SUM(fincas_2022) - SUM(fincas_2008))", "  / SUM(fincas_2008)"], size=12)
    callout(sl, 0.6, 6.15, 12.2, 0.8, "Un promedio de porcentajes no es el porcentaje total: calculá el indicador como razón de sumas.", size=14)
    pie2(sl, "Los nombres de los campos y las opciones del editor pueden variar según la versión de Looker Studio.")

def seccion_tarjetas():
    figura("Paso 3: tarjetas de resultados (KPI)", "Paso 3 de 8", "l1", ["Insertar → **Tarjeta de resultados**.", "Métrica: `fincas_2022`; agregá una segunda para la variación.", "Repetir con superficie, vacunos y % de productoras.", "Formato: miles con punto, un decimal en los porcentajes."], ["Las **cuatro tarjetas** resumen el país: 291.497 fincas; 30,4 millones de hectáreas.", "Cada KPI lleva su **comparación con 2008** (verde sube, naranja baja).", "El 38,3 % de las productoras mujeres sale de 93.828 sobre 245.002."], "KPI arriba y con comparación: lo primero que se lee.", "Tarjetas de resultados = scorecards.")

def seccion_mapa():
    figura("Paso 4: el mapa por departamento", "Paso 4 de 8", "l2", ["Insertar → **Mapa de burbujas** o **Mapa coroplético**.", "Dimensión geográfica: `iso_3166_2`.", "Métrica del tamaño o color: `superficie_2022_ha`.", "Opcional: color por región."], ["El **Chaco** (Occidental) concentra las fincas más extensas: Presidente Hayes, Boquerón y Alto Paraguay.", "En la Región Oriental hay **muchas fincas pequeñas**: el tamaño de burbuja es menor.", "Para el mapa de Looker, usá el código ISO (por ejemplo, PY-1 para Concepción)."], "El mapa responde dónde; no sirve para comparar con precisión: complementarlo con barras.", "El gráfico de esta diapositiva es una maqueta con coordenadas de los departamentos.")

def seccion_barras():
    figura("Paso 5: ranking con barras ordenadas", "Paso 5 de 8", "l3", ["Insertar → **Gráfico de barras** (horizontal).", "Dimensión: `departamento`; métrica: `superficie_2022_ha`.", "Orden: métrica descendente.", "Color de énfasis para el departamento de interés."], ["Presidente Hayes, Boquerón y Alto Paraguay suman **17 millones de ha** (56 % del total).", "Concepción, destacada en naranja, ocupa el **quinto lugar** con 1,5 millones.", "Barras horizontales y ordenadas: el ranking se lee de un vistazo."], "Un ranking claro: ordenado, horizontal y con un solo color de énfasis.", "Presidente Hayes 6,26 + Boquerón 5,87 + Alto Paraguay 4,87 = 17,0 M ha (55,9 %).")

def seccion_variacion():
    figura("Paso 6: comparar 2008 con 2022", "Paso 6 de 8", "l4", ["Campo `var_fincas_pct` en un gráfico de barras.", "Orden por la métrica; eje con el cero visible.", "Colores condicionales: azul si sube, naranja si baja.", "Título que enuncia el hallazgo."], ["**Boquerón (+30 %) y San Pedro (+29 %)** son los que más aumentaron la cantidad de fincas.", "**Central (−52 %), Amambay (−41 %) y Misiones (−33 %)** son los que más cayeron.", "A nivel país, la cantidad de fincas casi no cambió (+0,6 %), pero hubo grandes cambios por departamento."], "Una cifra nacional estable puede esconder cambios muy distintos entre departamentos.", "Cuadro 1 del Volumen I.")

def seccion_concentracion():
    figura("Paso 7: concentración de la tierra por tamaño de finca", "Paso 7 de 8", "l5", ["Usar la fuente **estratos** (12 filas).", "Barras agrupadas: `pct_fincas_2022` y `pct_superficie_2022`.", "Eje x: tamaño de finca en su orden natural (campo `orden`).", "Dos métricas, dos colores, una leyenda clara."], ["Las fincas de **1.000 ha o más** son el 1,6 % del total y manejan el **77,2 %** de la superficie.", "Las fincas de **menos de 20 ha** son el 82 % de las fincas y manejan solo el 4,2 % de la tierra.", "Combinar dos fuentes en un informe permite contar dos historias con los mismos datos."], "Dos barras por categoría muestran la desigualdad mejor que cualquier tabla.", "Cuadro 1: 4.524 fincas de 1.000 ha o más; 23,46 millones de ha.")

def seccion_uso():
    figura("Paso 8: uso de la tierra, el país frente a un departamento", "Paso 8 de 8", "l6", ["**Barras apiladas al 100 %** con una métrica por uso de la tierra.", "Dimensión: departamento (con un filtro por departamento).", "Una gama de colores consistente por tipo de uso."], ["En **Concepción** el 77 % de la superficie es pastura (49 % natural y 28 % cultivada); en el país, el 59 %.", "Los **cultivos temporales** son el 15 % en el país y solo el 4 % en Concepción.", "Con un filtro de departamento el mismo gráfico sirve para los 17."], "Un mismo gráfico con un filtro de departamento reemplaza 17 gráficos distintos.", "Cuadro 19: uso de la tierra (superficies de cada uso sobre la suma de los seis usos).")

def controles():
    sl = nueva("Controles e interacción: que el lector explore", "Interacción", "Controles: lista desplegable, control deslizante, rango de fechas. Filtrado cruzado entre gráficos.")
    ajustada(sl, "l7", 6.5, 1.35, 6.3, 3.85)
    viñetas(sl, 0.5, 1.4, 5.8, 4.0, ["**Lista desplegable** para Región y para Departamento: filtra todo el informe.", "**Control deslizante** (ejemplo: hectáreas por finca) para acotar el rango.", "**Filtrado cruzado:** al hacer clic en una barra o una burbuja, los demás gráficos se filtran.", "Los controles se colocan **arriba o a la izquierda**, en un solo lugar."], size=14)
    viñetas(sl, 0.5, 5.45, 8.2, 1.6, ["Mismo principio que el mantra de Shneiderman: vista general, zoom y filtros, detalle bajo demanda.", "Cada control debe responder una pregunta; los que nadie usa, se quitan."], size=13)
    callout(sl, 8.95, 5.45, 3.85, 1.55, "Pocos controles y bien ubicados: el informe se explora sin instrucciones.", size=13)
    pie2(sl)

def estilo():
    sl = nueva("Tema y diseño: jerarquía, color y texto", "Diseño", "Aplicar el checklist de la parte 1.")
    filas = [["Decisión de diseño", "En este informe"],
             ["Jerarquía de arriba hacia abajo", "KPI → mapa y ranking → detalle por estratos"],
             ["Título que enuncia un mensaje", "«Pocas fincas muy grandes concentran la tierra»"],
             ["Color con intención", "Azul para datos; naranja solo para Concepción o lo que baja"],
             ["Misma gama para el mismo concepto", "Verde o naranja siempre indican sube o baja"],
             ["Fuente y notas visibles", "Pie: «MAG, CAN 2022, Volumen I» y definición de cada indicador"],
             ["Menos es más", "Un informe de una página con 6 gráficos como máximo"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [5.0, 7.3], size=14, alto_fila=0.72)
    pie2(sl, "Basado en Few (2013) y en la parte 1 de la sesión 5.")

def compartir():
    sl = nueva("Compartir e incrustar el informe", "Publicación", "En Looker Studio: botón Compartir para permisos; menú Archivo → Incorporar informe para el iframe.")
    filas = [["Quiero…", "Cómo", "Cuidado con…"],
             ["Que lo vea un grupo", "Compartir → agregar correos con permiso de lector", "No dar permiso de editor a todos"],
             ["Que lo vea cualquiera con el enlace", "Compartir → acceso a cualquiera con el enlace", "Solo con datos públicos"],
             ["Ponerlo en una web o en el aula", "Archivo → Incorporar informe → copiar la URL de incrustación", "La hoja de origen también debe ser accesible"],
             ["Actualizar los datos", "Editar la hoja de cálculo", "Los datos del informe cambian para todos"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [3.3, 5.3, 3.7], size=13, alto_fila=0.8)
    callout(sl, 0.5, 5.8, 12.3, 0.9, "Para el aula: compartí el enlace del informe con permiso de lector y pegalo en la entrega; la URL de incrustación sirve para una web propia.", size=14)
    pie2(sl, "Los nombres de los menús pueden variar según el idioma y la versión de Looker Studio.")

def comparar():
    sl = nueva("¿Looker Studio, Shiny o plotly? Cuándo usar cada uno", "Para decidir", "Cierre de la sesión 5: tres herramientas de tableros y su criterio de elección.")
    filas = [["", "Looker Studio", "plotly (HTML estático)", "Shiny (R)"],
             ["Código", "Sin programar", "Python o R", "R (o Python con Shiny para Python)"],
             ["Servidor", "No (lo aloja Google)", "No (HTML en RPubs o GitHub Pages)", "Sí (shinyapps.io, Posit Connect)"],
             ["Datos", "Tabla preparada (Hoja, CSV, BigQuery)", "Embebidos en el archivo", "Cualquiera, con cálculos a pedido"],
             ["Personalización", "Media: depende de los gráficos disponibles", "Alta", "Muy alta"],
             ["Ideal para", "Informes de seguimiento para equipos", "Informes con pocos datos y mucho diseño", "Exploración con cálculos complejos"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [2.0, 3.4, 3.4, 3.5], size=12.5, alto_fila=0.78)
    callout(sl, 0.5, 6.15, 12.3, 0.8, "Elegí la herramienta más simple que resuelva la necesidad de tu audiencia.", size=15)
    pie2(sl, "Resumen de las tres presentaciones de la sesión 5.")

def practicar():
    sl = nueva("Para practicar: tu informe en Looker Studio", "Tu turno", "Cierre: Mini-proyecto 2 y Quiz 5C.")
    viñetas(sl, 0.7, 1.5, 7.3, 4.4, ["Subí `can2022_departamentos.csv` a una **Hoja de cálculo de Google** y conectala a un informe nuevo.", "Armá tarjetas, un ranking y un gráfico de variación 2008–2022.", "Agregá un control de **Región** y escribí un título con el mensaje principal.", "Compartilo con permiso de lector y pegá el **enlace** en el aula.", "Resolvé el **Quiz 5C** del aula: evalúa lo visto en esta presentación."], size=15)
    ajustada(sl, "l5", 8.3, 1.6, 4.5, 3.6)
    callout(sl, 0.7, 6.0, 12.1, 0.95, "Un buen informe de BI cuenta una historia verificable con datos oficiales y se entiende en cinco segundos.", size=16)

def construir():
    portada(); que_es(); datos(); preparar(); conectar(); tipos()
    seccion_tarjetas(); seccion_mapa(); seccion_barras(); seccion_variacion(); seccion_concentracion(); seccion_uso()
    controles(); estilo(); compartir(); comparar(); practicar()
    salida = M / "fuentes" / "looker_studio_can2022.pptx"; G.prs.save(salida); print("guardado", salida, len(G.prs.slides), "diapositivas")

if __name__ == "__main__": construir()
