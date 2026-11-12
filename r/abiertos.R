# Herramientas para datos abiertos reales (R) · equivalentes a src/cvd/abiertos.py
suppressPackageStartupMessages({ library(jsonlite); library(dplyr); library(tidyr); library(readr); library(purrr); library(tibble); library(lubridate) })
`%||%` <- function(a, b) if (is.null(a) || length(a) == 0 || (length(a) == 1 && is.na(a))) b else a

# Tipo de columna: numérica, categórica, fecha, identificador/texto, latitud, longitud, vacía
tipo_columna <- function(x, nombre = "") {
  nn <- x[!is.na(x)]; n <- length(x); if (!length(nn)) return("vacía")
  if (inherits(x, c("Date", "POSIXct"))) return("fecha")
  if (is.logical(x)) return("categórica")
  if (is.numeric(x)) {
    if (grepl("(^|_)(lat|latitud)($|_)", tolower(nombre))) return("latitud")
    if (grepl("(^|_)(lon|lng|long|longitud)($|_)", tolower(nombre))) return("longitud")
    if (n_distinct(nn) <= 12 && all(nn %% 1 == 0) && n_distinct(nn) / max(n, 1) < .2) return("categórica")
    return("numérica")
  }
  m <- head(as.character(nn), 300)
  if (grepl("fecha|date|periodo|período|dia|día|mes|anio|año", tolower(nombre)) || mean(grepl("^\\d{4}-\\d{2}(-\\d{2})?", m)) > .8 || mean(grepl("^\\d{1,2}/\\d{1,2}/\\d{2,4}", m)) > .8) {
    p <- suppressWarnings(parse_date_time(m, orders = c("Ymd", "dmY", "Y-m"), quiet = TRUE)); if (mean(!is.na(p)) > .85) return("fecha")
  }
  u <- n_distinct(nn); if (u / length(nn) > .9 && u > 30) return("identificador/texto")
  if (u <= max(30, .05 * n)) "categórica" else "identificador/texto"
}
SUGERENCIA <- c("numérica" = "histograma / ECDF; caja o violín por grupo; dispersión", "categórica" = "barras ordenadas (top-N); barras apiladas al 100 %",
  "fecha" = "línea por mes/año; heatmap año×mes", "latitud" = "mapa de puntos", "longitud" = "mapa de puntos", "identificador/texto" = "no graficar directo: contar únicos o duplicados", "vacía" = "descartar")
perfilar <- function(df) tibble(columna = names(df), tipo = map2_chr(df, names(df), tipo_columna), `nulos_%` = round(map_dbl(df, ~ mean(is.na(.x))) * 100, 1),
  unicos = map_int(df, ~ n_distinct(.x, na.rm = TRUE)), ejemplo = map_chr(df, ~ substr(as.character(first(na.omit(.x)) %||% ""), 1, 40))) %>% mutate(`gráfico sugerido` = unname(SUGERENCIA[tipo]))
calidad <- function(df) list(filas = nrow(df), columnas = ncol(df), filas_duplicadas = sum(duplicated(df)), celdas_nulas_pct = round(mean(is.na(df)) * 100, 1),
  columnas_vacias = names(df)[map_lgl(df, ~ all(is.na(.x)))], columnas_constantes = names(df)[map_lgl(df, ~ n_distinct(.x, na.rm = TRUE) == 1)])

# OCDS: una fila por proceso / una fila por adjudicación × proveedor (solo campos estándar; tolera ausentes)
lista_releases <- function(obj) { if (!is.null(obj$releases)) obj$releases else if (!is.null(obj$records)) map(obj$records, ~ .x$compiledRelease) else if (!is.null(obj$ocid)) list(obj) else obj }
ocds_a_tabla <- function(obj) {
  rel <- lista_releases(obj)
  if (!length(rel)) return(tibble(ocid = character(), fecha = as.POSIXct(character()), comprador = character(), titulo = character(), estado = character(), metodo = character(), categoria = character(),
                                   monto_estimado = numeric(), n_oferentes = numeric(), n_adjudicaciones = integer(), monto_adjudicado = numeric()))
  map_dfr(rel, function(r) {
    aw <- r$awards %||% list()
    tibble(ocid = r$ocid %||% NA_character_, fecha = r$date %||% NA_character_, comprador = r$buyer$name %||% NA_character_, titulo = r$tender$title %||% NA_character_, estado = r$tender$status %||% NA_character_,
           metodo = (r$tender$procurementMethodDetails %||% r$tender$procurementMethod) %||% NA_character_, categoria = r$tender$mainProcurementCategory %||% NA_character_,
           monto_estimado = as.numeric(r$tender$value$amount %||% NA), n_oferentes = as.numeric(r$tender$numberOfTenderers %||% NA), n_adjudicaciones = length(aw),
           monto_adjudicado = if (length(aw)) sum(map_dbl(aw, ~ as.numeric(.x$value$amount %||% 0))) else NA_real_)
  }) %>% mutate(fecha = suppressWarnings(as_datetime(fecha)))
}
ocds_adjudicaciones <- function(obj) {
  map_dfr(lista_releases(obj), function(r) map_dfr(r$awards %||% list(), function(a) map_dfr(a$suppliers %||% list(list()), function(s)
    tibble(ocid = r$ocid %||% NA_character_, comprador = r$buyer$name %||% NA_character_, proveedor = s$name %||% NA_character_, monto = as.numeric(a$value$amount %||% NA), fecha = a$date %||% r$date %||% NA_character_))))
}

# Banco Mundial: la API devuelve [metadatos, observaciones]
parsear_banco_mundial <- function(resp) {
  if (!is.list(resp) || length(resp) < 2 || is.null(resp[[2]])) return(tibble(pais = character(), iso3 = character(), anio = integer(), valor = numeric(), indicador = character()))
  d <- resp[[2]]; tibble(pais = d$country$value, iso3 = d$countryiso3code, anio = suppressWarnings(as.integer(d$date)), valor = as.numeric(d$value), indicador = d$indicator$value, codigo = d$indicator$id) %>% arrange(iso3, anio)
}
banco_mundial <- function(indicador, paises = c("PRY", "ARG", "BRA", "URY", "BOL"), desde = 2000, hasta = 2024) {
  url <- sprintf("https://api.worldbank.org/v2/country/%s/indicator/%s?format=json&per_page=20000&date=%d:%d", paste(paises, collapse = ";"), indicador, desde, hasta)
  parsear_banco_mundial(fromJSON(url))
}
