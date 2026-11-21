# Ejecuta el código REAL de cada paso (aula/media/unidad2_ggplot/fuentes/pasos/*.R) y guarda la figura.
# Así la diapositiva muestra exactamente el código que produce la imagen.
# Uso: Rscript tools/ggplot_figuras.R      (antes: python tools/ggplot_pasos_a_archivos.py ; datos: tools/ggplot_datos.R)
suppressMessages({library(ggplot2); library(dplyr); library(readr); library(patchwork); library(ragg)})
base <- "aula/media/unidad2_ggplot/fuentes"
ocup_larga <- read_csv(file.path(base, "datos", "ocup_concepcion.csv"), show_col_types = FALSE) |>
  mutate(ocup = factor(ocup, levels = c("Ocupado", "Desocupado", "Inactivo")))
piramide <- read_csv(file.path(base, "datos", "piramide_concepcion_2025.csv"), show_col_types = FALSE)
colores <- c(Ocupado = "#0072B2", Desocupado = "#D55E00", Inactivo = "#009E73")
dir.create(file.path(base, "figuras"), showWarnings = FALSE)

for (f in sort(list.files(file.path(base, "pasos"), pattern = "\\.R$", full.names = TRUE))) {
  id <- sub("\\.R$", "", basename(f))
  env <- new.env(parent = globalenv())
  env$ocup_larga <- ocup_larga; env$piramide <- piramide; env$colores <- colores
  g <- source(f, local = env, echo = FALSE)$value
  ancho <- if (id == "p06") 7.4 else 6.4
  ggsave(file.path(base, "figuras", paste0(id, ".png")), plot = g, width = ancho, height = 3.9, dpi = 170, device = ragg::agg_png, bg = "white")
  cat("✔", id, "\n")
}
