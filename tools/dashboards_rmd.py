"""Genera r/05_tablero_aduanas_python.Rmd (RStudio + reticulate: chunks de Python) con el MISMO código de las diapositivas (dashboards_spec.py)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import dashboards_spec as S
RAIZ = Path(__file__).resolve().parents[1]
sin = lambda ls: [l[1:] if l.startswith("§") else l for l in ls]
def chunk(nombre, lineas, asis=False):
    return "```{python %s%s}\n%s\n```\n" % (nombre, ", results='asis'" if asis else "", "\n".join(lineas))
def mostrar(): return ['print(fig.to_html(include_plotlyjs="cdn", full_html=False))']
T = {f["id"]: f for f in S.FIGS}
partes = ['''---
title: "Sesión 5 · Tablero de aduanas con Python en RStudio"
subtitle: "Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET – UNC"
author: "Tu nombre y apellido"
date: "`r format(Sys.Date(), '%d/%m/%Y')`"
output:
  html_document:
    toc: true
    toc_float: true
    code_folding: show
    theme: flatly
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = FALSE)
# Python dentro de RStudio con reticulate. La primera vez (en la consola):
#   install.packages("reticulate"); reticulate::virtualenv_create("r-viz")
#   reticulate::py_install(c("pandas", "plotly"), "r-viz")
library(reticulate)
use_virtualenv("r-viz", required = FALSE)
# Los datos agregados están en el repositorio del curso; se descargan si no existen.
base <- "https://raw.githubusercontent.com/diegomezapy/curso_visualiza_datos_UNC/main/aula/media/unidad5_dashboards/fuentes/datos/"
for (f in c("cubo_importaciones.csv", "subitems_muestra.csv"))
  if (!file.exists(f)) download.file(paste0(base, f), f, quiet = TRUE, mode = "wb")
```

> **Objetivo.** Construir, con **Python** (pandas + plotly) ejecutado desde **RStudio**, un tablero sobre las **importaciones de electrónica 2024–2025** (base de datos abiertos de aduanas, DNIT). Es el mismo código de la presentación de la sesión 5. Al final: *Knit → Publish → RPubs* (los filtros de plotly funcionan en el navegador, sin servidor).

# 1. Los datos

La base original de la DNIT usa **punto y coma** (`;`) como separador y **coma decimal**. Acá trabajamos con una versión **agregada** (año, mes, aduana, país, medio de transporte). Un detalle importante: cada fila de la base original es un **subítem** y repite el valor del ítem.

''', chunk("datos", S.SETUP), '''
```{python}
cubo.head()
```

# 2. Antes del tablero: validar el dato

La muestra `subitems_muestra.csv` conserva las filas de 300 despachos tal como vienen en la base.

''', chunk("trampa", ['sub = pd.read_csv("subitems_muestra.csv")'] + sin(T["k0"]["codigo"]), False), chunk("trampa_fig", mostrar(), True),
'''
**Pregunta:** ¿por cuánto se multiplica el valor si se suman todas las filas? ¿Por qué ocurre?

# 3. KPI y tendencia

''', chunk("kpi", sin(T["k1"]["codigo"])), chunk("kpi_fig", mostrar(), True), chunk("tendencia", sin(T["l1"]["codigo"])), chunk("tendencia_fig", mostrar(), True),
'''
# 4. Comparaciones y composición

''', chunk("ranking", sin(T["b1"]["codigo"])), chunk("ranking_fig", mostrar(), True), chunk("treemap", sin(T["t1"]["codigo"])), chunk("treemap_fig", mostrar(), True), chunk("calor", sin(T["h1"]["codigo"])), chunk("calor_fig", mostrar(), True),
'''
# 5. El tablero corregido y la interacción

''', chunk("tablero", sin(T["d1"]["codigo"])), chunk("tablero_fig", mostrar(), True), chunk("filtro", sin(T["i1"]["codigo"])), chunk("filtro_fig", mostrar(), True),
'''
# 6. Para entregar (Mini-proyecto 2)

1. Agregá un **filtro de año** al tablero y un indicador nuevo (por ejemplo, **USD por kilo neto**: necesitás la columna `kilo_neto` del cubo).
2. Escribí un **título que enuncie el mensaje** del tablero y una nota sobre las limitaciones (período, junio de 2025 ausente, deduplicación).
3. Aplicá el checklist de calidad de la presentación y comentá en 100 palabras qué cambiaste.
4. *Knit* y publicá en **RPubs**; pegá el enlace en el aula.
''']
(RAIZ / "r" / "05_tablero_aduanas_python.Rmd").write_text("".join(partes), encoding="utf-8")
print("escrito r/05_tablero_aduanas_python.Rmd")
