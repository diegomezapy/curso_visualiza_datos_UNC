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
