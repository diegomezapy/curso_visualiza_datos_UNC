/* Talleres 9 y 10. Los datos y territorios son ejemplos didácticos sintéticos. */
const PASOS = [
  {
    bloque: "1 · Datos desde cero", titulo: "Cargar valores manualmente",
    consigna: "Creá los valores 4, 6 y 10. Calculá su suma, guardala en respuesta y comprobá que hay tres observaciones.",
    esperado: 20, pistas: ["Primero construí un vector o una lista.", "R: c(4, 6, 10). Python: [4, 6, 10].", "Usá sum(valores)."],
    explicacion: "Tres observaciones suman 20; el siguiente paso generará datos nuevos.",
    codigo: { r: 'valores <- c(4, 6, 10)\nrespuesta <- NA_real_  # Calculá la suma.', python: 'valores = [4, 6, 10]\nrespuesta = None  # Calculá la suma.' }
  },
  {
    bloque: "1 · Datos desde cero", titulo: "Simular una muestra reproducible",
    consigna: "Generá 12 observaciones aleatorias con semilla 17. Guardá en respuesta la cantidad de observaciones y dibujá un histograma. Al repetirlo, la muestra debe mantenerse igual.",
    esperado: 12, grafico: true, pistas: ["Fijá la semilla antes de simular.", "R: set.seed(), rnorm(), hist(). Python: random.Random(), gauss(), plt.hist().", "Contá con length() o len() y activá el histograma."],
    explicacion: "La semilla permite reproducir la misma muestra sintética y revisar el histograma.",
    codigo: { r: 'set.seed(17)\nmuestra <- rnorm(12, mean = 10, sd = 2)\nrespuesta <- NA_integer_  # Cantidad de valores.\n# hist(muestra, col = "#56B4E9", main = "Muestra simulada", xlab = "Valor")', python: 'import random\nazar = random.Random(17)\nmuestra = [azar.gauss(10, 2) for _ in range(12)]\nrespuesta = None  # Cantidad de valores.\n# import matplotlib.pyplot as plt\n# plt.hist(muestra, color="#56B4E9")\n# plt.title("Muestra simulada")' }
  },
  {
    bloque: "1 · Datos desde cero", titulo: "Importar un CSV sencillo",
    consigna: "Leé el archivo de seis meses. Sumá la columna ventas en respuesta y trazá la serie. Los datos son sintéticos y están disponibles como datos.csv al ejecutar.",
    csv: "datos-codigo/taller_serie.csv", esperado: 135, grafico: true,
    pistas: ["Importá el CSV antes de calcular.", "R: read.csv('datos.csv'). Python: csv.DictReader().", "Convertí ventas a número antes de sumarlas y trazá mes frente a ventas."],
    explicacion: "La suma de la serie es 135. Separar archivo, cálculo y gráfico facilita revisar el resultado.",
    codigo: { r: 'datos <- read.csv("datos.csv")\nrespuesta <- NA_real_  # Suma de ventas.\n# plot(datos$mes, datos$ventas, type="b", pch=19, xlab="Mes", ylab="Ventas")', python: 'import csv\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\nrespuesta = None  # Suma de ventas.\n# import matplotlib.pyplot as plt\n# plt.plot([int(f["mes"]) for f in datos], [int(f["ventas"]) for f in datos], marker="o")\n# plt.xlabel("Mes"); plt.ylabel("Ventas")' }
  },
  {
    bloque: "2 · Construir una figura por capas", titulo: "Primera capa: puntos",
    consigna: "Construí un diagrama de dispersión para x = 1 a 5 e y = 2, 4, 5, 7, 9. Guardá en respuesta cuántos puntos hay. En R, iniciá ggplot() y agregá geom_point(); en Python, usá scatter().",
    esperado: 5, grafico: true, ggplot: true,
    pistas: ["Un gráfico empieza con datos y ejes.", "R: ggplot(datos, aes(x, y)) + geom_point(). Python: plt.scatter(x, y).", "En R usá print(p) para que la figura aparezca en el aula."],
    explicacion: "La primera capa sitúa cinco observaciones. Luego se codificará un grupo con color.",
    codigo: { r: 'library(ggplot2)\ndatos <- data.frame(x=1:5, y=c(2,4,5,7,9))\nrespuesta <- NA_integer_  # Número de puntos.\n# p <- ggplot(datos, aes(x, y)) + geom_point(size=3)\n# print(p)', python: 'import matplotlib.pyplot as plt\nx = [1, 2, 3, 4, 5]\ny = [2, 4, 5, 7, 9]\nrespuesta = None  # Número de puntos.\n# plt.scatter(x, y, s=70)' }
  },
  {
    bloque: "2 · Construir una figura por capas", titulo: "Segunda capa: color por grupo",
    consigna: "Usá los mismos cinco puntos y separá A = primeros dos, B = últimos tres. Guardá en respuesta el grupo con mayor media de y. Mostrá los grupos con colores y una leyenda.",
    esperado: "B", grafico: true, ggplot: true,
    pistas: ["La media de A es 3 y la de B es 7.", "R: aes(colour=grupo) en geom_point(). Python: scatter() por cada grupo y legend().", "El color representa grupo; mantené el mismo eje para comparar."],
    explicacion: "B tiene media 7 y A tiene media 3. La codificación por color agrega una dimensión sin cambiar los datos.",
    codigo: { r: 'library(ggplot2)\ndatos <- data.frame(x=1:5, y=c(2,4,5,7,9), grupo=c("A","A","B","B","B"))\nrespuesta <- NA_character_  # Grupo con mayor media.\n# p <- ggplot(datos, aes(x, y)) + geom_point(aes(colour=grupo), size=3)\n# print(p)', python: 'import matplotlib.pyplot as plt\nx = [1, 2, 3, 4, 5]\ny = [2, 4, 5, 7, 9]\ngrupo = ["A", "A", "B", "B", "B"]\nrespuesta = None  # Grupo con mayor media.\n# for g, color in [("A", "#0072B2"), ("B", "#E69F00")]:\n#     pares = [(a,b) for a,b,c in zip(x,y,grupo) if c==g]\n#     plt.scatter([a for a,b in pares], [b for a,b in pares], label=g, color=color)\n# plt.legend()' }
  },
  {
    bloque: "2 · Construir una figura por capas", titulo: "Tercera capa: recta de regresión",
    consigna: "Con x = 1, 2, 3 e y = 2, 4, 6, calculá la pendiente de la regresión lineal y guardala en respuesta. Mostrá puntos y recta ajustada. Describí una asociación, sin afirmar causalidad.",
    esperado: 2, grafico: true, ggplot: true,
    pistas: ["Cuando x aumenta 1, y aumenta 2 en estos datos.", "R: coef(lm(y ~ x, datos))[2] y geom_smooth(method='lm'). Python: statistics.linear_regression().", "La recta es y = 2x; el gráfico necesita puntos y línea."],
    explicacion: "La pendiente es 2. Una recta ajustada describe la asociación observada y no demuestra un efecto causal.",
    codigo: { r: 'library(ggplot2)\ndatos <- data.frame(x=1:3, y=c(2,4,6))\nmodelo <- lm(y ~ x, data=datos)\nrespuesta <- NA_real_  # Pendiente del modelo.\n# p <- ggplot(datos, aes(x,y)) + geom_point(size=3) + geom_smooth(method="lm", se=FALSE)\n# print(p)', python: 'import statistics\nimport matplotlib.pyplot as plt\nx = [1, 2, 3]\ny = [2, 4, 6]\npendiente, intercepto = statistics.linear_regression(x, y)\nrespuesta = None  # Pendiente.\n# plt.scatter(x,y)\n# plt.plot(x, [intercepto + pendiente*v for v in x], color="#D55E00")' }
  },
  {
    bloque: "3 · Gráficos analíticos", titulo: "Serie de tiempo: tendencia mensual",
    consigna: "Importá los seis meses del CSV. Guardá en respuesta el mes con la mayor venta (como número) y graficá la serie como línea con puntos, ejes y título.",
    csv: "datos-codigo/taller_serie.csv", esperado: 6, grafico: true, ggplot: true,
    pistas: ["El máximo está en la última fila.", "R: which.max(datos$ventas), geom_line() y geom_point(). Python: max(datos, key=...).", "Mes debe ir en el eje horizontal; ventas en el vertical."],
    explicacion: "El mes 6 tiene el máximo. La línea conecta períodos ordenados, sin rellenar meses ausentes.",
    codigo: { r: 'library(ggplot2)\ndatos <- read.csv("datos.csv")\nrespuesta <- NA_integer_  # Mes con máximo de ventas.\n# p <- ggplot(datos, aes(mes, ventas)) + geom_line(colour="#0072B2") + geom_point(size=2) + labs(title="Ventas mensuales", x="Mes", y="Ventas")\n# print(p)', python: 'import csv\nimport matplotlib.pyplot as plt\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\nrespuesta = None  # Número del mes máximo.\n# plt.plot([int(f["mes"]) for f in datos], [int(f["ventas"]) for f in datos], marker="o")\n# plt.title("Ventas mensuales"); plt.xlabel("Mes"); plt.ylabel("Ventas")' }
  },
  {
    bloque: "3 · Gráficos analíticos", titulo: "Mapa de calor: departamento y distrito",
    consigna: "Importá los datos territoriales sintéticos. Guardá en respuesta el distrito con el valor más alto. Creá un mapa de calor en cuadrícula: departamento en columnas, distrito en filas y color según valor. Es una matriz, no una coropleta geográfica.",
    csv: "datos-codigo/taller_territorios.csv", esperado: "Yby Yaú", grafico: true, ggplot: true,
    pistas: ["Compará la columna valor entre distritos.", "R: geom_tile(aes(fill=valor)). Python: imshow() con una matriz de 4 × 2 y colorbar().", "Las celdas sin distrito para un departamento deben quedar vacías, no con valor cero."],
    explicacion: "Yby Yaú tiene 60. La cuadrícula compara categorías territoriales; no representa ubicación, tamaño ni límites reales.",
    codigo: { r: 'library(ggplot2)\ndatos <- read.csv("datos.csv", fileEncoding="UTF-8")\nrespuesta <- NA_character_  # Distrito con valor máximo.\n# p <- ggplot(datos, aes(departamento, distrito, fill=valor)) + geom_tile(colour="white") + scale_fill_gradient(low="#d8f0fa", high="#005a8e") + labs(title="Indicador sintético por distrito", x="Departamento", y="Distrito")\n# print(p)', python: 'import csv\nimport matplotlib.pyplot as plt\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\nrespuesta = None  # Distrito con valor máximo.\n# departamentos = ["Concepción", "Central"]\n# distritos = ["Horqueta", "Yby Yaú", "Luque", "Capiatá"]\n# matriz = [[float("nan") for _ in departamentos] for _ in distritos]\n# for fila in datos:\n#     matriz[distritos.index(fila["distrito"])][departamentos.index(fila["departamento"])] = float(fila["valor"])\n# plt.imshow(matriz, cmap="YlOrRd", aspect="auto")\n# plt.xticks(range(2), departamentos); plt.yticks(range(4), distritos)\n# plt.colorbar(label="Valor")' }
  },
  {
    bloque: "3 · Gráficos analíticos", titulo: "Escala Likert divergente",
    consigna: "Las respuestas sintéticas son 1 muy en desacuerdo, 2 en desacuerdo, 3 neutral, 4 de acuerdo y 5 muy de acuerdo. Guardá en respuesta el total favorable y dibujá una barra Likert apilada: desacuerdo a la izquierda, neutral centrado y acuerdo a la derecha.",
    esperado: 9, grafico: true, ggplot: true,
    pistas: ["Favorables = de acuerdo + muy de acuerdo.", "Los extremos acumulados de los cinco segmentos son -4,5; -3,5; -1,5; 1,5; 5,5; 10,5.", "R: geom_rect() con xmin/xmax. Python: barh() con el argumento left. El neutral cruza cero."],
    explicacion: "Las categorías favorables suman 9. El neutral se centra en cero y los segmentos muestran frecuencias sin deformarlas.",
    codigo: { r: 'library(ggplot2)\ndatos <- data.frame(categoria=c("Muy en desacuerdo","En desacuerdo","Neutral","De acuerdo","Muy de acuerdo"), conteo=c(1,2,3,4,5), xmin=c(-4.5,-3.5,-1.5,1.5,5.5), xmax=c(-3.5,-1.5,1.5,5.5,10.5))\nrespuesta <- NA_integer_  # Suma de las dos categorías favorables.\n# p <- ggplot(datos) + geom_rect(aes(xmin=xmin, xmax=xmax, ymin=0, ymax=1, fill=categoria), colour="white") + geom_vline(xintercept=0) + labs(title="Escala Likert", x="Frecuencia centrada", y=NULL) + theme_minimal() + theme(axis.text.y=element_blank())\n# print(p)', python: 'import matplotlib.pyplot as plt\ncategorias = ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"]\nconteos = [1, 2, 3, 4, 5]\ninicios = [-4.5, -3.5, -1.5, 1.5, 5.5]\nrespuesta = None  # Total favorable.\n# for categoria, ancho, inicio, color in zip(categorias, conteos, inicios, ["#D55E00", "#E69F00", "#999999", "#56B4E9", "#0072B2"]):\n#     plt.barh(["Respuesta"], [ancho], left=[inicio], label=categoria, color=color)\n# plt.axvline(0, color="black"); plt.xlabel("Frecuencia centrada")\n# plt.legend()' }
  },
  {
    bloque: "4 · Refinar y comparar", titulo: "Facetas para dos grupos",
    consigna: "Usá dos grupos de tres observaciones. Guardá en respuesta cuántos grupos hay y creá una figura con un panel por grupo, manteniendo la misma escala para compararlos.",
    esperado: 2, grafico: true, ggplot: true,
    pistas: ["Hay A y B.", "R: facet_wrap(~grupo). Python: plt.subplots(1, 2).", "Definí el mismo límite vertical en los dos paneles."],
    explicacion: "Dos facetas permiten comparar patrones sin superponer las series.",
    codigo: { r: 'library(ggplot2)\ndatos <- data.frame(x=rep(1:3,2), y=c(2,3,5,4,6,8), grupo=rep(c("A","B"), each=3))\nrespuesta <- NA_integer_  # Número de grupos.\n# p <- ggplot(datos, aes(x,y)) + geom_line() + geom_point() + facet_wrap(~grupo) + coord_cartesian(ylim=c(0,9))\n# print(p)', python: 'import matplotlib.pyplot as plt\ngrupo = {"A": [2,3,5], "B": [4,6,8]}\nrespuesta = None  # Número de grupos.\n# fig, ejes = plt.subplots(1, 2, figsize=(8,3), sharey=True)\n# for eje, (nombre, valores) in zip(ejes, grupo.items()):\n#     eje.plot([1,2,3], valores, marker="o"); eje.set_title(nombre); eje.set_ylim(0,9)\n# fig.tight_layout()' }
  },
  {
    bloque: "4 · Refinar y comparar", titulo: "Modificar etiquetas, tema y anotaciones",
    consigna: "Retomá la serie de cinco puntos. Guardá en respuesta el valor máximo de y. Añadí título, nombres de ejes, un tema legible y una anotación que marque ese máximo.",
    esperado: 9, grafico: true, ggplot: true,
    pistas: ["El máximo de y es 9.", "R: labs(), theme_minimal() y annotate(). Python: title(), xlabel(), ylabel() y annotate().", "La anotación corresponde al punto (5, 9)."],
    explicacion: "La anotación conduce la mirada al máximo sin alterar la escala ni el dato.",
    codigo: { r: 'library(ggplot2)\ndatos <- data.frame(x=1:5, y=c(2,4,5,7,9))\nrespuesta <- NA_real_  # Máximo de y.\n# p <- ggplot(datos, aes(x,y)) + geom_line(colour="#0072B2") + geom_point() + labs(title="Evolución observada", x="Período", y="Valor") + theme_minimal() + annotate("text", x=5, y=9, label="Máximo", hjust=1, vjust=-.5)\n# print(p)', python: 'import matplotlib.pyplot as plt\nx = [1,2,3,4,5]\ny = [2,4,5,7,9]\nrespuesta = None  # Máximo de y.\n# plt.plot(x,y,marker="o",color="#0072B2")\n# plt.title("Evolución observada"); plt.xlabel("Período"); plt.ylabel("Valor")\n# plt.annotate("Máximo", (5,9), xytext=(4,9.5), arrowprops={"arrowstyle":"->"})' }
  },
  {
    bloque: "4 · Refinar y comparar", titulo: "Figura final con datos importados",
    consigna: "Importá las series sintéticas Norte y Sur. Guardá en respuesta el grupo cuyo valor creció más entre el primer y último período. Completá una figura con ambas series, puntos, leyenda, título y escala vertical desde cero.",
    csv: "datos-codigo/taller_grupos.csv", esperado: "Norte", grafico: true, ggplot: true,
    pistas: ["Compará último menos primero dentro de cada grupo.", "R: subset() y ggplot() + geom_line() + geom_point(). Python: agrupar filas y plt.plot() por grupo.", "Norte pasa de 10 a 30; Sur de 20 a 25."],
    explicacion: "Norte crece 20 y Sur crece 5. La figura final combina importación, cálculo, capas, leyenda y escala.",
    codigo: { r: 'library(ggplot2)\ndatos <- read.csv("datos.csv")\nrespuesta <- NA_character_  # Grupo con mayor aumento.\n# p <- ggplot(datos, aes(periodo, valor, colour=grupo)) + geom_line() + geom_point(size=3) + scale_y_continuous(limits=c(0,35)) + labs(title="Cambio por grupo", x="Período", y="Valor") + theme_minimal()\n# print(p)', python: 'import csv\nimport matplotlib.pyplot as plt\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\nrespuesta = None  # Grupo con mayor aumento.\n# for grupo, color in [("Norte", "#0072B2"), ("Sur", "#E69F00")]:\n#     filas = [f for f in datos if f["grupo"] == grupo]\n#     plt.plot([int(f["periodo"]) for f in filas], [int(f["valor"]) for f in filas], marker="o", label=grupo, color=color)\n# plt.ylim(0,35); plt.xlabel("Período"); plt.ylabel("Valor")\n# plt.title("Cambio por grupo"); plt.legend()' }
  }
];

export const RETOS_TALLERES = [
  ...PASOS.map((p, i) => ({ ...p, n: 9, id: `taller_r_${i + 1}`, paso: i + 1 })),
  ...PASOS.map((p, i) => ({ ...p, n: 10, id: `taller_python_${i + 1}`, paso: i + 1 }))
];
