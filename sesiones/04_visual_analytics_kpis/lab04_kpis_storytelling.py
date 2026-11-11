# %% [markdown]
# # Lab 4 · Visual analytics: KPIs, *small multiples* y storytelling
# Del dato crudo a una narrativa: **contexto → conflicto → resolución**. Dataset: `ventas_retail`.
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

v = datos.ventas()
v["mes"] = v.fecha.dt.to_period("M").dt.to_timestamp(); v["anio"] = v.fecha.dt.year

# %% [markdown]
# ## 1. Definir KPIs (con fórmula y contexto)
# | KPI | Definición | Comparación |
# |---|---|---|
# | Ventas | Σ ventas | vs. año anterior |
# | Margen % | (ventas − costo) / ventas | vs. año anterior (pp) |
# | Ticket por unidad | ventas / unidades | vs. año anterior |

# %%
def kpis(df):
    return pd.Series({"ventas": df.ventas_gs_miles.sum() / 1e6,
                      "margen_pct": (1 - df.costo_gs_miles.sum() / df.ventas_gs_miles.sum()) * 100,
                      "ticket": df.ventas_gs_miles.sum() / df.unidades.sum()})
k = v.groupby("anio").apply(kpis, include_groups=False); print(k.round(2))

# %%
fig, axs = plt.subplots(1, 3, figsize=(12, 2.6))
for ax, (col, titulo, fmt, unid) in zip(axs, [("ventas", "Ventas 2025", "{:,.1f}", "miles de millones de Gs."),
                                              ("margen_pct", "Margen bruto 2025", "{:.1f}%", "(ventas − costo) / ventas"),
                                              ("ticket", "Ticket / unidad 2025", "{:,.0f}", "miles de Gs. por unidad")]):
    a, b = k.loc[2025, col], k.loc[2024, col]; delta = a - b if col == "margen_pct" else (a / b - 1) * 100
    ax.text(.02, .62, fmt.format(a), fontsize=30, fontweight="bold", color=estilo.BASE, transform=ax.transAxes)
    txt = f"{abs(delta):.2f} pp" if col == "margen_pct" else f"{abs(delta):.1f}%"
    ax.text(.02, .28, f"{'▲' if delta >= 0 else '▼'} {txt} vs 2024", fontsize=12,
            color="#009E73" if delta >= 0 else estilo.ENFASIS, transform=ax.transAxes)
    ax.set_title(titulo, loc="left", fontsize=11); ax.text(.02, .92, unid, fontsize=9, color=estilo.GRIS, transform=ax.transAxes); ax.axis("off")
estilo.guardar(fig, "lab04_tarjetas_kpi.png")

# %% [markdown]
# ## 2. *Small multiples*: comparar muchas series sin saturar

# %%
s = v.groupby(["mes", "sucursal"]).ventas_gs_miles.sum().unstack() / 1e3
fig, axs = plt.subplots(1, 5, figsize=(15, 2.8), sharex=True, sharey=True)
for ax, c in zip(axs, s.columns):
    for o in s.columns: ax.plot(s.index, s[o], color=estilo.GRIS_CLARO, lw=1)
    ax.plot(s.index, s[c], color=estilo.ENFASIS, lw=2); ax.set_title(c, fontsize=10); ax.tick_params(labelsize=8)
    ax.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
fig.suptitle("Ventas mensuales por sucursal (millones de Gs.)", x=0.01, ha="left", fontweight="bold")
estilo.guardar(fig, "lab04_small_multiples.png")

# %% [markdown]
# ## 3. Storytelling: un gráfico, un mensaje
# Respondé: **¿qué sucursal/categoría explica el crecimiento 2025 vs 2024?** (gráfico de contribución al cambio)

# %%
c = v.pivot_table(index="sucursal", columns="anio", values="ventas_gs_miles", aggfunc="sum") / 1e6
c["delta"] = c[2025] - c[2024]; c = c.sort_values("delta")
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.barh(c.index, c.delta, color=[estilo.ENFASIS if x == c.delta.max() else estilo.GRIS_CLARO for x in c.delta])
ax.set_title(f"{c.delta.idxmax()} aporta {c.delta.max()/c.delta.sum():.0%} del crecimiento 2025")
ax.set_xlabel("Variación de ventas 2025 vs 2024 (miles de MM Gs.)"); ax.grid(False)
estilo.guardar(fig, "lab04_contribucion.png")

# %% [markdown]
# ## 4. Ejercicio (mini-proyecto 1)
# Preparar **1 página** (figura única o panel de ≤4 gráficos) para un gerente comercial que responda
# *"¿dónde actuar el próximo trimestre?"*. Incluí: título-mensaje, KPIs con comparación, 1 gráfico de apoyo, fuente y nota metodológica. Usá la rúbrica de `docs/rubricas.md`.
