"""Fuente de verdad del cuestionario diagnóstico (sesión 1). Se usa para generar:
la página del cuestionario, el tablero, el script de Google Apps Script y los datos de ejemplo."""

AREAS = ["Ingeniería", "Ciencias exactas", "Informática / Sistemas", "Ciencias económicas / Administración", "Salud", "Educación", "Otra"]
EXPERIENCIA = ["Ninguna", "Menos de 1 año", "1 a 3 años", "Más de 3 años"]
HERRAMIENTAS = ["Excel / Google Sheets", "Python", "R / RStudio", "SQL", "Power BI / Tableau / Looker", "Google Colab / Jupyter", "Ninguna"]

# Autoevaluación 1 (nunca lo hice) a 5 (lo hago con soltura)
AUTO = [
 ("au_python", "Programar en Python"),
 ("au_r", "Programar en R"),
 ("au_datos", "Manipular datos (pandas / dplyr)"),
 ("au_graf_py", "Graficar con matplotlib, seaborn o plotly"),
 ("au_graf_r", "Graficar con ggplot2"),
 ("au_colab", "Usar Google Colab o Jupyter"),
 ("au_rstudio", "Usar RStudio y R Markdown"),
 ("au_tablero", "Construir dashboards / tableros"),
 ("au_diseno", "Criterios de diseño visual (color, escalas, ética)"),
]

# id, tema (viz|py|r), enunciado, opciones, índice correcto (0-3), explicación
PREGUNTAS = [
 ("V1", "viz", "Un gráfico de barras cuyo eje Y empieza en 96 en lugar de 0…",
  ["Ahorra espacio sin cambiar el mensaje", "Exagera visualmente las diferencias entre las barras", "Es obligatorio cuando los valores son altos", "Mejora la precisión de lectura"], 1,
  "En barras la longitud codifica el valor: truncar el eje exagera las diferencias."),
 ("V2", "viz", "¿Qué codificación visual se percibe con mayor precisión?",
  ["Posición sobre una escala común", "Ángulo (como en una torta)", "Área", "Saturación del color"], 0,
  "Cleveland y McGill: posición > longitud > ángulo > área > color."),
 ("V3", "viz", "Para comparar la distribución de notas entre tres carreras conviene…",
  ["Una torta por carrera", "Un área apilada", "Cajas o violines por carrera", "Un gráfico de radar"], 2,
  "Caja/violín muestran forma, centro y dispersión de cada grupo con la misma escala."),
 ("V4", "viz", "Para una variable con un punto neutro (por ejemplo, variación respecto a una meta) la paleta adecuada es…",
  ["Cualitativa", "Secuencial", "Divergente, centrada en el punto neutro", "Arcoíris"], 2,
  "La paleta divergente separa lo positivo de lo negativo alrededor del valor neutro."),
 ("P1", "py", "En pandas, df.groupby('sucursal')['ventas'].sum() devuelve…",
  ["La suma de ventas por sucursal", "Las ventas ordenadas por sucursal", "Solo las filas de la primera sucursal", "El número de sucursales"], 0,
  "groupby agrupa por sucursal y .sum() suma la columna ventas dentro de cada grupo."),
 ("P2", "py", "fig, ax = plt.subplots(1, 3) en matplotlib crea…",
  ["Tres figuras separadas", "Una figura con tres ejes (paneles) en una fila", "Un gráfico con tres series", "Una figura de 1×3 píxeles"], 1,
  "subplots(1, 3) devuelve una figura y un arreglo de 3 ejes dispuestos en 1 fila."),
 ("P3", "py", "En seaborn, para ver la distribución de una variable por grupo con forma de densidad usarías…",
  ["sns.lineplot", "sns.heatmap", "sns.regplot", "sns.violinplot"], 3,
  "violinplot combina un estimador de densidad con resumen por grupo."),
 ("P4", "py", "¿Qué hace pd.read_csv('datos.csv', parse_dates=['fecha'])?",
  ["Lee solo la columna fecha", "Ordena el archivo por fecha", "Lee el CSV y convierte la columna fecha a tipo fecha/hora", "Elimina las fechas duplicadas"], 2,
  "parse_dates convierte las columnas indicadas a datetime al leer el archivo."),
 ("R1", "r", "En R, el operador %>% (o |>) sirve para…",
  ["Pasar el resultado de una expresión como primer argumento de la siguiente", "Comparar dos vectores", "Calcular porcentajes", "Crear un bucle"], 0,
  "El pipe encadena operaciones: x %>% f() equivale a f(x)."),
 ("R2", "r", "En ggplot2 las capas de un gráfico se combinan con…",
  ["El operador %>%", "El operador +", "El operador &", "Punto y coma"], 1,
  "ggplot(...) + geom_...() + theme_...(): las capas se suman con +."),
 ("R3", "r", "geom_col() frente a geom_bar(): la diferencia principal es que…",
  ["geom_col dibuja barras horizontales", "geom_bar solo acepta fechas", "geom_col usa los valores de y tal cual; geom_bar cuenta filas por defecto", "No hay ninguna diferencia"], 2,
  "geom_bar() usa stat_count por defecto; geom_col() usa stat_identity (alturas dadas)."),
 ("R4", "r", "En RStudio, ¿qué botón genera el HTML de un documento R Markdown?",
  ["Run App", "Source", "Commit", "Knit"], 3,
  "Knit ejecuta el código y compila el documento al formato indicado (HTML, PDF, Word)."),
]
TEMAS = {"viz": "Visualización (conceptos)", "py": "Python", "r": "R"}
LETRAS = "ABCD"
def nivel(total):  # total de 0 a 12
    return "Inicial" if total <= 4 else "Intermedio" if total <= 8 else "Avanzado"
COLUMNAS = (["ts", "pid", "area", "cohorte", "experiencia", "herramientas"] + [a for a, _ in AUTO]
            + ["a_" + p[0] for p in PREGUNTAS] + ["ok_" + p[0] for p in PREGUNTAS]
            + ["score_viz", "score_py", "score_r", "score_total", "nivel", "comentario"])
PUBLICAS = [c for c in COLUMNAS if c not in ("pid", "comentario")]   # columnas que expone el endpoint de datos
