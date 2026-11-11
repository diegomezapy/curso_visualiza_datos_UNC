# %% [markdown]
# # Lab 1 · Percepción y por qué visualizar
# **Objetivos:** (1) ver por qué las estadísticas resumen engañan; (2) comparar la precisión de
# codificaciones visuales (posición > longitud > ángulo/área); (3) aplicar "preatentivos" para guiar la mirada.
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

# %% [markdown]
# ## 1. El cuarteto de Anscombe
# Cuatro datasets con **misma media, varianza, correlación y recta de regresión**.

# %%
a = datos.anscombe()
print(a.groupby("dataset").agg(x_med=("x", "mean"), y_med=("y", "mean"), y_var=("y", "var"),
      r=("x", lambda s: np.corrcoef(s, a.loc[s.index, "y"])[0, 1])).round(2))

# %%
fig, axs = plt.subplots(1, 4, figsize=(14, 3.4), sharex=True, sharey=True)
for ax, (nombre, g) in zip(axs, a.groupby("dataset")):
    ax.scatter(g.x, g.y, color=estilo.BASE, s=30)
    m, b = np.polyfit(g.x, g.y, 1)
    xs = np.array([3, 20]); ax.plot(xs, m * xs + b, color=estilo.ENFASIS, lw=1.5)
    ax.set_title(f"Dataset {nombre}", fontsize=11)
fig.suptitle("Mismos números, historias distintas", x=0.01, ha="left", fontweight="bold")
estilo.guardar(fig, "lab01_anscombe.png")

# %% [markdown]
# ## 2. Jerarquía de la percepción (Cleveland & McGill)
# Mismos 5 valores codificados con **posición**, **longitud** y **ángulo**. ¿Con cuál se comparan mejor los valores cercanos?

# %%
cat = list("ABCDE"); val = np.array([23, 25, 21, 24, 26])
fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
axs[0].plot(val, cat, "o", color=estilo.BASE); axs[0].set_title("Posición (puntos)")
axs[1].barh(cat, val, color=estilo.BASE); axs[1].set_title("Longitud (barras)")
axs[2].pie(val, labels=cat, colors=estilo.OKABE_ITO[:5]); axs[2].set_title("Ángulo (torta)")
axs[0].invert_yaxis(); axs[1].invert_yaxis()
estilo.guardar(fig, "lab01_jerarquia.png")

# %% [markdown]
# **Pregunta:** ¿cuál es la categoría mayor? ¿y la segunda? Cronometrá cuánto tardás con cada panel.

# %% [markdown]
# ## 3. Atributos preatentivos: el color como foco
# Contá cuántos puntos "outlier" hay. Primero sin guía; luego con color de énfasis.

# %%
rng = np.random.default_rng(1)
x, y = rng.normal(size=(2, 300)); fuera = rng.choice(300, 8, replace=False)
fig, axs = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
axs[0].scatter(x, y, color=estilo.BASE, s=18); axs[0].set_title("Sin énfasis")
c = np.full(300, estilo.GRIS_CLARO, dtype=object); c[fuera] = estilo.ENFASIS
axs[1].scatter(x, y, color=c, s=18); axs[1].set_title("Con color de énfasis")
estilo.guardar(fig, "lab01_preatentivo.png")

# %% [markdown]
# ## 4. Ejercicio (entregable de la sesión)
# Elegí **un gráfico de un medio de prensa** (periódico, informe institucional) y:
# 1. identificá variable, codificación visual y mensaje;
# 2. evaluá con la jerarquía de Cleveland-McGill;
# 3. rehacelo con `matplotlib` aplicando *data-ink ratio* (Tufte). Entregá antes/después + 5 líneas de justificación.
