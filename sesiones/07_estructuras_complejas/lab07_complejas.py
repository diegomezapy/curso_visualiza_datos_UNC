# %% [markdown]
# # Lab 7 · Estructuras complejas: alta dimensionalidad, series temporales y geodatos
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

import plotly.express as px
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# %% [markdown]
# ## A. Alta dimensionalidad (dataset *wine*: 13 variables, 3 clases)
# ### A1. Coordenadas paralelas y matriz de correlación

# %%
w = load_wine(as_frame=True); X, y = w.data, w.target.map(dict(enumerate(w.target_names)))
Z = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)
fig = px.parallel_coordinates(Z.assign(clase=w.target), color="clase", color_continuous_scale=px.colors.qualitative.Safe[:3] and "Viridis",
                              template=estilo.PLOTLY_TEMPLATE, title="Coordenadas paralelas (variables estandarizadas)")
fig.write_html(estilo.salida("lab07_paralelas.html"))
fig, ax = plt.subplots(figsize=(7, 6)); im = ax.imshow(X.corr(), cmap="RdBu", vmin=-1, vmax=1)
ax.set_xticks(range(13)); ax.set_xticklabels(X.columns, rotation=90, fontsize=8); ax.set_yticks(range(13)); ax.set_yticklabels(X.columns, fontsize=8)
ax.grid(False); fig.colorbar(im, shrink=.8); ax.set_title("Correlaciones (paleta divergente centrada en 0)")
estilo.guardar(fig, "lab07_correlacion.png")

# %% [markdown]
# ### A2. Reducción de dimensión: PCA vs t-SNE
# PCA es lineal y **las distancias globales tienen sentido**; t-SNE preserva vecindades locales pero
# **tamaños de clúster y distancias entre clústeres no son interpretables**. Ver sesgo de lectura.

# %%
p = PCA(n_components=2).fit(Z); P = p.transform(Z)
T = TSNE(n_components=2, perplexity=30, random_state=0, init="pca").fit_transform(Z)
fig, axs = plt.subplots(1, 2, figsize=(11, 4.3))
for ax, E, t in [(axs[0], P, f"PCA ({p.explained_variance_ratio_.sum():.0%} de la varianza)"), (axs[1], T, "t-SNE")]:
    for i, (c, col) in enumerate(zip(w.target_names, estilo.OKABE_ITO)):
        ax.scatter(*E[w.target == i].T, color=col, label=c, s=22)
    ax.set_title(t)
axs[0].legend(); estilo.guardar(fig, "lab07_pca_tsne.png")

# %% [markdown]
# ## B. Series temporales (`demanda_energia`)
# ### B1. Descomposición visual: tendencia, estacionalidad semanal y anual, anomalías

# %%
s = datos.serie_diaria().set_index("fecha").demanda_mwh
tend = s.rolling(365, center=True).mean()
resid = s - s.rolling(28, center=True).mean()
z = (resid - resid.mean()) / resid.std(); anom = s[z.abs() > 4]
fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
axs[0].plot(s, color=estilo.GRIS_CLARO, lw=.8); axs[0].plot(tend, color=estilo.ENFASIS, lw=2, label="Tendencia (media móvil 365 d)")
axs[0].scatter(anom.index, anom, color="k", s=25, zorder=3, label="Anomalías (|z|>4)"); axs[0].legend(); axs[0].set_title("Demanda diaria de energía (MWh)")
axs[1].plot(resid, color=estilo.BASE, lw=.8); axs[1].set_title("Residuo vs media móvil 28 d")
estilo.guardar(fig, "lab07_serie.png")

# %% [markdown]
# ### B2. Heatmap calendario: año × día de la semana / mes

# %%
h = s.to_frame("x"); h["mes"], h["anio"] = h.index.month, h.index.year
pv = h.pivot_table(index="anio", columns="mes", values="x", aggfunc="mean")
fig, ax = plt.subplots(figsize=(9, 2.8)); im = ax.imshow(pv, cmap="YlOrRd", aspect="auto")
ax.set_xticks(range(12)); ax.set_xticklabels(range(1, 13)); ax.set_yticks(range(len(pv))); ax.set_yticklabels(pv.index); ax.grid(False)
fig.colorbar(im, label="MWh"); ax.set_title("Estacionalidad anual: pico en verano austral (dic-feb)")
estilo.guardar(fig, "lab07_heatmap.png")

# %% [markdown]
# ## C. Geodatos
# ### C1. Mapa de burbujas + choropleth: cuándo usar cada uno
# Sin shapefiles pesados: mostramos centroides departamentales (coordenadas **aproximadas**, indicadores **sintéticos**).
# Para choropleth reales: GeoJSON de departamentos (DGEEC/INE, `geoBoundaries`) + `px.choropleth_map` o `geopandas`.

# %%
d = datos.departamentos()
fig = px.scatter_geo(d, lat="lat", lon="lon", size="poblacion_miles", color="indice_acceso_internet", hover_name="departamento",
                     color_continuous_scale="Viridis", scope="south america", template=estilo.PLOTLY_TEMPLATE, size_max=40,
                     title="Acceso a internet por departamento (datos sintéticos)")
fig.update_geos(lataxis_range=[-28, -19], lonaxis_range=[-63, -53], showcountries=True, countrycolor="#999")
fig.write_html(estilo.salida("lab07_mapa.html"))

# %% [markdown]
# ### C2. Trampa clásica: el mapa coroplético de **totales** vs **tasas**
# Regla: *nunca* colorear por conteos absolutos entre áreas de población desigual → usar tasas o densidades; y avisar del problema del área modificable (MAUP).
#
# ## Ejercicio (mini-proyecto 3)
# Elegí un dataset real (p. ej. *datos.gov.py*, *BCP*, *DGEEC*, *Our World in Data*) con dimensión temporal **o** geográfica y construí 3 vistas complementarias con un titular analítico.
