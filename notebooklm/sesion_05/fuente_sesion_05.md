# Sesión 5 · Dashboards interactivos
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U2.
Resumen: Jerarquía y filtros con propósito; Plotly (HTML interactivo) y Dash (callbacks).

## Objetivos
- Diseñar la jerarquía y los filtros de un tablero según la audiencia.
- Implementar interacción con propósito en Plotly y opcionalmente Dash.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 5 · Dashboards interactivos
**Unidad del programa:** U2 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Diseñar la jerarquía y los filtros de un tablero según la audiencia.
- Implementar interacción con propósito en Plotly (y opcionalmente Dash).

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-40 | Revisión de MP1 (galería y retroalimentación con rúbrica R2) |
| 40-90 | Principios de diseño de dashboards; mantra de Shneiderman; anti-patrones |
| 90-105 | Pausa |
| 105-190 | **Lab 5** (Plotly) + demo de `app_dash.py` con callbacks |
| 190-240 | Planificación del **Mini-proyecto 2** |

## Trabajo asincrónico
- Lectura: Few (2013), capítulos sobre errores y principios de diseño; documentación de Plotly y Dash.
- **Mini-proyecto 2:** extender el dashboard (filtro de año + heatmap/mapa + insight dinámico).
- Quiz 5.

## Entrega y evaluación
**Mini-proyecto 2** (10 pts, R2) · Quiz 5.

## Laboratorio
[`lab05_dashboards_plotly.py`](lab05_dashboards_plotly.py) · [`app_dash.py`](app_dash.py)

### Pista R (RStudio → RPubs)
[`r/05_dashboards_interactivos.Rmd`](../../r/05_dashboards_interactivos.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_05_dashboards.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/5).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **El mantra de Shneiderman para visualización interactiva es…** → Overview first, zoom and filter, then details on demand. Primero visión general, luego filtrar/acercar y finalmente detalles bajo demanda.
- **¿Dónde conviene ubicar los KPIs principales de un dashboard?** → Arriba a la izquierda, en la zona de mayor atención. En culturas de lectura izquierda-derecha y arriba-abajo esa es la zona que se ve primero.
- **Un filtro global debe…** → Afectar de forma coherente y visible a todas las vistas indicadas. Si el usuario no sabe qué afecta el filtro, el tablero se vuelve engañoso.
- **Una interacción 'decorativa' es aquella que…** → No ayuda a responder la pregunta de la audiencia. La interacción debe servir a la tarea: filtrar, comparar, detallar.
- **Un objetivo razonable de rendimiento para un tablero web es…** → Cargar en menos de 3 segundos agregando o precalculando datos. Una carga lenta hace que los usuarios abandonen; conviene agregar y precalcular.

## Actividades evaluadas
- Mini-proyecto 2: dashboard con filtro de año + heatmap/mapa + insight · RPubs (R) + Colab (Python) (10 pts)

## Texto de la presentación de la sesión (Dashboards con datos de aduanas)
### Diapositiva 1 · MAESTRÍA EN INGENIERÍA Y CIENCIA DE DATOS · FACET – UNC
- Dashboards: del dato al tablero
- Cómo diseñar un tablero que responde preguntas, con datos reales de la base de aduanas (DNIT) y código Python en RStudio
- Sesión 5 · Unidad 2 · Visual analytics, KPIs y storytelling
### Diapositiva 2 · Un tablero responde preguntas de una audiencia
- Punto de partida
- Audiencia
- ¿Quién lo mira?
- Un jefe de aduanas, un analista de comercio exterior o una empresa importadora necesitan tableros distintos.
- Decisión
- ¿Qué decisión apoya?
- «¿Dónde se concentra la importación y cómo evoluciona respecto del año anterior?»
- Frecuencia
- ¿Cada cuánto se consulta?
- Una vista mensual de seguimiento; una exploración puntual de detalle. Cambia el nivel de detalle.
- Un tablero es una pantalla única que reúne la información clave para un objetivo y se entiende de un vistazo (Few, 2013).
- Few, S. (2013). Information Dashboard Design. Analytics Press.
### Diapositiva 3 · Los datos: importaciones de electrónica en la base de aduanas
- Punto de partida
- import pandas as pd
- import plotly.express as px
- import plotly.graph_objects as go
- import plotly.io as pio
- from plotly.subplots import make_subplots
- pio.templates.default = "plotly_white"
- cubo = pd.read_csv("cubo_importaciones.csv")
- cubo["fecha"] = pd.to_datetime(
- dict(year=cubo.anio, month=cubo.mes, day=1))
- cubo["fob_mm"] = cubo.fob_usd / 1e6   # millones de USD
- # La base no trae junio de 2025: se excluye ese mes
- # de ambos años para comparar períodos iguales
- cubo = cubo[cubo.mes != 6]
- anio
- mes
- aduana
- pais
- medio
- items
- fob_usd
- AEROP. PETTIRO
- ALEMANIA
- AVION
- AEROP. PETTIRO
- ARGENTINA
- AVION
- AEROP. PETTIRO
- BRASIL
- AVION
- AEROP. PETTIRO
- BULGARIA
- AVION
- AEROP. PETTIRO
- CHILE
- AVION
- AEROP. PETTIRO
- CHINA
- AVION
- …
- …
- …
- …
- …
- …
- …
- ▸ Datos agregados por año, mes, aduana, país y medio de transporte (3.304 filas).
- ▸ Sale de 141.816 filas de subítems; el archivo original usa ; y coma decimal.
- ▸ La base no trae junio de 2025: se excluye de ambos años.
- Antes de graficar: ¿qué representa una fila? ¿están todos los períodos? Un tablero hereda los problemas de sus datos.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 4 · Antes del tablero: sumar subítems infla las cifras
- Los datos · trampa
- ingenuo = sub.groupby("aduana").fob_usd.sum()
- correcto = (sub.drop_duplicates(["despacho", "item"])
- .groupby("aduana").fob_usd.sum())
- t = pd.DataFrame({"Suma de todas las filas": ingenuo,
- "Un registro por ítem": correcto})
- t = t.nlargest(6, "Suma de todas las filas") / 1e6
- fig = px.bar(t, barmode="group",
- color_discrete_sequence=["#D55E00", "#0072B2"],
- title="FOB por aduana (muestra de 300 despachos)",
- labels={"value": "Millones de USD", "aduana": "",
- "variable": ""})
- ▸ Cada fila de la base es un subítem; el valor FOB del ítem se repite en cada subítem.
- ▸ En una muestra de 300 despachos, sumar todas las filas da unas 6 veces el valor real.
- ▸ Un tablero con la cifra equivocada es peor que no tener tablero: primero se valida el dato.
- Antes de diseñar el tablero, definí la unidad de análisis: acá, un registro por ítem de despacho.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 5 · Anatomía de un tablero: qué va en cada zona
- Diseño
- KPI
- 437 M USD
- KPI
- 15.813 ítems
- KPI
- 85 % China
- Tendencia
- valor mensual 2024 vs 2025
- Comparación
- ranking de aduanas
- Detalle bajo demanda
- tabla filtrable · mapa de calor
- Arriba: KPI con su comparación
- Centro: tendencia en el tiempo
- Costado: comparación entre categorías
- Abajo: detalle para quien lo necesite
- Lo más importante, arriba y a la izquierda; lo menos importante, abajo.
- Cada zona responde una pregunta distinta; los valores de ejemplo son los de las diapositivas siguientes.
### Diapositiva 6 · Arriba, lo que el lector necesita ver primero: los KPI
- Tarjetas de KPI
- a = cubo.groupby("anio").agg(fob=("fob_mm", "sum"),
- items=("items", "sum"))
- china = (cubo[cubo.pais == "CHINA"].groupby("anio").fob_mm.sum()
- / a.fob)
- kpis = [("Valor FOB (millones de USD)", a.fob, ",.0f"),
- ("Ítems importados", a["items"], ",d"),
- ("Participación de China", china, ".0%")]
- fig = go.Figure()
- for i, (nombre, s, fmt) in enumerate(kpis):
- fig.add_trace(go.Indicator(
- mode="number+delta", value=s[2025],
- delta=dict(reference=s[2024], relative=True,
- valueformat=".1%"),
- number=dict(valueformat=fmt),
- title=dict(text=nombre),
- domain=dict(row=0, column=i)))
- fig.update_layout(grid=dict(rows=1, columns=3),
- title="2025 frente a 2024 (mismos meses)")
- ▸ Un KPI = una cifra + una comparación. Acá: valor de 2025 y variación respecto de 2024, en los mismos meses (la base no trae junio de 2025).
- ▸ go.Indicator dibuja el número y el delta (verde si sube, rojo si baja).
- ▸ Pocos KPI, grandes y arriba: son lo primero que se mira (overview first).
- Un KPI sin comparación no se puede interpretar: siempre con referencia.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 7 · La tendencia en el tiempo: dos años superpuestos por mes
- Tendencia
- m = cubo.groupby(["anio", "mes"], as_index=False).fob_mm.sum()
- m["anio"] = m.anio.astype(str)
- fig = px.line(m, x="mes", y="fob_mm", color="anio",
- markers=True,
- color_discrete_map={"2024": "#9FB6CB",
- "2025": "#D55E00"},
- title="Valor importado por mes",
- labels={"fob_mm": "Millones de USD",
- "mes": "Mes", "anio": ""})
- fig.update_xaxes(dtick=1)
- ▸ Superponer 2024 y 2025 por mes permite ver la estacionalidad y la variación en un mismo plano.
- ▸ Se resalta el año actual (naranja) y el anterior queda como contexto (gris).
- ▸ En un tablero, el color de énfasis se usa solo para lo que importa.
- Una línea por año, un color de énfasis: la comparación se lee sin leyenda complicada.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 8 · Comparar categorías: ranking de aduanas, ordenado y con foco
- Ranking
- r = (cubo.groupby("aduana", as_index=False).fob_mm.sum()
- .nlargest(10, "fob_mm").sort_values("fob_mm"))
- r["color"] = ["#D55E00" if a == r.aduana.iloc[-1]
- else "#9FB6CB" for a in r.aduana]
- fig = go.Figure(go.Bar(
- x=r.fob_mm, y=r.aduana, orientation="h",
- marker_color=r.color,
- hovertemplate="%{y}: %{x:,.1f} millones<extra></extra>"))
- fig.update_layout(title="Aduanas con mayor valor importado")
- fig.update_xaxes(title="Millones de USD (2024–2025)")
- ▸ Barras horizontales ordenadas: el ranking se lee de un vistazo.
- ▸ hovertemplate agrega el detalle bajo demanda: al pasar el mouse aparece el valor exacto.
- ▸ Las 3 primeras aduanas concentran más de la mitad del valor importado.
- Ordenar y resaltar una sola barra: el ranking responde la pregunta sin esfuerzo.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 9 · Composición: países de origen con un treemap
- Composición
- p = cubo.groupby("pais", as_index=False).fob_mm.sum()
- p = p.sort_values("fob_mm", ascending=False)
- p["grupo"] = p.pais.where(p.index.isin(p.index[:8]), "OTROS")
- p = p.groupby("grupo", as_index=False).fob_mm.sum()
- fig = px.treemap(p, path=["grupo"], values="fob_mm",
- title="Origen del valor importado")
- fig.update_traces(texttemplate="%{label}<br>%{value:,.0f}",
- marker_colors=["#0072B2"] * len(p))
- ▸ El treemap muestra la proporción de cada país como un área: sirve con muchas categorías.
- ▸ China domina con claridad; el resto son cuotas pequeñas: se agrupan en «Otros».
- ▸ Cuando una categoría domina, una barra ordenada compara mejor que un treemap: elegir según la pregunta.
- Agrupá la cola de categorías pequeñas y declaralo: así el gráfico se entiende.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 10 · Patrones: mapa de calor aduana × mes
- Estacionalidad
- top = cubo.groupby("aduana").fob_mm.sum().nlargest(8).index
- z = (cubo[cubo.aduana.isin(top) & (cubo.anio == 2025)]
- .pivot_table(index="aduana", columns="mes",
- values="fob_mm", aggfunc="sum")
- .loc[top])
- fig = px.imshow(z, aspect="auto",
- color_continuous_scale="Blues",
- title="Valor importado por aduana y mes (2025)",
- labels=dict(x="Mes (2025)", y="",
- color="Millones<br>de USD"))
- ▸ Un mapa de calor cruza dos categorías (aduana y mes) y colorea el valor.
- ▸ Muestra dónde y cuándo se concentra la actividad; los blancos son meses sin operaciones.
- ▸ Útil como vista de detalle: no para un lector que necesita una cifra.
- El color codifica intensidad: usá una sola gama (secuencial) para valores que crecen.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 11 · Anti-patrón: el tablero recargado
- Anti-patrón
- fig = make_subplots(
- rows=2, cols=3,
- specs=[[{"type": "pie"}] * 3,
- [{"type": "bar"}, {"type": "pie"}, {"type": "bar"}]])
- pais = cubo.groupby("pais").fob_mm.sum().nlargest(12)
- aduana = cubo.groupby("aduana").fob_mm.sum().nlargest(12)
- medio = cubo.groupby("medio").fob_mm.sum()
- fig.add_trace(go.Pie(labels=pais.index, values=pais), 1, 1)
- fig.add_trace(go.Pie(labels=aduana.index, values=aduana), 1, 2)
- fig.add_trace(go.Pie(labels=medio.index, values=medio), 1, 3)
- fig.add_trace(go.Bar(x=pais.index, y=pais), 2, 1)
- fig.add_trace(go.Pie(labels=pais.index, values=pais, hole=.5), 2, 2)
- fig.add_trace(go.Bar(x=aduana.index, y=aduana), 2, 3)
- ▸ Seis gráficos del mismo dato: ninguno responde una pregunta concreta.
- ▸ Tortas con 12 sectores, etiquetas superpuestas y colores de arcoíris sin criterio.
- ▸ Sin KPI, sin título ni jerarquía: el lector no sabe por dónde empezar.
- Más gráficos no es más información: cada elemento debe responder una pregunta.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 12 · La versión corregida: jerarquía, un mensaje y color con intención
- Tablero corregido
- fig = make_subplots(rows=1, cols=2, column_widths=[.5, .5],
- horizontal_spacing=.3,
- subplot_titles=("Valor mensual (millones de USD)",
- "Top 8 aduanas (2024–2025)"))
- for anio, col in [(2024, "#9FB6CB"), (2025, "#D55E00")]:
- s = cubo[cubo.anio == anio].groupby("mes").fob_mm.sum()
- fig.add_trace(go.Scatter(x=s.index, y=s.values,
- name=str(anio), mode="lines+markers",
- line=dict(color=col)), 1, 1)
- r = (cubo.groupby("aduana").fob_mm.sum()
- .nlargest(8).sort_values())
- fig.add_trace(go.Bar(x=r.values, y=r.index, orientation="h",
- marker_color="#0072B2", showlegend=False), 1, 2)
- fig.update_layout(title="Importaciones de electrónica: "
- "2025 supera a 2024 (+39 %)")
- ▸ Un título que dice el mensaje («2025 supera a 2024») en lugar de un título descriptivo.
- ▸ Cada panel responde una pregunta: ¿cómo evolucionó? y ¿dónde entra la mercadería?
- ▸ Mismo color para el mismo año en todos los paneles; el resto en azul o gris.
- Menos elementos, mejor jerarquía: el título cuenta la conclusión y los paneles la sostienen.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 13 · Interacción con propósito: un filtro por medio de transporte
- Interacción con propósito
- medios = sorted(cubo.medio.unique())
- fig = go.Figure()
- for m in medios:
- s = cubo[cubo.medio == m].groupby("fecha").fob_mm.sum()
- fig.add_scatter(x=s.index, y=s.values, name=m,
- mode="lines")
- botones = [dict(label="Todos", method="update",
- args=[{"visible": [True] * len(medios)}])]
- botones += [dict(label=m.title(), method="update",
- args=[{"visible": [x == m for x in medios]}])
- for m in medios]
- fig.update_layout(updatemenus=[dict(buttons=botones, x=1,
- xanchor="right", y=1.17)],
- title="Valor mensual por medio de transporte",
- yaxis_title="Millones de USD")
- ▸ El menú desplegable filtra qué series se ven: acá, por medio de transporte.
- ▸ Se agrega solo la interacción que sirve a una pregunta: ¿cambia el patrón según el medio?
- ▸ En el aula hay un tablero interactivo para probarlo (se exporta con fig.write_html()).
- Cada control debe tener un propósito; si no responde una pregunta, sobra.
- Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD
### Diapositiva 14 · El mantra de Shneiderman aplicado a este tablero
- Interacción
- Vista general primero
- KPI + tendencia + ranking de aduanas, todo visible sin hacer nada.
- Tarjetas y gráficos de las diapositivas 6–9
- Zoom y filtros
- El lector acota por medio de transporte, año o aduana.
- Menú desplegable de la diapositiva 13
- Detalles bajo demanda
- Al pasar el mouse aparece el valor exacto; la tabla muestra los registros.
- hovertemplate y mapa de calor
- Interactividad con propósito: cada filtro y cada hover debe ayudar a responder una pregunta concreta.
- Shneiderman, B. (1996). The eyes have it: a task by data type taxonomy for information visualizations.
### Diapositiva 15 · RStudio con código Python: el paquete reticulate
- Herramientas
- # En la consola de R (una sola vez)
- install.packages("reticulate")
- library(reticulate)
- virtualenv_create("r-viz")
- py_install(c("pandas", "plotly"), "r-viz")
- ---
- title: "Tablero de aduanas"
- output: html_document
- ---
- ```{r}
- reticulate::use_virtualenv("r-viz")
- ```
- ```{python}
- import pandas as pd
- ```
- ▸ Un documento R Markdown puede mezclar chunks de R ( `{r} ) y de Python ( `{python} ).
- ▸ Los objetos de Python se leen desde R con py$objeto, y los de R desde Python con r.objeto.
- ▸ Los gráficos de plotly se incrustan como HTML interactivo en el documento.
- ▸ Knit → Publish → RPubs: el tablero queda en un enlace, sin servidor (los filtros corren en el navegador).
- ▸ Por qué: usamos el entorno de R que ya conocemos (editor, Knit, RPubs) con las librerías de Python.
- El código de esta presentación está en r/05_tablero_aduanas_python.Rmd listo para abrir en RStudio.
- Documentación: rstudio.github.io/reticulate
### Diapositiva 16 · Checklist de calidad de un tablero
- Para recordar
- Pregunta de control
- Si la respuesta es no…
- ¿Se sabe en 5 segundos cuál es el mensaje principal?
- Poner un título que enuncie la conclusión
- ¿Los KPI están arriba y tienen una comparación?
- Agregar referencia: período anterior o meta
- ¿Cada gráfico responde una pregunta distinta?
- Eliminar o fusionar los que se repiten
- ¿Se usa el color con intención (énfasis, una gama)?
- Reducir a un color de énfasis y grises
- ¿Cada control interactivo tiene un propósito?
- Quitar los filtros que nadie usa
- ¿Están declaradas la fuente, los períodos y las limitaciones?
- Agregar pie con fuente y notas (p. ej. «sin junio 2025»)
- Basado en Few (2013) y en el mantra de Shneiderman.
### Diapositiva 17 · Para practicar: tu propio tablero
- Tu turno
- ▸ Abrí 05_tablero_aduanas_python.Rmd en RStudio y ejecutalo con los datos agregados.
- ▸ Agregá un filtro de año y un indicador nuevo (por ejemplo, el valor por kilo).
- ▸ Corregí el tablero recargado aplicando el checklist.
- ▸ Resolvé el Quiz 5A del aula: evalúa lo visto en esta presentación.
- Un buen tablero no muestra todo: muestra lo que ayuda a decidir.

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Plotly para Python · documentación (web, en) · https://plotly.com/python/ · 
- Dash · documentación (web, en) · https://dash.plotly.com/ · 
- crosstalk · filtros interactivos para HTML estático (R) (web, en) · https://rstudio.github.io/crosstalk/ · funciona en RPubs
- Shiny · documentación (web, en) · https://shiny.posit.co/ · requiere servidor
