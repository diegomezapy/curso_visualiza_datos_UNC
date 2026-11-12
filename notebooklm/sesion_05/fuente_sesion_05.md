# Sesión 5 · Dashboards interactivos
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U2.
Resumen: Jerarquía y filtros con propósito; Plotly (HTML interactivo) y Dash (callbacks).

## Objetivos
- Diseñar la jerarquía y los filtros de un tablero según la audiencia.
- Implementar interacción con propósito en Plotly y opcionalmente Dash.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 5 · Dashboards interactivos
**Unidad del programa:** U2 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Diseñar la jerarquía y los filtros de un tablero según la audiencia.
- Implementar interacción con propósito en Plotly (y opcionalmente Dash).

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-40 | Revisión de MP1 (galería y retroalimentación con rúbrica R2) |
| 40-90 | Principios de diseño de dashboards; mantra de Shneiderman; anti-patrones |
| 90-105 | Pausa |
| 105-190 | **Lab 5** (Plotly) + demo de `app_dash.py` con callbacks |
| 190-240 | Planificación del **Mini-proyecto 2** |

## Trabajo asincrónico
- Lectura: Few (2013), capítulos sobre errores y principios de diseño; documentación de Plotly y Dash.
- **Mini-proyecto 2:** extender el dashboard (filtro de año + heatmap/mapa + insight dinámico).
- Quiz 5.

## Entrega y evaluación
**Mini-proyecto 2** (10 pts, R2) · Quiz 5.

## Laboratorio
[`lab05_dashboards_plotly.py`](lab05_dashboards_plotly.py) · [`app_dash.py`](app_dash.py)

### Pista R (RStudio → RPubs)
[`r/05_dashboards_interactivos.Rmd`](../../r/05_dashboards_interactivos.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_05_dashboards.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/5).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **El mantra de Shneiderman para visualización interactiva es…** → Overview first, zoom and filter, then details on demand. Primero visión general, luego filtrar/acercar y finalmente detalles bajo demanda.
- **¿Dónde conviene ubicar los KPIs principales de un dashboard?** → Arriba a la izquierda, en la zona de mayor atención. En culturas de lectura izquierda-derecha y arriba-abajo esa es la zona que se ve primero.
- **Un filtro global debe…** → Afectar de forma coherente y visible a todas las vistas indicadas. Si el usuario no sabe qué afecta el filtro, el tablero se vuelve engañoso.
- **Una interacción 'decorativa' es aquella que…** → No ayuda a responder la pregunta de la audiencia. La interacción debe servir a la tarea: filtrar, comparar, detallar.
- **Un objetivo razonable de rendimiento para un tablero web es…** → Cargar en menos de 3 segundos agregando o precalculando datos. Una carga lenta hace que los usuarios abandonen; conviene agregar y precalcular.

## Actividades evaluadas
- Mini-proyecto 2: dashboard con filtro de año + heatmap/mapa + insight · RPubs (R) + Colab (Python) (10 pts)

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Plotly para Python · documentación (web, en) · https://plotly.com/python/ · 
- Dash · documentación (web, en) · https://dash.plotly.com/ · 
- crosstalk · filtros interactivos para HTML estático (R) (web, en) · https://rstudio.github.io/crosstalk/ · funciona en RPubs
- Shiny · documentación (web, en) · https://shiny.posit.co/ · requiere servidor
