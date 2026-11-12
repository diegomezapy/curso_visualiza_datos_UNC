# Genera los 8 HTML en r/salidas/ (útil para revisar todo de una vez).  Rscript r/render_todo.R
setwd(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))
dir.create("salidas", showWarnings = FALSE)
for (f in sort(list.files(pattern = "^(0[0-8]|pr0[0-9]).*\\.Rmd$"))) {
  cat("→", f, "\n"); rmarkdown::render(f, output_dir = "salidas", quiet = TRUE)
}
