# Instala los paquetes de R usados en el curso (ejecutar una sola vez en RStudio)
paquetes <- c("rmarkdown", "knitr", "ggplot2", "dplyr", "tidyr", "readr", "scales", "lubridate", "patchwork",
              "plotly", "crosstalk", "DT", "igraph", "Rtsne", "ggrepel", "viridis", "hexbin", "rsconnect")
faltan <- setdiff(paquetes, rownames(installed.packages()))
if (length(faltan)) install.packages(faltan)
cat("Listo. Paquetes instalados:", length(paquetes) - length(faltan), "ya estaban;", length(faltan), "nuevos.\n")
