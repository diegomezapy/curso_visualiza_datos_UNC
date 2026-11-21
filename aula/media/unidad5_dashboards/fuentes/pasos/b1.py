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
