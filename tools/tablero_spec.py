"""Contenido de la presentación «Tablero dinámico en RStudio (Shiny)» (sesión 5, Unidad 2): datos de aduanas (DNIT), importaciones de electrónica.
Cada paso es una app COMPLETA (se ejecuta y se captura la pantalla real); las líneas con § son las nuevas respecto del paso anterior."""
def L(t): return t.strip("\n").split("\n")
CAB = '''library(shiny)
library(bslib)
library(dplyr)
library(plotly)

cubo <- read.csv("cubo_importaciones.csv") |>
  filter(mes != 6) |>   # la base no trae junio de 2025
  mutate(fob_mm = fob_usd / 1e6)
fmt <- scales::label_number(
  big.mark = ".", decimal.mark = ",")
'''
V1 = CAB + '''
ui <- page_fluid(
  h2("Importaciones de electrónica"),
  value_box("Valor FOB (millones de USD)",
            textOutput("fob"), theme = "primary")
)

server <- function(input, output, session) {
  output$fob <- renderText(fmt(sum(cubo$fob_mm)))
}

shinyApp(ui, server)
'''
KPI_UI = '''  layout_columns(fill = FALSE,
    value_box("Valor FOB (millones de USD)",
              textOutput("fob"), theme = "primary"),
    value_box("Ítems importados",
              textOutput("items"), theme = "secondary"),
    value_box("USD por kilo neto",
              textOutput("usd_kg"), theme = "info"),
    value_box("Participación de China",
              textOutput("china"), theme = "success")),
'''
SIDEBAR = '''  sidebar = sidebar(
    checkboxGroupInput("anio", "Año",
                       c(2024, 2025), c(2024, 2025)),
    checkboxGroupInput("medio", "Medio de transporte",
                       medios, medios)),
'''
DATOS = '''  datos <- reactive({
    req(input$anio, input$medio)
    cubo |>
      filter(anio %in% input$anio,
             medio %in% input$medio)
  })
'''
DATOS5 = '''  aduana_sel <- reactiveVal(NULL)
  observeEvent(
    event_data("plotly_click", source = "rank"),
    aduana_sel(event_data("plotly_click",
                          source = "rank")$y))
  observeEvent(input$limpiar, aduana_sel(NULL))
  datos <- reactive({
    req(input$anio, input$medio)
    d <- cubo |>
      filter(anio %in% input$anio,
             medio %in% input$medio)
    if (!is.null(aduana_sel()))
      d <- filter(d, aduana == aduana_sel())
    d
  })
'''
KPIS_SRV = '''  output$fob <- renderText(fmt(sum(datos()$fob_mm)))
  output$items <- renderText(fmt(sum(datos()$items)))
  output$usd_kg <- renderText(scales::number(
    sum(datos()$fob_usd) / sum(datos()$kilo_neto),
    0.01, big.mark = ".", decimal.mark = ","))
  output$china <- renderText(scales::percent(
    sum(datos()$fob_usd[datos()$pais == "CHINA"]) /
      sum(datos()$fob_usd), 0.1))
'''
TEND_UI = '''  card(card_header("Valor mensual (millones de USD)"),
       plotlyOutput("tendencia", height = 170)),
'''
TEND_SRV = '''  output$tendencia <- renderPlotly({
    m <- datos() |>
      group_by(anio, mes) |>
      summarise(fob_mm = sum(fob_mm), .groups = "drop")
    plot_ly(m, x = ~mes, y = ~fob_mm,
            color = ~factor(anio),
            type = "scatter", mode = "lines+markers",
            colors = c("2024" = "#9FB6CB",
                       "2025" = "#D55E00")) |>
      layout(xaxis = list(title = "Mes", dtick = 1),
             yaxis = list(title = ""),
             legend = list(orientation = "h"))
  })
'''
RANK_UI = '''  layout_columns(fill = FALSE,
    card(card_header("Aduanas con mayor valor (clic)"),
         plotlyOutput("aduanas", height = 190)),
    card(card_header("Países de origen"),
         plotlyOutput("paises", height = 190))),
'''
RANK_SRV = '''  output$aduanas <- renderPlotly({
    r <- datos() |>
      group_by(aduana) |>
      summarise(fob_mm = sum(fob_mm)) |>
      slice_max(fob_mm, n = 8)
    plot_ly(r, x = ~fob_mm,
            y = ~reorder(aduana, fob_mm),
            type = "bar", orientation = "h",
            source = "rank",
            marker = list(color = "#0072B2")) |>
      layout(xaxis = list(title = "Millones de USD"),
             yaxis = list(title = ""))
  })
  output$paises <- renderPlotly({
    p <- datos() |>
      group_by(pais) |>
      summarise(fob_mm = sum(fob_mm)) |>
      slice_max(fob_mm, n = 8)
    plot_ly(p, x = ~fob_mm, y = ~reorder(pais, fob_mm),
            type = "bar", orientation = "h",
            marker = list(color = "#9FB6CB")) |>
      layout(xaxis = list(title = "Millones de USD"),
             yaxis = list(title = ""))
  })
'''
LIMPIAR = '''    actionButton("limpiar", "Quitar filtro de aduana",
                 class = "btn-sm"),
    textOutput("sel"),
'''
SEL_SRV = '''  output$sel <- renderText(
    if (is.null(aduana_sel())) "Todas las aduanas"
    else paste("Aduana:", aduana_sel()))
'''
TABLA_UI = '''  card(card_header("Detalle",
         downloadButton("bajar", "Descargar CSV",
                        class = "btn-sm")),
       DT::DTOutput("tabla"))
'''
TABLA_SRV = '''  output$tabla <- DT::renderDT(
    datos() |>
      group_by(aduana, pais) |>
      summarise(items = sum(items),
                fob_mm = round(sum(fob_mm), 2),
                .groups = "drop") |>
      arrange(desc(fob_mm)),
    options = list(pageLength = 6, dom = "tip"),
    rownames = FALSE)
  output$bajar <- downloadHandler(
    "importaciones_filtradas.csv",
    function(file) write.csv(datos(), file,
                             row.names = FALSE))
'''
def app(sidebar_extra="", kpi=True, tend=False, rank=False, tabla=False, sel=False, tema=False):
    ui = "ui <- page_sidebar(\n  title = \"Importaciones de electrónica · DNIT\",\n  fillable = FALSE,\n"
    if tema: ui += '  theme = bs_theme(primary = "#0072B2"),\n'
    sb = SIDEBAR
    if sel: sb = sb.replace('medios, medios)),\n', 'medios, medios),\n' + LIMPIAR.rstrip(",\n") + '),\n')
    ui += sb + KPI_UI
    if tend: ui += TEND_UI
    if rank: ui += RANK_UI
    if tabla: ui += TABLA_UI
    ui = ui.rstrip(",\n") + "\n)\n"
    srv = "\nserver <- function(input, output, session) {\n" + (DATOS5 if sel else DATOS) + KPIS_SRV
    if tend: srv += TEND_SRV
    if rank: srv += RANK_SRV.replace('yaxis = list(title = ""))\n  })\n  output$paises', 'yaxis = list(title = "")) |>\n      event_register("plotly_click")\n  })\n  output$paises', 1) if sel else RANK_SRV
    if sel: srv += SEL_SRV
    if tabla: srv += TABLA_SRV
    srv += "}\n\nshinyApp(ui, server)\n"
    return CAB + "medios <- sort(unique(cubo$medio))\n\n" + ui + srv
V2 = app(); V3 = app(tend=True); V4 = app(tend=True, rank=True); V5 = app(tend=True, rank=True, sel=True); V6 = app(tend=True, rank=True, sel=True, tabla=True, tema=True)
APPS = {"v1": V1, "v2": V2, "v3": V3, "v4": V4, "v5": V5, "v6": V6}
if __name__ == "__main__":
    print(V6)
