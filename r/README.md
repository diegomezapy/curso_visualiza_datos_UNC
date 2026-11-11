# Pista R · RStudio → RPubs

Ocho documentos R Markdown (uno por sesión) equivalentes a los laboratorios de Python, pensados para **publicarse en RPubs**.

| Sesión | Documento | Temas |
|---|---|---|
| 1 | `01_percepcion.Rmd` | Anscombe, jerarquía perceptiva, preatentivos |
| 2 | `02_eleccion_graficos.Rmd` | distribuciones, ranking, overplotting, matriz de decisión |
| 3 | `03_color_diseno_etica.Rmd` | paletas, anotación, galería de engaños |
| 4 | `04_kpis_storytelling.Rmd` | KPIs, small multiples, contribución al cambio |
| 5 | `05_dashboards_interactivos.Rmd` | plotly + crosstalk + DT (sin servidor) |
| 6 | `06_reporting_automatizado.Rmd` + `plantilla_reporte_sucursal.Rmd` | informes parametrizados |
| 7 | `07_estructuras_complejas.Rmd` | PCA, t-SNE, series, mapa |
| 8 | `08_redes.Rmd` | igraph, centralidad, matriz de adyacencia |

## Uso
```r
source("r/instalar_paquetes.R")          # una sola vez
rmarkdown::render("r/01_percepcion.Rmd") # o botón Knit en RStudio
```
Para generar todos: `Rscript r/render_todo.R`. Publicar: **Publish → RPubs** en la vista previa (ver `docs/pista_python_r.md`).

Probado con R 4.3 y ggplot2 3.4: los 8 documentos compilan.
