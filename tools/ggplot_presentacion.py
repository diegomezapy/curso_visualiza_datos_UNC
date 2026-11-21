"""Presentación de la sesión 2: cómo se construye una figura con ggplot2, capa por capa, con datos reales de la EPHC (INE).

Flujo (cada etapa se puede repetir sola):
  1) python tools/ggplot_presentacion.py pasos     → escribe el código de cada paso en aula/media/unidad2_ggplot/fuentes/pasos/*.R
  2) Rscript tools/ggplot_figuras.R                → ejecuta ESE MISMO código y guarda cada figura (así lo que se muestra es lo que corre)
  3) python tools/ggplot_presentacion.py pptx      → arma presentacion.pptx con python-pptx
  4) python tools/procesar_presentacion.py unidad2_ggplot  → PDF + diapositivas .webp + slides.json (requiere LibreOffice y pdftoppm)
Los datos agregados salen de tools/ggplot_datos.R (a partir de los CSV del INE; no se versionan filas individuales)."""
import json, re, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
M = RAIZ / "aula" / "media" / "unidad2_ggplot"
FU = M / "fuentes"; PASOS = FU / "pasos"; FIG = FU / "figuras"

# ---------- pasos de construcción (cada línea que empieza con § es NUEVA en ese paso) ----------
COLORES = ['colores <- c(Ocupado = "#0072B2",', '           Desocupado = "#D55E00",', '           Inactivo = "#009E73")']
ETIQ = ['ocup_larga <- ocup_larga |>', '  mutate(etiqueta = scales::number(personas,', '         big.mark = ".", decimal.mark = ","))']

def cadena(*capas):
    """Une capas con ' +' al final de la anterior (así se escribe en R)."""
    out = []
    for i, capa in enumerate(capas):
        capa = list(capa)
        if i < len(capas) - 1: capa[-1] += " +"
        out += capa
    return out

def N(lineas): return ["§" + l for l in lineas]   # marca como nuevas

B0 = ["ggplot(data = ocup_larga)"]
B1 = ["ggplot(data = ocup_larga,", "       mapping = aes(x = anio, y = personas))"]
B3 = ["ggplot(data = ocup_larga,", "       mapping = aes(x = anio, y = personas,", "                     group = ocup))"]
B4 = ["ggplot(data = ocup_larga,", "       mapping = aes(x = anio, y = personas,", "                     color = ocup))"]
SX = ["scale_x_continuous(breaks = 2022:2025)"]
SY = ['scale_y_continuous(labels = scales::label_number(', '                     big.mark = ".", decimal.mark = ","))']
SC = ["scale_color_manual(values = colores)"]
SY2 = ['scale_y_continuous(labels = scales::label_number(', '                     big.mark = ".", decimal.mark = ","),', '                     expand = expansion(mult = c(0.05, 0.15)))']
LABS = ['labs(title = "Concepción: personas ocupadas, desocupadas e inactivas",', '     subtitle = "Estimaciones con factor de expansión, 2022–2025",', '     x = "Año", y = "Personas estimadas", color = "Situación",', '     caption = "Fuente: INE, EPHC anual.")']
TEMA = ['theme_minimal(base_size = 12)', 'theme(legend.position = "bottom",', '      plot.title = element_text(face = "bold"))']

# (id, sección, título, código [con §], mostrar(opcional, con §/…), explicación (viñetas), mensaje inferior, nota para quien presenta)
PASOS_DEF = [
 ("p00", "Paso 0 de 12 · El lienzo", "ggplot() crea el lienzo y le asigna los datos",
  B0, None,
  ["`ggplot()` crea un objeto y guarda **dónde están los datos** (`ocup_larga`).", "Todavía no hay variables asignadas ni formas dibujadas: el panel está vacío.", "Es el único argumento obligatorio de partida: el data frame."],
  "Sin estéticas ni geometrías, ggplot2 no sabe qué dibujar. Todo lo que sigue se agrega con +, una capa a la vez.",
  "Mostrar que ejecutar solo ggplot(data) no produce error: produce un lienzo vacío."),
 ("p01", "Paso 1 de 12 · Estéticas", "aes() conecta variables con atributos visuales",
  N(B1[:1]) + N(B1[1:]) if False else ["ggplot(data = ocup_larga,", "§       mapping = aes(x = anio, y = personas))"], None,
  ["`aes()` (de *aesthetics*) dice **qué variable va a qué atributo**: `anio` al eje x, `personas` al eje y.", "Los ejes aparecen con el rango de los datos, pero **todavía no se dibuja ningún dato**.", "Una estética no es un dibujo: es una asignación."],
  "Mapear es decidir qué variable controla qué atributo visual (posición, color, tamaño, forma…).",
  "Los ejes ya muestran 2022–2025 y el rango de personas: ggplot2 calculó las escalas a partir de los datos."),
 ("p02", "Paso 2 de 12 · Geometrías", "geom_line() dibuja una forma… pero falta algo",
  cadena(B1, N(["geom_line()"])), None,
  ["Una **geometría** (`geom_*`) es la forma con la que se dibujan los datos: línea, punto, barra…", "Se suma al gráfico con `+`.", "Resultado: **una sola línea en zigzag**. Une los 12 puntos por orden de año, mezclando las tres situaciones."],
  "Sin decirle cómo agrupar, ggplot2 trata todas las filas como una única serie.",
  "Es el error más común de los principiantes con líneas. Pedir a la audiencia que explique el zigzag."),
 ("p03", "Paso 3 de 12 · Grupos", "group separa las series",
  cadena(B3[:2] + ["§                     group = ocup))"], ["geom_line()"]), None,
  ["`group = ocup` le indica que dibuje **una línea por cada situación** de ocupación.", "Ahora hay tres series… pero todas tienen el mismo color y no se sabe cuál es cuál."],
  "group define las unidades que se unen entre sí. Una línea por cada nivel de la variable.",
  ""),
 ("p04", "Paso 4 de 12 · Color", "color también es una estética",
  cadena(B3[:2] + ["§                     color = ocup))"], ["geom_line()"]), None,
  ["Si `color` se mapea a una variable **discreta**, ggplot2 **agrupa automáticamente** (ya no hace falta `group`).", "Asigna un color a cada categoría y **crea la leyenda solo**.", "Los colores por defecto son un punto de partida, no el resultado final."],
  "Una estética mapeada produce a la vez el atributo visual y su leyenda.",
  "Notar que se reemplazó group por color."),
 ("p05", "Paso 5 de 12 · Más capas", "Se pueden sumar tantas capas como se necesite",
  cadena(B4, ["geom_line()"], N(["geom_point()"])), None,
  ["`geom_point()` agrega los puntos de cada año encima de las líneas.", "Todas las capas **heredan** los datos y las estéticas de `ggplot()`: no hace falta repetirlos.", "Los puntos muestran que hay observaciones solo en cuatro años."],
  "Un gráfico de ggplot2 es una pila de capas. Cada + agrega una.",
  ""),
 ("p06", "Paso 6 de 12 · Estética o atributo fijo", "Dentro de aes() varía con los datos; fuera de aes() es igual para todo",
  ["pA <- ggplot(ocup_larga,", "§             aes(x = anio, y = personas, color = ocup)) +", "  geom_point(size = 3) + labs(title = \"A · color DENTRO de aes()\")", "", "pB <- ggplot(ocup_larga, aes(x = anio, y = personas)) +", "§  geom_point(size = 3, color = \"#D55E00\") +", "  labs(title = \"B · color FUERA de aes()\")", "", "pA | pB   # patchwork: dos gráficos lado a lado"], None,
  ["**A:** `color = ocup` está dentro de `aes()`: el color **depende** de la variable.", "**B:** `color = \"#D55E00\"` está fuera: es un **atributo fijo**, igual para todos los puntos.", "Si querés que un color represente datos, va dentro de `aes()`."],
  "Regla práctica: dentro de aes() lo que viene de los datos; fuera, lo que elegís vos.",
  "Mostrar que en B no hay leyenda: no hay variable asignada."),
 ("p07", "Paso 7 de 12 · Escalas (eje x)", "Las escalas controlan cómo se leen los ejes",
  cadena(B4, ["geom_line()"], ["geom_point()"], N(SX)), None,
  ["Cada estética tiene una **escala** (`scale_*`): traduce valores de los datos a posiciones, colores, etc.", "El eje de años mostraba valores como 2022,5. `breaks = 2022:2025` deja **solo los años reales**.", "Nombre de la función = `scale_` + estética + tipo de variable."],
  "Las escalas deciden las marcas, los límites y las etiquetas de cada eje y leyenda.",
  "Comparar con el paso 5: los años intermedios desaparecieron."),
 ("p08", "Paso 8 de 12 · Escalas (eje y)", "Formato legible para los números",
  cadena(B4, ["geom_line()"], ["geom_point()"], SX, N(SY)), None,
  ["`label_number()` da formato a las marcas del eje: **punto para miles**, coma para decimales.", "El eje pasa de `100000` a `100.000`.", "Los datos no cambian: solo cómo se **muestran**."],
  "Un buen formato numérico ahorra esfuerzo al lector y evita malinterpretar magnitudes.",
  ""),
 ("p09", "Paso 9 de 12 · Escala de color", "Colores elegidos a propósito, no los de fábrica",
  COLORES[:2] + ["§" + COLORES[2]], ["# … colores definidos arriba y capas anteriores …"] + [],
  ["`scale_color_manual()` asigna **un color a cada categoría**, con nombre.", "Paleta de **Okabe-Ito**: se distingue también con daltonismo y en blanco y negro.", "Los nombres del vector deben coincidir con los niveles de `ocup`."],
  "El color es un código: elegilo para distinguir, no para decorar (sesión 3).",
  ""),
 ("p10", "Paso 10 de 12 · Etiquetas de datos", "geom_text() escribe el valor en cada punto",
  [], None, [], "", ""),   # se completa abajo
 ("p11", "Paso 11 de 12 · Títulos", "labs() cuenta qué estamos viendo",
  [], None, [], "", ""),
 ("p12", "Paso 12 de 12 · Tema", "theme_*() y theme() ajustan el aspecto general",
  [], None, [], "", ""),
]

BASE_FULL = lambda extra=None: None  # (documentación)

def cod_p09():
    cod = COLORES + [""] + cadena(B4, ["geom_line()"], ["geom_point()"], SX, SY, N(SC))
    cod[0:3] = ["§" + l for l in COLORES]
    mostrar = ["§" + l for l in COLORES] + ["", "ggplot(ocup_larga, aes(x = anio, y = personas,", "                      color = ocup)) +", "  geom_line() + geom_point() +", "  # … escalas de x e y …"] + N(SC)
    return cod, mostrar

def cod_p10():
    cod = N(ETIQ) + [""] + cadena(B4, ["geom_line()"], ["geom_point()"], N(['geom_text(aes(label = etiqueta), vjust = -0.9,', '          size = 3, show.legend = FALSE)']), SX, SY2, SC)
    cod = N(ETIQ) + [""] + cadena(B4, ["geom_line()"], ["geom_point()"], N(['geom_text(aes(label = etiqueta), vjust = -0.9,', '          size = 3, show.legend = FALSE)']), SX, SY2[:2] + ["§" + SY2[2].replace("§", "")] if False else SY2, SC)
    mostrar = N(ETIQ) + ["", "ggplot(ocup_larga, aes(x = anio, y = personas,", "                      color = ocup)) +", "  geom_line() + geom_point() +"] + N(['  geom_text(aes(label = etiqueta), vjust = -0.9,', '            size = 3, show.legend = FALSE) +']) + ["  # … escalas de x, y y color …"]
    return cod, mostrar

def cod_p11():
    cuerpo = cadena(B4, ["geom_line()"], ["geom_point()"], ['geom_text(aes(label = etiqueta), vjust = -0.9,', '          size = 3, show.legend = FALSE)'], SX, SY2, SC, N(LABS))
    cod = ETIQ + [""] + cuerpo
    mostrar = ["# … datos, capas y escalas anteriores …", ""] + N(LABS)
    return cod, mostrar

def cod_p12():
    cuerpo = cadena(B4, ["geom_line()"], ["geom_point()"], ['geom_text(aes(label = etiqueta), vjust = -0.9,', '          size = 3, show.legend = FALSE)'], SX, SY2, SC, LABS, N(TEMA))
    cod = ETIQ + [""] + cuerpo
    mostrar = ["# … datos, capas, escalas y títulos anteriores …", ""] + N(TEMA)
    return cod, mostrar

for i, (k, fn) in enumerate([("p09", cod_p09), ("p10", cod_p10), ("p11", cod_p11), ("p12", cod_p12)]):
    idx = next(j for j, p in enumerate(PASOS_DEF) if p[0] == k)
    c, m = fn(); p = list(PASOS_DEF[idx]); p[3] = c; p[4] = m; PASOS_DEF[idx] = tuple(p)

# textos de los pasos 10-12 (explicación, mensaje, nota)
TXT = {
 "p10": (["`geom_text()` es otra capa: dibuja **texto** y toma su contenido de la estética `label`.", "`vjust = -0.9` sube el texto para que no tape el punto; `show.legend = FALSE` evita que aparezca una «a» en la leyenda.", "Así el lector lee el **valor exacto** sin estimarlo en el eje."],
         "Las etiquetas muestran el dato; el eje muestra la tendencia. Usalas cuando el valor importa.", "Se agregó también expand = expansion() en el eje y para dejar espacio arriba."),
 "p11": (["`labs()` agrega **título, subtítulo, nombres de ejes, leyenda y fuente**.", "El título conviene que diga el **mensaje** o al menos qué se mide y dónde.", "Siempre la **fuente** (`caption`): de dónde salen los datos."],
         "Un gráfico sin título ni fuente no se puede interpretar ni citar.", ""),
 "p12": (["`theme_minimal()` aplica un tema completo: quita el fondo gris y deja líneas suaves.", "`theme()` ajusta detalles: leyenda abajo, título en negrita.", "Esta es la **figura final** del ejercicio: 12 pasos, una capa por vez."],
         "Datos + estéticas + geometrías + escalas + títulos + tema: eso es una figura en ggplot2.", ""),
}
for k, (e, msg, nota) in TXT.items():
    idx = next(j for j, p in enumerate(PASOS_DEF) if p[0] == k)
    p = list(PASOS_DEF[idx]); p[5] = e; p[6] = msg; p[7] = nota; PASOS_DEF[idx] = tuple(p)

# otras figuras (no numeradas como pasos)
EXTRA = {
 "f_facetas": cadena(["ggplot(ocup_larga, aes(x = anio, y = personas, color = ocup))"], ["geom_line() + geom_point()"], SX, SC, N(['facet_wrap(~ ocup, scales = "free_y")']), ['theme_minimal() + theme(legend.position = "none")']),
 "f_barras": cadena(["ggplot(ocup_larga, aes(x = factor(anio), y = personas, fill = ocup))"], N(['geom_col(position = "dodge")']), ['scale_fill_manual(values = colores)'], SY, ['labs(x = "Año", y = "Personas estimadas", fill = "Situación")'], ["theme_minimal()"]),
 "f_piramide": ['piramide <- piramide |> mutate(grupo = forcats::fct_inorder(grupo))', "", "piramide |>", "  mutate(n = ifelse(sexo == \"Hombres\", -personas, personas)) |>", "  ggplot(aes(x = grupo, y = n, fill = sexo)) +", "  geom_col(width = 0.9) +", "§  coord_flip() +", '  scale_y_continuous(labels = ~ scales::label_number(', '                       big.mark = ".")(abs(.x))) +', '  scale_fill_manual(values = c(Hombres = "#0072B2",', '                               Mujeres = "#D55E00")) +', '  labs(title = "Concepción 2025: población por sexo y edad",', '       x = "Grupo de edad", y = "Personas estimadas", fill = NULL) +', "  theme_minimal()"],
}

def quitar_marcas(lineas): return [l[1:] if l.startswith("§") else l for l in lineas]

def escribir_pasos():
    PASOS.mkdir(parents=True, exist_ok=True)
    for p in PASOS.glob("*.R"): p.write_bytes(b"") if False else None
    for k, _, _, cod, *_ in PASOS_DEF:
        (PASOS / f"{k}.R").write_text("\n".join(quitar_marcas(cod)) + "\n", encoding="utf-8")
    for k, cod in EXTRA.items():
        (PASOS / f"{k}.R").write_text("\n".join(quitar_marcas(cod)) + "\n", encoding="utf-8")
    print("pasos escritos:", len(PASOS_DEF) + len(EXTRA))

if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "pasos"
    if modo == "pasos": escribir_pasos()
    elif modo == "pptx":
        from ggplot_pptx import construir
        construir()
