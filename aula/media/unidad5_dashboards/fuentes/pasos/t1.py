p = cubo.groupby("pais", as_index=False).fob_mm.sum()
p = p.sort_values("fob_mm", ascending=False)
p["grupo"] = p.pais.where(p.index.isin(p.index[:8]), "OTROS")
p = p.groupby("grupo", as_index=False).fob_mm.sum()
fig = px.treemap(p, path=["grupo"], values="fob_mm",
                 title="Origen del valor importado")
fig.update_traces(texttemplate="%{label}<br>%{value:,.0f}",
                  marker_colors=["#0072B2"] * len(p))
