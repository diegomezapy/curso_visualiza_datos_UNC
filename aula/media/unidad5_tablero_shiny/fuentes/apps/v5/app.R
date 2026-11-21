library(shiny)
library(bslib)
library(dplyr)
library(plotly)

cubo <- read.csv("cubo_importaciones.csv") |>
  filter(mes != 6) |>   # la base no trae junio de 2025
  mutate(fob_mm = fob_usd / 1e6)
fmt <- scales::label_number(
  big.mark = ".", decimal.mark = ",")
medios <- sort(unique(cubo$medio))

ui <- page_sidebar(
  title = "Importaciones de electrónica · DNIT",
  fillable = FALSE,
  sidebar = sidebar(
    checkboxGroupInput("anio", "Año",
                       c(2024, 2025), c(2024, 2025)),
    checkboxGroupInput("medio", "Medio de transporte",
                       medios, medios),
    actionButton("limpiar", "Quitar filtro de aduana",
                 class = "btn-sm"),
    textOutput("sel")),
  layout_columns(fill = FALSE,
    value_box("Valor FOB (millones de USD)",
              textOutput("fob"), theme = "primary"),
    value_box("Ítems importados",
              textOutput("items"), theme = "secondary"),
    value_box("USD por kilo neto",
              textOutput("usd_kg"), theme = "info"),
    value_box("Participación de China",
              textOutput("china"), theme = "success")),
  card(card_header("Valor mensual (millones de USD)"),
       plotlyOutput("tendencia", height = 170)),
  layout_columns(fill = FALSE,
    card(card_header("Aduanas con mayor valor (clic)"),
         plotlyOutput("aduanas", height = 190)),
    card(card_header("Países de origen"),
         plotlyOutput("paises", height = 190)))
)

server <- function(input, output, session) {
  aduana_sel <- reactiveVal(NULL)
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
  output$fob <- renderText(fmt(sum(datos()$fob_mm)))
  output$items <- renderText(fmt(sum(datos()$items)))
  output$usd_kg <- renderText(scales::number(
    sum(datos()$fob_usd) / sum(datos()$kilo_neto),
    0.01, big.mark = ".", decimal.mark = ","))
  output$china <- renderText(scales::percent(
    sum(datos()$fob_usd[datos()$pais == "CHINA"]) /
      sum(datos()$fob_usd), 0.1))
  output$tendencia <- renderPlotly({
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
  output$aduanas <- renderPlotly({
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
             yaxis = list(title = "")) |>
      event_register("plotly_click")
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
  output$sel <- renderText(
    if (is.null(aduana_sel())) "Todas las aduanas"
    else paste("Aduana:", aduana_sel()))
}

shinyApp(ui, server)
