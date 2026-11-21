# Prepara los datos AGREGADOS (sin filas individuales) que usa la presentación de ggplot2.
# Entrada: carpeta con REG02_EPHC_ANUAL_<año>.csv del INE (ver r/02_ejercicio_ephc_concepcion.Rmd).
# Uso: Rscript tools/ggplot_datos.R [carpeta_con_los_csv]
suppressMessages({library(dplyr); library(readr)})
args <- commandArgs(trailingOnly = TRUE)
dir_in <- if (length(args)) args[1] else "datos_ephc"
dir_out <- "aula/media/unidad2_ggplot/fuentes/datos"; dir.create(dir_out, showWarnings = FALSE, recursive = TRUE)
leer <- function(y) read_delim(file.path(dir_in, sprintf("REG02_EPHC_ANUAL_%d.csv", y)), delim = ";", na = c("", " "), show_col_types = FALSE,
  locale = locale(decimal_mark = ",", grouping_mark = ".", encoding = "UTF-8"), col_select = any_of(c("AÑO", "DPTO", "P02", "P06", "PEAA", "FACTOR"))) |> rename(anio = any_of("AÑO"))
eph <- bind_rows(lapply(2022:2025, leer)) |>
  mutate(sexo = factor(P06, levels = c(1, 6), labels = c("Hombres", "Mujeres")), ocup = factor(PEAA, levels = 1:3, labels = c("Ocupado", "Desocupado", "Inactivo")))
conce <- filter(eph, DPTO == 1)
ocup_larga <- conce |> filter(!is.na(ocup), !is.na(FACTOR)) |> group_by(anio, ocup) |>
  summarise(personas = round(sum(FACTOR)), casos_muestrales = n(), .groups = "drop") |> arrange(anio, ocup)
write_csv(ocup_larga, file.path(dir_out, "ocup_concepcion.csv"))
cortes <- c(seq(0, 80, 5), Inf); etq <- c(paste(seq(0, 75, 5), seq(4, 79, 5), sep = "-"), "80+")
piramide <- conce |> filter(anio == 2025, !is.na(P02), !is.na(sexo), !is.na(FACTOR)) |>
  mutate(grupo = cut(P02, breaks = cortes, labels = etq, right = FALSE)) |> group_by(grupo, sexo) |>
  summarise(personas = round(sum(FACTOR)), casos_muestrales = n(), .groups = "drop")
write_csv(piramide, file.path(dir_out, "piramide_concepcion_2025.csv"))
print(ocup_larga); cat("pirámide:", nrow(piramide), "filas; total", sum(piramide$personas), "\n")
