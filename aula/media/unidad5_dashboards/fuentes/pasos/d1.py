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
