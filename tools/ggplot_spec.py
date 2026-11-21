"""Contenido de la presentación «ggplot2, capa por capa» (sesión 4, Unidad 2). Solo datos: no dibuja nada.
En el código de cada paso, las líneas que empiezan con § son las NUEVAS de ese paso (se resaltan en la diapositiva y se quita la marca al ejecutar)."""

def cadena(*capas):
    """Une capas con ' +' al final de la anterior, como se escribe en R."""
    out = []
    for i, capa in enumerate(capas):
        capa = list(capa)
        if i > 0:   # las capas después de ggplot() van con dos espacios de sangría
            capa = [("§  " + l[1:]) if l.startswith("§") else ("  " + l if l else l) for l in capa]
        if i < len(capas) - 1: capa[-1] += " +"
        out += capa
    return out

def nuevo(lineas): return ["§" + l for l in lineas]

def ind(lineas):
    """Sangría de 2 espacios para una capa mostrada como continuación de ggplot()."""
    return [("§  " + l[1:]) if l.startswith("§") else ("  " + l if l else l) for l in lineas]

COLORES = ['colores <- c(Ocupado = "#0072B2",', '           Desocupado = "#D55E00",', '           Inactivo = "#009E73")']
ETIQ = ['ocup_larga <- ocup_larga |>', '  mutate(etiqueta = scales::number(', '    personas, big.mark = ".", decimal.mark = ","))']
A1 = ["ggplot(data = ocup_larga,", "       mapping = aes(x = anio, y = personas))"]
A_GROUP = ["ggplot(data = ocup_larga,", "       mapping = aes(x = anio, y = personas,", "                     group = ocup))"]
A_COLOR = ["ggplot(data = ocup_larga,", "       mapping = aes(x = anio, y = personas,", "                     color = ocup))"]
LINE, POINT = ["geom_line()"], ["geom_point()"]
TEXTO = ["geom_text(aes(label = etiqueta), vjust = -0.9,", "          size = 3, show.legend = FALSE)"]
SX = ["scale_x_continuous(breaks = 2022:2025)"]
SY = ["scale_y_continuous(labels = scales::label_number(", '                     big.mark = ".", decimal.mark = ","))']
SY2 = ["scale_y_continuous(labels = scales::label_number(", '                     big.mark = ".", decimal.mark = ","),', "                     expand = expansion(mult = c(0.05, 0.15)))"]
SC = ["scale_color_manual(values = colores)"]
LABS = ['labs(title = "Concepción: situación de ocupación",', '     subtitle = "Estimaciones con factor de expansión",', '     x = "Año", y = "Personas estimadas",', '     color = "Situación",', '     caption = "Fuente: INE, EPHC anual.")']
TEMA1 = ["theme_minimal(base_size = 12)"]
TEMA2 = ['theme(legend.position = "bottom",', '      plot.title = element_text(face = "bold"))']
ANCLA = ["ggplot(ocup_larga, aes(x = anio, y = personas,", "                      color = ocup)) +"]
RESUMEN_MOSTRAR = ANCLA + ["  geom_line() + geom_point() +"]

def paso(id, tag, titulo, codigo, puntos, mensaje, nota="", mostrar=None):
    return dict(id=id, tag=tag, titulo=titulo, codigo=codigo, mostrar=mostrar or codigo, puntos=puntos, mensaje=mensaje, nota=nota)

PASOS = [
 paso("p00", "Paso 0 de 12 · El lienzo", "ggplot() crea el lienzo y le asigna los datos",
      nuevo(["ggplot(data = ocup_larga)"]),
      ["`ggplot()` crea un objeto y guarda **dónde están los datos** (`ocup_larga`).", "Todavía no hay variables asignadas ni formas dibujadas: el panel está vacío.", "El data frame es lo único obligatorio para empezar."],
      "Sin estéticas ni geometrías, ggplot2 no sabe qué dibujar. Todo lo que sigue se agrega con +, una capa a la vez.",
      "Ejecutar solo ggplot(data) no produce error: produce un lienzo vacío."),
 paso("p01", "Paso 1 de 12 · Estéticas", "aes() conecta variables con atributos visuales",
      [A1[0], "§" + A1[1]],
      ["`aes()` (de *aesthetics*) dice **qué variable va a qué atributo**: `anio` al eje x, `personas` al eje y.", "Los ejes aparecen con el rango de los datos, pero **todavía no se dibuja ningún dato**.", "Una estética no es un dibujo: es una asignación."],
      "Mapear es decidir qué variable controla qué atributo visual: posición, color, tamaño, forma…",
      "Los ejes ya muestran 2022–2025 y el rango de personas: ggplot2 calculó las escalas a partir de los datos."),
 paso("p02", "Paso 2 de 12 · Geometrías", "geom_line() dibuja una forma… pero falta algo",
      cadena(A1, nuevo(LINE)),
      ["Una **geometría** (`geom_*`) es la forma con la que se dibujan los datos: línea, punto, barra…", "Se suma al gráfico con `+`.", "Resultado: **una sola línea en zigzag**. Une los 12 puntos por orden de año, mezclando las tres situaciones."],
      "Sin decirle cómo agrupar, ggplot2 trata todas las filas como una única serie.",
      "Es el error más común con líneas. Pedir a la audiencia que explique el zigzag."),
 paso("p03", "Paso 3 de 12 · Grupos", "group separa las series",
      cadena(A_GROUP[:2] + ["§" + A_GROUP[2]], LINE),
      ["`group = ocup` le indica que dibuje **una línea por cada situación** de ocupación.", "Ahora hay tres series… pero todas tienen el mismo color y no se sabe cuál es cuál."],
      "group define las unidades que se unen entre sí: una línea por cada nivel de la variable."),
 paso("p04", "Paso 4 de 12 · Color", "color también es una estética",
      cadena(A_COLOR[:2] + ["§" + A_COLOR[2]], LINE),
      ["Si `color` se mapea a una variable **discreta**, ggplot2 **agrupa automáticamente** (ya no hace falta `group`).", "Asigna un color a cada categoría y **crea la leyenda solo**.", "Los colores por defecto son un punto de partida, no el resultado final."],
      "Una estética mapeada produce a la vez el atributo visual y su leyenda.",
      "Notar que group se reemplazó por color."),
 paso("p05", "Paso 5 de 12 · Más capas", "Se pueden sumar tantas capas como se necesite",
      cadena(A_COLOR, LINE, nuevo(POINT)),
      ["`geom_point()` agrega los puntos de cada año encima de las líneas.", "Todas las capas **heredan** los datos y las estéticas de `ggplot()`: no hace falta repetirlos.", "Los puntos dejan ver que hay observaciones solo en cuatro años."],
      "Un gráfico de ggplot2 es una pila de capas. Cada + agrega una."),
 paso("p06", "Paso 6 de 12 · aes() o fijo", "Dentro de aes() varía; fuera de aes() es fijo",
      ["pA <- ggplot(ocup_larga,", "§             aes(x = anio, y = personas, color = ocup)) +", '  geom_point(size = 3) +', '  labs(title = "A · color DENTRO de aes()")', "", "pB <- ggplot(ocup_larga, aes(x = anio, y = personas)) +", '§  geom_point(size = 3, color = "#D55E00") +', '  labs(title = "B · color FUERA de aes()")', "", "pA | pB   # patchwork: lado a lado"],
      ["**A:** `color = ocup` está dentro de `aes()`: el color **depende** de la variable.", "**B:** `color = \"#D55E00\"` está fuera: es un **atributo fijo**, igual para todos los puntos.", "Si un color tiene que representar datos, va dentro de `aes()`."],
      "Regla práctica: dentro de aes() lo que viene de los datos; fuera, lo que elegís vos.",
      "En B no hay leyenda: no hay ninguna variable asignada."),
 paso("p07", "Paso 7 de 12 · Escalas (eje x)", "Las escalas controlan cómo se leen los ejes",
      cadena(A_COLOR, LINE, POINT, nuevo(SX)),
      ["Cada estética tiene una **escala** (`scale_*`): traduce valores de los datos a posiciones, colores, etc.", "El eje mostraba valores como 2022,5. `breaks = 2022:2025` deja **solo los años reales**.", "Nombre de la función = `scale_` + estética + tipo de variable."],
      "Las escalas deciden las marcas, los límites y las etiquetas de cada eje y de cada leyenda.",
      "Comparar con el paso 5: los años intermedios desaparecieron.",
      mostrar=RESUMEN_MOSTRAR + ind(nuevo(SX))),
 paso("p08", "Paso 8 de 12 · Escalas (eje y)", "Formato legible para los números",
      cadena(A_COLOR, LINE, POINT, SX, nuevo(SY)),
      ["`label_number()` da formato a las marcas del eje: **punto para miles**, coma para decimales.", "El eje pasa de `100000` a `100.000`.", "Los datos no cambian: solo cómo se **muestran**."],
      "Un buen formato numérico ahorra esfuerzo al lector y evita malinterpretar magnitudes.",
      mostrar=RESUMEN_MOSTRAR + ["  # … escala del eje x …"] + ind(nuevo(SY))),
 paso("p09", "Paso 9 de 12 · Escala de color", "Colores elegidos a propósito, no los de fábrica",
      nuevo(COLORES) + [""] + cadena(A_COLOR, LINE, POINT, SX, SY, nuevo(SC)),
      ["`scale_color_manual()` asigna **un color a cada categoría**, con nombre.", "Paleta de **Okabe-Ito**: se distingue también con daltonismo y en blanco y negro.", "Los nombres del vector deben coincidir con los niveles de `ocup`."],
      "El color es un código: elegilo para distinguir, no para decorar (sesión 3).",
      mostrar=nuevo(COLORES) + [""] + RESUMEN_MOSTRAR + ["  # … escalas de x e y …"] + ind(nuevo(SC))),
 paso("p10", "Paso 10 de 12 · Etiquetas de datos", "geom_text() escribe el valor en cada punto",
      nuevo(ETIQ) + [""] + cadena(A_COLOR, LINE, POINT, nuevo(TEXTO), SX, SY2, SC),
      ["`geom_text()` es otra capa: dibuja **texto** y toma su contenido de la estética `label`.", "`vjust = -0.9` sube el texto para que no tape el punto; `show.legend = FALSE` evita una «a» en la leyenda.", "Así el lector lee el **valor exacto** sin estimarlo en el eje."],
      "Las etiquetas muestran el dato; el eje muestra la tendencia. Usalas cuando el valor importa.",
      "También se agregó expand = expansion() en el eje y para dejar espacio arriba.",
      mostrar=nuevo(ETIQ) + [""] + RESUMEN_MOSTRAR + nuevo(["  geom_text(aes(label = etiqueta), vjust = -0.9,", "            size = 3, show.legend = FALSE) +"]) + ["  # … escalas de x, y y color …"]),
 paso("p11", "Paso 11 de 12 · Títulos", "labs() cuenta qué estamos viendo",
      ETIQ + [""] + cadena(A_COLOR, LINE, POINT, TEXTO, SX, SY2, SC, nuevo(LABS)),
      ["`labs()` agrega **título, subtítulo, nombres de ejes, leyenda y fuente**.", "El título conviene que diga el **mensaje** o, al menos, qué se mide y dónde.", "Siempre la **fuente** (`caption`): de dónde salen los datos."],
      "Un gráfico sin título ni fuente no se puede interpretar ni citar.",
      mostrar=ANCLA + ["  # … geom_*(), scale_*() … +"] + ind(nuevo(LABS))),
 paso("p12", "Paso 12 de 12 · Tema", "theme_*() y theme() ajustan el aspecto general",
      ETIQ + [""] + cadena(A_COLOR, LINE, POINT, TEXTO, SX, SY2, SC, LABS, nuevo(TEMA1), nuevo(TEMA2)),
      ["`theme_minimal()` aplica un tema completo: quita el fondo gris y deja líneas suaves.", "`theme()` ajusta detalles: leyenda abajo, título en negrita.", "Esta es la **figura final** del ejercicio: 12 pasos, una capa por vez."],
      "Datos + estéticas + geometrías + escalas + títulos + tema: eso es una figura en ggplot2.",
      mostrar=ANCLA + ["  # … geom_*(), scale_*(), labs() … +"] + ind(nuevo([TEMA1[0] + " +"])) + ind(nuevo(TEMA2))),
]

# Figuras de otras diapositivas (el código también se ejecuta para producir la imagen)
EXTRA = {
 "f_facetas": cadena(["ggplot(ocup_larga,", "       aes(x = anio, y = personas, color = ocup))"], ["geom_line() + geom_point()"], SX, SC, nuevo(['facet_wrap(~ ocup, scales = "free_y")']), ['theme_minimal() + theme(legend.position = "none")']),
 "f_barras": cadena(["ggplot(ocup_larga,", "       aes(x = factor(anio), y = personas,", "           fill = ocup))"], nuevo(['geom_col(position = "dodge")']), ["scale_fill_manual(values = colores)"], SY, ['labs(x = "Año", y = "Personas estimadas", fill = "Situación")'], ["theme_minimal()"]),
 "f_piramide": ["piramide <- piramide |>", "  mutate(grupo = forcats::fct_inorder(grupo))", "", "piramide |>", '  mutate(n = ifelse(sexo == "Hombres", -personas, personas)) |>', "  ggplot(aes(x = grupo, y = n, fill = sexo)) +", "  geom_col(width = 0.9) +", "§  coord_flip() +", "  scale_y_continuous(labels = ~ scales::number(", '                       abs(.x), big.mark = ".",', '                       decimal.mark = ",")) +', '  scale_fill_manual(values = c(Hombres = "#0072B2",', '                               Mujeres = "#D55E00")) +', '  labs(title = "Concepción 2025: población por sexo y edad",', '       x = "Grupo de edad", y = "Personas", fill = NULL) +', "  theme_minimal()"],
}

def sin_marcas(lineas): return [l[1:] if l.startswith("§") else l for l in lineas]
