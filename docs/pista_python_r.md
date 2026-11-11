# Cómo se trabaja: Python en Colab + R en RStudio (RPubs)

El curso usa **dos lenguajes complementarios**, con los mismos datos y los mismos objetivos de aprendizaje en cada sesión:

| | **Python · Google Colab** | **R · RStudio → RPubs** |
|---|---|---|
| Rol en el curso | Laboratorios de análisis, visualización y automatización | Informes reproducibles que se **publican en la web** y se entregan como enlace |
| Dónde | Colab (navegador, sin instalar) | RStudio Desktop (instalación local) |
| Archivos | `sesiones/*/labXX_*.py` → notebooks `.ipynb` | `r/0X_*.Rmd` |
| Librerías | pandas, matplotlib, seaborn, plotly, scikit-learn, networkx | ggplot2, dplyr, plotly, crosstalk, DT, igraph |
| Entrega | Enlace de Colab compartido (*Lector*) | Enlace de **RPubs** |

## Qué se entrega en cada actividad
| Actividad | Puntos | Entrega |
|---|---|---|
| Ejercicios S1, S2, S3 y S6 | 5 c/u | **RPubs** |
| Mini-proyecto 1 | 10 | **RPubs** |
| Mini-proyecto 2 | 10 | **RPubs** (tablero plotly/crosstalk) + **Colab** (versión Python) |
| Mini-proyecto 3 | 10 | **RPubs** + **Colab** |
| Integrador | 20 | Informe en **RPubs** + notebook reproducible en **Colab** |
| Ejercicio de redes (opcional) | +3 | **RPubs** |

Los enlaces se pegan en cada actividad del **aula virtual**; el docente los ve en su panel.

## Puesta en marcha
1. **Colab:** botón *Python · Laboratorio en Google Colab* de cada sesión → *Entorno de ejecución → Ejecutar todas*.
2. **R:** instalar R y RStudio; abrir `r/01_percepcion.Rmd`; ejecutar antes `r/instalar_paquetes.R`; **Knit**.
3. **RPubs:** cuenta gratuita en <https://rpubs.com> → en la vista previa, **Publish → RPubs** → copiar el enlace.

Guía ilustrada en PDF: `materiales/pdf/00_guia_inicio.pdf`.

## Notas importantes
- **RPubs es público y estático.** No publicar datos personales (cédulas, nombres de terceros) ni información confidencial.
- Shiny **no** funciona en RPubs (necesita servidor). Para tableros interactivos publicables en RPubs se usan **plotly + crosstalk + DT** (los filtros se ejecutan en el navegador).
- Los `.Rmd` leen los datos desde `datos/` si trabajan dentro del repositorio; si no, los descargan de GitHub automáticamente.
- Cada `.Rmd` tiene `author: "Tu nombre y apellido"`: cambiarlo antes de publicar.

## Equivalencias rápidas
| Tarea | Python | R |
|---|---|---|
| Leer CSV | `pd.read_csv()` | `readr::read_csv()` |
| Agrupar y resumir | `df.groupby().agg()` | `group_by() %>% summarise()` |
| Gráfico de barras | `ax.barh()` | `geom_col()` |
| Paneles pequeños | `plt.subplots()` | `facet_wrap()` |
| Gráfico interactivo | `plotly.express` | `plotly::plot_ly()` |
| Informe parametrizado | Jinja2 / papermill / Quarto | R Markdown `params:` |
| Redes | `networkx` | `igraph` |
