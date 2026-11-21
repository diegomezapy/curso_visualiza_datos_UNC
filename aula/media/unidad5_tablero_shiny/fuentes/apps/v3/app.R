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
                       medios, medios)),
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
       plotlyOutput("tendencia", height = 170))
)

server <- function(input, output, session) {
  datos <- reactive({
    req(input$anio, input$medio)
    cubo |>
      filter(anio %in% input$anio,
             medio %in% input$medio)
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
}

shinyApp(ui, server)
