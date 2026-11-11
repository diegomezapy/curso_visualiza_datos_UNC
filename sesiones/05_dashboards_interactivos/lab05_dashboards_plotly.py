# %% [markdown]
# # Lab 5 · Dashboards interactivos con Plotly
# Principios: jerarquía (KPIs arriba), filtros globales, interacción con propósito (*overview first, zoom & filter, details on demand*).
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

import plotly.express as px, plotly.graph_objects as go
from plotly.subplots import make_subplots
v = datos.ventas(); v["mes"] = v.fecha.dt.to_period("M").dt.to_timestamp()

# %% [markdown]
# ## 1. Gráfico interactivo con filtro (dropdown) y selector de rango

# %%
m = v.groupby(["mes", "sucursal"]).ventas_gs_miles.sum().reset_index()
fig = go.Figure()
for i, s in enumerate(m.sucursal.unique()):
    g = m[m.sucursal == s]
    fig.add_scatter(x=g.mes, y=g.ventas_gs_miles / 1e3, name=s, mode="lines", visible=True,
                    line=dict(color=estilo.OKABE_ITO[i]))
sucs = list(m.sucursal.unique())
botones = [dict(label="Todas", method="update", args=[{"visible": [True] * len(sucs)}])] + \
          [dict(label=s, method="update", args=[{"visible": [j == i for j in range(len(sucs))]}]) for i, s in enumerate(sucs)]
fig.update_layout(template=estilo.PLOTLY_TEMPLATE, title="Ventas mensuales por sucursal (millones de Gs.)",
                  updatemenus=[dict(buttons=botones, x=1.0, xanchor="right", y=1.15)],
                  xaxis=dict(rangeslider=dict(visible=True)), hovermode="x unified", yaxis_title="Millones de Gs.")
fig.write_html(estilo.salida("lab05_serie_interactiva.html")); print("ok")

# %% [markdown]
# ## 2. Panel (dashboard estático-interactivo) en un solo HTML

# %%
tot = v.ventas_gs_miles.sum() / 1e6; mg = (1 - v.costo_gs_miles.sum() / v.ventas_gs_miles.sum()) * 100
fig = make_subplots(rows=2, cols=2, specs=[[{"type": "indicator"}, {"type": "indicator"}], [{"type": "bar"}, {"type": "xy"}]],
                    row_heights=[.25, .75], subplot_titles=("", "", "Ventas por categoría", "Evolución mensual"))
fig.add_trace(go.Indicator(mode="number", value=tot, title="Ventas totales (miles de MM Gs.)", number=dict(valueformat=",.1f")), 1, 1)
fig.add_trace(go.Indicator(mode="number", value=mg, title="Margen bruto", number=dict(suffix="%", valueformat=".1f")), 1, 2)
c = v.groupby("categoria").ventas_gs_miles.sum().sort_values() / 1e6
fig.add_trace(go.Bar(x=c.values, y=c.index, orientation="h", marker_color=estilo.BASE, hovertemplate="%{y}: %{x:.2f}<extra></extra>"), 2, 1)
t = v.groupby("mes").ventas_gs_miles.sum() / 1e3
fig.add_trace(go.Scatter(x=t.index, y=t.values, line=dict(color=estilo.ENFASIS), name="Ventas"), 2, 2)
fig.update_layout(template=estilo.PLOTLY_TEMPLATE, height=620, showlegend=False, title="Dashboard comercial 2024-2025")
fig.write_html(estilo.salida("lab05_dashboard.html")); print("ok")

# %% [markdown]
# ## 3. App Dash (opcional): filtros reales con *callbacks*
# Ejecutá `python sesiones/05_dashboards_interactivos/app_dash.py` y abrí http://127.0.0.1:8050.
# Requiere `pip install dash`.
#
# ## 4. Checklist de dashboard
# - ¿Se responde la pregunta de la audiencia en 5 segundos? - ¿Los KPIs tienen comparación y unidad?
# - ¿Los filtros afectan a todo lo que dicen afectar? - ¿Hay estado de "sin datos"? - ¿Carga rápido (<3 s)?
# - ¿Accesible (contraste, tamaño de fuente, no solo color)?
#
# ## 5. Ejercicio (mini-proyecto 2)
# Extendé el dashboard con (a) filtro de año, (b) un mapa o heatmap día×hora/mes×categoría, (c) texto de insight dinámico.
