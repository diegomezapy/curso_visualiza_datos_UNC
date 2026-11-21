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
