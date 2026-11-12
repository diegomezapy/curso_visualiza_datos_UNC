# Sesión 2 · Elección de gráficos según objetivo, audiencia y dato
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U1.
Resumen: Catálogo de gráficos para distribución, cantidad, proporción, relación y tiempo; overplotting y matriz de decisión.

## Objetivos
- Mapear preguntas analíticas a gráficos adecuados.
- Resolver problemas de overplotting, binning y ordenamiento.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 2 · Elección de gráficos según objetivo, audiencia y dato
**Unidad del programa:** U1 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Clasificar preguntas analíticas (distribución, cantidad, proporción, relación, tiempo) y mapearlas a gráficos.
- Reconocer y resolver problemas de *overplotting*, binning y ordenamiento.

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-30 | Repaso y revisión de ejercicios S1 (galería de mejores/peores) |
| 30-90 | **Catálogo de gráficos:** distribuciones, cantidades, proporciones, relaciones, series |
| 90-105 | Pausa |
| 105-190 | **Lab 2** guiado: matriz de decisión aplicada a notas y ventas |
| 190-240 | *Chart clinic*: el grupo critica 3 gráficos voluntarios |

## Trabajo asincrónico
- Lectura: Wilke caps. 5-12 (distribuciones, cantidades, proporciones, relaciones).
- Ejercicio: 5 preguntas de negocio → 5 gráficos justificados.
- Quiz 2.

## Entrega y evaluación
Ejercicio S2 (5 pts, R1) · Quiz 2.

## Laboratorio
[`lab02_eleccion_graficos.py`](lab02_eleccion_graficos.py)

### Pista R (RStudio → RPubs)
[`r/02_eleccion_graficos.Rmd`](../../r/02_eleccion_graficos.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_02_eleccion.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/2).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **Para ver la forma de la distribución de 400 notas conviene…** → Un histograma, ECDF o violín. Son los gráficos diseñados para mostrar forma, centro y dispersión; probá varios anchos de bin.
- **Un diagrama de dispersión con 50 000 puntos sufre principalmente de…** → Overplotting: se tapan puntos; usar transparencia, hexbin o densidad. Con muchos puntos superpuestos se pierde la densidad; transparencia o binning la recuperan.
- **Ranking de categorías con nombres largos:** → Barras horizontales ordenadas. Las barras horizontales dejan espacio a las etiquetas y el orden descendente facilita la lectura.
- **Para mostrar partes de un todo a lo largo del tiempo con muchas categorías:** → Barras apiladas al 100 % o small multiples. Las tortas múltiples obligan a comparar ángulos entre gráficos; las barras apiladas o paneles facilitan la comparación.
- **Las barras pueden empezar en un valor distinto de cero si se anota el eje.** → Falso. En barras la longitud codifica el valor: truncar el eje exagera las diferencias. Para puntos/líneas sí puede justificarse.

## Actividades evaluadas
- Ejercicio S2: 5 preguntas de negocio → 5 gráficos justificados · publicar en RPubs (5 pts)

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Wilke · caps. 5-12 (cantidades, distribuciones, proporciones, relaciones) (libro, en) · https://clauswilke.com/dataviz/ · 
- From Data to Viz · árbol de decisión para elegir el gráfico (web, en) · https://www.data-to-viz.com · 
- Python Graph Gallery · ejemplos con código (web, en) · https://python-graph-gallery.com · 
- The R Graph Gallery · ejemplos con código (web, en) · https://r-graph-gallery.com · 
- Royal Statistical Society · Choosing a visualisation type (PDF) (pdf, en) · https://royal-statistical-society.github.io/datavisguide/docs/choosing.pdf · 
- Posit · Cheatsheet «Data visualization with ggplot2» (PDF) (pdf, en) · https://rstudio.github.io/cheatsheets/data-visualization.pdf · hay traducciones en la galería de cheatsheets de Posit
