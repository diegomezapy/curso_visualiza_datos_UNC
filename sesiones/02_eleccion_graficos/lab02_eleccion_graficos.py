# %% [markdown]
# # Lab 2 · Elección del gráfico según pregunta y tipo de dato
# Catálogo: **distribución · cantidad · proporción · relación · tiempo**. Datos: `notas_estudiantes`, `ventas_retail`.
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

import seaborn as sns
n = datos.notas(); v = datos.ventas()

# %% [markdown]
# ## 1. Distribuciones — ¿cómo se reparten las notas?
# El histograma depende del ancho de *bin*; KDE, ECDF y violin complementan.

# %%
fig, axs = plt.subplots(2, 2, figsize=(11, 7))
for ax, bins in zip(axs[0], (8, 40)):
    ax.hist(n.nota_final, bins=bins, color=estilo.BASE, edgecolor="white"); ax.set_title(f"Histograma · {bins} bins")
sns.violinplot(data=n, x="carrera", y="nota_final", color=estilo.BASE, inner="quartile", ax=axs[1, 0], linewidth=1)
axs[1, 0].set_title("Violín por carrera")
for c, g in n.groupby("carrera"):
    xs = np.sort(g.nota_final); axs[1, 1].step(xs, np.arange(1, len(xs) + 1) / len(xs), label=c)
axs[1, 1].legend(); axs[1, 1].set_title("ECDF por carrera")
fig.tight_layout(); estilo.guardar(fig, "lab02_distribuciones.png")

# %% [markdown]
# ## 2. Cantidades — ranking con barras ordenadas (y por qué no la torta)

# %%
t = (v.groupby("sucursal").ventas_gs_miles.sum() / 1e6).sort_values()
fig, ax = plt.subplots(figsize=(8, 3.8))
cols = [estilo.GRIS_CLARO] * (len(t) - 1) + [estilo.ENFASIS]
ax.barh(t.index, t.values, color=cols)
for i, val in enumerate(t.values): ax.text(val, i, f" {val:,.1f}", va="center")
ax.set_title("Asunción lidera las ventas 2024-25"); ax.set_xlabel("Ventas (miles de millones de Gs.)")
ax.grid(False); estilo.guardar(fig, "lab02_ranking.png")

# %% [markdown]
# ## 3. Relaciones — dispersión, densidad y el problema del *overplotting*

# %%
fig, axs = plt.subplots(1, 3, figsize=(14, 4), sharex=True, sharey=True)
axs[0].scatter(n.horas_estudio_sem, n.nota_final, color=estilo.BASE); axs[0].set_title("Puntos opacos")
axs[1].scatter(n.horas_estudio_sem, n.nota_final, color=estilo.BASE, alpha=.25, s=18); axs[1].set_title("Transparencia")
axs[2].hexbin(n.horas_estudio_sem, n.nota_final, gridsize=18, cmap="Blues"); axs[2].set_title("Hexbin (densidad)")
for ax in axs: ax.set_xlabel("Horas de estudio / semana")
axs[0].set_ylabel("Nota final"); estilo.guardar(fig, "lab02_relaciones.png")

# %% [markdown]
# ## 4. Matriz de decisión
# | Pregunta | Datos | Gráfico recomendado |
# |---|---|---|
# | ¿Cómo se distribuye X? | 1 numérica | histograma / ECDF / violín |
# | ¿Cuánto por categoría? | cat + num | barras ordenadas / *lollipop* |
# | ¿Qué parte del total? | partes→todo | barras apiladas 100 % (torta solo ≤3 partes) |
# | ¿Se relacionan X e Y? | 2 numéricas | dispersión / hexbin / *regplot* |
# | ¿Cómo cambia en el tiempo? | serie | línea / *small multiples* |
#
# ## 5. Ejercicio
# Para 5 preguntas de negocio sobre `ventas_retail` (p. ej. *¿qué categoría tiene mayor margen?*), elegí el gráfico, justificalo con la
# matriz y construilo. Entregá un notebook con 5 figuras + 1 frase-mensaje por figura.
