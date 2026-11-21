# Sesión 4 · Visual analytics, KPIs y storytelling
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U2.
Resumen: Definición de KPIs accionables, small multiples, contribución al cambio y narrativa de datos.

## Objetivos
- Definir KPIs con comparación y contexto.
- Construir una narrativa visual con small multiples y contribución al cambio.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 4 · Visual analytics, KPIs y storytelling
**Unidad del programa:** U2 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Definir KPIs accionables con comparación y contexto.
- Construir una narrativa visual (contexto → conflicto → resolución) con *small multiples* y contribución al cambio.

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-45 | Visual analytics: ciclo pregunta → exploración → hallazgo → decisión; tipos de KPI |
| 45-90 | Storytelling con datos; anatomía de una página ejecutiva |
| 90-105 | Pausa |
| 105-190 | **Lab 4** guiado |
| 190-240 | Arranque del **Mini-proyecto 1** y formación de dupla |

## Trabajo asincrónico
- Lectura: Knaflic (2015), capítulos iniciales (selección); Few (2013), capítulos sobre diseño de tableros.
- **Mini-proyecto 1:** una página para un gerente (*¿dónde actuar el próximo trimestre?*).
- Quiz 4.

## Entrega y evaluación
**Mini-proyecto 1** (10 pts, rúbrica R2) · Quiz 4.

## Laboratorio
[`lab04_kpis_storytelling.py`](lab04_kpis_storytelling.py)

### Pista R (RStudio → RPubs)
[`r/04_kpis_storytelling.Rmd`](../../r/04_kpis_storytelling.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_04_kpis_storytelling.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/4).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **Un buen KPI incluye…** → Definición, unidad, periodo y comparación o meta. Sin contexto (comparación, meta, unidad) un número no permite decidir.
- **Los small multiples sirven para…** → Comparar muchas series con la misma escala sin saturar un único gráfico. Repetir el mismo gráfico por subgrupo, con ejes comunes, facilita comparar patrones.
- **La estructura clásica de una narrativa de datos es…** → Contexto → conflicto → resolución/llamado a la acción. Storytelling con datos: situar a la audiencia, mostrar el problema/hallazgo y proponer qué hacer.
- **Más gráficos en un panel siempre aumentan la comprensión.** → Falso. La saturación aumenta la carga cognitiva: cada elemento debe ganarse su lugar respondiendo la pregunta de la audiencia.
- **Una métrica 'accionable' se diferencia de una de vanidad porque…** → Permite tomar una decisión o cambiar algo. Las métricas de vanidad suben pero no orientan acciones.

## Actividades evaluadas
- Mini-proyecto 1: una página para un gerente (¿dónde actuar el próximo trimestre?) · publicar en RPubs (10 pts)

## Texto de la presentación de la sesión (ggplot2, capa por capa)
### Diapositiva 1 · Cómo se construye una figura en R con ggplot2
- Capa por capa, con datos reales de la Encuesta Permanente de Hogares Continua (INE)
- MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC
- Sesión 4 · Visual analytics, KPIs y storytelling
### Diapositiva 2 · El ejemplo: ocupación en Concepción con la EPHC
- Punto de partida
- anio
- ocup
- personas
- casos_muestrales
- Ocupado
- Desocupado
- Inactivo
- Ocupado
- Desocupado
- Inactivo
- …
- …
- …
- …
- ▸ Pregunta: ¿cómo cambió entre 2022 y 2025 el número de personas ocupadas, desocupadas e inactivas en Concepción?
- ▸ Fuente: microdatos de la EPHC anual del INE (tabla de personas).
- ▸ personas = suma del factor de expansión; casos_muestrales = encuestados que respaldan cada cifra.
- ▸ El data frame está en formato largo: una fila por año y situación. Es lo que espera ggplot2.
- Antes de graficar, siempre mirá los datos: ¿qué representa una fila? ¿qué variable irá a cada atributo del gráfico?
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 3 · La gramática de los gráficos: un gráfico son capas
- Idea central
- Datos
- data
- ¿Qué se grafica?
- un data frame ordenado
- Estéticas
- aes()
- ¿Qué variable controla qué atributo?
- x, y, color, size, shape, label, group
- Geometrías
- geom_*()
- ¿Con qué forma se dibuja?
- line, point, col, text, histogram
- Escalas
- scale_*()
- ¿Cómo se traducen datos a ejes y colores?
- breaks, labels, paleta manual
- Facetas
- facet_*()
- ¿Un panel o varios?
- facet_wrap, facet_grid
- Coordenadas
- coord_*()
- ¿Qué sistema de ejes?
- cartesiano, coord_flip, polar
- Tema
- theme_*()
- ¿Cómo se ve?
- theme_minimal, theme()
- Las capas se suman con +, de a una, y se leen de arriba hacia abajo.
### Diapositiva 4 · Anatomía de una llamada a ggplot()
- Idea central
- ggplot(data = ocup_larga,
- mapping = aes(x = anio, y = personas)) +
- geom_line()
- ①
- data  ·  El data frame con las filas a graficar.
- ②
- mapping = aes()  ·  Qué variable va a qué atributo visual.
- ③
- geom_*()  ·  La forma con la que se dibujan los datos.
- ▸ ggplot() crea el lienzo.
- ▸ El + va al final de la línea, nunca al inicio de la siguiente.
- ▸ Se puede escribir con los argumentos con nombre o en orden: ggplot(ocup_larga, aes(anio, personas)).
- ▸ Lo demás (escalas, títulos, temas) son capas opcionales que mejoran la lectura.
- Receta mínima: datos + estéticas + una geometría. Con eso ya hay un gráfico.
### Diapositiva 5 · ggplot() crea el lienzo y le asigna los datos
- Paso 0 de 12 · El lienzo
- ggplot(data = ocup_larga)
- ▸ ggplot() crea un objeto y guarda dónde están los datos (ocup_larga).
- ▸ Todavía no hay variables asignadas ni formas dibujadas: el panel está vacío.
- ▸ El data frame es lo único obligatorio para empezar.
- Sin estéticas ni geometrías, ggplot2 no sabe qué dibujar. Todo lo que sigue se agrega con +, una capa a la vez.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 6 · aes() conecta variables con atributos visuales
- Paso 1 de 12 · Estéticas
- ggplot(data = ocup_larga,
- mapping = aes(x = anio, y = personas))
- ▸ aes() (de aesthetics) dice qué variable va a qué atributo: anio al eje x, personas al eje y.
- ▸ Los ejes aparecen con el rango de los datos, pero todavía no se dibuja ningún dato.
- ▸ Una estética no es un dibujo: es una asignación.
- Mapear es decidir qué variable controla qué atributo visual: posición, color, tamaño, forma…
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 7 · geom_line() dibuja una forma… pero falta algo
- Paso 2 de 12 · Geometrías
- ggplot(data = ocup_larga,
- mapping = aes(x = anio, y = personas)) +
- geom_line()
- ▸ Una geometría (geom_*) es la forma con la que se dibujan los datos: línea, punto, barra…
- ▸ Se suma al gráfico con +.
- ▸ Resultado: una sola línea en zigzag. Une los 12 puntos por orden de año, mezclando las tres situaciones.
- Sin decirle cómo agrupar, ggplot2 trata todas las filas como una única serie.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 8 · group separa las series
- Paso 3 de 12 · Grupos
- ggplot(data = ocup_larga,
- mapping = aes(x = anio, y = personas,
- group = ocup)) +
- geom_line()
- ▸ group = ocup le indica que dibuje una línea por cada situación de ocupación.
- ▸ Ahora hay tres series… pero todas tienen el mismo color y no se sabe cuál es cuál.
- group define las unidades que se unen entre sí: una línea por cada nivel de la variable.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 9 · color también es una estética
- Paso 4 de 12 · Color
- ggplot(data = ocup_larga,
- mapping = aes(x = anio, y = personas,
- color = ocup)) +
- geom_line()
- ▸ Si color se mapea a una variable discreta, ggplot2 agrupa automáticamente (ya no hace falta group).
- ▸ Asigna un color a cada categoría y crea la leyenda solo.
- ▸ Los colores por defecto son un punto de partida, no el resultado final.
- Una estética mapeada produce a la vez el atributo visual y su leyenda.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 10 · Se pueden sumar tantas capas como se necesite
- Paso 5 de 12 · Más capas
- ggplot(data = ocup_larga,
- mapping = aes(x = anio, y = personas,
- color = ocup)) +
- geom_line() +
- geom_point()
- ▸ geom_point() agrega los puntos de cada año encima de las líneas.
- ▸ Todas las capas heredan los datos y las estéticas de ggplot(): no hace falta repetirlos.
- ▸ Los puntos dejan ver que hay observaciones solo en cuatro años.
- Un gráfico de ggplot2 es una pila de capas. Cada + agrega una.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 11 · Dentro de aes() varía; fuera de aes() es fijo
- Paso 6 de 12 · aes() o fijo
- pA <- ggplot(ocup_larga,
- aes(x = anio, y = personas, color = ocup)) +
- geom_point(size = 3) +
- labs(title = "A · color DENTRO de aes()")
- pB <- ggplot(ocup_larga, aes(x = anio, y = personas)) +
- geom_point(size = 3, color = "#D55E00") +
- labs(title = "B · color FUERA de aes()")
- pA | pB   # patchwork: lado a lado
- ▸ A: color = ocup está dentro de aes(): el color depende de la variable.
- ▸ B: color = "#D55E00" está fuera: es un atributo fijo, igual para todos los puntos.
- ▸ Si un color tiene que representar datos, va dentro de aes().
- Regla práctica: dentro de aes() lo que viene de los datos; fuera, lo que elegís vos.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 12 · Las escalas controlan cómo se leen los ejes
- Paso 7 de 12 · Escalas (eje x)
- ggplot(ocup_larga, aes(x = anio, y = personas,
- color = ocup)) +
- geom_line() + geom_point() +
- scale_x_continuous(breaks = 2022:2025)
- ▸ Cada estética tiene una escala (scale_*): traduce valores de los datos a posiciones, colores, etc.
- ▸ El eje mostraba valores como 2022,5. breaks = 2022:2025 deja solo los años reales.
- ▸ Nombre de la función = scale_ + estética + tipo de variable.
- Las escalas deciden las marcas, los límites y las etiquetas de cada eje y de cada leyenda.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 13 · Formato legible para los números
- Paso 8 de 12 · Escalas (eje y)
- ggplot(ocup_larga, aes(x = anio, y = personas,
- color = ocup)) +
- geom_line() + geom_point() +
- # … escala del eje x …
- scale_y_continuous(labels = scales::label_number(
- big.mark = ".", decimal.mark = ","))
- ▸ label_number() da formato a las marcas del eje: punto para miles, coma para decimales.
- ▸ El eje pasa de 100000 a 100.000.
- ▸ Los datos no cambian: solo cómo se muestran.
- Un buen formato numérico ahorra esfuerzo al lector y evita malinterpretar magnitudes.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 14 · Colores elegidos a propósito, no los de fábrica
- Paso 9 de 12 · Escala de color
- colores <- c(Ocupado = "#0072B2",
- Desocupado = "#D55E00",
- Inactivo = "#009E73")
- ggplot(ocup_larga, aes(x = anio, y = personas,
- color = ocup)) +
- geom_line() + geom_point() +
- # … escalas de x e y …
- scale_color_manual(values = colores)
- ▸ scale_color_manual() asigna un color a cada categoría, con nombre.
- ▸ Paleta de Okabe-Ito: se distingue también con daltonismo y en blanco y negro.
- ▸ Los nombres del vector deben coincidir con los niveles de ocup.
- El color es un código: elegilo para distinguir, no para decorar (sesión 3).
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 15 · geom_text() escribe el valor en cada punto
- Paso 10 de 12 · Etiquetas de datos
- ocup_larga <- ocup_larga |>
- mutate(etiqueta = scales::number(
- personas, big.mark = ".", decimal.mark = ","))
- ggplot(ocup_larga, aes(x = anio, y = personas,
- color = ocup)) +
- geom_line() + geom_point() +
- geom_text(aes(label = etiqueta), vjust = -0.9,
- size = 3, show.legend = FALSE) +
- # … escalas de x, y y color …
- ▸ geom_text() es otra capa: dibuja texto y toma su contenido de la estética label.
- ▸ vjust = -0.9 sube el texto para que no tape el punto; show.legend = FALSE evita una «a» en la leyenda.
- ▸ Así el lector lee el valor exacto sin estimarlo en el eje.
- Las etiquetas muestran el dato; el eje muestra la tendencia. Usalas cuando el valor importa.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 16 · labs() cuenta qué estamos viendo
- Paso 11 de 12 · Títulos
- ggplot(ocup_larga, aes(x = anio, y = personas,
- color = ocup)) +
- # … geom_*(), scale_*() … +
- labs(title = "Concepción: situación de ocupación",
- subtitle = "Estimaciones con factor de expansión",
- x = "Año", y = "Personas estimadas",
- color = "Situación",
- caption = "Fuente: INE, EPHC anual.")
- ▸ labs() agrega título, subtítulo, nombres de ejes, leyenda y fuente.
- ▸ El título conviene que diga el mensaje o, al menos, qué se mide y dónde.
- ▸ Siempre la fuente (caption): de dónde salen los datos.
- Un gráfico sin título ni fuente no se puede interpretar ni citar.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 17 · theme_*() y theme() ajustan el aspecto general
- Paso 12 de 12 · Tema
- ggplot(ocup_larga, aes(x = anio, y = personas,
- color = ocup)) +
- # … geom_*(), scale_*(), labs() … +
- theme_minimal(base_size = 12) +
- theme(legend.position = "bottom",
- plot.title = element_text(face = "bold"))
- ▸ theme_minimal() aplica un tema completo: quita el fondo gris y deja líneas suaves.
- ▸ theme() ajusta detalles: leyenda abajo, título en negrita.
- ▸ Esta es la figura final del ejercicio: 12 pasos, una capa por vez.
- Datos + estéticas + geometrías + escalas + títulos + tema: eso es una figura en ggplot2.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 18 · Facetas: un panel por categoría
- Más componentes
- ggplot(ocup_larga,
- aes(x = anio, y = personas, color = ocup)) +
- geom_line() + geom_point() +
- scale_x_continuous(breaks = 2022:2025) +
- scale_color_manual(values = colores) +
- facet_wrap(~ ocup, scales = "free_y") +
- theme_minimal() + theme(legend.position = "none")
- ▸ facet_wrap(~ ocup) divide el gráfico en paneles pequeños (small multiples).
- ▸ scales = "free_y" deja que cada panel tenga su propio eje y.
- ▸ Útil cuando las magnitudes son muy distintas: ahora se ve la forma de cada serie.
- Cuidado: con ejes libres no se pueden comparar alturas entre paneles.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 19 · Cambiar de geometría: barras agrupadas
- Más componentes
- ggplot(ocup_larga,
- aes(x = factor(anio), y = personas,
- fill = ocup)) +
- geom_col(position = "dodge") +
- scale_fill_manual(values = colores) +
- scale_y_continuous(labels = scales::label_number(
- big.mark = ".", decimal.mark = ",")) +
- labs(x = "Año", y = "Personas estimadas", fill = "Situación") +
- theme_minimal()
- ▸ Mismos datos y estéticas; cambia la geometría: geom_col(position = "dodge").
- ▸ position = "dodge" pone las barras una al lado de la otra.
- ▸ fill pinta el interior; color es solo el borde.
- Con una serie en el tiempo, las líneas muestran mejor la tendencia; las barras comparan valores puntuales.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 20 · Coordenadas: la pirámide de población
- Más componentes
- piramide <- piramide |>
- mutate(grupo = forcats::fct_inorder(grupo))
- piramide |>
- mutate(n = ifelse(sexo == "Hombres", -personas, personas)) |>
- ggplot(aes(x = grupo, y = n, fill = sexo)) +
- geom_col(width = 0.9) +
- coord_flip() +
- scale_y_continuous(labels = ~ scales::number(
- abs(.x), big.mark = ".",
- decimal.mark = ",")) +
- scale_fill_manual(values = c(Hombres = "#0072B2",
- Mujeres = "#D55E00")) +
- labs(title = "Concepción 2025: población por sexo y edad",
- x = "Grupo de edad", y = "Personas", fill = NULL) +
- theme_minimal()
- ▸ Otro ejemplo de la EPHC: población estimada de Concepción en 2025 por sexo y grupo de edad.
- ▸ coord_flip() intercambia los ejes; los hombres se grafican con valores negativos.
- ▸ Cada barra suma el factor de expansión, no cuenta filas.
- Las coordenadas cambian cómo se orientan los ejes sin tocar los datos ni las estéticas.
- Fuente: INE, Encuesta Permanente de Hogares Continua (anual) · Concepción (DPTO 1) · estimaciones con factor de expansión
### Diapositiva 21 · Receta: de la pregunta a la figura
- Para recordar
- Pregunta o mensaje
- ¿Qué querés que entienda el lector?
- Datos ordenados
- Una fila por observación (formato largo); pivot_longer() si hace falta.
- Estéticas
- aes(): qué variable va a x, y, color…
- Geometría
- Elegida según la tarea perceptiva: posición y longitud antes que ángulo y área.
- Escalas
- Marcas, formatos y colores accesibles (Okabe-Ito).
- Textos
- Título, ejes con unidades, leyenda y fuente.
- Tema y revisión
- theme_*() y el checklist de calidad visual y ética.
- Cada paso del gráfico se resuelve con una capa o un argumento: la receta es siempre la misma.
### Diapositiva 22 · Errores frecuentes y cómo leerlos
- Para recordar
- Síntoma
- Causa probable
- Arreglo
- Línea en zigzag
- Falta separar las series
- Mapear color o group a la variable
- Error: Cannot add ggproto objects together
- El + quedó al inicio de la línea
- Ponerlo al final de la línea anterior
- Object 'x' not found
- Variable mal escrita o fuera de aes()
- Revisar el nombre con names(datos)
- La leyenda dice «#D55E00»
- El color fijo quedó dentro de aes()
- Sacar color = ... de aes()
- Años como 2022,5
- anio es numérica continua
- scale_x_continuous(breaks = ...) o factor(anio)
- No se puede mapear 3 series
- Datos en formato ancho
- tidyr::pivot_longer() a formato largo
- Consejo: ejecutá el gráfico después de agregar cada capa; así el error aparece donde se lo cometió.
### Diapositiva 23 · El código completo de la figura
- Resumen
- ocup_larga <- ocup_larga |>
- mutate(etiqueta = scales::number(
- personas, big.mark = ".", decimal.mark = ","))
- ggplot(data = ocup_larga,
- mapping = aes(x = anio, y = personas,
- color = ocup)) +
- geom_line() +
- geom_point() +
- geom_text(aes(label = etiqueta), vjust = -0.9,
- size = 3, show.legend = FALSE) +
- scale_x_continuous(breaks = 2022:2025) +
- scale_y_continuous(labels = scales::label_number(
- big.mark = ".", decimal.mark = ","),
- expand = expansion(mult = c(0.05, 0.15))) +
- scale_color_manual(values = colores) +
- labs(title = "Concepción: situación de ocupación",
- subtitle = "Estimaciones con factor de expansión",
- x = "Año", y = "Personas estimadas",
- color = "Situación",
- caption = "Fuente: INE, EPHC anual.") +
- theme_minimal(base_size = 12) +
- theme(legend.position = "bottom",
- plot.title = element_text(face = "bold"))
- Cada línea corresponde a una de las capas de los 12 pasos. Probá quitar una y mirá qué cambia.
### Diapositiva 24 · Para practicar
- Tu turno
- ▸ Corré el ejercicio guiado 04_ejercicio_ephc_concepcion.Rmd: usa estas mismas capas con los microdatos completos de la EPHC.
- ▸ Cambiá un paso por vez y observá qué ocurre: quitá group, mové color fuera de aes(), probá geom_col().
- ▸ Reemplazá Concepción por otro departamento (DPTO == 2, 3…) y volvé a mirar el mensaje.
- ▸ Respondé el Quiz 4B del aula para comprobar lo aprendido.
- ggplot2 no dibuja un gráfico: lo describe. Datos + estéticas + capas + escalas + textos + tema.

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- storytelling with data · blog y recursos (web, en) · https://www.storytellingwithdata.com · 
- Few, Information Dashboard Design (libro; consultar en biblioteca) (libro, en) · https://www.perceptualedge.com · sitio del autor
