# Sesión 1 · Principios de visualización: percepción
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U1.
Resumen: Por qué visualizar (Anscombe), jerarquía perceptiva de Cleveland-McGill, atributos preatentivos y Gestalt.

## Objetivos
- Explicar por qué visualizar y qué propiedades perceptivas condicionan la lectura de un gráfico.
- Aplicar la jerarquía de Cleveland-McGill y atributos preatentivos para guiar la mirada.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 1 · Principios de visualización: percepción
**Unidad del programa:** U1 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Explicar por qué visualizar (Anscombe) y qué propiedades perceptivas condicionan la lectura de un gráfico.
- Aplicar la jerarquía de Cleveland-McGill y atributos preatentivos para guiar la mirada.

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-20 | Presentación del curso, criterios de evaluación y herramientas |
| 20-60 | **Exposición:** ¿Para qué visualizar? Anscombe, Datasaurus, historia (Minard, Nightingale, Snow) |
| 60-105 | **Percepción:** posición > longitud > ángulo > área > color; preatentivos; Gestalt |
| 105-120 | Pausa |
| 120-190 | **Lab 1** guiado + dinámica de cronometraje (¿qué gráfico se lee más rápido?) |
| 190-240 | Discusión del ejercicio asincrónico y dudas |

## Trabajo asincrónico
- Lectura: Cairo (2011), capítulos introductorios; Wilke (2019) caps. 1-4 y 26.
- Ejercicio: rehacer un gráfico de prensa (antes/después + 5 líneas de justificación).
- Quiz 1 (15 min, en plataforma).

## Entrega y evaluación
Ejercicio S1 (5 pts, rúbrica R1) · Quiz 1 (teoría).

## Laboratorio
[`lab01_percepcion.py`](lab01_percepcion.py) — Anscombe, jerarquía perceptiva, color de énfasis.

### Pista R (RStudio → RPubs)
[`r/01_percepcion.Rmd`](../../r/01_percepcion.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_01_percepcion.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/1).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **Según Cleveland y McGill, ¿qué codificación visual se decodifica con mayor precisión?** → Posición sobre una escala común. La posición sobre una escala común es la tarea perceptiva más precisa; luego longitud, ángulo/pendiente, área y color.
- **El cuarteto de Anscombe demuestra que…** → Estadísticos resumen idénticos pueden ocultar estructuras muy distintas. Los cuatro datasets comparten media, varianza, correlación y recta, pero al graficarlos se ven totalmente diferentes.
- **Un atributo preatentivo es aquel que…** → El sistema visual detecta rápidamente sin búsqueda serial. Color de énfasis, tamaño u orientación se detectan en menos de ~250 ms, por eso sirven para guiar la mirada.
- **El 'data-ink ratio' de Tufte propone…** → Maximizar la proporción de tinta que representa datos. Se trata de quitar la tinta que no informa (no de eliminar todo): borrar el ruido para que destaque el dato.
- **Para comparar 8 categorías con valores similares, ¿qué gráfico es más adecuado?** → Barras ordenadas. Las barras usan longitud/posición (más precisas) y el orden facilita el ranking; la torta usa ángulo/área.

## Actividades evaluadas
- Actividad 0 · Responder el diagnóstico inicial (10–15 min, anónimo y sin nota) (0 pts)
- Actividad 0b · Del dato a la visualización: publicá tu análisis de los resultados del diagnóstico · RPubs (R) + Colab (Python) (0 pts)
- Ejercicio S1: rehacer un gráfico de prensa (antes/después + 5 líneas) · publicar en RPubs (5 pts)

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Wilke, Fundamentals of Data Visualization (libro abierto) · caps. 1-4 (libro, en) · https://clauswilke.com/dataviz/ · gratuito en línea
- Cleveland & McGill (1984), Graphical Perception · JASA 79(387) (artículo, en) · https://doi.org/10.2307/2288400 · artículo clásico sobre percepción
- UOC · Guía de lecturas en el ámbito de la visualización de datos (PDF) (pdf, es) · https://openaccess.uoc.edu/bitstream/10609/101188/6/Gu%c3%ada%20de%20lecturas%20en%20el%20%c3%a1mbito%20de%20la%20visualizaci%c3%b3n%20de%20datos.pdf · acceso abierto
- Cairo · «Cómo mienten los gráficos»: resumen de la introducción (PDF) (pdf, es) · https://knightcenter.utexas.edu/JC/courses/DATA0819/Esp/%e2%80%9cC%c3%b3mo%20mienten%20los%20gr%c3%a1ficos%e2%80%9d%20de%20Alberto%20Cairo%20-%20Resumen%20por%20Adriano%20Belis%c3%a1rio,%20traducci%c3%b3n%20de%20Paulette%20Desormeaux.pdf · Knight Center · resumen
- R para Ciencia de Datos · cap. 3: Visualización de datos (libro, es) · https://es.r4ds.hadley.nz/03-visualize.html · gratuito en línea
