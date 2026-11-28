/* Ensayos formativos: nueve pasos nuevos y el ensayo original como cierre de cada unidad. */
import { PASOS_CODIGO } from "./codigo-pasos.mjs";

const RETOS_FINALES = [
  {
    n: 1, titulo: "Cargar datos a mano y reconocer un valor atípico",
    consigna: "Usá los cuatro valores del ejemplo. Calculá su media y su mediana. En respuesta guardá media menos mediana.",
    esperado: 2, explicacion: "La media es 4 y la mediana es 2. El valor 10 desplaza la media.",
    pistas: ["La media y la mediana resumen aspectos distintos de los mismos datos.", "R: mean() y median(). Python: statistics.mean() y statistics.median().", "Calculá media menos mediana para [2, 2, 2, 10]."],
    codigo: {
      r: `# 1. Cargá los datos manualmente.\nvalores <- c(2, 2, 2, 10)\n# 2. Reemplazá NA por tu cálculo.\nrespuesta <- NA`,
      python: `# 1. Cargá los datos manualmente.\nvalores = [2, 2, 2, 10]\n# 2. Reemplazá None por tu cálculo.\nimport statistics\nrespuesta = None`
    }
  },
  {
    n: 2, titulo: "Elegir barras para comparar categorías",
    consigna: "Contá cuántas veces aparece cada letra. En respuesta guardá la letra más frecuente. Después dibujá una barra para cada letra.",
    esperado: "B", grafico: true, explicacion: "B aparece tres veces. Las barras comparan magnitudes discretas en una escala común.",
    pistas: ["Contá cada categoría antes de decidir cuál lidera.", "R: table() y names(which.max()). Python: Counter() y max(..., key=...).", "La lista es A, B, C, B, A, B. Usá barplot() o plt.bar()."],
    codigo: {
      r: `categorias <- c("A", "B", "C", "B", "A", "B")\nconteos <- table(categorias)\nrespuesta <- NA_character_  # Reemplazá esta línea.\n# TODO: descomentá la línea para mostrar las barras.\n# barplot(conteos, col = "#0072B2", ylab = "Frecuencia", main = "Frecuencia por categoría")`,
      python: `from collections import Counter\ncategorias = ["A", "B", "C", "B", "A", "B"]\nconteos = Counter(categorias)\nrespuesta = None  # Reemplazá esta línea.\n# TODO: descomentá estas líneas para mostrar las barras.\n# import matplotlib.pyplot as plt\n# plt.bar(list(conteos), list(conteos.values()), color="#0072B2")\n# plt.ylabel("Frecuencia")\n# plt.title("Frecuencia por categoría")`
    }
  },
  {
    n: 3, titulo: "Leer un CSV y evitar un eje engañoso",
    consigna: "Leé el CSV. Calculá la razón entre las alturas visibles de B y A si el eje empezara en 95; guardala en respuesta. Después dibujá ambas barras con el eje desde cero.",
    csv: "datos-codigo/etica.csv", esperado: 5, grafico: true,
    explicacion: "Con eje en 95, las alturas visibles son 5 y 1: razón 5. El gráfico corregido comienza en cero.",
    pistas: ["La altura aparente se mide desde el límite inferior del eje.", "R: read.csv() y barplot(ylim=c(0,...)). Python: csv.DictReader() y plt.ylim(bottom=0).", "Calculá (100−95)/(96−95) y asegurá que el eje visual arranque en cero."],
    codigo: {
      r: `# El aula descargó un CSV sintético y lo montó como datos.csv.\ndatos <- read.csv("datos.csv")\nrespuesta <- NA_real_  # Reemplazá esta línea.\n# TODO: descomentá para mostrar barras con eje honesto.\n# barplot(datos$valor, names.arg = datos$categoria, ylim = c(0, 110), col = "#0072B2", ylab = "Valor")`,
      python: `# El aula descargó un CSV sintético y lo montó como datos.csv.\nimport csv\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\nrespuesta = None  # Reemplazá esta línea.\n# TODO: descomentá para mostrar barras con eje honesto.\n# import matplotlib.pyplot as plt\n# plt.bar([fila["categoria"] for fila in datos], [float(fila["valor"]) for fila in datos], color="#0072B2")\n# plt.ylim(bottom=0)\n# plt.ylabel("Valor")`
    }
  },
  {
    n: 4, titulo: "Comparar contribuciones a un KPI",
    consigna: "Leé el CSV y restá antes a después en cada sector. En respuesta guardá el sector con mayor aumento. Dibujá barras para comparar los dos períodos.",
    csv: "datos-codigo/kpis.csv", esperado: "B", grafico: true,
    explicacion: "B crece 12 unidades, más que A (+5) y C (+3). La comparación emparejada muestra el aporte.",
    pistas: ["Calculá después menos antes por sector.", "R: which.max(). Python: max(filas, key=...).", "Mostrá barras agrupadas con before/after; el sector B crece 12."],
    codigo: {
      r: `datos <- read.csv("datos.csv")\naumento <- datos$despues - datos$antes\nrespuesta <- NA_character_  # Reemplazá esta línea.\n# TODO: descomentá para comparar ambos períodos.\n# barplot(rbind(datos$antes, datos$despues), beside = TRUE, names.arg = datos$sector, col = c("#56B4E9", "#E69F00"), ylab = "Unidades")\n# legend("topright", legend = c("Antes", "Después"), fill = c("#56B4E9", "#E69F00"))`,
      python: `import csv\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\naumento = [int(f["despues"]) - int(f["antes"]) for f in datos]\nrespuesta = None  # Reemplazá esta línea.\n# TODO: descomentá para comparar ambos períodos.\n# import matplotlib.pyplot as plt\n# x = range(len(datos))\n# plt.bar([i - .2 for i in x], [int(f["antes"]) for f in datos], width=.4, label="Antes")\n# plt.bar([i + .2 for i in x], [int(f["despues"]) for f in datos], width=.4, label="Después")\n# plt.xticks(list(x), [f["sector"] for f in datos])\n# plt.legend()`
    }
  },
  {
    n: 5, titulo: "Aplicar filtros consistentes en un tablero",
    consigna: "Leé el CSV y quedate solo con las filas del año 2025 y la sucursal Norte. En respuesta guardá la suma de sus ventas. Graficá únicamente esas filas.",
    csv: "datos-codigo/sucursales.csv", esperado: 130, grafico: true,
    explicacion: "La intersección de año 2025 y sucursal Norte contiene 130 ventas. Un filtro debe afectar también al gráfico.",
    pistas: ["Aplicá ambas condiciones a las mismas filas.", "R: subset(). Python: comprensión con dos condiciones.", "Filtrá año == 2025 y sucursal == Norte antes de calcular y graficar."],
    codigo: {
      r: `datos <- read.csv("datos.csv")\nfiltrado <- subset(datos, anio == 2025 & sucursal == "Norte")\nrespuesta <- NA_real_  # Reemplazá esta línea.\n# TODO: descomentá para graficar solo el filtro activo.\n# barplot(filtrado$ventas, names.arg = filtrado$periodo, col = "#0072B2", ylab = "Ventas")`,
      python: `import csv\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\nfiltrado = [f for f in datos if int(f["anio"]) == 2025 and f["sucursal"] == "Norte"]\nrespuesta = None  # Reemplazá esta línea.\n# TODO: descomentá para graficar solo el filtro activo.\n# import matplotlib.pyplot as plt\n# plt.bar([f["periodo"] for f in filtrado], [int(f["ventas"]) for f in filtrado])\n# plt.ylabel("Ventas")`
    }
  },
  {
    n: 6, titulo: "Convertir un cálculo en reporte repetible",
    consigna: "Completá la función margen(ventas, costo). Usala con (120, 90) y (200, 100). En respuesta guardá los dos porcentajes, en ese orden, y dibujá sus barras.",
    esperado: [25, 50], grafico: true,
    explicacion: "Margen = (ventas − costo) / ventas × 100. Una función permite repetir el cálculo sin copiar fórmulas.",
    pistas: ["La base del porcentaje son las ventas.", "La fórmula es (ventas − costo) / ventas × 100.", "La función debe devolver 25 y 50; graficá ambos resultados."],
    codigo: {
      r: `margen <- function(ventas, costo) {\n  NA_real_  # Reemplazá por la fórmula.\n}\nrespuesta <- c(margen(120, 90), margen(200, 100))\n# TODO: descomentá para mostrar los márgenes.\n# barplot(respuesta, names.arg = c("Caso 1", "Caso 2"), ylim = c(0, 60), col = "#009E73", ylab = "%")`,
      python: `def margen(ventas, costo):\n    return None  # Reemplazá por la fórmula.\n\nrespuesta = [margen(120, 90), margen(200, 100)]\n# TODO: descomentá para mostrar los márgenes.\n# import matplotlib.pyplot as plt\n# plt.bar(["Caso 1", "Caso 2"], respuesta, color="#009E73")\n# plt.ylim(0, 60)\n# plt.ylabel("%")`
    }
  },
  {
    n: 7, titulo: "Normalizar tasas antes de comparar territorios",
    consigna: "Leé el CSV y calculá casos por 100.000 habitantes en cada territorio. En respuesta guardá el nombre del territorio con mayor tasa. Dibujá los puntos según sus coordenadas y su tasa.",
    csv: "datos-codigo/territorios.csv", esperado: "B", grafico: true,
    explicacion: "A tiene 40 por 100.000 y B tiene 100 por 100.000. El tamaño del punto representa la tasa, no el total de casos.",
    pistas: ["Compará tasas, no números absolutos de casos.", "Tasa = casos / población × 100.000.", "Usá lon y lat para ubicar los puntos y escalá el tamaño por tasa."],
    codigo: {
      r: `datos <- read.csv("datos.csv")\ntasa <- datos$casos / datos$poblacion * 100000\nrespuesta <- NA_character_  # Reemplazá esta línea.\n# TODO: descomentá para mostrar los puntos proporcionales.\n# plot(datos$lon, datos$lat, cex = tasa / 30, pch = 19, col = "#0072B2", xlab = "Longitud", ylab = "Latitud", main = "Tasa por 100.000")\n# text(datos$lon, datos$lat, labels = datos$territorio, pos = 3)`,
      python: `import csv\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\ntasa = [int(f["casos"]) / int(f["poblacion"]) * 100000 for f in datos]\nrespuesta = None  # Reemplazá esta línea.\n# TODO: descomentá para mostrar los puntos proporcionales.\n# import matplotlib.pyplot as plt\n# plt.scatter([float(f["lon"]) for f in datos], [float(f["lat"]) for f in datos], s=[t * 8 for t in tasa])\n# for f in datos: plt.annotate(f["territorio"], (float(f["lon"]), float(f["lat"])))\n# plt.xlabel("Longitud"); plt.ylabel("Latitud")`
    }
  },
  {
    n: 8, titulo: "Integrador: comparar cambios con paneles",
    consigna: "Leé el CSV. Sumá antes y después para cada grupo y calculá su cambio porcentual. En respuesta guardá el grupo que más creció. Dibujá dos paneles, uno por grupo.",
    csv: "datos-codigo/integrador.csv", esperado: "Norte", grafico: true,
    explicacion: "Norte pasa de 170 a 199 (+17,1%); Sur pasa de 220 a 200 (−9,1%). Los paneles permiten revisar cada serie.",
    pistas: ["Sumá los dos períodos de cada grupo antes de calcular el porcentaje.", "Cambio = (suma después − suma antes) / suma antes × 100.", "Norte tiene crecimiento positivo; dibujá ambos grupos en paneles separados."],
    codigo: {
      r: `datos <- read.csv("datos.csv")\ngrupos <- unique(datos$grupo)\ncambio <- sapply(grupos, function(g) {\n  d <- subset(datos, grupo == g)\n  (sum(d$despues) - sum(d$antes)) / sum(d$antes) * 100\n})\nrespuesta <- NA_character_  # Reemplazá esta línea.\n# TODO: descomentá el bloque para crear dos paneles.\n# par(mfrow = c(1, 2))\n# for (g in grupos) {\n#   d <- subset(datos, grupo == g)\n#   matplot(d$periodo, cbind(d$antes, d$despues), type = "b", pch = 19, lty = 1, col = c("#56B4E9", "#E69F00"), main = g, xlab = "Período", ylab = "Valor")\n# }`,
      python: `import csv\nwith open("datos.csv", encoding="utf-8") as archivo:\n    datos = list(csv.DictReader(archivo))\ngrupos = sorted({f["grupo"] for f in datos})\ncambio = {}\nfor grupo in grupos:\n    filas = [f for f in datos if f["grupo"] == grupo]\n    antes = sum(int(f["antes"]) for f in filas)\n    despues = sum(int(f["despues"]) for f in filas)\n    cambio[grupo] = (despues - antes) / antes * 100\nrespuesta = None  # Reemplazá esta línea.\n# TODO: descomentá el bloque para crear dos paneles.\n# import matplotlib.pyplot as plt\n# fig, ejes = plt.subplots(1, 2, figsize=(8, 3))\n# for eje, grupo in zip(ejes, grupos):\n#     filas = [f for f in datos if f["grupo"] == grupo]\n#     eje.plot([f["periodo"] for f in filas], [int(f["antes"]) for f in filas], marker="o", label="Antes")\n#     eje.plot([f["periodo"] for f in filas], [int(f["despues"]) for f in filas], marker="o", label="Después")\n#     eje.set_title(grupo); eje.legend()\n# fig.tight_layout()`
    }
  }
];

export const RETOS_CODIGO = [...PASOS_CODIGO, ...RETOS_FINALES.map(r => ({ ...r, id: String(r.n), paso: 10 }))]
  .sort((a, b) => a.n - b.n || a.paso - b.paso);
