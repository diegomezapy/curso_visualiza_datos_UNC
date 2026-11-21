# Genera los 8 HTML en r/salidas/ (útil para revisar todo de una vez).  Rscript r/render_todo.R
setwd(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))
dir.create("salidas", showWarnings = FALSE)
# El ejercicio de la EPHC (~100 MB del INE) y el tablero de aduanas (Python con reticulate) se renderizan aparte.
for (f in setdiff(sort(list.files(pattern = "^(0[0-8]|pr0[0-9]).*\\.Rmd$")), c("04_ejercicio_ephc_concepcion.Rmd", "05_tablero_aduanas_python.Rmd"))) {
  cat("→", f, "\n"); rmarkdown::render(f, output_dir = "salidas", quiet = TRUE)
}
