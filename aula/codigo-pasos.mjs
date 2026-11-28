/* Nueve microprácticas por unidad. El reto original de codigo-retos.mjs es el paso 10. */

const CSV = {
  3: "datos-codigo/etica.csv",
  4: "datos-codigo/kpis.csv",
  5: "datos-codigo/sucursales.csv",
  7: "datos-codigo/territorios.csv",
  8: "datos-codigo/integrador.csv"
};
const CSV_DESDE = { 3: 4, 4: 5, 5: 5, 7: 5, 8: 5 };

const MANUAL = {
  1: {
    r: "valores <- c(2, 2, 2, 10)",
    python: "valores = [2, 2, 2, 10]"
  },
  2: {
    r: 'categorias <- c("A", "B", "C", "B", "A", "B")',
    python: 'categorias = ["A", "B", "C", "B", "A", "B"]'
  },
  3: {
    r: "valores <- c(A = 96, B = 100)",
    python: 'valores = {"A": 96, "B": 100}'
  },
  4: {
    r: "antes <- c(A = 50, B = 30, C = 20)\ndespues <- c(A = 55, B = 42, C = 23)",
    python: 'antes = {"A": 50, "B": 30, "C": 20}\ndespues = {"A": 55, "B": 42, "C": 23}'
  },
  5: {
    r: "ventas_2024 <- c(Norte = 100, Sur = 120)\nventas_2025 <- c(Norte = 130, Sur = 150)",
    python: 'ventas_2024 = {"Norte": 100, "Sur": 120}\nventas_2025 = {"Norte": 130, "Sur": 150}'
  },
  6: {
    r: "ventas <- c(120, 200)\ncostos <- c(90, 100)",
    python: "ventas = [120, 200]\ncostos = [90, 100]"
  },
  7: {
    r: "casos <- c(A = 40, B = 30)\npoblacion <- c(A = 100000, B = 30000)",
    python: 'casos = {"A": 40, "B": 30}\npoblacion = {"A": 100000, "B": 30000}'
  },
  8: {
    r: "norte_antes <- c(80, 90)\nnorte_despues <- c(100, 99)\nsur_antes <- c(100, 120)\nsur_despues <- c(90, 110)",
    python: "norte_antes = [80, 90]\nnorte_despues = [100, 99]\nsur_antes = [100, 120]\nsur_despues = [90, 110]"
  }
};

const LECTURA_CSV = {
  r: 'datos <- read.csv("datos.csv")',
  python: 'import csv\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))'
};

const GRAFICOS = {
  1: {
    7: { r: 'stripchart(valores, method = "stack", pch = 19, col = "#0072B2", xlab = "Valor", main = "Valores individuales")', python: 'import matplotlib.pyplot as plt\nplt.scatter(valores, [0] * len(valores), color="#0072B2")\nplt.xlabel("Valor")' },
    8: { r: 'hist(valores, breaks = c(0, 4, 8, 12), col = "#56B4E9", xlab = "Valor", main = "Distribución")', python: 'import matplotlib.pyplot as plt\nplt.hist(valores, bins=[0, 4, 8, 12], color="#56B4E9")\nplt.xlabel("Valor")' },
    9: { r: 'barplot(c(mean(valores), mean(valores[valores < max(valores)])), names.arg = c("Todos", "Sin 10"), ylim = c(0, 5), col = "#0072B2", ylab = "Media")', python: 'import matplotlib.pyplot as plt\nplt.bar(["Todos", "Sin 10"], [sum(valores)/len(valores), sum(v for v in valores if v < max(valores))/sum(v < max(valores) for v in valores)], color="#0072B2")\nplt.ylabel("Media")' }
  },
  2: {
    7: { r: 'barplot(table(factor(categorias, levels = c("A", "B", "C"))), col = "#0072B2", ylab = "Frecuencia")', python: 'import matplotlib.pyplot as plt\nplt.bar(["A", "B", "C"], [categorias.count(x) for x in ["A", "B", "C"]], color="#0072B2")\nplt.ylabel("Frecuencia")' },
    8: { r: 'conteos <- sort(table(categorias), decreasing = TRUE)\nbarplot(conteos, col = "#0072B2", ylab = "Frecuencia")', python: 'import matplotlib.pyplot as plt\norden = sorted(set(categorias), key=lambda x: (-categorias.count(x), x))\nplt.bar(orden, [categorias.count(x) for x in orden], color="#0072B2")\nplt.ylabel("Frecuencia")' },
    9: { r: 'porcentajes <- prop.table(table(categorias)) * 100\nbarplot(porcentajes, ylim = c(0, 60), col = "#0072B2", ylab = "%")', python: 'import matplotlib.pyplot as plt\nplt.bar(["A", "B", "C"], [categorias.count(x)/len(categorias)*100 for x in ["A", "B", "C"]], color="#0072B2")\nplt.ylabel("%")' }
  },
  3: {
    7: { r: 'barplot(datos$valor, names.arg = datos$categoria, ylim = c(0, 110), col = "#0072B2", ylab = "Valor")', python: 'import matplotlib.pyplot as plt\nplt.bar([f["categoria"] for f in datos], [float(f["valor"]) for f in datos], color="#0072B2")\nplt.ylim(bottom=0)\nplt.ylabel("Valor")' },
    8: { r: 'barplot(datos$valor, names.arg = datos$categoria, ylim = c(90, 105), col = "#D55E00", ylab = "Valor", main = "Eje recortado: compará su efecto")', python: 'import matplotlib.pyplot as plt\nplt.bar([f["categoria"] for f in datos], [float(f["valor"]) for f in datos], color="#D55E00")\nplt.ylim(90, 105)\nplt.ylabel("Valor: eje recortado")' },
    9: { r: 'barras <- barplot(datos$valor, names.arg = datos$categoria, ylim = c(0, 110), col = "#0072B2", ylab = "Valor")\ntext(barras, datos$valor + 3, labels = datos$valor)', python: 'import matplotlib.pyplot as plt\nplt.bar([f["categoria"] for f in datos], [float(f["valor"]) for f in datos], color="#0072B2")\nplt.ylim(bottom=0)\nfor f in datos: plt.text(f["categoria"], float(f["valor"])+2, f["valor"], ha="center")' }
  },
  4: {
    7: { r: 'barplot(datos$antes, names.arg = datos$sector, col = "#56B4E9", ylab = "Antes")', python: 'import matplotlib.pyplot as plt\nplt.bar([f["sector"] for f in datos], [int(f["antes"]) for f in datos], color="#56B4E9")\nplt.ylabel("Antes")' },
    8: { r: 'barplot(rbind(datos$antes, datos$despues), beside = TRUE, names.arg = datos$sector, col = c("#56B4E9", "#E69F00"), ylab = "Unidades")\nlegend("topright", c("Antes", "Después"), fill = c("#56B4E9", "#E69F00"))', python: 'import matplotlib.pyplot as plt\nx = list(range(len(datos)))\nplt.bar([i-.2 for i in x], [int(f["antes"]) for f in datos], width=.4, label="Antes")\nplt.bar([i+.2 for i in x], [int(f["despues"]) for f in datos], width=.4, label="Después")\nplt.xticks(x, [f["sector"] for f in datos])\nplt.legend()' },
    9: { r: 'aumentos <- datos$despues - datos$antes\nbarplot(aumentos, names.arg = datos$sector, col = "#009E73", ylab = "Aumento")', python: 'import matplotlib.pyplot as plt\nplt.bar([f["sector"] for f in datos], [int(f["despues"])-int(f["antes"]) for f in datos], color="#009E73")\nplt.ylabel("Aumento")' }
  },
  5: {
    7: { r: 'd <- subset(datos, anio == 2025)\nbarplot(d$ventas, names.arg = d$sucursal, col = "#0072B2", ylab = "Ventas 2025")', python: 'import matplotlib.pyplot as plt\nd = [f for f in datos if int(f["anio"]) == 2025]\nplt.bar([f["sucursal"] for f in d], [int(f["ventas"]) for f in d], color="#0072B2")\nplt.ylabel("Ventas 2025")' },
    8: { r: 'matriz <- rbind(subset(datos, anio == 2024)$ventas, subset(datos, anio == 2025)$ventas)\nbarplot(matriz, beside = TRUE, names.arg = c("Norte", "Sur"), col = c("#56B4E9", "#E69F00"), ylab = "Ventas")\nlegend("topleft", c("2024", "2025"), fill = c("#56B4E9", "#E69F00"))', python: 'import matplotlib.pyplot as plt\nplt.bar(["Norte 2024", "Sur 2024", "Norte 2025", "Sur 2025"], [int(f["ventas"]) for f in datos], color=["#56B4E9", "#56B4E9", "#E69F00", "#E69F00"])\nplt.xticks(rotation=20)\nplt.ylabel("Ventas")' },
    9: { r: 'd <- subset(datos, anio == 2025)\nbarplot(d$ventas, names.arg = d$sucursal, col = "#009E73", ylab = "Ventas filtradas: 2025")', python: 'import matplotlib.pyplot as plt\nd = [f for f in datos if int(f["anio"]) == 2025]\nplt.bar([f["sucursal"] for f in d], [int(f["ventas"]) for f in d], color="#009E73")\nplt.ylabel("Ventas filtradas: 2025")' }
  },
  6: {
    7: { r: 'margenes <- (ventas - costos) / ventas * 100\nbarplot(margenes, names.arg = c("Caso 1", "Caso 2"), ylim = c(0, 60), col = "#009E73", ylab = "Margen (%)")', python: 'import matplotlib.pyplot as plt\nmargenes = [(v-c)/v*100 for v,c in zip(ventas,costos)]\nplt.bar(["Caso 1", "Caso 2"], margenes, color="#009E73")\nplt.ylabel("Margen (%)")' },
    8: { r: 'barplot(rbind(ventas, costos), beside = TRUE, names.arg = c("Caso 1", "Caso 2"), col = c("#56B4E9", "#E69F00"), ylab = "Unidades")\nlegend("topleft", c("Ventas", "Costos"), fill = c("#56B4E9", "#E69F00"))', python: 'import matplotlib.pyplot as plt\nx = [0,1]\nplt.bar([i-.2 for i in x], ventas, width=.4, label="Ventas")\nplt.bar([i+.2 for i in x], costos, width=.4, label="Costos")\nplt.xticks(x, ["Caso 1", "Caso 2"])\nplt.legend()' },
    9: { r: 'margen <- function(ventas, costo) (ventas - costo) / ventas * 100\nbarplot(c(margen(120,90), margen(200,100), margen(80,60)), names.arg = c("1", "2", "3"), ylim = c(0,60), col = "#009E73", ylab = "Margen (%)")', python: 'import matplotlib.pyplot as plt\ndef margen(ventas, costo): return (ventas-costo)/ventas*100\nplt.bar(["1", "2", "3"], [margen(120,90), margen(200,100), margen(80,60)], color="#009E73")\nplt.ylabel("Margen (%)")' }
  },
  7: {
    7: { r: 'barplot(datos$casos, names.arg = datos$territorio, col = "#56B4E9", ylab = "Casos")', python: 'import matplotlib.pyplot as plt\nplt.bar([f["territorio"] for f in datos], [int(f["casos"]) for f in datos], color="#56B4E9")\nplt.ylabel("Casos")' },
    8: { r: 'tasas <- datos$casos / datos$poblacion * 100000\nbarplot(tasas, names.arg = datos$territorio, col = "#009E73", ylab = "Tasa por 100.000")', python: 'import matplotlib.pyplot as plt\ntasas = [int(f["casos"])/int(f["poblacion"])*100000 for f in datos]\nplt.bar([f["territorio"] for f in datos], tasas, color="#009E73")\nplt.ylabel("Tasa por 100.000")' },
    9: { r: 'tasas <- datos$casos / datos$poblacion * 100000\nplot(datos$lon, datos$lat, cex = tasas/30, pch = 19, col = "#0072B2", xlab = "Longitud", ylab = "Latitud")\ntext(datos$lon, datos$lat, labels = datos$territorio, pos = 3)', python: 'import matplotlib.pyplot as plt\ntasas = [int(f["casos"])/int(f["poblacion"])*100000 for f in datos]\nplt.scatter([float(f["lon"]) for f in datos], [float(f["lat"]) for f in datos], s=[t*8 for t in tasas], color="#0072B2")\nfor f in datos: plt.annotate(f["territorio"], (float(f["lon"]), float(f["lat"])))\nplt.xlabel("Longitud"); plt.ylabel("Latitud")' }
  },
  8: {
    7: { r: 'd <- subset(datos, grupo == "Norte")\nmatplot(d$periodo, cbind(d$antes, d$despues), type = "b", pch = 19, lty = 1, col = c("#56B4E9", "#E69F00"), xlab = "Período", ylab = "Valor", main = "Norte")\nlegend("topleft", c("Antes", "Después"), col = c("#56B4E9", "#E69F00"), lty = 1)', python: 'import matplotlib.pyplot as plt\nd = [f for f in datos if f["grupo"] == "Norte"]\nplt.plot([int(f["periodo"]) for f in d], [int(f["antes"]) for f in d], marker="o", label="Antes")\nplt.plot([int(f["periodo"]) for f in d], [int(f["despues"]) for f in d], marker="o", label="Después")\nplt.title("Norte"); plt.xlabel("Período"); plt.legend()' },
    8: { r: 'd <- subset(datos, grupo == "Sur")\nmatplot(d$periodo, cbind(d$antes, d$despues), type = "b", pch = 19, lty = 1, col = c("#56B4E9", "#E69F00"), xlab = "Período", ylab = "Valor", main = "Sur")\nlegend("topleft", c("Antes", "Después"), col = c("#56B4E9", "#E69F00"), lty = 1)', python: 'import matplotlib.pyplot as plt\nd = [f for f in datos if f["grupo"] == "Sur"]\nplt.plot([int(f["periodo"]) for f in d], [int(f["antes"]) for f in d], marker="o", label="Antes")\nplt.plot([int(f["periodo"]) for f in d], [int(f["despues"]) for f in d], marker="o", label="Después")\nplt.title("Sur"); plt.xlabel("Período"); plt.legend()' },
    9: { r: 'par(mfrow = c(1, 2))\nfor (g in c("Norte", "Sur")) {\n  d <- subset(datos, grupo == g)\n  matplot(d$periodo, cbind(d$antes, d$despues), type = "b", pch = 19, lty = 1, col = c("#56B4E9", "#E69F00"), main = g, xlab = "Período", ylab = "Valor")\n}', python: 'import matplotlib.pyplot as plt\nfig, ejes = plt.subplots(1, 2, figsize=(8, 3))\nfor eje, grupo in zip(ejes, ["Norte", "Sur"]):\n    d = [f for f in datos if f["grupo"] == grupo]\n    eje.plot([int(f["periodo"]) for f in d], [int(f["antes"]) for f in d], marker="o", label="Antes")\n    eje.plot([int(f["periodo"]) for f in d], [int(f["despues"]) for f in d], marker="o", label="Después")\n    eje.set_title(grupo); eje.legend()\nfig.tight_layout()' }
  }
};

// Cada fila: título, consigna, respuesta, pista conceptual, herramienta, orientación final.
const DEFINICIONES = {
  1: [
    ["Contar observaciones", "Ingresá los cuatro valores y guardá cuántos hay en respuesta.", 4, "Cada número ocupa una posición.", "R: length(). Python: len().", "Contá los elementos de valores."],
    ["Sumar valores", "Calculá la suma de los cuatro valores.", 16, "La suma usa todos los datos.", "R y Python: sum().", "Sumá el vector valores completo."],
    ["Detectar el máximo", "Encontrá el valor más alto de los cuatro datos.", 10, "Buscá el extremo superior.", "R y Python: max().", "Aplicá max() a valores."],
    ["Calcular la media", "Calculá el promedio de los cuatro valores.", 4, "Dividí la suma por la cantidad.", "R: mean(). Python: sum()/len().", "Usá los cuatro números, incluido el 10."],
    ["Ordenar los datos", "Guardá los valores en orden ascendente.", [2, 2, 2, 10], "Los valores repetidos se conservan.", "R: sort(). Python: sorted().", "El resultado debe tener cuatro posiciones."],
    ["Calcular la mediana", "Encontrá el valor central de los cuatro datos.", 2, "Con cuatro valores, promediá los dos del centro.", "R: median(). Python: statistics.median().", "Los dos valores centrales ordenados son 2 y 2."],
    ["Ubicar el valor alto", "Dibujá los valores individuales y contá cuántos superan la mediana.", 1, "Compará cada valor con la mediana.", "R: sum(valores > median(valores)). Python: sum(v > median(...) for v in valores).", "Descomentá el gráfico de puntos y contá solo los valores estrictamente mayores."],
    ["Medir la amplitud", "Creá un histograma y calculá máximo menos mínimo.", 8, "La amplitud mide la distancia entre extremos.", "R y Python: max() y min().", "El 10 y el 2 fijan los extremos; descomentá el histograma."],
    ["Comparar medias", "Mostrá dos barras, media total y media sin el máximo, y guardá la segunda media.", 2, "Quitá solo el valor más alto.", "R: filtrar con valores < max(valores). Python: comprensión condicional.", "Calculá la media de [2, 2, 2] y descomentá las barras."]
  ],
  2: [
    ["Contar registros", "Contá cuántas categorías se registraron.", 6, "Cada letra de la lista es un registro.", "R: length(). Python: len().", "Contá todos los elementos, incluso repetidos."],
    ["Contar A", "Calculá cuántas veces aparece A.", 2, "Compará cada elemento con A.", "R: sum(categorias == \"A\"). Python: categorias.count(\"A\").", "A aparece en la primera y quinta posición."],
    ["Contar B", "Calculá cuántas veces aparece B.", 3, "El conteo incluye todas las repeticiones.", "R: sum(... == \"B\"). Python: .count(\"B\").", "B aparece en tres posiciones."],
    ["Listar categorías", "Guardá las categorías diferentes en orden alfabético.", ["A", "B", "C"], "Una categoría se escribe una sola vez.", "R: sort(unique()). Python: sorted(set()).", "El vector de salida tiene tres letras."],
    ["Contar C", "Calculá cuántas veces aparece la categoría C.", 1, "Frecuencia es cantidad de apariciones.", "R: sum(categorias == \"C\"). Python: .count(\"C\").", "C aparece una vez."],
    ["Comparar frecuencias", "Calculá frecuencia de B menos frecuencia de A.", 1, "Restá los dos conteos.", "R: table(). Python: .count().", "La operación es 3 menos 2."],
    ["Dibujar barras", "Mostrá barras A, B y C y guardá sus frecuencias en ese orden.", [2, 3, 1], "Cada barra representa una categoría.", "R: table(). Python: .count() o Counter().", "Conservá el orden A, B, C y descomentá el gráfico."],
    ["Ordenar las barras", "Ordená las barras de mayor a menor y guardá el orden de categorías.", ["B", "A", "C"], "Ordená por frecuencia, no por letra.", "R: sort(table(...), decreasing=TRUE). Python: sorted(..., key=...).", "Las frecuencias ordenadas son 3, 2 y 1."],
    ["Mostrar porcentajes", "Dibujá porcentajes por categoría y guardá el porcentaje de B.", 50, "Dividí su frecuencia por los seis registros.", "R: prop.table(). Python: count()/len()*100.", "B representa 3/6 del total; descomentá el gráfico."]
  ],
  3: [
    ["Sumar valores", "Ingresá A=96 y B=100; calculá su suma.", 196, "La suma considera las dos categorías.", "R: sum(valores). Python: sum(valores.values()).", "Sumá 96 y 100."],
    ["Calcular diferencia", "Restá el valor de A al valor de B y guardá el resultado.", 4, "La resta compara los dos valores.", "R: valores[\"B\"] - valores[\"A\"]. Python: acceso por clave.", "Restá 100 menos 96."],
    ["Calcular media", "Calculá el promedio de los valores A y B.", 98, "Promediá ambos valores.", "R: mean(valores). Python: sum(...)/len(...).", "Dividí 196 entre dos."],
    ["Leer el CSV", "Leé datos.csv y contá sus filas.", 2, "Una fila corresponde a una categoría.", "R: nrow(datos). Python: len(datos).", "El archivo contiene A y B."],
    ["Extraer A", "Buscá en el CSV el valor de A.", 96, "Seleccioná la fila cuya categoría es A.", "R: datos$valor[datos$categoria == \"A\"]. Python: filtrar e int().", "Convertí a número en Python antes de asignar respuesta."],
    ["Extraer B", "Buscá en el CSV el valor de B.", 100, "Seleccioná la fila cuya categoría es B.", "R: indexación lógica. Python: next() e int().", "La categoría B tiene el valor mayor."],
    ["Barras desde cero", "Dibujá barras con eje desde cero y calculá B dividido A.", 100 / 96, "La razón real compara alturas desde cero.", "R: indexá valor por categoría. Python: int() o float().", "Dividí 100 entre 96 y descomentá las barras."],
    ["Probar un eje recortado", "Dibujá barras con eje desde 90 y calculá la razón entre alturas visibles B y A.", 10 / 6, "Restá 90 a cada valor antes de comparar alturas.", "R y Python: (B-90)/(A-90).", "Las alturas visibles son 10 y 6; descomentá el gráfico para observar el efecto."],
    ["Rotular una escala honesta", "Volvé al eje desde cero, rotulá ambas barras y calculá la diferencia porcentual respecto de A.", 400 / 96, "Usá A como base del porcentaje.", "R y Python: (B-A)/A*100.", "La diferencia absoluta es 4; descomentá barras y etiquetas."]
  ],
  4: [
    ["Sumar la línea base", "Ingresá los valores antes y calculá su total.", 100, "Sumá A, B y C.", "R: sum(antes). Python: sum(antes.values()).", "50 + 30 + 20."],
    ["Sumar el nuevo total", "Calculá la suma de los valores después.", 120, "Usá las tres categorías.", "R: sum(despues). Python: sum(despues.values()).", "55 + 42 + 23."],
    ["Medir el cambio total", "Restá el total antes del total después.", 20, "Compará totales de igual cobertura.", "R y Python: sum(despues) - sum(antes).", "Restá 120 menos 100."],
    ["Cambio del sector A", "Calculá cuánto aumentó el sector A entre antes y después.", 5, "Aumento es después menos antes.", "R: indexación por nombre. Python: diccionario[\"A\"].", "Restá 55 menos 50."],
    ["Leer sectores", "Leé datos.csv y contá los sectores.", 3, "Cada fila es un sector.", "R: nrow(datos). Python: len(datos).", "Encontrarás A, B y C."],
    ["Calcular tres aumentos", "Guardá los aumentos de A, B y C en ese orden.", [5, 12, 3], "Restá columnas fila por fila.", "R: datos$despues - datos$antes. Python: comprensión con int().", "El vector debe mantener el orden del CSV."],
    ["Barras de la línea base", "Graficá los valores antes y guardá el sector mayor.", "A", "Compará las alturas de la columna antes.", "R: which.max(). Python: max(..., key=...).", "A tiene 50 antes; descomentá las barras."],
    ["Barras agrupadas", "Dibujá antes y después por sector y guardá el total después.", 120, "Sumá solo la segunda serie.", "R: sum(datos$despues). Python: sum(int(...)).", "El total después reúne 55, 42 y 23."],
    ["Aporte al crecimiento", "Graficá los aumentos y calculá qué porcentaje del aumento total aportó B.", 60, "Dividí el aumento B por el aumento total.", "R y Python: 12/20*100.", "Usá el aumento total de 20 como denominador." ]
  ],
  5: [
    ["Total de 2024", "Ingresá Norte y Sur de 2024; calculá el total.", 220, "Sumá ambas sucursales.", "R: sum(ventas_2024). Python: sum(ventas_2024.values()).", "100 + 120."],
    ["Total de 2025", "Calculá el total de ventas de 2025.", 280, "Sumá solo 2025.", "R y Python: suma de ventas_2025.", "130 + 150."],
    ["Cambio anual absoluto", "Calculá cuánto aumentaron las ventas totales de 2024 a 2025.", 60, "Restá los totales en orden temporal.", "R y Python: total 2025 menos total 2024.", "Restá 280 menos 220."],
    ["Crecimiento porcentual", "Calculá el aumento porcentual respecto de 2024.", 6000 / 220, "La base es el total inicial de 2024.", "R y Python: (nuevo-viejo)/viejo*100.", "Usá 60/220*100."],
    ["Leer ventas", "Leé datos.csv y contá sus registros.", 4, "Cada fila es un año y una sucursal.", "R: nrow(datos). Python: len(datos).", "Hay dos sucursales en dos años."],
    ["Filtrar Norte 2024", "Buscá las ventas de Norte en 2024.", 100, "Aplicá simultáneamente año y sucursal.", "R: subset(). Python: dos condiciones en una comprensión.", "Convertí anio y ventas a número en Python."],
    ["Barras de 2025", "Graficá Norte y Sur de 2025 y guardá la sucursal con más ventas.", "Sur", "Primero filtrá el año.", "R: subset() y which.max(). Python: max(filas, key=...).", "Sur tiene 150 en 2025; descomentá las barras."],
    ["Comparar ambos años", "Dibujá ventas por sucursal y año; guardá las ventas Sur 2024.", 120, "Buscá la intersección de año y sucursal.", "R: subset(). Python: next(...).", "El gráfico debe mostrar las cuatro combinaciones."],
    ["Tablero con filtro", "Filtrá 2025, graficá solo ese año y guardá su total.", 280, "La cifra y el gráfico usan el mismo filtro.", "R: subset() y sum(). Python: comprensión y sum().", "Sumá 130 y 150 luego de filtrar." ]
  ],
  6: [
    ["Beneficio del primer caso", "Con ventas 120 y costo 90, calculá el beneficio.", 30, "Beneficio es ingreso menos costo.", "R: ventas[1]-costos[1]. Python: ventas[0]-costos[0].", "Restá 120 menos 90."],
    ["Margen del primer caso", "Calculá el margen porcentual del primer caso.", 25, "Dividí el beneficio por las ventas.", "R y Python: (ventas-costo)/ventas*100.", "Usá 30/120*100."],
    ["Beneficio del segundo caso", "Calculá el beneficio con ventas 200 y costo 100.", 100, "Restá costo de ventas.", "R: índice 2. Python: índice 1.", "Restá 200 menos 100."],
    ["Margen del segundo caso", "Calculá el margen porcentual del segundo caso.", 50, "La base son las ventas de ese caso.", "R y Python: beneficio/ventas*100.", "Usá 100/200*100."],
    ["Calcular dos márgenes", "Guardá los márgenes porcentuales de los dos casos en orden.", [25, 50], "Aplicá la misma fórmula a cada par.", "R: operaciones vectorizadas. Python: zip() y comprensión.", "El primer margen es 25 y el segundo 50."],
    ["Promediar márgenes", "Calculá el promedio simple de los dos márgenes.", 37.5, "Promediá porcentajes por caso.", "R: mean(). Python: sum()/len().", "Calculá (25 + 50)/2."],
    ["Barras de márgenes", "Dibujá los dos márgenes y guardá el mayor.", 50, "Compará porcentajes, no beneficios absolutos.", "R y Python: max() de los márgenes.", "Descomentá las barras; el segundo caso tiene mayor margen."],
    ["Comparar ventas y costos", "Dibujá barras de ventas y costos para ambos casos; calculá el costo promedio.", 95, "Promediá solo los costos.", "R: mean(costos). Python: sum(costos)/len(costos).", "Los costos son 90 y 100."],
    ["Aplicar una función", "Definí una función de margen, graficá tres casos y calculá el margen de (80, 60).", 25, "Reutilizá la misma fórmula para el caso nuevo.", "R: function(). Python: def.", "Calculá (80-60)/80*100; descomentá el gráfico de tres casos."]
  ],
  7: [
    ["Casos de A", "Ingresá los casos y guardá cuántos corresponden a A.", 40, "Buscá el valor por nombre de territorio.", "R: casos[\"A\"]. Python: casos[\"A\"].", "A registra 40 casos."],
    ["Casos de B", "Guardá la cantidad de casos de B.", 30, "Seleccioná el segundo territorio.", "R y Python: acceso por nombre B.", "B registra 30 casos."],
    ["Comparar casos absolutos", "Indicá qué territorio tiene más casos sin normalizar.", "A", "Compará 40 frente a 30.", "R: names(which.max(casos)). Python: max(casos, key=casos.get).", "El resultado es el nombre del territorio."],
    ["Leer poblaciones", "Guardá las poblaciones de A y B en ese orden.", [100000, 30000], "Una tasa necesita el denominador poblacional.", "R: unname(poblacion). Python: lista de accesos por clave.", "Conservá el orden A, B."],
    ["Leer el CSV territorial", "Leé datos.csv y contá los territorios.", 2, "Cada fila representa un territorio.", "R: nrow(datos). Python: len(datos).", "Hay A y B."],
    ["Calcular tasa de A", "Calculá los casos de A por 100.000 habitantes.", 40, "Dividí casos por población y escalá.", "R y Python: casos/poblacion*100000.", "Para A: 40/100000*100000."],
    ["Barras de casos", "Graficá casos absolutos y guardá el territorio con más casos.", "A", "Las barras muestran totales, no tasas.", "R: which.max(datos$casos). Python: max(..., key=...).", "Descomentá el gráfico; A tiene 40."],
    ["Barras de tasas", "Graficá tasas por 100.000 y guardá el territorio con la tasa mayor.", "B", "Cada territorio tiene población distinta.", "R y Python: casos/poblacion*100000 para cada fila.", "A tiene tasa 40 y B tasa 100."],
    ["Puntos proporcionales", "Ubicá lon y lat, escalá el tamaño por tasa y guardá la tasa de B.", 100, "El tamaño debe representar la tasa.", "R: plot(..., cex=tasas/30). Python: scatter(..., s=...).", "B tiene 30 casos entre 30.000 habitantes." ]
  ],
  8: [
    ["Total Norte antes", "Sumá los dos períodos de Norte antes.", 170, "No mezcles los grupos.", "R: sum(norte_antes). Python: sum(norte_antes).", "80 + 90."],
    ["Total Norte después", "Sumá los dos períodos de Norte después.", 199, "Usá solo la serie después de Norte.", "R y Python: sum(norte_despues).", "100 + 99."],
    ["Total Sur antes", "Sumá los dos períodos de Sur antes.", 220, "Usá ambos períodos de Sur.", "R y Python: sum(sur_antes).", "100 + 120."],
    ["Total Sur después", "Sumá los dos períodos de Sur después.", 200, "Conservá el mismo grupo.", "R y Python: sum(sur_despues).", "90 + 110."],
    ["Leer el integrador", "Leé datos.csv y contá sus registros.", 4, "Hay dos grupos por dos períodos.", "R: nrow(datos). Python: len(datos).", "El archivo contiene cuatro filas."],
    ["Cambio absoluto Norte", "Calculá la diferencia entre total después y antes de Norte.", 29, "Compará totales del mismo grupo.", "R: subset(datos, grupo==\"Norte\"). Python: filtrar grupo.", "Restá 199 menos 170."],
    ["Líneas de Norte", "Dibujá antes y después de Norte y guardá el cambio del período 1.", 20, "Compará dos valores del mismo período.", "R: subset() e indexación. Python: filtrá el grupo y convertí números.", "En período 1, Norte pasa de 80 a 100."],
    ["Líneas de Sur", "Dibujá antes y después de Sur y guardá los cambios de ambos períodos en orden.", [-10, -10], "Restá después menos antes en cada período.", "R: subset() y resta de columnas. Python: comprensión sobre filas filtradas.", "Ambos períodos disminuyen 10."],
    ["Dos paneles", "Dibujá un panel por grupo y guardá los cambios porcentuales totales [Norte, Sur].", [2900 / 170, -2000 / 220], "Primero agregá los dos períodos por grupo.", "R y Python: (total después-total antes)/total antes*100.", "Norte crece 29/170 y Sur cae 20/220; mantené el orden Norte, Sur."]
  ]
};

function comentar(codigo) {
  return codigo.split("\n").map(linea => `# ${linea}`).join("\n");
}

function crearPaso(n, indice, fila) {
  const paso = indice + 1;
  const [titulo, consigna, esperado, pista1, pista2, pista3] = fila;
  const usaCsv = CSV_DESDE[n] !== undefined && paso >= CSV_DESDE[n];
  const grafico = paso >= 7;
  const preparacion = usaCsv ? LECTURA_CSV : MANUAL[n];
  const trama = grafico ? GRAFICOS[n][paso] : null;
  const orientacion = grafico ? "# Descomentá el gráfico luego de completar respuesta.\n" : "";
  const codigo = {
    r: `${preparacion.r}\nrespuesta <- NA\n${grafico ? orientacion + comentar(trama.r) : ""}`.trimEnd(),
    python: `${preparacion.python}\nrespuesta = None\n${grafico ? orientacion + comentar(trama.python) : ""}`.trimEnd()
  };
  return {
    n,
    paso,
    id: `${n}_${String(paso).padStart(2, "0")}`,
    titulo,
    consigna,
    esperado,
    explicacion: "Resultado: " + (Array.isArray(esperado) ? esperado.join(", ") : esperado) + ". " + pista3,
    pistas: [pista1, pista2, pista3],
    codigo,
    ...(usaCsv ? { csv: CSV[n] } : {}),
    ...(grafico ? { grafico: true } : {})
  };
}

export const PASOS_CODIGO = Object.entries(DEFINICIONES).flatMap(([numero, filas]) =>
  filas.map((fila, indice) => crearPaso(Number(numero), indice, fila))
);
