"""Contenido de las fichas de estudio y hojas de referencia (se convierten a PDF con tools/build_pdfs.py)."""

PY = "py"; R = "r"

FICHAS = {
"ficha_01_percepcion": dict(
  titulo="Ficha 1 · Percepción y por qué visualizar", sesion=1,
  claves=[
    "<b>Graficá siempre</b>: el cuarteto de Anscombe tiene los mismos estadísticos (media, varianza, correlación, recta) y cuatro formas totalmente distintas.",
    "<b>Jerarquía perceptiva</b> (Cleveland y McGill, 1984), de más a menos precisa: posición en escala común → posición en escalas no alineadas → longitud → ángulo/pendiente → área → volumen → color/saturación.",
    "<b>Atributos preatentivos</b> (color de énfasis, tamaño, orientación, posición) se detectan en milisegundos: usalos para guiar la mirada hacia lo importante, no para decorar.",
    "<b>Gestalt</b>: proximidad, similitud, cierre, continuidad y figura-fondo explican cómo el ojo agrupa elementos.",
    "<b>Data-ink ratio</b> (Tufte): maximizá la proporción de tinta que representa datos; borrá lo que no informa (bordes, fondos, 3D, rejillas pesadas)."],
  errores=["Torta o dona con más de 3-4 partes.", "Efectos 3D o sombras.", "Más de 5-6 colores sin significado.", "Decorar con íconos que compiten con el dato."],
  py="""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
colores = ["#D9D9D9"] * len(y); colores[idx_max] = "#D55E00"   # énfasis en un solo dato
ax.barh(categorias, y, color=colores)
ax.spines[["top", "right"]].set_visible(False)""",
  r="""library(ggplot2)
ggplot(d, aes(valor, reorder(cat, valor), fill = valor == max(valor))) +
  geom_col(show.legend = FALSE) +
  scale_fill_manual(values = c(`FALSE` = "#D9D9D9", `TRUE` = "#D55E00")) +
  theme_minimal()""",
  check=["¿Qué debe comparar el lector? ¿Lo hice con posición o longitud?", "¿Hay un solo foco de atención (color de énfasis)?", "¿Quité todo lo que no informa?"],
  mas=["Wilke, <i>Fundamentals of Data Visualization</i>, caps. 1-4.", "Cleveland & McGill (1984), <i>Graphical Perception</i>, JASA 79(387).", "Laboratorio: <code>lab01_percepcion</code> (Colab) y <code>01_percepcion.Rmd</code> (RStudio → RPubs)."]),

"ficha_02_eleccion": dict(
  titulo="Ficha 2 · Elección del gráfico", sesion=2,
  claves=[
    "Empezá por la <b>pregunta</b> y el <b>tipo de dato</b>, no por el gráfico: distribución, cantidad, proporción, relación o tiempo.",
    "<b>Distribución</b>: histograma (probar varios anchos de bin), densidad, ECDF, caja, violín. <b>Cantidad</b>: barras ordenadas o lollipop. <b>Proporción</b>: barras apiladas al 100 %. <b>Relación</b>: dispersión, hexbin, suavizado. <b>Tiempo</b>: línea o small multiples.",
    "<b>Overplotting</b> (muchos puntos superpuestos): transparencia, jitter, hexbin/bin2d o densidad 2D.",
    "Las <b>barras</b> codifican con longitud: el eje debe empezar en cero. Ordenalas por valor salvo que exista un orden natural (meses, edades).",
    "Si dudás, probá el árbol de decisión de <i>From Data to Viz</i> (data-to-viz.com)."],
  errores=["Torta para comparar 8 categorías parecidas.", "Histograma con un único ancho de bin (puede ocultar la forma).", "Barras horizontales sin orden.", "Línea para categorías sin orden temporal."],
  py="""import seaborn as sns
sns.histplot(df, x="nota_final", bins=30)                    # distribución
sns.violinplot(data=df, x="carrera", y="nota_final")         # por grupo
plt.hexbin(df.horas, df.nota, gridsize=18, cmap="Blues")     # densidad""",
  r="""ggplot(df, aes(nota_final)) + geom_histogram(bins = 30)          # distribución
ggplot(df, aes(carrera, nota_final)) + geom_violin()             # por grupo
ggplot(df, aes(horas, nota)) + geom_bin2d(bins = 18)             # densidad""",
  check=["¿La pregunta está escrita antes de elegir el gráfico?", "¿Probé al menos dos anchos de bin?", "¿Las barras empiezan en cero y están ordenadas?"],
  mas=["Wilke, caps. 5-12 (directorio de visualizaciones).", "data-to-viz.com · python-graph-gallery.com · r-graph-gallery.com.", "Laboratorio: <code>lab02_eleccion_graficos</code> / <code>02_eleccion_graficos.Rmd</code>."]),

"ficha_03_color_etica": dict(
  titulo="Ficha 3 · Color, diseño y ética visual", sesion=3,
  claves=[
    "<b>Tres tipos de paleta</b>: cualitativa (categorías), secuencial (magnitud ordenada) y divergente (valores con un centro neutro, p. ej. variación vs meta).",
    "<b>Accesibilidad</b>: ~8 % de los varones tiene daltonismo rojo-verde. Usá paletas seguras (Okabe-Ito, viridis) y no dependas solo del color: sumá etiquetas, formas o patrones. Contraste mínimo de texto 4,5:1 (WCAG).",
    "<b>Anotá en vez de usar leyendas</b>: etiquetado directo y un <b>título-mensaje</b> que afirme un hallazgo (“Las ventas crecieron 7 % en 2025”), no solo describa (“Ventas 2025”).",
    "<b>Engaños frecuentes</b>: eje truncado en barras, doble eje Y, recortes temporales a conveniencia (<i>cherry-picking</i>), áreas/volúmenes desproporcionados, mapas que colorean conteos absolutos.",
    "<b>Integridad</b>: mostrá fuente, fecha, definición de la métrica, tamaño de muestra e incertidumbre."],
  errores=["Arcoíris para datos secuenciales.", "Rojo/verde como único diferenciador.", "Doble eje que “fabrica” correlación.", "Título que promete más de lo que muestran los datos."],
  py="""OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=OKABE_ITO)
ax.set_ylim(0, 100)                       # barras: eje en cero
ax.set_title("Electrónica se dispara en diciembre", loc="left", fontweight="bold")""",
  r="""okabe_ito <- c("#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000")
ggplot(df, aes(mes, ventas, color = cat)) + geom_line() +
  scale_color_manual(values = okabe_ito) +
  labs(title = "Electrónica se dispara en diciembre") + coord_cartesian(ylim = c(0, NA))""",
  check=["¿Se entiende en escala de grises o con daltonismo?", "¿El título afirma algo que los datos sostienen?", "¿Hay fuente, fecha, métrica y n?", "¿Eje en cero (barras) y escalas comparables entre paneles?"],
  mas=["Okabe & Ito, <i>Color Universal Design</i> (jfly.uni-koeln.de/color).", "Cairo, <i>How Charts Lie</i> (2019); Wilke caps. 17, 19-20, 29.", "Laboratorio: <code>lab03_color_diseno_etica</code> / <code>03_color_diseno_etica.Rmd</code>."]),

"ficha_04_kpis_storytelling": dict(
  titulo="Ficha 4 · Visual analytics, KPIs y storytelling", sesion=4,
  claves=[
    "<b>Anatomía de un KPI</b>: nombre, definición/fórmula, unidad, periodo, comparación (periodo anterior o meta) y semáforo/umbral. Sin contexto, un número no decide nada.",
    "<b>Métricas accionables vs de vanidad</b>: ¿qué decisión cambia si este número sube o baja?",
    "<b>Small multiples</b>: mismo gráfico repetido por subgrupo con ejes comunes; resaltá la serie de cada panel y dejá el resto en gris.",
    "<b>Contribución al cambio</b>: descomponé una variación total en lo que aporta cada subgrupo.",
    "<b>Narrativa</b>: contexto → conflicto (hallazgo) → resolución (acción). Un gráfico = un mensaje."],
  errores=["Paneles con 10 gráficos sin jerarquía.", "KPIs sin comparación ni unidad.", "Colores de semáforo sin considerar daltonismo.", "Contar la historia en el título de la diapositiva y contradecirla en el gráfico."],
  py="""k = df.groupby("anio").agg(ventas=("ventas", "sum"), costo=("costo", "sum"))
k["margen_pct"] = (1 - k.costo / k.ventas) * 100
delta = k.loc[2025, "ventas"] / k.loc[2024, "ventas"] - 1          # variación %""",
  r="""k <- df %>% group_by(anio) %>% summarise(ventas = sum(ventas), costo = sum(costo)) %>%
  mutate(margen_pct = (1 - costo / ventas) * 100)
delta <- k$ventas[k$anio == 2025] / k$ventas[k$anio == 2024] - 1""",
  check=["¿Cada KPI tiene fórmula, unidad y comparación?", "¿El título dice qué hacer o qué pasó?", "¿Un panel responde una sola pregunta?"],
  mas=["Knaflic, <i>Storytelling con datos</i>.", "Few, <i>Information Dashboard Design</i>.", "Laboratorio: <code>lab04_kpis_storytelling</code> / <code>04_kpis_storytelling.Rmd</code>."]),

"ficha_05_dashboards": dict(
  titulo="Ficha 5 · Dashboards interactivos", sesion=5,
  claves=[
    "<b>Mantra de Shneiderman</b>: <i>overview first, zoom and filter, then details on demand</i>.",
    "<b>Jerarquía</b>: KPIs arriba a la izquierda → tendencia → comparación → detalle. Se debe responder la pregunta de la audiencia en ~5 segundos.",
    "<b>Filtros con propósito</b>: un filtro global debe afectar de forma visible y coherente a todo lo que dice afectar. La interacción decorativa distrae.",
    "<b>Rendimiento</b>: agregá y precalculá datos; objetivo de carga &lt; 3 s.",
    "<b>Dónde publicar</b>: Plotly/HTML estático y <b>RPubs</b> (HTML sin servidor: usar plotly + crosstalk + DT); Dash o Shiny necesitan un servidor (Render, shinyapps.io…)."],
  errores=["Filtros que no afectan todos los gráficos sin avisar.", "Tablas enormes sin resumen.", "Sin estado “sin datos”.", "Animaciones que no ayudan a decidir."],
  py="""import plotly.express as px
fig = px.line(m, x="mes", y="ventas", color="sucursal", template="simple_white")
fig.update_xaxes(rangeslider_visible=True)       # selector de rango
fig.write_html("dashboard.html")                 # archivo autocontenido""",
  r="""library(plotly); library(crosstalk)
sd <- SharedData$new(m)
bscols(widths = c(3, 9),
  filter_select("suc", "Sucursal", sd, ~sucursal),
  plot_ly(sd, x = ~mes, y = ~ventas, color = ~sucursal, type = "bar"))""",
  check=["¿Los KPIs tienen unidad y comparación?", "¿Cada filtro afecta lo que declara?", "¿Funciona en el celular y con teclado?"],
  mas=["plotly.com/python · dash.plotly.com · rstudio.github.io/crosstalk.", "Laboratorio: <code>lab05_dashboards_plotly</code> / <code>05_dashboards_interactivos.Rmd</code>."]),

"ficha_06_reporting": dict(
  titulo="Ficha 6 · Reporting automatizado", sesion=6,
  claves=[
    "<b>Reporte reproducible = plantilla + datos + parámetros</b>, ejecutable sin pasos manuales.",
    "<b>R Markdown</b>: declarar <code>params:</code> en el YAML y usarlos como <code>params$sucursal</code>; en RStudio, <i>Knit with Parameters</i>. <b>Python</b>: Jinja2 (HTML), papermill (notebooks) o Quarto (<code>-P</code>).",
    "<b>Alertas útiles</b>: umbral explícito, contexto y destinatario (“margen &lt; 25 %: revisar costos de Electrónica”).",
    "<b>Programar</b>: cron o GitHub Actions (<code>schedule</code>) para regenerar informes periódicamente.",
    "<b>Validar antes de publicar</b>: la automatización replica también los errores de datos; agregá chequeos (nulos, rangos, duplicados)."],
  errores=["Copiar y pegar gráficos en Word cada mes.", "Parámetros hardcodeados dentro del código.", "Informes sin fecha de generación ni fuente."],
  py="""from jinja2 import Template
html = Template(plantilla).render(sucursal="Asunción", kpis=kpis, img=img_base64)
Path(f"informe_{sucursal}.html").write_text(html, encoding="utf-8")""",
  r="""rmarkdown::render("plantilla_reporte_sucursal.Rmd",
  params = list(sucursal = "Asunción", anio = 2025),
  output_file = "informe_Asuncion.html")""",
  check=["¿Se regenera con un comando?", "¿Los parámetros están en un solo lugar?", "¿Hay fecha, fuente y notas metodológicas?"],
  mas=["bookdown.org/yihui/rmarkdown (guía oficial de R Markdown).", "Laboratorio: <code>lab06_reportes_automaticos</code> / <code>06_reporting_automatizado.Rmd</code>."]),

"ficha_07_complejas": dict(
  titulo="Ficha 7 · Alta dimensionalidad, series y geodatos", sesion=7,
  claves=[
    "<b>Muchas variables</b>: matriz de correlación (paleta divergente centrada en 0), coordenadas paralelas, <i>small multiples</i>, y reducción de dimensión.",
    "<b>PCA</b>: proyección lineal que maximiza varianza; las distancias globales tienen sentido. <b>t-SNE</b>: conserva vecindades locales; <b>no interpretes</b> tamaños de clúster ni distancias entre clústeres, y probá varias perplejidades.",
    "<b>Series temporales</b>: tendencia (media móvil), estacionalidad (heatmap año×mes, subseries), residuo y anomalías. Mostrá siempre el contexto temporal completo.",
    "<b>Mapas</b>: coropleta con <b>tasas o densidades</b>, nunca conteos absolutos entre áreas desiguales; ojo con el <b>MAUP</b> (el patrón depende de cómo se agregan las áreas). Burbujas para valores absolutos.",
    "Cada dimensión extra tiene un costo cognitivo: simplificá."],
  errores=["Interpretar distancias entre clústeres de t-SNE.", "Coropleta de población total.", "Mostrar solo 3 meses de una serie con ciclo anual.", "Arcoíris en heatmaps."],
  py="""from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
Z = StandardScaler().fit_transform(X)
P = PCA(2).fit_transform(Z); T = TSNE(2, perplexity=30, random_state=0).fit_transform(Z)""",
  r="""pc <- prcomp(X, scale. = TRUE)
set.seed(0); ts <- Rtsne::Rtsne(scale(X), perplexity = 30, check_duplicates = FALSE)""",
  check=["¿Expliqué cuánta varianza retiene el PCA?", "¿Las tasas están normalizadas por población?", "¿Mostré la serie completa y marqué anomalías?"],
  mas=["Distill, <i>How to Use t-SNE Effectively</i>.", "datos.gov.py · ine.gov.py (Portal Geoestadístico).", "Laboratorio: <code>lab07_complejas</code> / <code>07_estructuras_complejas.Rmd</code>."]),

"ficha_08_redes": dict(
  titulo="Ficha 8 · Redes (opcional)", sesion=8,
  claves=[
    "<b>Layouts</b> de fuerzas (Fruchterman-Reingold, Kamada-Kawai), circular: la posición ayuda a ver estructura pero <b>no mide distancias exactas</b>.",
    "<b>Codificá métricas</b>: tamaño = centralidad (grado, intermediación), color = comunidad, pocas etiquetas (solo nodos clave).",
    "<b>Hairball</b>: si el grafo es denso, filtrá aristas débiles, agregá nodos o usá una <b>matriz de adyacencia</b> ordenada.",
    "<b>Centralidad de intermediación</b>: cuánto actúa un nodo como puente en los caminos más cortos.",
    "Herramientas: NetworkX, igraph, Gephi, Cytoscape, pyvis/visNetwork (interactivo)."],
  errores=["Etiquetar todos los nodos.", "Layout aleatorio sin semilla (no reproducible).", "Reportar “se ve bonito” sin métricas."],
  py="""import networkx as nx
G = nx.karate_club_graph(); cen = nx.betweenness_centrality(G)
com = nx.algorithms.community.greedy_modularity_communities(G)
nx.draw_networkx(G, nx.spring_layout(G, seed=7), node_size=[200 + 3000 * cen[n] for n in G])""",
  r="""library(igraph)
G <- graph_from_data_frame(aristas, directed = FALSE)
cen <- betweenness(G, normalized = TRUE); com <- cluster_louvain(G)
set.seed(7); plot(G, layout = layout_with_fr(G), vertex.size = 5 + 40 * cen, vertex.color = membership(com))""",
  check=["¿El layout es reproducible (semilla)?", "¿Reporté métricas y no solo la imagen?", "¿Probé matriz si la red es densa?"],
  mas=["networkx.org · r.igraph.org · gephi.org.", "Laboratorio: <code>lab08_redes</code> / <code>08_redes.Rmd</code>."]),
}

GUIA_INICIO = dict(titulo="Guía de inicio · Colab, RStudio y RPubs", secciones=[
 ("1. Cómo se trabaja en este curso", """<p>El curso usa <b>dos lenguajes complementarios</b>:</p>
 <ul><li><b>Python en Google Colab</b>: laboratorios de análisis y visualización (sin instalar nada).</li>
 <li><b>R en RStudio, publicado en RPubs</b>: informes reproducibles (R Markdown) que se publican en la web y se entregan como enlace.</li></ul>
 <p>Las entregas se registran en el <b>aula virtual</b> pegando el enlace de Colab y/o de RPubs en cada actividad.</p>"""),
 ("2. Google Colab (Python)", """<ol><li>Desde el aula, abrí el botón <b>“Laboratorio en Google Colab”</b> de la sesión (necesitás tu cuenta de Google).</li>
 <li>Menú <b>Entorno de ejecución → Ejecutar todas</b>. La primera celda clona el repositorio para acceder a los datos.</li>
 <li><b>Archivo → Guardar una copia en Drive</b> para trabajar sobre tu propia copia.</li>
 <li>Para entregar: <b>Compartir → Acceso general → Cualquier persona con el enlace → Lector</b>, copiá el enlace y pegalo en el aula.</li></ol>"""),
 ("3. RStudio (R)", """<ol><li>Instalá <b>R</b> (cran.r-project.org) y luego <b>RStudio Desktop</b> (posit.co/downloads).</li>
 <li>Descargá o cloná el repositorio del curso y abrí el archivo de la sesión, p. ej. <code>r/01_percepcion.Rmd</code>.</li>
 <li>Ejecutá una sola vez <code>r/instalar_paquetes.R</code> para instalar los paquetes.</li>
 <li>Presioná <b>Knit</b>: se genera un HTML con tu análisis. Cambiá el autor en el encabezado (YAML) por tu nombre.</li></ol>"""),
 ("4. Publicar en RPubs", """<ol><li>Creá una cuenta gratuita en <b>rpubs.com</b>.</li>
 <li>En la vista previa del Knit, botón <b>Publish → RPubs</b>, ingresá con tu cuenta y poné un título descriptivo.</li>
 <li>Copiá el enlace (<code>https://rpubs.com/tu_usuario/...</code>) y pegalo en el aula.</li>
 <li>Para actualizar: volvé a presionar <b>Publish</b> y elegí <b>el mismo documento</b> (mantiene el enlace).</li></ol>
 <p class='warn'><b>Atención:</b> RPubs es <b>público</b> y estático. No publiques datos personales, cédulas ni información confidencial. Para tableros que requieren servidor (Shiny) se necesita otro servicio (p. ej. shinyapps.io).</p>"""),
 ("5. Qué se entrega y cómo se evalúa", """<table><tr><th>Entrega</th><th>Formato</th></tr>
 <tr><td>Ejercicios S1–S3 y S6</td><td>Documento R Markdown publicado en <b>RPubs</b> (enlace)</td></tr>
 <tr><td>Mini-proyecto 1</td><td>RPubs (una página ejecutiva)</td></tr>
 <tr><td>Mini-proyecto 2</td><td>RPubs (tablero plotly/crosstalk) <b>+</b> Colab (versión Python)</td></tr>
 <tr><td>Mini-proyecto 3</td><td>RPubs <b>+</b> Colab</td></tr>
 <tr><td>Integrador</td><td>Informe en RPubs <b>+</b> notebook reproducible en Colab y repositorio</td></tr></table>
 <p>Las rúbricas están en el aula (Recursos → Rúbricas).</p>"""),
])

CHECKLIST = [
 ("Mensaje y audiencia", ["¿Qué pregunta responde y para quién?", "¿El título afirma un hallazgo que los datos sostienen?", "¿Un gráfico = un mensaje?"]),
 ("Elección y construcción", ["¿El gráfico corresponde al tipo de dato y a la pregunta?", "¿Las barras parten de cero y están ordenadas?", "¿Evité 3D, sombras y decoración?", "¿Resolví el overplotting?"]),
 ("Color y accesibilidad", ["¿Uso paleta segura (Okabe-Ito/viridis)?", "¿Se entiende en escala de grises?", "¿Hay contraste suficiente y tipografía legible?", "¿Etiqueté directamente en vez de usar leyendas lejanas?"]),
 ("Integridad y ética", ["¿Las escalas son comparables entre paneles?", "¿Evité doble eje y recortes temporales a conveniencia?", "¿Mostré el n y la incertidumbre?", "¿Citó la fuente, fecha y definición de métricas?", "¿Los mapas usan tasas y no conteos?"]),
 ("Reproducibilidad", ["¿El informe se regenera con un comando?", "¿Fijé semillas (set.seed / random_state)?", "¿Documenté paquetes y versiones?", "¿Declaré el uso de herramientas de IA?"]),
]

ELEGIR = [
 ("¿Cómo se distribuye una variable?", "1 numérica", "Histograma (probar bins), densidad, ECDF", "Caja o violín si hay grupos", "Torta"),
 ("¿Cuánto hay por categoría?", "categórica + numérica", "Barras ordenadas, lollipop, dot plot", "Barras agrupadas (pocas categorías)", "Torta/dona con muchas partes"),
 ("¿Qué parte del total?", "partes → todo", "Barras apiladas al 100 %", "Treemap (jerarquías)", "Torta con más de 3 partes"),
 ("¿Se relacionan X e Y?", "2 numéricas", "Dispersión (con transparencia)", "Hexbin / bin2d / suavizado", "Doble eje Y"),
 ("¿Cómo cambia en el tiempo?", "serie temporal", "Línea", "Small multiples; heatmap año×mes", "Barras con eje truncado"),
 ("¿Cómo se comparan muchos grupos en el tiempo?", "serie × grupo", "Small multiples con ejes comunes", "Línea resaltada + resto en gris", "Spaghetti de 20 colores"),
 ("¿Qué pasa en el mapa?", "geográfico", "Coropleta con tasas; burbujas para absolutos", "Mapas de puntos/densidad", "Coropleta de conteos absolutos"),
 ("¿Cómo se conectan las entidades?", "red", "Layout de fuerzas con pocas etiquetas", "Matriz de adyacencia ordenada", "Hairball sin filtrar"),
 ("¿Cómo comparo muchas variables?", "alta dimensión", "Matriz de correlación, coordenadas paralelas", "PCA (interpretable), t-SNE (solo vecindades)", "Radar con muchas series"),
]
