# Ejecuta el código REAL de cada figura de la presentación «Elección de gráficos» (aula/media/unidad2_eleccion/fuentes/pasos/*.R).
# Uso: python tools/eleccion_pptx.py --pasos ; Rscript tools/eleccion_datos.R <csv> ; Rscript tools/eleccion_figuras.R
suppressMessages({library(ggplot2); library(dplyr); library(readr); library(ragg)})
base <- "aula/media/unidad2_eleccion/fuentes"
eph <- read_csv(file.path(base, "datos", "ocupados_2025_muestra.csv"), show_col_types = FALSE) |> mutate(sexo = factor(sexo), area = factor(area, levels = c("Urbana", "Rural")))
dptos <- read_csv(file.path(base, "datos", "ingreso_mediano_departamentos_2025.csv"), show_col_types = FALSE)
compo <- read_csv(file.path(base, "datos", "situacion_por_area_2025.csv"), show_col_types = FALSE) |>
  mutate(situacion = factor(situacion, levels = c("Ocupado", "Desocupado", "Inactivo")), area = factor(area, levels = c("Urbana", "Rural")))
tasa <- read_csv(file.path(base, "datos", "tasa_ocupacion_sexo.csv"), show_col_types = FALSE) |> mutate(sexo = factor(sexo, levels = c("Hombres", "Mujeres")))
colores <- c(Ocupado = "#0072B2", Desocupado = "#D55E00", Inactivo = "#009E73")
dir.create(file.path(base, "figuras"), showWarnings = FALSE)
for (f in sort(list.files(file.path(base, "pasos"), pattern = "\\.R$", full.names = TRUE))) {
  id <- sub("\\.R$", "", basename(f)); env <- new.env(parent = globalenv())
  for (n in c("eph", "dptos", "compo", "tasa", "colores")) assign(n, get(n), envir = env)
  g <- suppressMessages(source(f, local = env, echo = FALSE)$value)
  ggsave(file.path(base, "figuras", paste0(id, ".png")), plot = g, width = 6.4, height = 3.9, dpi = 170, device = ragg::agg_png, bg = "white")
  cat("✔", id, "\n")
}
