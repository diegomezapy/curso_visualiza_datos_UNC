# Datos de la presentación «Elección de gráficos» (sesión 2): microdatos de la EPHC anual del INE, solo columnas analíticas
# (sin identificadores de hogar ni de persona) y tablas agregadas. Uso: Rscript tools/eleccion_datos.R [carpeta_con_los_csv]
suppressMessages({library(dplyr); library(readr)})
args <- commandArgs(trailingOnly = TRUE); dir_in <- if (length(args)) args[1] else "datos_ephc"
dir_out <- "aula/media/unidad2_eleccion/fuentes/datos"; dir.create(dir_out, showWarnings = FALSE, recursive = TRUE)
leer <- function(y) read_delim(file.path(dir_in, sprintf("REG02_EPHC_ANUAL_%d.csv", y)), delim = ";", na = c("", " "), show_col_types = FALSE,
  locale = locale(decimal_mark = ",", grouping_mark = ".", encoding = "UTF-8"),
  col_select = any_of(c("AÑO", "DPTO", "AREA", "P02", "P06", "PEAA", "FACTOR", "añoest", "e01aimde"))) |> rename(anio = any_of("AÑO"))
eph <- bind_rows(lapply(2022:2025, leer)) |> mutate(
  sexo = factor(P06, levels = c(1, 6), labels = c("Hombres", "Mujeres")), area = factor(AREA, levels = c(1, 6), labels = c("Urbana", "Rural")),
  situacion = factor(PEAA, levels = 1:3, labels = c("Ocupado", "Desocupado", "Inactivo")))
DEP <- c("Asunción", "Concepción", "San Pedro", "Cordillera", "Guairá", "Caaguazú", "Caazapá", "Itapúa", "Misiones", "Paraguarí", "Alto Paraná", "Central", "Ñeembucú", "Amambay", "Canindeyú", "Presidente Hayes")
wmed <- function(x, w) { o <- order(x); x <- x[o]; w <- w[o]; x[which(cumsum(w) >= sum(w) / 2)[1]] }
e25 <- filter(eph, anio == 2025)
ocup <- e25 |> filter(situacion == "Ocupado", !is.na(e01aimde), e01aimde > 0, P02 >= 15, !is.na(sexo), !is.na(area), !is.na(añoest), añoest <= 30)
# 1) muestra aleatoria de 6.000 ocupados con ingreso (para distribuciones y relaciones)
set.seed(2026)
muestra <- ocup |> slice_sample(n = 6000) |> transmute(sexo, area, edad = P02, anios_est = añoest, ingreso = e01aimde, dpto = DEP[DPTO + 1])
write_csv(muestra, file.path(dir_out, "ocupados_2025_muestra.csv"))
# 2) ranking de departamentos: ingreso mediano (ponderado) y personas ocupadas con ingreso
dptos <- ocup |> group_by(dpto = DEP[DPTO + 1]) |> summarise(ingreso_mediano = round(wmed(e01aimde, FACTOR)), ocupados = round(sum(FACTOR)), casos = n(), .groups = "drop") |> arrange(desc(ingreso_mediano))
write_csv(dptos, file.path(dir_out, "ingreso_mediano_departamentos_2025.csv"))
# 3) composición de la situación de ocupación (15 años o más) por área, 2025
compo <- e25 |> filter(P02 >= 15, !is.na(situacion), !is.na(area), !is.na(FACTOR)) |> group_by(area, situacion) |> summarise(personas = round(sum(FACTOR)), casos = n(), .groups = "drop")
write_csv(compo, file.path(dir_out, "situacion_por_area_2025.csv"))
# 4) tasa de ocupación (ocupados / población de 15 años o más) por sexo, 2022-2025
tasa <- eph |> filter(P02 >= 15, !is.na(situacion), !is.na(sexo), !is.na(FACTOR)) |> group_by(anio, sexo) |>
  summarise(tasa = round(100 * sum(FACTOR[situacion == "Ocupado"]) / sum(FACTOR), 1), casos = n(), .groups = "drop")
write_csv(tasa, file.path(dir_out, "tasa_ocupacion_sexo.csv"))
print(dptos); print(compo); print(tasa); print(summary(muestra)); cat(nrow(ocup), "ocupados con ingreso\n")
