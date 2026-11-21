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
