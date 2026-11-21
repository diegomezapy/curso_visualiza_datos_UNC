"""Presentación «Tablero dinámico en RStudio con Shiny» (sesión 5, Unidad 2): construye el tablero de aduanas paso a paso, con capturas REALES de cada versión.
Uso: python tools/tablero_capturas.py ; python tools/tablero_pptx.py ; python tools/procesar_presentacion.py unidad5_tablero_shiny"""
import sys, difflib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ggplot_pptx import *
import ggplot_pptx as G
import tablero_spec as T
M = G.RAIZ / "aula" / "media" / "unidad5_tablero_shiny"; CAP = M / "fuentes" / "capturas"
PIE = "Fuente: DNIT, base de datos abiertos de aduanas · importaciones de electrónica 2024–2025 (sin junio de 2025) · capturas de la app en ejecución"
pie2 = lambda sl, t=PIE: G.pie(sl, t)
ASPECT = 820 / 1280

def nuevas(prev, cur):
    """Líneas nuevas de `cur` respecto de `prev`, marcadas con § y separadas con «# …» donde se omite código."""
    a, b = prev.split("\n"), cur.split("\n"); out = []; ult = -1
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("insert", "replace"):
            if out and j1 - 1 != ult: out.append("# …")
            out += ["§" + l for l in b[j1:j2]]; ult = j2 - 1
    return out

def paso(titulo, tag, img, codigo_lin, puntos, mensaje, nota="", tam=10):
    sl = nueva(titulo, tag, nota)
    tam = min(tam, round(3.85 * 72 / (1.22 * len(codigo_lin)), 1))   # que todas las líneas quepan en el recuadro
    codigo(sl, 0.5, 1.3, 5.75, 4.1, codigo_lin, size=tam)
    w = 6.3; h = w * ASPECT
    imagen(sl, CAP / img, 6.55, 1.3, w, h)
    viñetas(sl, 0.5, 5.55, 8.4, 1.5, puntos, size=12.5)
    callout(sl, 9.0, 5.55, 3.8, 1.45, mensaje, size=12.5)
    pie2(sl)
    return sl

def portada():
    sl = G.prs.slides.add_slide(G.BLANK); sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb(BG)
    caja(sl, 0.7, 1.35, 6.3, 0.4, ["MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC"], size=11, color=ACC, bold=True)
    caja(sl, 0.7, 2.0, 6.3, 2.2, ["Un tablero dinámico en RStudio con Shiny"], size=36, color=DARK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(sl, 0.7, 4.3, 6.2, 0.9, ["Lo construimos paso a paso con la base de aduanas (DNIT): filtros, KPI, gráficos que responden al clic y descarga de datos"], size=16, color=MUT)
    caja(sl, 0.7, 5.6, 6.2, 0.6, ["Sesión 5 · Unidad 2 · Dashboards interactivos"], size=14, color=TXT)
    imagen(sl, CAP / "v5_clic.png", 7.1, 1.7, 5.9, 5.9 * ASPECT)
    sl.notes_slide.notes_text_frame.text = "Parte 2 de la sesión 5: del tablero estático (RPubs) al tablero dinámico con Shiny. Cada captura es de la app real ejecutándose; el código de cada diapositiva es el que se ejecutó."

def estatico_vs_dinamico():
    sl = nueva("Estático o dinámico: ¿dónde corre el cálculo?", "Punto de partida", "Diferencia clave: un servidor de R detrás del tablero.")
    filas = [["", "Estático (RPubs, plotly)", "Dinámico (Shiny)"],
             ["Dónde corre el código", "Una sola vez, al hacer Knit", "En un servidor de R, cada vez que alguien interactúa"],
             ["Filtros", "Dentro del navegador, sobre datos ya incluidos", "Recalculan con R: cualquier análisis o dato"],
             ["Datos", "Embebidos en el HTML (tamaño limitado)", "Pueden leerse de archivos, bases o APIs"],
             ["Publicación", "RPubs, GitHub Pages: gratis y sin servidor", "shinyapps.io, Posit Connect o servidor propio"],
             ["Ideal para", "Informes y tableros con pocos datos", "Exploración con muchos datos o cálculos a pedido"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [2.4, 4.6, 5.3], size=13, alto_fila=0.72)
    callout(sl, 0.5, 6.0, 12.3, 0.9, "Elegí lo más simple que resuelva la necesidad: si los filtros alcanzan con HTML estático, no hace falta un servidor.", size=15)
    pie2(sl, "Chang et al. (2024). Shiny: Web Application Framework for R. shiny.posit.co")

def arquitectura():
    sl = nueva("Cómo piensa Shiny: entradas, cálculos reactivos y salidas", "Idea central", "Reactividad: cuando cambia una entrada, solo se recalcula lo que depende de ella.")
    cajas = [("Entradas", "input$anio\ninput$medio", ACC, 0.7), ("Datos reactivos", "datos <- reactive({…})", GRN, 4.9), ("Salidas", "output$fob\noutput$tendencia\noutput$tabla", ORA, 9.1)]
    for t, c, col, x in cajas:
        rect(sl, x, 1.7, 3.5, 2.2, "FFFFFF", line=col); rect(sl, x, 1.7, 3.5, 0.55, col, radius=0.1)
        caja(sl, x, 1.7, 3.5, 0.55, [f"**{t}**"], size=16, color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        caja(sl, x + 0.1, 2.3, 3.3, 1.6, c.split("\n"), size=14, font=G.MONO, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    for x in (4.3, 8.5):
        caja(sl, x, 2.5, 0.6, 0.8, ["→"], size=30, color=MUT, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    viñetas(sl, 0.7, 4.3, 12.1, 1.6, ["**ui** describe la pantalla: controles (`checkboxGroupInput`) y contenedores de resultados (`plotlyOutput`).", "**server** es una función con la lógica: `reactive()` calcula una vez los datos filtrados y todas las salidas los reutilizan.", "Cuando el usuario cambia un filtro, Shiny **invalida** solo lo que depende de él y lo recalcula."], size=14)
    callout(sl, 0.7, 6.1, 12.1, 0.8, "Regla de oro: el filtrado se escribe una sola vez en un `reactive()`, no en cada gráfico.", size=15)
    pie2(sl, "Referencia: mastering-shiny.org (Wickham)")

def preparacion():
    sl = nueva("Preparación: paquetes, datos y carpeta de la app", "Punto de partida", "Mostrar la estructura de carpeta: app.R + el CSV agregado en la misma carpeta.")
    codigo(sl, 0.5, 1.3, 6.3, 2.3, ["# En la consola de R (una sola vez)", 'install.packages(c("shiny", "bslib", "plotly",', '                   "dplyr", "DT"))', "", "# Estructura de la carpeta", "tablero_aduanas/", "├── app.R", "└── cubo_importaciones.csv"], size=12)
    codigo(sl, 0.5, 3.8, 6.3, 2.3, ["cubo <- read.csv(\"cubo_importaciones.csv\") |>", "  filter(mes != 6) |>   # la base no trae junio de 2025", "  mutate(fob_mm = fob_usd / 1e6)", "", "# Original DNIT: separador ';' y coma decimal", 'read.csv2("aduana_2025_ENERO.csv")', "# equivale a read.csv(sep = \";\", dec = \",\")"], size=11.5)
    viñetas(sl, 7.2, 1.35, 5.6, 4.9, ["La base original de aduanas viene separada por **punto y coma** y con coma decimal: `read.csv2()` lo lee bien.", "Cada fila es un **subítem**: se deduplica por despacho e ítem antes de agregar (visto en la parte 1 de la sesión).", "La app lee un **cubo agregado** (año, mes, aduana, país, medio): liviano y rápido.", "Un tablero dinámico **no debería leer 200 MB en cada consulta**: se preagrega.", "Para correrla: abrir `app.R` en RStudio y pulsar **Run App**."], size=14)
    pie2(sl)

def paso_diff(titulo, tag, k_prev, k, img, puntos, mensaje, nota="", tam=10.5, lin=None):
    prev = T.APPS[k_prev] if k_prev else ""
    lin = lin or nuevas(prev, T.APPS[k]) if k_prev else ["§" + l for l in T.APPS[k].split("\n")[:24]] + ["§# …"]
    return paso(titulo, tag, img, lin, puntos, mensaje, nota, tam)

def esqueleto():
    sl = nueva("El tablero completo: esqueleto de la app", "Resumen", "Estructura final: ui + server con un reactive central.")
    esq = ["library(shiny); library(bslib); library(dplyr); library(plotly)", "cubo <- read.csv(\"cubo_importaciones.csv\") |> …", "", "ui <- page_sidebar(", "  title = \"Importaciones de electrónica · DNIT\",", "  sidebar = sidebar(<filtros>, <botón limpiar>),", "  layout_columns(<4 value_box de KPI>),", "  card(plotlyOutput(\"tendencia\")),", "  layout_columns(card(plotlyOutput(\"aduanas\")),", "                 card(plotlyOutput(\"paises\"))),", "  card(DT::DTOutput(\"tabla\"))", ")", "", "server <- function(input, output, session) {", "  aduana_sel <- reactiveVal(NULL)   # estado del clic", "  datos <- reactive({ … })          # filtro único", "  output$fob <- renderText(…)       # KPI", "  output$tendencia <- renderPlotly(…)", "  output$aduanas <- renderPlotly(…)  # clic = filtro", "  output$tabla <- DT::renderDT(…)", "}", "shinyApp(ui, server)"]
    codigo(sl, 0.5, 1.3, 6.6, 5.4, esq, size=11.5)
    imagen(sl, CAP / "v6_clic.png", 7.3, 1.45, 5.6, 5.6 * ASPECT)
    viñetas(sl, 7.3, 5.2, 5.6, 1.7, ["65 líneas de R: KPI, tendencia, ranking, composición, tabla y descarga.", "El archivo completo está en `r/app_tablero_aduanas/app.R`."], size=13)
    pie2(sl)

def buenas_practicas():
    sl = nueva("Buenas prácticas para un tablero dinámico", "Para recordar", "Cuidar rendimiento, validación y claridad.")
    filas = [["Práctica", "Por qué", "En el código"],
             ["Un solo `reactive()` para filtrar", "Evita repetir y recalcular el filtro", "`datos <- reactive({…})`"],
             ["Validar entradas con `req()`", "Sin selección, la app no falla ni muestra errores", "`req(input$anio, input$medio)`"],
             ["Preagregar los datos", "Menos filas = respuesta inmediata", "`cubo_importaciones.csv` (3.304 filas)"],
             ["Estado explícito de la interacción", "El clic debe poder deshacerse", "`reactiveVal()` y botón «Quitar filtro»"],
             ["Mostrar el filtro activo", "El lector sabe qué está viendo", "`output$sel` («Aduana: …»)"],
             ["Declarar fuente y límites", "Reproducibilidad y honestidad", "Título, pie y nota (sin junio de 2025)"]]
    G.tabla(sl, 0.5, 1.4, 12.3, filas, [3.9, 4.4, 4.0], size=13, alto_fila=0.7)
    pie2(sl, "Few (2013) y Wickham, Mastering Shiny.")

def publicar():
    sl = nueva("Cómo publicar y compartir el tablero", "Herramientas", "RPubs no ejecuta Shiny: hay que usar un servidor de R.")
    codigo(sl, 0.5, 1.3, 6.2, 2.4, ["# Publicar en shinyapps.io (cuenta gratuita)", 'install.packages("rsconnect")', 'rsconnect::setAccountInfo(name = "…", token = "…",', '                         secret = "…")', 'rsconnect::deployApp("tablero_aduanas")'], size=12)
    codigo(sl, 0.5, 3.9, 6.2, 1.5, ["# Ejecutarla en tu computadora", 'shiny::runApp("tablero_aduanas")'], size=13)
    viñetas(sl, 7.1, 1.35, 5.7, 4.3, ["**RPubs** publica HTML estático: sirve para el tablero de la parte 1 (plotly), **no** para Shiny.", "**shinyapps.io**: la forma más rápida de compartir una app con un enlace (plan gratuito con límites).", "**Posit Connect** o **Shiny Server**: para uso institucional con control de acceso.", "Alternativa sin servidor: **Shinylive** (la app corre en el navegador con WebAssembly)."], size=14)
    callout(sl, 0.5, 5.75, 12.3, 0.85, "Antes de publicar datos: verificá que sean públicos o estén agregados, y que el pie declare la fuente.", size=14)
    pie2(sl, "Documentación: docs.posit.co/shinyapps.io")

def practicar():
    sl = nueva("Para practicar: ampliá el tablero", "Tu turno", "Cierre: Mini-proyecto 2 y Quiz 5B.")
    viñetas(sl, 0.7, 1.5, 7.2, 4.4, ["Abrí `r/app_tablero_aduanas/app.R` en **RStudio** y pulsá **Run App**.", "Agregá un filtro por **país** y un KPI nuevo (por ejemplo, el valor medio por ítem).", "Hacé que el clic en el gráfico de países también filtre el tablero.", "Escribí un **título que enuncie el mensaje** y una nota con las limitaciones de los datos.", "Resolvé el **Quiz 5B** del aula: evalúa lo visto en esta presentación."], size=15)
    imagen(sl, CAP / "v6_tabla.png", 8.2, 1.6, 4.6, 4.6 * ASPECT)
    callout(sl, 0.7, 6.0, 12.1, 0.95, "Un tablero dinámico bien hecho responde preguntas que el autor todavía no pensó, sin perder claridad.", size=16)

def construir():
    portada(); estatico_vs_dinamico(); arquitectura(); preparacion()
    paso_diff("Paso 1: una app mínima, con un solo valor", "Paso 1 de 6", None, "v1", "v1.png", ["`page_fluid()` crea la página; `value_box()` muestra el KPI.", "`textOutput(\"fob\")` en la **ui** es un hueco que el **server** llena con `renderText()`.", "Todavía sin filtros: el valor es la suma de todos los datos."], "ui declara los huecos; server decide qué poner en cada uno.", "App mínima.", 11.5)
    paso_diff("Paso 2: filtros y KPI que se recalculan", "Paso 2 de 6", "v1", "v2", "v2.png", ["`checkboxGroupInput()` crea los filtros; `page_sidebar()` los ubica a la izquierda.", "`datos <- reactive({…})` filtra **una sola vez**; los 4 KPI lo reutilizan.", "En la captura se desmarcó AVION: el valor FOB pasó de 750 a 614 millones de USD."], "Un cambio en un filtro recalcula solo lo que depende de él.", "En la captura de este paso, AVION está desmarcado.", lin=["§medios <- sort(unique(cubo$medio))", "", "ui <- page_sidebar(", "§  sidebar = sidebar(", '§    checkboxGroupInput("anio", "Año", …),', '§    checkboxGroupInput("medio", "Medio…",', "§                       medios, medios)),", "§  layout_columns(fill = FALSE,", '§    value_box("Valor FOB…", textOutput("fob")),', '§    value_box("Ítems…", textOutput("items")),', "§    # … otros 2 value_box (USD/kg, % China)", "  )", ")", "", "server <- function(input, output, session) {", "§  datos <- reactive({", "§    req(input$anio, input$medio)", "§    cubo |>", "§      filter(anio %in% input$anio,", "§             medio %in% input$medio)", "§  })", "§  output$fob <- renderText(", "§    fmt(sum(datos()$fob_mm)))", "§  # … items, usd_kg y china igual", "}"])
    paso_diff("Paso 3: un gráfico de tendencia reactivo", "Paso 3 de 6", "v2", "v3", "v3.png", ["`plotlyOutput()` en la ui y `renderPlotly()` en el server: el gráfico usa `datos()`.", "Dos años superpuestos por mes: 2025 en naranja, 2024 en gris de contexto.", "Si se cambian los filtros, la curva se redibuja sola."], "El gráfico no filtra: consume los datos reactivos ya filtrados.")
    paso_diff("Paso 4: ranking de aduanas y países de origen", "Paso 4 de 6", "v3", "v4", "v4.png", ["Dos tarjetas en `layout_columns()`: barras horizontales **ordenadas** con `reorder()`.", "Aduanas en azul de énfasis; países en gris: el color guía la mirada.", "Ambos gráficos reutilizan `datos()`."], "Cada gráfico responde una pregunta: ¿dónde entra? y ¿de dónde viene?", "", 10)
    paso_diff("Paso 5: interacción con propósito: el clic filtra", "Paso 5 de 6", "v4", "v5", "v5_clic.png", ["`event_data(\"plotly_click\")` lee la barra que el usuario tocó.", "`reactiveVal()` guarda la aduana elegida; `datos()` agrega ese filtro.", "En la captura se hizo clic en PTO SEGURO FLUVIAL: todos los KPI y gráficos se actualizan."], "Hacer clic en un dato para filtrar es *zoom y filtros* del mantra de Shneiderman.", "El botón «Quitar filtro» vuelve al estado inicial.", 10.5, lin=["§    actionButton(\"limpiar\", \"Quitar filtro…\"),", "§    textOutput(\"sel\"),", "# …", "server <- function(input, output, session) {", "§  aduana_sel <- reactiveVal(NULL)", "§  observeEvent(", '§    event_data("plotly_click", source = "rank"),', "§    aduana_sel(event_data(\"plotly_click\",", '§                          source = "rank")$y))', "§  observeEvent(input$limpiar, aduana_sel(NULL))", "  datos <- reactive({", "    req(input$anio, input$medio)", "    d <- cubo |> filter(…)", "§    if (!is.null(aduana_sel()))", "§      d <- filter(d, aduana == aduana_sel())", "    d", "  })", "# … en el gráfico de aduanas:", "§      event_register(\"plotly_click\")"])
    paso_diff("Paso 6: detalle bajo demanda, descarga y tema", "Paso 6 de 6", "v5", "v6", "v6_tabla.png", ["`DT::DTOutput()` muestra una tabla paginada con el detalle (*details on demand*).", "`downloadButton()` + `downloadHandler()` permiten bajar los datos filtrados.", "`bs_theme()` ajusta colores: pocos cambios, mucha coherencia."], "Detalle y descarga: el lector puede verificar y reutilizar lo que ve.", "La tabla respeta el filtro de aduana.", 9.5)
    esqueleto(); buenas_practicas(); publicar(); practicar()
    salida = M / "fuentes" / "tablero_shiny_aduanas.pptx"; G.prs.save(salida); print("guardado", salida, len(G.prs.slides), "diapositivas")

if __name__ == "__main__": construir()
