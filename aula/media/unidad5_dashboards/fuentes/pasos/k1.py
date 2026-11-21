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
