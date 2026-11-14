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
- Estudiar la **presentación** de la unidad (14 diapositivas) y la **infografía** «La ciencia de la percepción gráfica» (en el aula, sesión 1).
- Quiz 1 (15 min, en plataforma) y **Quiz 1B** (10 preguntas: evalúa la lectura y el estudio de la presentación).

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

## Texto de la presentación de la unidad (Ciencia de la percepción gráfica)
### Diapositiva 1 · Módulo de Visualización de Datos
- Sesiones 1-3: La Ciencia de la Percepción Gráfica
- MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS
### Diapositiva 2 · Arquitectura del Módulo
- 1-3
- Sesiones 1-3
- Principios de percepción, elección y ética.
- 4-6
- Sesiones 4-6
- Visual Analytics y Dashboards.
- Sesión 7
- Estructuras complejas.
- Sesión 8
- Redes.
- Antes de construir dashboards automatizados, debemos entender el hardware en el que se procesan: el cerebro humano.
### Diapositiva 3 · El Paradigma de Codificación y Decodificación
- Sistema / Diseñador
- Datos estructurados
- Mapeo visual
- Gráfico
- Usuario / Cerebro
- Detección óptica
- Ensamblaje
- Estimación del valor
- El objetivo de la visualización no es mostrar decimales exactos, sino maximizar la precisión de la decodificación visual.
### Diapositiva 4 · Velocidad de Procesamiento y Memoria Icónica
- Lado A: Búsqueda tabular (secuencial)
- Lado B: Detección instantánea (preatencional)
- Cuadrícula de números, lectura elemento por elemento
- Señal por elemento, unidades ilustrativas
- El procesamiento preatencional aprovecha la mitad de la corteza cerebral dedicada a la visión. Los datos deben saltar a la vista, no ser leídos.
- < 250 ms
### Diapositiva 5 · El Arsenal Preatencional
- 1. Forma
- 2. Color
- 3. Posición espacial
- 4. Movimiento / orientación
- Advertencia técnica: el abuso de estos atributos destruye su eficiencia. Si todo resalta, nada resalta.
### Diapositiva 6 · Ensamblaje Visual: Las Leyes de Gestalt
- Proximidad
- Similitud
- Conexión
- Cerramiento
- Jerarquía de fuerza perceptual: Conexión y Cerramiento vencen a Proximidad y Similitud.
### Diapositiva 7 · La Jerarquía de la Percepción Gráfica
- Mayor a menor precisión
- (Cleveland & McGill)
- 1. Posición en escala común
- 2. Posición en escalas no alineadas
- 3. Longitud, dirección, ángulo
- 4. Área
- 5. Volumen, curvatura
- 6. Sombreado, saturación de color
- El Principio de Oro: todo gráfico debe emplear las tareas elementales más altas posibles en esta jerarquía matemática.
### Diapositiva 8 · Distorsión Perceptual: Ángulo y Área vs. Posición
- Baja precisión de decodificación
- Alta precisión de decodificación
- Participación por categoría, ángulo de cada sector
- Participación por categoría, longitud de cada barra
- Nuestro cerebro juzga distancias lineales casi perfectamente, pero distorsiona sistemáticamente áreas (2D) y volúmenes (3D) debido a su crecimiento exponencial.
### Diapositiva 9 · Innovación en Precisión: El Rectángulo Enmarcado
- Paso 1: Barras flotantes
- Paso 2: Ley de Weber aplicada
- ?
- Al agregar un marco, el espacio vacío se convierte en un nuevo dato comparativo.
- La Ley de Weber demuestra que contrastar las áreas no llenas aumenta exponencialmente la precisión.
### Diapositiva 10 · Los 3 Pilares del Mapeo: Tipología del Dato
- Naturaleza matemática del dato
- Cuantitativos
- (Ratio / Intervalo)
- Operaciones aritméticas completas.
- Cualitativos ordinales
- Clasificación con orden inherente, distancia indeterminada.
- Cualitativos nominales
- Categorías sin orden jerárquico.
- No existe el «gráfico correcto» sin antes definir matemáticamente la naturaleza del dato subyacente.
- Ej: Costo ($), Tiempo (Años)
- Ej: Tallas, Posiciones (1°, 2°, 3°)
- Ej: Marcas, Países, Departamentos
### Diapositiva 11 · Matriz de Decisión para Mapeo Visual
- Tipo de dato
- Mejor atributo visual
- Gráfico recomendado
- Antipatrón (evitar)
- Cuantitativo
- Posición / Longitud
- Barras, scatter plots, líneas
- Volumen y 3D
- Ordinal
- Sombreado / Densidad
- Barras ordenadas, heatmaps
- Colores arcoíris inconexos
- Nominal
- Forma / Tono
- Dot plots, barras categóricas
- Líneas de tendencia conectadas
- Magnitudes requieren posición; secuencias requieren intensidad; categorías requieren forma o tono.
### Diapositiva 12 · Integridad y Ética Visual
- Error 1: eje Y truncado
- Error 2: volumen 3D injustificado
- Valor por ítem, eje desde 50
- Participación por categoría, %
- Exagera engañosamente diferencias minúsculas: 52 frente a 51 parece el doble.
- Infla las proporciones frontales y oculta la matemática real.
- La ética exige transparencia absoluta. Truncar escalas de magnitud o utilizar distorsión 3D no es una elección estética, es una mentira estadística.
### Diapositiva 13 · Aplicación Estructural: El Dashboard Analítico
- KPI 1
- — — —
- KPI 2
- — — —
- KPI 3
- — — —
- Tendencias sparkline
- Bullet charts: rendimiento vs meta
- KPIs numéricos: reducen el esfuerzo cognitivo inmediato (memoria icónica).
- Sparklines: explotan la ley de Gestalt de Conexión para mostrar tendencias.
- Bullet charts: utilizan la posición en escala común (nivel 1 de precisión).
- Un dashboard no es una colección de gráficos; es una interfaz de toma de decisiones basada en la ingeniería de la percepción visual.
### Diapositiva 14 · El Código del Diseñador Analítico
- MAPEO
- Conoce la naturaleza matemática de tu dato (nominal, ordinal, cuantitativo).
- PRECISIÓN
- Prioriza implacablemente la posición espacial y la longitud (Cleveland & McGill).
- ATENCIÓN
- Reserva el color divergente y la forma solo para alertas preatencionales.
- ÉTICA
- Rechaza el 3D, el volumen injustificado y los ejes truncados.
- La visualización es la interfaz final y crítica entre tu modelo de machine learning y la mente humana.

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Wilke, Fundamentals of Data Visualization (libro abierto) · caps. 1-4 (libro, en) · https://clauswilke.com/dataviz/ · gratuito en línea
- Cleveland & McGill (1984), Graphical Perception · JASA 79(387) (artículo, en) · https://doi.org/10.2307/2288400 · artículo clásico sobre percepción
- UOC · Guía de lecturas en el ámbito de la visualización de datos (PDF) (pdf, es) · https://openaccess.uoc.edu/bitstream/10609/101188/6/Gu%c3%ada%20de%20lecturas%20en%20el%20%c3%a1mbito%20de%20la%20visualizaci%c3%b3n%20de%20datos.pdf · acceso abierto
- Cairo · «Cómo mienten los gráficos»: resumen de la introducción (PDF) (pdf, es) · https://knightcenter.utexas.edu/JC/courses/DATA0819/Esp/%e2%80%9cC%c3%b3mo%20mienten%20los%20gr%c3%a1ficos%e2%80%9d%20de%20Alberto%20Cairo%20-%20Resumen%20por%20Adriano%20Belis%c3%a1rio,%20traducci%c3%b3n%20de%20Paulette%20Desormeaux.pdf · Knight Center · resumen
- R para Ciencia de Datos · cap. 3: Visualización de datos (libro, es) · https://es.r4ds.hadley.nz/03-visualize.html · gratuito en línea
