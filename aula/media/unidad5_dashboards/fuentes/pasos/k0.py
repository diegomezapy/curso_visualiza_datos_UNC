ingenuo = sub.groupby("aduana").fob_usd.sum()
correcto = (sub.drop_duplicates(["despacho", "item"])
               .groupby("aduana").fob_usd.sum())
t = pd.DataFrame({"Suma de todas las filas": ingenuo,
                  "Un registro por ítem": correcto})
t = t.nlargest(6, "Suma de todas las filas") / 1e6
fig = px.bar(t, barmode="group",
             color_discrete_sequence=["#D55E00", "#0072B2"],
             title="FOB por aduana (muestra de 300 despachos)",
             labels={"value": "Millones de USD", "aduana": "",
                     "variable": ""})
