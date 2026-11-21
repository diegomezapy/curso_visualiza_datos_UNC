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
