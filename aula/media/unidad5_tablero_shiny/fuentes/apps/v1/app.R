library(shiny)
library(bslib)
library(dplyr)
library(plotly)

cubo <- read.csv("cubo_importaciones.csv") |>
  filter(mes != 6) |>   # la base no trae junio de 2025
  mutate(fob_mm = fob_usd / 1e6)
fmt <- scales::label_number(
  big.mark = ".", decimal.mark = ",")

ui <- page_fluid(
  h2("Importaciones de electrónica"),
  value_box("Valor FOB (millones de USD)",
            textOutput("fob"), theme = "primary")
)

server <- function(input, output, session) {
  output$fob <- renderText(fmt(sum(cubo$fob_mm)))
}

shinyApp(ui, server)
