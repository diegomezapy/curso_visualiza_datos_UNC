"""App Dash de ejemplo: ventas por sucursal/categoría con filtros.  python app_dash.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import pandas as pd, plotly.express as px
from dash import Dash, dcc, html, Input, Output
from cvd import datos

v = datos.ventas(); v["mes"] = v.fecha.dt.to_period("M").dt.to_timestamp(); v["anio"] = v.fecha.dt.year
app = Dash(__name__)
app.layout = html.Div(style={"maxWidth": 1000, "margin": "auto", "fontFamily": "sans-serif"}, children=[
    html.H2("Dashboard de ventas"),
    html.Div([dcc.Dropdown(sorted(v.sucursal.unique()), multi=True, id="suc", placeholder="Sucursales (todas)"),
              dcc.RadioItems([2024, 2025, "Ambos"], "Ambos", id="anio", inline=True)]),
    html.H3(id="kpi"), dcc.Graph(id="serie"), dcc.Graph(id="cat")])

@app.callback(Output("kpi", "children"), Output("serie", "figure"), Output("cat", "figure"),
              Input("suc", "value"), Input("anio", "value"))
def actualizar(suc, anio):
    d = v if not suc else v[v.sucursal.isin(suc)]
    if anio != "Ambos": d = d[d.anio == anio]
    kpi = f"Ventas: {d.ventas_gs_miles.sum()/1e6:,.2f} miles de MM Gs. · Margen: {(1-d.costo_gs_miles.sum()/d.ventas_gs_miles.sum())*100:.1f}%"
    s = px.line(d.groupby("mes").ventas_gs_miles.sum().reset_index(), x="mes", y="ventas_gs_miles", template="simple_white")
    c = px.bar(d.groupby("categoria").ventas_gs_miles.sum().sort_values().reset_index(), x="ventas_gs_miles", y="categoria",
               orientation="h", template="simple_white")
    return kpi, s, c

if __name__ == "__main__":
    app.run(debug=True)
