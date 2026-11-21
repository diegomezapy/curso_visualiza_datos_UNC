"""Contenido de la presentación «Elección de gráficos» (sesión 2, Unidad 1). Solo datos: no dibuja nada.
El código de cada figura se ejecuta en R (tools/eleccion_figuras.R); las líneas con § son las que cambian respecto de la figura anterior."""
THEME = "  theme_minimal(base_size = 11)"
PIE = "Fuente: INE, EPHC anual 2025 (microdatos) · ocupados con ingreso declarado · muestra aleatoria de 6.000 casos"
PIE_AGR = "Fuente: INE, EPHC anual 2025 · estimaciones con factor de expansión"
PIE_TASA = "Fuente: INE, EPHC anual 2022–2025 · población de 15 años o más · estimaciones con factor de expansión"

def L(texto): return [l for l in texto.strip("\n").split("\n")]

FIGS = [
 dict(id="d1", tag="Distribución · 1 de 3", titulo="Distribución: el histograma con la configuración por defecto engaña", pie=PIE,
  codigo=L('''
ggplot(eph, aes(x = ingreso)) +
§  geom_histogram(fill = "#0072B2") +
  scale_x_continuous(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Ingreso mensual de los ocupados",
       x = "Guaraníes", y = "Personas (muestra)") +
  theme_minimal(base_size = 11)'''),
  puntos=["Pregunta: **¿cómo se distribuyen los ingresos?** Tarea: *distribución* de una variable numérica.", "La mayoría de las barras se amontona a la izquierda: unos pocos ingresos enormes **estiran el eje**.", "`geom_histogram()` usa 30 intervalos por defecto; sin mirar la escala, el gráfico casi no informa."],
  mensaje="Una distribución muy asimétrica necesita otra escala: el histograma por defecto esconde lo que importa.",
  nota="Mostrar primero esta figura y preguntar qué se ve. La respuesta: casi nada. Luego pasar a la escala logarítmica."),
 dict(id="d2", tag="Distribución · 2 de 3", titulo="Con escala logarítmica y bins explícitos, la forma aparece", pie=PIE,
  codigo=L('''
ggplot(eph, aes(x = ingreso)) +
§  geom_histogram(bins = 40, fill = "#0072B2") +
§  scale_x_log10(
§    labels = scales::label_number(
§      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Ingreso mensual de los ocupados",
       x = "Guaraníes (escala logarítmica)",
       y = "Personas (muestra)") +
  theme_minimal(base_size = 11)'''),
  puntos=["`scale_x_log10()`: cada marca del eje multiplica el valor por 10; las diferencias **proporcionales** pasan a ser iguales.", "`bins = 40` fija la cantidad de intervalos: probá 15, 40 y 100 y compará la forma.", "Ahora se distingue la **concentración** alrededor de 2–3 millones y la cola de ingresos altos."],
  mensaje="Elegir el ancho de los intervalos y la escala es parte del análisis, no un detalle estético.",
  nota="Aclarar que con escala log el eje deja de ser lineal: avisar a la audiencia en el título del eje."),
 dict(id="d3", tag="Distribución · 3 de 3", titulo="Comparar distribuciones entre grupos: diagrama de cajas", pie=PIE,
  codigo=L('''
ggplot(eph, aes(x = area, y = ingreso,
                fill = sexo)) +
§  geom_boxplot(outlier.alpha = 0.2) +
  scale_y_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
§  scale_fill_manual(values = c(Hombres = "#0072B2",
§                               Mujeres = "#D55E00")) +
  labs(title = "Ingreso por área y sexo",
       x = NULL, y = "Guaraníes (escala log)",
       fill = NULL) +
  theme_minimal(base_size = 11)'''),
  puntos=["Para comparar **varias distribuciones** a la vez, el diagrama de cajas resume mediana, cuartiles y valores atípicos.", "La caja contiene el 50 % central; la línea es la **mediana**; los puntos son atípicos.", "Se compara posición (mediana) entre grupos: la tarea perceptiva más precisa."],
  mensaje="Una caja por grupo permite comparar medianas y dispersión sin dibujar cientos de barras.",
  nota="Si la audiencia es técnica, el boxplot; si no, considerar un violín o barras de la mediana con una nota."),
 dict(id="c1", tag="Cantidad · 1 de 2", titulo="Cantidad: barras verticales con nombres largos", pie=PIE_AGR,
  codigo=L('''
ggplot(dptos, aes(x = dpto, y = ingreso_mediano)) +
§  geom_col(fill = "#0072B2") +
  labs(title = "Ingreso mediano por departamento",
       x = NULL, y = "Guaraníes") +
  theme_minimal(base_size = 11)'''),
  puntos=["Pregunta: **¿cómo se comparan los 16 departamentos?** Tarea: *cantidad* por categoría.", "Los nombres largos se **superponen** y el orden es alfabético, que no significa nada para el lector.", "Para comparar, el lector necesita ver el **ranking**."],
  mensaje="Barras desordenadas obligan a buscar: el orden alfabético solo sirve para consultar, no para comparar.",
  nota="Problema doble: legibilidad de etiquetas y orden sin sentido."),
 dict(id="c2", tag="Cantidad · 2 de 2", titulo="Barras horizontales, ordenadas y con el foco en Concepción", pie=PIE_AGR,
  codigo=L('''
dptos |>
§  mutate(foco = dpto == "Concepción") |>
  ggplot(aes(x = ingreso_mediano,
§             y = forcats::fct_reorder(dpto, ingreso_mediano),
§             fill = foco)) +
  geom_col(show.legend = FALSE) +
§  scale_fill_manual(values = c("FALSE" = "#9FB6CB",
§                               "TRUE" = "#D55E00")) +
  scale_x_continuous(labels = scales::label_number(
    big.mark = ".", decimal.mark = ",")) +
  labs(title = "Ingreso mediano por departamento",
       x = "Guaraníes", y = NULL) +
  theme_minimal(base_size = 11)'''),
  puntos=["Con las categorías en el eje y, los nombres se leen **sin girar la cabeza**.", "`forcats::fct_reorder()` ordena las categorías **por el valor**, no alfabéticamente.", "Un solo color de énfasis (`#D55E00`) guía la mirada hacia el departamento de interés."],
  mensaje="Ordená por valor, poné las categorías en el eje y y resaltá una sola cosa: así se lee el ranking.",
  nota="Barras empiezan en cero: tienen que hacerlo porque la longitud codifica la cantidad."),
 dict(id="p1", tag="Proporción · 1 de 2", titulo="Proporciones: el gráfico de torta no ayuda a comparar", pie=PIE_AGR,
  codigo=L('''
ggplot(compo, aes(x = "", y = personas,
                  fill = situacion)) +
§  geom_col(position = "fill", width = 1) +
§  coord_polar(theta = "y") +
§  facet_wrap(~ area) +
  scale_fill_manual(values = colores) +
  labs(title = "Situación de ocupación, 2025",
       fill = NULL) +
§  theme_void(base_size = 11)'''),
  puntos=["Pregunta: **¿qué proporción está ocupada, desocupada o inactiva en cada área?** Tarea: *proporción de un todo*.", "`coord_polar()` convierte las barras en una torta: se compara **ángulo y área**, que son menos precisos.", "Comparar el tamaño de «Desocupado» entre las dos tortas es casi imposible."],
  mensaje="Con pocas categorías y un solo todo la torta puede servir; para comparar entre grupos, no.",
  nota="Cleveland y McGill: ángulos y áreas se juzgan peor que posiciones alineadas."),
 dict(id="p2", tag="Proporción · 2 de 2", titulo="Barras apiladas al 100 %: mismas proporciones, comparación posible", pie=PIE_AGR,
  codigo=L('''
ggplot(compo, aes(x = area, y = personas,
                  fill = situacion)) +
§  geom_col(position = "fill") +
§  scale_y_continuous(
§    labels = scales::label_percent()) +
  scale_fill_manual(values = colores) +
§  coord_flip() +
  labs(title = "Situación de ocupación, 2025",
       x = NULL, y = "Porcentaje de la población de 15+",
       fill = NULL) +
  theme_minimal(base_size = 11)'''),
  puntos=["`position = \"fill\"` apila las barras y las lleva al **100 %**: se comparan longitudes sobre una base común.", "La barra de abajo y la de arriba parten de la misma base: se compara con claridad que la **desocupación** es menor en el área rural (2,3 % frente a 3,8 %).", "Si el mensaje es una sola categoría, conviene una barra por grupo y esa categoría sola."],
  mensaje="Mismas cifras, mejor tarea perceptiva: posición y longitud antes que ángulo.",
  nota="Los segmentos del medio (Desocupado) no comparten base: si importa comparar esa categoría, graficarla sola."),
 dict(id="r1", tag="Relación · 1 de 4", titulo="Relación entre dos variables: el diagrama de dispersión básico", pie=PIE,
  codigo=L('''
ggplot(eph, aes(x = anios_est, y = ingreso)) +
§  geom_point() +
  scale_y_continuous(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Educación e ingreso",
       x = "Años de estudio", y = "Guaraníes") +
  theme_minimal(base_size = 11)'''),
  puntos=["Pregunta: **¿los ingresos crecen con la educación?** Tarea: *relación* entre dos variables numéricas.", "Con 6.000 puntos aparece el **overplotting**: los puntos se tapan entre sí y la densidad se pierde.", "Además, los años de estudio son enteros: los puntos forman columnas."],
  mensaje="Cuando los puntos se superponen, el gráfico muestra dónde hay datos pero no cuántos.",
  nota="Con la base completa (26.000 casos) el problema es peor: eso es lo que ocurre en la práctica."),
 dict(id="r2", tag="Relación · 2 de 4", titulo="Transparencia, jitter y escala log reducen el overplotting", pie=PIE,
  codigo=L('''
ggplot(eph, aes(x = anios_est, y = ingreso)) +
§  geom_jitter(width = 0.3, height = 0,
§              alpha = 0.15, size = 1,
§              color = "#0072B2") +
§  scale_y_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Educación e ingreso",
       x = "Años de estudio",
       y = "Guaraníes (escala log)") +
  theme_minimal(base_size = 11)'''),
  puntos=["`alpha = 0.15` vuelve los puntos translúcidos: donde hay más, **el color se oscurece**.", "`geom_jitter(width = 0.3)` separa horizontalmente los puntos que comparten un valor entero.", "`scale_y_log10()` abre la zona densa donde se concentran los ingresos."],
  mensaje="Transparencia + jitter + escala adecuada: tres ajustes pequeños, un gráfico legible.",
  nota="Aclarar que el jitter agrega ruido solo visual, no modifica los datos."),
 dict(id="r3", tag="Relación · 3 de 4", titulo="Agrupar en celdas (binning): contar en vez de dibujar cada punto", pie=PIE,
  codigo=L('''
ggplot(eph, aes(x = anios_est, y = ingreso)) +
§  geom_bin2d(bins = 18) +
  scale_y_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
§  scale_fill_gradient(low = "#DCE9F5",
§                      high = "#0B2E4A") +
  labs(title = "Educación e ingreso",
       x = "Años de estudio",
       y = "Guaraníes (escala log)",
       fill = "Personas") +
  theme_minimal(base_size = 11)'''),
  puntos=["`geom_bin2d()` divide el plano en celdas y **cuenta** cuántas observaciones hay en cada una.", "El color codifica la densidad: oscuro = muchos casos. Con millones de filas es la opción escalable.", "Perdemos los puntos individuales pero ganamos la estructura: hay una nube central y pocos valores extremos."],
  mensaje="Con muchos datos, resumí en celdas: el color cuenta lo que los puntos ya no pueden mostrar.",
  nota="Alternativa: geom_hex() (paquete hexbin), mismo principio con hexágonos."),
 dict(id="r4", tag="Relación · 4 de 4", titulo="Agregar una tendencia resume la relación", pie=PIE,
  codigo=L('''
ggplot(eph, aes(x = anios_est, y = ingreso)) +
  geom_jitter(width = 0.3, height = 0,
              alpha = 0.1, size = 1,
              color = "#9FB6CB") +
§  geom_smooth(color = "#D55E00", se = FALSE,
§              linewidth = 1.2) +
  scale_y_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Educación e ingreso: la tendencia",
       x = "Años de estudio",
       y = "Guaraníes (escala log)") +
  theme_minimal(base_size = 11)'''),
  puntos=["`geom_smooth()` ajusta una **curva de tendencia** (por defecto, un suavizado) y la dibuja como capa extra.", "Los puntos quedan en gris claro como contexto; la **tendencia** lleva el color de énfasis.", "Cuidado: una relación observada **no prueba causalidad**."],
  mensaje="Datos al fondo, mensaje al frente: la capa de la tendencia es la que se cuenta.",
  nota="Los datos de la EPHC son una encuesta transversal: correlación no es causalidad."),
 dict(id="t1", tag="Tiempo · 1 de 2", titulo="Tiempo con barras: un eje truncado exagera las diferencias", pie=PIE_TASA,
  codigo=L('''
ggplot(tasa, aes(x = factor(anio), y = tasa,
                 fill = sexo)) +
  geom_col(position = "dodge") +
§  coord_cartesian(ylim = c(50, 82)) +
  scale_fill_manual(values = c(Hombres = "#0072B2",
                               Mujeres = "#D55E00")) +
  labs(title = "Tasa de ocupación por sexo",
       x = NULL, y = "% de la población de 15+",
       fill = NULL) +
  theme_minimal(base_size = 11)'''),
  puntos=["Pregunta: **¿cómo cambió la ocupación entre 2022 y 2025?** Tarea: *evolución en el tiempo*.", "`coord_cartesian(ylim = c(50, 82))` **corta la base de las barras**: la barra de las mujeres parece **duplicarse** y las de los hombres casi no cambian: la diferencia visual es mayor que la real.", "La longitud de una barra codifica la cantidad: su base **tiene que ser cero**."],
  mensaje="Recortar el eje de barras no es un detalle de estilo: cambia la magnitud que el lector percibe.",
  nota="Mostrar junto a la siguiente: el mismo dato con una geometría honesta para el tiempo."),
 dict(id="t2", tag="Tiempo · 2 de 2", titulo="Para series en el tiempo, líneas con etiquetas directas", pie=PIE_TASA,
  codigo=L('''
ggplot(tasa, aes(x = anio, y = tasa,
                 color = sexo)) +
§  geom_line(linewidth = 1.1) +
§  geom_point(size = 2.5) +
§  geom_text(data = filter(tasa, anio == 2025),
§            aes(label = sexo), hjust = -0.15,
§            show.legend = FALSE) +
  scale_color_manual(values = c(Hombres = "#0072B2",
                                Mujeres = "#D55E00")) +
  scale_x_continuous(breaks = 2022:2025,
§                     expand = expansion(add = c(0.1, 0.7))) +
  labs(title = "Tasa de ocupación por sexo",
       x = NULL, y = "% de la población de 15+") +
  theme_minimal(base_size = 11) +
  theme(legend.position = "none")'''),
  puntos=["Las **líneas** muestran la tendencia; el eje y no necesita empezar en cero porque se lee la *pendiente*, no la longitud.", "Las **etiquetas directas** (`geom_text()` sobre el último punto) reemplazan la leyenda.", "Hecho: la brecha entre hombres y mujeres pasó de 23,3 a 21,6 puntos entre 2022 y 2025."],
  mensaje="Líneas para el tiempo, etiquetas junto a los datos y un solo mensaje por gráfico.",
  nota="La brecha se calcula con las tasas de la tabla: 77,4 − 54,1 = 23,3 (2022) y 79,6 − 58,0 = 21,6 (2025)."),
]
def sin_marcas(lineas): return [l[1:] if l.startswith("§") else l for l in lineas]
