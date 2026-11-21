# Tablero dinámico de aduanas (Shiny)

App de la sesión 5. Datos: importaciones de electrónica 2024–2025 (base de datos abiertos de aduanas, DNIT), agregadas por año, mes, aduana, país y medio de transporte. La base no trae junio de 2025.

1. Instalar: `install.packages(c("shiny", "bslib", "dplyr", "plotly", "DT"))`
2. Abrir `app.R` en RStudio y pulsar **Run App** (o `shiny::runApp("r/app_tablero_aduanas")`).
3. Publicar: `rsconnect::deployApp("r/app_tablero_aduanas")` (shinyapps.io).

El paso a paso (6 versiones) está en la presentación de la sesión 5 del aula.
