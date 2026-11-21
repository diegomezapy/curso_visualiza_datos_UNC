"""Contenido de la presentación «Dashboards» (sesión 5, Unidad 2). Datos: importaciones de electrónica 2024-2025 (base de aduanas, DNIT).
El código es Python (se ejecuta en RStudio con reticulate: chunks ```{python}```); tools/dashboards_figuras.py ejecuta ESTE mismo código para generar las figuras.
Las líneas con § son las nuevas respecto de la figura anterior de la misma diapositiva."""
def L(t): return t.strip("\n").split("\n")
SETUP = L('''
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.templates.default = "plotly_white"

cubo = pd.read_csv("cubo_importaciones.csv")
cubo["fecha"] = pd.to_datetime(
    dict(year=cubo.anio, month=cubo.mes, day=1))
cubo["fob_mm"] = cubo.fob_usd / 1e6   # millones de USD
# La base no trae junio de 2025: se excluye ese mes
# de ambos años para comparar períodos iguales
cubo = cubo[cubo.mes != 6]
''')
PIE = "Fuente: DNIT, base de datos abiertos de aduanas · importaciones del rubro electrónica, 2024–2025 · valor FOB en USD"
FIGS = [
 dict(id="k0", tag="Los datos · trampa", pie=PIE, titulo="Antes del tablero: sumar subítems infla las cifras",
  codigo=L('''
ingenuo = sub.groupby("aduana").fob_usd.sum()
correcto = (sub.drop_duplicates(["despacho", "item"])
               .groupby("aduana").fob_usd.sum())
t = pd.DataFrame({"Suma de todas las filas": ingenuo,
                  "Un registro por ítem": correcto})
t = t.nlargest(6, "Suma de todas las filas") / 1e6
fig = px.bar(t, barmode="group",
             color_discrete_sequence=["#D55E00", "#0072B2"],
             title="FOB por aduana (muestra de 300 despachos)",
             labels={"value": "Millones de USD", "aduana": "",
                     "variable": ""})
'''),
  puntos=["Cada fila de la base es un **subítem**; el valor FOB del ítem se **repite** en cada subítem.", "En una muestra de 300 despachos, sumar todas las filas da unas **6 veces** el valor real.", "Un tablero con la cifra equivocada es peor que no tener tablero: primero se valida el dato."],
  mensaje="Antes de diseñar el tablero, definí la unidad de análisis: acá, un registro por ítem de despacho.",
  nota="Mostrar el error numérico antes de graficar. Deduplicar por (despacho, ítem)."),
 dict(id="k1", tag="Tarjetas de KPI", pie=PIE, titulo="Arriba, lo que el lector necesita ver primero: los KPI",
  codigo=L('''
a = cubo.groupby("anio").agg(fob=("fob_mm", "sum"),
                             items=("items", "sum"))
china = (cubo[cubo.pais == "CHINA"].groupby("anio").fob_mm.sum()
         / a.fob)
kpis = [("Valor FOB (millones de USD)", a.fob, ",.0f"),
        ("Ítems importados", a["items"], ",d"),
        ("Participación de China", china, ".0%")]
fig = go.Figure()
for i, (nombre, s, fmt) in enumerate(kpis):
    fig.add_trace(go.Indicator(
        mode="number+delta", value=s[2025],
        delta=dict(reference=s[2024], relative=True,
                   valueformat=".1%"),
        number=dict(valueformat=fmt),
        title=dict(text=nombre),
        domain=dict(row=0, column=i)))
fig.update_layout(grid=dict(rows=1, columns=3),
                  title="2025 frente a 2024 (mismos meses)")
'''),
  puntos=["Un **KPI** = una cifra + una comparación. Acá: valor de 2025 y variación respecto de 2024, en los **mismos meses** (la base no trae junio de 2025).", "`go.Indicator` dibuja el número y el delta (verde si sube, rojo si baja).", "Pocos KPI, grandes y arriba: son lo primero que se mira (*overview first*)."],
  mensaje="Un KPI sin comparación no se puede interpretar: siempre con referencia.",
  nota="Ojo: el color del delta no implica juicio de valor: una suba de importaciones no es buena ni mala por sí misma."),
 dict(id="l1", tag="Tendencia", pie=PIE, titulo="La tendencia en el tiempo: dos años superpuestos por mes",
  codigo=L('''
m = cubo.groupby(["anio", "mes"], as_index=False).fob_mm.sum()
m["anio"] = m.anio.astype(str)
fig = px.line(m, x="mes", y="fob_mm", color="anio",
              markers=True,
              color_discrete_map={"2024": "#9FB6CB",
                                  "2025": "#D55E00"},
              title="Valor importado por mes",
              labels={"fob_mm": "Millones de USD",
                      "mes": "Mes", "anio": ""})
fig.update_xaxes(dtick=1)
'''),
  puntos=["Superponer **2024 y 2025** por mes permite ver la estacionalidad y la variación en un mismo plano.", "Se resalta el año actual (naranja) y el anterior queda como contexto (gris).", "En un tablero, el color de énfasis se usa **solo** para lo que importa."],
  mensaje="Una línea por año, un color de énfasis: la comparación se lee sin leyenda complicada.",
  nota="Si falta algún mes en 2025 la línea se corta: avisar en el pie."),
 dict(id="b1", tag="Ranking", pie=PIE, titulo="Comparar categorías: ranking de aduanas, ordenado y con foco",
  codigo=L('''
r = (cubo.groupby("aduana", as_index=False).fob_mm.sum()
         .nlargest(10, "fob_mm").sort_values("fob_mm"))
r["color"] = ["#D55E00" if a == r.aduana.iloc[-1]
              else "#9FB6CB" for a in r.aduana]
fig = go.Figure(go.Bar(
    x=r.fob_mm, y=r.aduana, orientation="h",
    marker_color=r.color,
    hovertemplate="%{y}: %{x:,.1f} millones<extra></extra>"))
fig.update_layout(title="Aduanas con mayor valor importado")
fig.update_xaxes(title="Millones de USD (2024–2025)")
'''),
  puntos=["Barras horizontales **ordenadas**: el ranking se lee de un vistazo.", "`hovertemplate` agrega el **detalle bajo demanda**: al pasar el mouse aparece el valor exacto.", "Las 3 primeras aduanas concentran más de la mitad del valor importado."],
  mensaje="Ordenar y resaltar una sola barra: el ranking responde la pregunta sin esfuerzo.",
  nota="Verificar la afirmación del tercer punto con los números de la figura antes de presentarla."),
 dict(id="t1", tag="Composición", pie=PIE, titulo="Composición: países de origen con un treemap",
  codigo=L('''
p = cubo.groupby("pais", as_index=False).fob_mm.sum()
p = p.sort_values("fob_mm", ascending=False)
p["grupo"] = p.pais.where(p.index.isin(p.index[:8]), "OTROS")
p = p.groupby("grupo", as_index=False).fob_mm.sum()
fig = px.treemap(p, path=["grupo"], values="fob_mm",
                 title="Origen del valor importado")
fig.update_traces(texttemplate="%{label}<br>%{value:,.0f}",
                  marker_colors=["#0072B2"] * len(p))
'''),
  puntos=["El **treemap** muestra la proporción de cada país como un área: sirve con muchas categorías.", "China domina con claridad; el resto son cuotas pequeñas: se agrupan en **«Otros»**.", "Cuando una categoría domina, una **barra ordenada** compara mejor que un treemap: elegir según la pregunta."],
  mensaje="Agrupá la cola de categorías pequeñas y declaralo: así el gráfico se entiende.",
  nota="Alternativa más precisa: barras ordenadas con el porcentaje."),
 dict(id="h1", tag="Estacionalidad", pie=PIE, titulo="Patrones: mapa de calor aduana × mes",
  codigo=L('''
top = cubo.groupby("aduana").fob_mm.sum().nlargest(8).index
z = (cubo[cubo.aduana.isin(top) & (cubo.anio == 2025)]
     .pivot_table(index="aduana", columns="mes",
                  values="fob_mm", aggfunc="sum")
     .loc[top])
fig = px.imshow(z, aspect="auto",
                color_continuous_scale="Blues",
                title="Valor importado por aduana y mes (2025)",
                labels=dict(x="Mes (2025)", y="",
                            color="Millones<br>de USD"))
'''),
  puntos=["Un **mapa de calor** cruza dos categorías (aduana y mes) y colorea el valor.", "Muestra **dónde** y **cuándo** se concentra la actividad; los blancos son meses sin operaciones.", "Útil como vista de detalle: no para un lector que necesita una cifra."],
  mensaje="El color codifica intensidad: usá una sola gama (secuencial) para valores que crecen.",
  nota="Una escala secuencial de un solo tono; evitar arcoíris."),
 dict(id="a1", tag="Anti-patrón", pie=PIE, titulo="Anti-patrón: el tablero recargado",
  codigo=L('''
fig = make_subplots(
    rows=2, cols=3,
    specs=[[{"type": "pie"}] * 3,
           [{"type": "bar"}, {"type": "pie"}, {"type": "bar"}]])
pais = cubo.groupby("pais").fob_mm.sum().nlargest(12)
aduana = cubo.groupby("aduana").fob_mm.sum().nlargest(12)
medio = cubo.groupby("medio").fob_mm.sum()
fig.add_trace(go.Pie(labels=pais.index, values=pais), 1, 1)
fig.add_trace(go.Pie(labels=aduana.index, values=aduana), 1, 2)
fig.add_trace(go.Pie(labels=medio.index, values=medio), 1, 3)
fig.add_trace(go.Bar(x=pais.index, y=pais), 2, 1)
fig.add_trace(go.Pie(labels=pais.index, values=pais, hole=.5), 2, 2)
fig.add_trace(go.Bar(x=aduana.index, y=aduana), 2, 3)
'''),
  puntos=["**Seis gráficos** del mismo dato: ninguno responde una pregunta concreta.", "Tortas con 12 sectores, etiquetas superpuestas y colores de arcoíris sin criterio.", "Sin KPI, sin título ni jerarquía: el lector no sabe por dónde empezar."],
  mensaje="Más gráficos no es más información: cada elemento debe responder una pregunta.",
  nota="Pedir a la audiencia que enumere los problemas antes de mostrar la versión corregida."),
 dict(id="d1", tag="Tablero corregido", pie=PIE, titulo="La versión corregida: jerarquía, un mensaje y color con intención",
  codigo=L('''
fig = make_subplots(rows=1, cols=2, column_widths=[.5, .5],
    horizontal_spacing=.3,
    subplot_titles=("Valor mensual (millones de USD)",
                    "Top 8 aduanas (2024–2025)"))
for anio, col in [(2024, "#9FB6CB"), (2025, "#D55E00")]:
    s = cubo[cubo.anio == anio].groupby("mes").fob_mm.sum()
    fig.add_trace(go.Scatter(x=s.index, y=s.values,
        name=str(anio), mode="lines+markers",
        line=dict(color=col)), 1, 1)
r = (cubo.groupby("aduana").fob_mm.sum()
         .nlargest(8).sort_values())
fig.add_trace(go.Bar(x=r.values, y=r.index, orientation="h",
        marker_color="#0072B2", showlegend=False), 1, 2)
fig.update_layout(title="Importaciones de electrónica: "
                  "2025 supera a 2024 (+39 %)")
'''),
  puntos=["Un **título que dice el mensaje** («2025 supera a 2024») en lugar de un título descriptivo.", "Cada panel responde **una** pregunta: ¿cómo evolucionó? y ¿dónde entra la mercadería?", "Mismo color para el mismo año en todos los paneles; el resto en azul o gris."],
  mensaje="Menos elementos, mejor jerarquía: el título cuenta la conclusión y los paneles la sostienen.",
  nota="El +39 % compara 436,7 y 313,0 millones de USD (enero–mayo y julio–diciembre; junio de 2025 no está en la base)."),
 dict(id="i1", tag="Interacción con propósito", pie=PIE, titulo="Interacción con propósito: un filtro por medio de transporte",
  codigo=L('''
medios = sorted(cubo.medio.unique())
fig = go.Figure()
for m in medios:
    s = cubo[cubo.medio == m].groupby("fecha").fob_mm.sum()
    fig.add_scatter(x=s.index, y=s.values, name=m,
                    mode="lines")
botones = [dict(label="Todos", method="update",
                args=[{"visible": [True] * len(medios)}])]
botones += [dict(label=m.title(), method="update",
                 args=[{"visible": [x == m for x in medios]}])
            for m in medios]
fig.update_layout(updatemenus=[dict(buttons=botones, x=1,
                                    xanchor="right", y=1.17)],
                  title="Valor mensual por medio de transporte",
                  yaxis_title="Millones de USD")
'''),
  puntos=["El menú desplegable **filtra** qué series se ven: acá, por medio de transporte.", "Se agrega solo la interacción que **sirve a una pregunta**: ¿cambia el patrón según el medio?", "En el aula hay un tablero interactivo para probarlo (se exporta con `fig.write_html()`)."],
  mensaje="Cada control debe tener un propósito; si no responde una pregunta, sobra.",
  nota="RPubs publica HTML estático: los filtros de plotly funcionan en el navegador, sin servidor."),
]
