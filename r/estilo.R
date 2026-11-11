# Utilidades comunes de la pista R · Visualización de Datos (MICD · FACET-UNC)
# Uso en cada .Rmd:  source("estilo.R")   (o la versión en línea, ver el chunk de setup)
suppressPackageStartupMessages({ library(ggplot2); library(dplyr); library(tidyr); library(readr); library(scales); library(lubridate); library(patchwork) })

# Paleta Okabe-Ito: segura para daltonismo
okabe_ito  <- c("#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000")
BASE <- "#0072B2"; ENFASIS <- "#D55E00"; GRIS <- "#8C8C8C"; GRIS_CLARO <- "#D9D9D9"
options(ggplot2.discrete.colour = list(okabe_ito), ggplot2.discrete.fill = list(okabe_ito))

# Busca datos/ junto al repositorio; si no existe, los descarga de GitHub (útil al publicar o trabajar sin clonar)
ruta_datos <- function(archivo) {
  locales <- file.path(c(".", "..", "../.."), "datos", archivo)
  locales <- locales[file.exists(locales)]
  if (length(locales)) return(locales[1])
  paste0("https://raw.githubusercontent.com/diegomezapy/curso_visualiza_datos_UNC/main/datos/", archivo)
}
leer <- function(archivo, ...) readr::read_csv(ruta_datos(archivo), show_col_types = FALSE, ...)

# Tema limpio: poca tinta, título alineado a la izquierda
tema_curso <- function(base_size = 12) {
  theme_minimal(base_size = base_size) +
    theme(plot.title = element_text(face = "bold", hjust = 0), plot.title.position = "plot",
          panel.grid.minor = element_blank(), legend.position = "bottom")
}
theme_set(tema_curso())

fmt_num <- function(x, d = 1) formatC(x, format = "f", digits = d, big.mark = ".", decimal.mark = ",")
