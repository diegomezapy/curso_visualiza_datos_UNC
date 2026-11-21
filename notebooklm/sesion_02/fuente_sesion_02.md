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

## Texto de la presentación de la sesión (Elección de gráficos)
### Diapositiva 1 · MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC
- Elección de gráficos según objetivo, audiencia y dato
- Cinco preguntas, cinco familias de gráficos; ejemplos reales de la Encuesta Permanente de Hogares Continua (INE)
- Sesión 2 · Unidad 1 · Fundamentos de la visualización
### Diapositiva 2 · Antes de elegir un gráfico: tres preguntas
- Punto de partida
- Objetivo
- ¿Qué quiero que el lector haga o entienda?
- Comparar, ver una distribución, seguir una evolución, descubrir una relación, mostrar una composición.
- Audiencia
- ¿Quién lo va a leer y cuánto tiempo tiene?
- Un equipo técnico tolera un boxplot; un directivo necesita un mensaje y un gráfico simple.
- Dato
- ¿Qué tipo de variables tengo y cuántas observaciones?
- Categórica, numérica, temporal; pocas o millones de filas; una o varias series.
- Primero la pregunta; después el gráfico. Un mismo dato admite muchos gráficos, pero solo algunos responden la pregunta.
- Resumen de la matriz de decisión: objetivo + audiencia + dato → gráfico.
### Diapositiva 3 · Cinco tareas, cinco familias de gráficos
- Mapa de la sesión
- Tarea
- Pregunta con la EPHC
- Gráfico adecuado
- Cuidado con…
- Distribución
- ¿Cómo se reparten los ingresos?
- Histograma, densidad, boxplot
- Ancho de bins, escala, atípicos
- Cantidad
- ¿Qué departamento tiene mayor ingreso mediano?
- Barras ordenadas
- Nombres largos, orden alfabético
- Proporción
- ¿Qué parte de la población está ocupada, desocupada, inactiva?
- Barras apiladas al 100 %
- Tortas con muchas partes
- Relación
- ¿Cómo se relacionan educación e ingreso?
- Dispersión, bin2d, tendencia
- Overplotting, causalidad
- Tiempo
- ¿Cómo cambió la tasa de ocupación 2022–2025?
- Líneas con etiquetas directas
- Ejes truncados en barras
- Cada fila se desarrolla en las siguientes diapositivas: primero el gráfico que no funciona, después el que sí.
- Todos los ejemplos usan el microdato público de la EPHC anual 2022–2025 del INE.
### Diapositiva 4 · Elegir bien: qué tarea perceptiva le pedimos al lector
- Fundamento
- Posición en una escala común
- Posición en escalas no alineadas
- Longitud
- Ángulo y pendiente
- Área
- Volumen, color y saturación
- Más preciso ↑
- Barras, puntos y líneas se leen con posición y longitud.
- Menos preciso ↓
- ▸ Por eso comparamos con barras ordenadas antes que con tortas, y mostramos la tendencia con líneas.
- Cleveland, W. y McGill, R. (1984). Graphical perception. Journal of the American Statistical Association.
### Diapositiva 5 · Distribución: el histograma con la configuración por defecto engaña
- Distribución · 1 de 3
- ggplot(eph, aes(x = ingreso)) +
- geom_histogram(fill = "#0072B2") +
- scale_x_continuous(
- labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- labs(title = "Ingreso mensual de los ocupados",
- x = "Guaraníes", y = "Personas (muestra)") +
- theme_minimal(base_size = 11)
- ▸ Pregunta: ¿cómo se distribuyen los ingresos? Tarea: distribución de una variable numérica.
- ▸ La mayoría de las barras se amontona a la izquierda: unos pocos ingresos enormes estiran el eje.
- ▸ geom_histogram() usa 30 intervalos por defecto; sin mirar la escala, el gráfico casi no informa.
- Una distribución muy asimétrica necesita otra escala: el histograma por defecto esconde lo que importa.
- Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos
### Diapositiva 6 · Con escala logarítmica y bins explícitos, la forma aparece
- Distribución · 2 de 3
- ggplot(eph, aes(x = ingreso)) +
- geom_histogram(bins = 40, fill = "#0072B2") +
- scale_x_log10(
- labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- labs(title = "Ingreso mensual de los ocupados",
- x = "Guaraníes (escala logarítmica)",
- y = "Personas (muestra)") +
- theme_minimal(base_size = 11)
- ▸ scale_x_log10(): cada marca del eje multiplica el valor por 10; las diferencias proporcionales pasan a ser iguales.
- ▸ bins = 40 fija la cantidad de intervalos: probá 15, 40 y 100 y compará la forma.
- ▸ Ahora se distingue la concentración alrededor de 2–3 millones y la cola de ingresos altos.
- Elegir el ancho de los intervalos y la escala es parte del análisis, no un detalle estético.
- Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos
### Diapositiva 7 · Comparar distribuciones entre grupos: diagrama de cajas
- Distribución · 3 de 3
- ggplot(eph, aes(x = area, y = ingreso,
- fill = sexo)) +
- geom_boxplot(outlier.alpha = 0.2) +
- scale_y_log10(
- labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- scale_fill_manual(values = c(Hombres = "#0072B2",
- Mujeres = "#D55E00")) +
- labs(title = "Ingreso por área y sexo",
- x = NULL, y = "Guaraníes (escala log)",
- fill = NULL) +
- theme_minimal(base_size = 11)
- ▸ Para comparar varias distribuciones a la vez, el diagrama de cajas resume mediana, cuartiles y valores atípicos.
- ▸ La caja contiene el 50 % central; la línea es la mediana; los puntos son atípicos.
- ▸ Se compara posición (mediana) entre grupos: la tarea perceptiva más precisa.
- Una caja por grupo permite comparar medianas y dispersión sin dibujar cientos de barras.
- Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos
### Diapositiva 8 · Cantidad: barras verticales con nombres largos
- Cantidad · 1 de 2
- ggplot(dptos, aes(x = dpto, y = ingreso_mediano)) +
- geom_col(fill = "#0072B2") +
- labs(title = "Ingreso mediano por departamento",
- x = NULL, y = "Guaraníes") +
- theme_minimal(base_size = 11)
- ▸ Pregunta: ¿cómo se comparan los 16 departamentos? Tarea: cantidad por categoría.
- ▸ Los nombres largos se superponen y el orden es alfabético, que no significa nada para el lector.
- ▸ Para comparar, el lector necesita ver el ranking.
- Barras desordenadas obligan a buscar: el orden alfabético solo sirve para consultar, no para comparar.
- Fuente: INE, EPHC anual 2025 · estimaciones con factor de expansión
### Diapositiva 9 · Barras horizontales, ordenadas y con el foco en Concepción
- Cantidad · 2 de 2
- dptos |>
- mutate(foco = dpto == "Concepción") |>
- ggplot(aes(x = ingreso_mediano,
- y = forcats::fct_reorder(dpto, ingreso_mediano),
- fill = foco)) +
- geom_col(show.legend = FALSE) +
- scale_fill_manual(values = c("FALSE" = "#9FB6CB",
- "TRUE" = "#D55E00")) +
- scale_x_continuous(labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- labs(title = "Ingreso mediano por departamento",
- x = "Guaraníes", y = NULL) +
- theme_minimal(base_size = 11)
- ▸ Con las categorías en el eje y, los nombres se leen sin girar la cabeza.
- ▸ forcats::fct_reorder() ordena las categorías por el valor, no alfabéticamente.
- ▸ Un solo color de énfasis (#D55E00) guía la mirada hacia el departamento de interés.
- Ordená por valor, poné las categorías en el eje y y resaltá una sola cosa: así se lee el ranking.
- Fuente: INE, EPHC anual 2025 · estimaciones con factor de expansión
### Diapositiva 10 · Proporciones: el gráfico de torta no ayuda a comparar
- Proporción · 1 de 2
- ggplot(compo, aes(x = "", y = personas,
- fill = situacion)) +
- geom_col(position = "fill", width = 1) +
- coord_polar(theta = "y") +
- facet_wrap(~ area) +
- scale_fill_manual(values = colores) +
- labs(title = "Situación de ocupación, 2025",
- fill = NULL) +
- theme_void(base_size = 11)
- ▸ Pregunta: ¿qué proporción está ocupada, desocupada o inactiva en cada área? Tarea: proporción de un todo.
- ▸ coord_polar() convierte las barras en una torta: se compara ángulo y área, que son menos precisos.
- ▸ Comparar el tamaño de «Desocupado» entre las dos tortas es casi imposible.
- Con pocas categorías y un solo todo la torta puede servir; para comparar entre grupos, no.
- Fuente: INE, EPHC anual 2025 · estimaciones con factor de expansión
### Diapositiva 11 · Barras apiladas al 100 %: mismas proporciones, comparación posible
- Proporción · 2 de 2
- ggplot(compo, aes(x = area, y = personas,
- fill = situacion)) +
- geom_col(position = "fill") +
- scale_y_continuous(
- labels = scales::label_percent()) +
- scale_fill_manual(values = colores) +
- coord_flip() +
- labs(title = "Situación de ocupación, 2025",
- x = NULL, y = "Porcentaje de la población de 15+",
- fill = NULL) +
- theme_minimal(base_size = 11)
- ▸ position = "fill" apila las barras y las lleva al 100 %: se comparan longitudes sobre una base común.
- ▸ La barra de abajo y la de arriba parten de la misma base: se compara con claridad que la desocupación es menor en el área rural (2,3 % frente a 3,8 %).
- ▸ Si el mensaje es una sola categoría, conviene una barra por grupo y esa categoría sola.
- Mismas cifras, mejor tarea perceptiva: posición y longitud antes que ángulo.
- Fuente: INE, EPHC anual 2025 · estimaciones con factor de expansión
### Diapositiva 12 · Relación entre dos variables: el diagrama de dispersión básico
- Relación · 1 de 4
- ggplot(eph, aes(x = anios_est, y = ingreso)) +
- geom_point() +
- scale_y_continuous(
- labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- labs(title = "Educación e ingreso",
- x = "Años de estudio", y = "Guaraníes") +
- theme_minimal(base_size = 11)
- ▸ Pregunta: ¿los ingresos crecen con la educación? Tarea: relación entre dos variables numéricas.
- ▸ Con 6.000 puntos aparece el overplotting: los puntos se tapan entre sí y la densidad se pierde.
- ▸ Además, los años de estudio son enteros: los puntos forman columnas.
- Cuando los puntos se superponen, el gráfico muestra dónde hay datos pero no cuántos.
- Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos
### Diapositiva 13 · Transparencia, jitter y escala log reducen el overplotting
- Relación · 2 de 4
- ggplot(eph, aes(x = anios_est, y = ingreso)) +
- geom_jitter(width = 0.3, height = 0,
- alpha = 0.15, size = 1,
- color = "#0072B2") +
- scale_y_log10(
- labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- labs(title = "Educación e ingreso",
- x = "Años de estudio",
- y = "Guaraníes (escala log)") +
- theme_minimal(base_size = 11)
- ▸ alpha = 0.15 vuelve los puntos translúcidos: donde hay más, el color se oscurece.
- ▸ geom_jitter(width = 0.3) separa horizontalmente los puntos que comparten un valor entero.
- ▸ scale_y_log10() abre la zona densa donde se concentran los ingresos.
- Transparencia + jitter + escala adecuada: tres ajustes pequeños, un gráfico legible.
- Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos
### Diapositiva 14 · Agrupar en celdas (binning): contar en vez de dibujar cada punto
- Relación · 3 de 4
- ggplot(eph, aes(x = anios_est, y = ingreso)) +
- geom_bin2d(bins = 18) +
- scale_y_log10(
- labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- scale_fill_gradient(low = "#DCE9F5",
- high = "#0B2E4A") +
- labs(title = "Educación e ingreso",
- x = "Años de estudio",
- y = "Guaraníes (escala log)",
- fill = "Personas") +
- theme_minimal(base_size = 11)
- ▸ geom_bin2d() divide el plano en celdas y cuenta cuántas observaciones hay en cada una.
- ▸ El color codifica la densidad: oscuro = muchos casos. Con millones de filas es la opción escalable.
- ▸ Perdemos los puntos individuales pero ganamos la estructura: hay una nube central y pocos valores extremos.
- Con muchos datos, resumí en celdas: el color cuenta lo que los puntos ya no pueden mostrar.
- Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos
### Diapositiva 15 · Agregar una tendencia resume la relación
- Relación · 4 de 4
- ggplot(eph, aes(x = anios_est, y = ingreso)) +
- geom_jitter(width = 0.3, height = 0,
- alpha = 0.1, size = 1,
- color = "#9FB6CB") +
- geom_smooth(color = "#D55E00", se = FALSE,
- linewidth = 1.2) +
- scale_y_log10(
- labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- labs(title = "Educación e ingreso: la tendencia",
- x = "Años de estudio",
- y = "Guaraníes (escala log)") +
- theme_minimal(base_size = 11)
- ▸ geom_smooth() ajusta una curva de tendencia (por defecto, un suavizado) y la dibuja como capa extra.
- ▸ Los puntos quedan en gris claro como contexto; la tendencia lleva el color de énfasis.
- ▸ Cuidado: una relación observada no prueba causalidad.
- Datos al fondo, mensaje al frente: la capa de la tendencia es la que se cuenta.
- Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos
### Diapositiva 16 · Tiempo con barras: un eje truncado exagera las diferencias
- Tiempo · 1 de 2
- ggplot(tasa, aes(x = factor(anio), y = tasa,
- fill = sexo)) +
- geom_col(position = "dodge") +
- coord_cartesian(ylim = c(50, 82)) +
- scale_fill_manual(values = c(Hombres = "#0072B2",
- Mujeres = "#D55E00")) +
- labs(title = "Tasa de ocupación por sexo",
- x = NULL, y = "% de la población de 15+",
- fill = NULL) +
- theme_minimal(base_size = 11)
- ▸ Pregunta: ¿cómo cambió la ocupación entre 2022 y 2025? Tarea: evolución en el tiempo.
- ▸ coord_cartesian(ylim = c(50, 82)) corta la base de las barras: la barra de las mujeres parece duplicarse y las de los hombres casi no cambian: la diferencia visual es mayor que la real.
- ▸ La longitud de una barra codifica la cantidad: su base tiene que ser cero.
- Recortar el eje de barras no es un detalle de estilo: cambia la magnitud que el lector percibe.
- Fuente: INE, EPHC anual 2022–2025 · población de 15 años o más · estimaciones con factor de expansión
### Diapositiva 17 · Para series en el tiempo, líneas con etiquetas directas
- Tiempo · 2 de 2
- ggplot(tasa, aes(x = anio, y = tasa,
- color = sexo)) +
- geom_line(linewidth = 1.1) +
- geom_point(size = 2.5) +
- geom_text(data = filter(tasa, anio == 2025),
- aes(label = sexo), hjust = -0.15,
- show.legend = FALSE) +
- scale_color_manual(values = c(Hombres = "#0072B2",
- Mujeres = "#D55E00")) +
- scale_x_continuous(breaks = 2022:2025,
- expand = expansion(add = c(0.1, 0.7))) +
- labs(title = "Tasa de ocupación por sexo",
- x = NULL, y = "% de la población de 15+") +
- theme_minimal(base_size = 11) +
- theme(legend.position = "none")
- ▸ Las líneas muestran la tendencia; el eje y no necesita empezar en cero porque se lee la pendiente, no la longitud.
- ▸ Las etiquetas directas (geom_text() sobre el último punto) reemplazan la leyenda.
- ▸ Hecho: la brecha entre hombres y mujeres pasó de 23,3 a 21,6 puntos entre 2022 y 2025.
- Líneas para el tiempo, etiquetas junto a los datos y un solo mensaje por gráfico.
- Fuente: INE, EPHC anual 2022–2025 · población de 15 años o más · estimaciones con factor de expansión
### Diapositiva 18 · Matriz de decisión: del dato al gráfico
- Para decidir
- Quiero mostrar…
- Con estos datos
- Primera opción
- Alternativa
- Evitar
- Distribución
- 1 variable numérica
- Histograma / densidad
- Boxplot por grupo
- Barras de promedios
- Cantidad
- Categoría + valor
- Barras horizontales ordenadas
- Puntos (lollipop)
- Torta, 3D
- Proporción
- Partes de un todo
- Barras apiladas al 100 %
- Barra única segmentada
- Torta con 6+ partes
- Relación
- 2 variables numéricas
- Dispersión (con alpha / bins)
- Dispersión + tendencia
- Doble eje y
- Tiempo
- Serie temporal
- Líneas
- Barras (pocos periodos, base 0)
- Barras con eje truncado
- Muchos datos
- Miles de puntos
- Binning (bin2d / hex)
- Muestreo + alpha
- Puntos opacos
- La matriz orienta, no obliga: el objetivo y la audiencia pueden cambiar la elección.
- Esta tabla es la base del Laboratorio 2 (matriz de decisión) y del chart clinic.
### Diapositiva 19 · Chart clinic: diagnosticá y corregí
- Para practicar
- Síntoma
- Diagnóstico
- Corrección en ggplot2
- Barras apretadas y nombres superpuestos
- Eje con categorías largas
- Categorías en el eje y; forcats::fct_reorder()
- Histograma con una sola barra alta
- Cola larga de valores extremos
- scale_x_log10() y bins explícitos
- Nube de puntos opaca
- Overplotting
- alpha, geom_jitter(), geom_bin2d()
- Torta con varias partes parecidas
- Ángulos difíciles de comparar
- geom_col(position = "fill")
- Barras con la base recortada
- Eje y que no empieza en 0
- Quitar coord_cartesian(ylim=) o usar líneas
- Leyenda lejos de los datos
- Búsqueda visual costosa
- Etiquetas directas con geom_text()
- Consejo: antes de entregar un gráfico, leelo como si no conocieras los datos.
### Diapositiva 20 · Para practicar: de cinco preguntas a cinco gráficos
- Tu turno
- ▸ Para cada una de las cinco tareas, formulá una pregunta con datos de la EPHC o de tu propio trabajo.
- ▸ Elegí el gráfico con la matriz de decisión y justificá en una línea: objetivo, audiencia, dato.
- ▸ Escribí el código con ggplot2 capa por capa (ver la presentación de la sesión 4) y revisá el checklist.
- ▸ Resolvé el Quiz 2A del aula: evalúa lo visto en esta presentación.
- No existe «el mejor gráfico»: existe el más adecuado para esta pregunta, esta audiencia y estos datos.

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Wilke · caps. 5-12 (cantidades, distribuciones, proporciones, relaciones) (libro, en) · https://clauswilke.com/dataviz/ · 
- From Data to Viz · árbol de decisión para elegir el gráfico (web, en) · https://www.data-to-viz.com · 
- Python Graph Gallery · ejemplos con código (web, en) · https://python-graph-gallery.com · 
- The R Graph Gallery · ejemplos con código (web, en) · https://r-graph-gallery.com · 
- Royal Statistical Society · Choosing a visualisation type (PDF) (pdf, en) · https://royal-statistical-society.github.io/datavisguide/docs/choosing.pdf · 
- Posit · Cheatsheet «Data visualization with ggplot2» (PDF) (pdf, en) · https://rstudio.github.io/cheatsheets/data-visualization.pdf · hay traducciones en la galería de cheatsheets de Posit
