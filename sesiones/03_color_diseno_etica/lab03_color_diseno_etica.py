# %% [markdown]
# # Lab 3 · Color, tipografía, anotación y ética visual
# Parte A: buenas prácticas de diseño. Parte B: galería de **gráficos engañosos** y su corrección.
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

v = datos.ventas()

# %% [markdown]
# ## A1. Tres tipos de paleta: cualitativa, secuencial, divergente

# %%
fig, axs = plt.subplots(3, 1, figsize=(8, 3))
g = np.linspace(0, 1, 256)[None, :]
for ax, (nombre, cm) in zip(axs, [("Cualitativa (Okabe-Ito)", None), ("Secuencial (viridis)", "viridis"), ("Divergente (RdBu)", "RdBu")]):
    if cm: ax.imshow(g, aspect="auto", cmap=cm)
    else:
        for i, c in enumerate(estilo.OKABE_ITO): ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=c))
        ax.set_xlim(0, 8); ax.set_ylim(0, 1)
    ax.set_title(nombre, fontsize=10); ax.axis("off")
estilo.guardar(fig, "lab03_paletas.png")

# %% [markdown]
# ## A2. Anotar > leyendas. Etiquetado directo y título que dice el mensaje

# %%
m = v.assign(mes=v.fecha.dt.to_period("M").dt.to_timestamp()).groupby(["mes", "categoria"]).ventas_gs_miles.sum().unstack() / 1e3
fig, ax = plt.subplots(figsize=(9, 4.5))
for c in m.columns:
    resaltar = c == "Electrónica"
    ax.plot(m.index, m[c], color=estilo.ENFASIS if resaltar else estilo.GRIS_CLARO, lw=2.5 if resaltar else 1.5)
    ax.text(m.index[-1], m[c].iloc[-1], f"  {c}", color=estilo.ENFASIS if resaltar else estilo.GRIS, va="center", fontsize=10)
pico = m["Electrónica"].idxmax()
ax.annotate("Pico navideño", (pico, m.loc[pico, "Electrónica"]), xytext=(-110, -10), textcoords="offset points",
            arrowprops=dict(arrowstyle="->", color=estilo.GRIS))
ax.set_title("Electrónica concentra las ventas y se dispara en diciembre"); ax.set_ylabel("Ventas (millones de Gs.)")
ax.set_xlim(right=m.index[-1] + pd.Timedelta(days=130)); estilo.guardar(fig, "lab03_anotacion.png")

# %% [markdown]
# ## B. Galería de engaños y su corrección
# ### B1. Eje truncado en barras

# %%
vals = pd.Series({"A": 96.5, "B": 97.2, "C": 98.1})
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
axs[0].bar(vals.index, vals, color=estilo.BASE); axs[0].set_ylim(96, 98.5); axs[0].set_title("❌ Eje truncado: 'C triplica a A'")
axs[1].bar(vals.index, vals, color=estilo.BASE); axs[1].set_ylim(0, 100); axs[1].set_title("✅ Eje en cero: diferencias modestas")
estilo.guardar(fig, "lab03_eje_truncado.png")

# %% [markdown]
# ### B2. Doble eje que fabrica correlación

# %%
rng = np.random.default_rng(3); x = np.arange(12)
s1 = 100 + rng.normal(0, 3, 12).cumsum(); s2 = 50 + rng.normal(0, 3, 12).cumsum()
fig, axs = plt.subplots(1, 2, figsize=(11, 3.8))
axs[0].plot(x, s1, color=estilo.BASE); ax2 = axs[0].twinx(); ax2.plot(x, s2, color=estilo.ENFASIS)
axs[0].set_title("❌ Doble eje: la escala la elige el autor")
for s, c, l in [(s1, estilo.BASE, "Serie 1"), (s2, estilo.ENFASIS, "Serie 2")]:
    axs[1].plot(x, (s / s[0]) * 100, color=c, label=l)
axs[1].set_title("✅ Índice base 100 en un solo eje"); axs[1].legend()
estilo.guardar(fig, "lab03_doble_eje.png")

# %% [markdown]
# ### B3. Elección arbitraria del recorte temporal (cherry-picking)

# %%
d = datos.serie_diaria().set_index("fecha").demanda_mwh
fig, axs = plt.subplots(1, 2, figsize=(11, 3.6))
d["2023-07":"2023-09"].plot(ax=axs[0], color=estilo.ENFASIS); axs[0].set_title("❌ Recorte conveniente (3 meses)")
d.resample("ME").mean().plot(ax=axs[1], color=estilo.BASE); axs[1].set_title("✅ Serie completa (media mensual)")
estilo.guardar(fig, "lab03_recorte.png")

# %% [markdown]
# ## Checklist ético (usar en todo entregable)
# 1. ¿El eje de barras empieza en 0? 2. ¿Las escalas son comparables entre paneles?
# 3. ¿Se muestra la incertidumbre / el n? 4. ¿Hay fuente, fecha y definición de la métrica?
# 5. ¿El color distingue a personas con daltonismo? 6. ¿El título afirma algo que los datos sí sostienen?
#
# ## Ejercicio
# Se entrega un gráfico "malo" (`datos/` + enunciado del docente). Identificá ≥3 problemas con el checklist, corregilo y escribí 150 palabras sobre el daño potencial de la versión original.
