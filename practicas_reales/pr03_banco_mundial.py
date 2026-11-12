# %% [markdown]
# # Práctica 3 · Paraguay en la región: comercio exterior y economía (API del Banco Mundial)
# La API es **pública y no requiere clave**. Aprenderás a consumir una API, ordenar los datos y construir **gráficos honestos** (sesiones 2–3).
# Es también la **alternativa estable** para comercio exterior mientras se aclara el estado del portal de Aduanas.
# > Doc. oficial: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581
# %%
import sys, json, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, abiertos as A
estilo.aplicar_tema()
EJ = RAIZ / "datos" / "ejemplos_abiertos"
AZUL, NARANJA, VERDE, GRIS = "#0072B2", "#D55E00", "#009E73", "#D9D9D9"
def aviso(msg):
    print("\n" + "!" * 70 + f"\n{msg}\n" + "!" * 70)

# %% [markdown]
# ## 1. Descargar indicadores
# Códigos WDI: `NE.EXP.GNFS.ZS` exportaciones (% del PIB) · `NE.IMP.GNFS.ZS` importaciones (% del PIB) · `NY.GDP.PCAP.CD` PIB per cápita (US$ corrientes) · `NY.GDP.MKTP.KD.ZG` crecimiento del PIB (%).

# %%
PAISES = ("PRY", "ARG", "BRA", "URY", "BOL"); DESDE, HASTA = 2000, 2024
IND = {"NE.EXP.GNFS.ZS": "Exportaciones (% del PIB)", "NE.IMP.GNFS.ZS": "Importaciones (% del PIB)", "NY.GDP.PCAP.CD": "PIB per cápita (US$)", "NY.GDP.MKTP.KD.ZG": "Crecimiento del PIB (%)"}
SINTETICO = False
try:
    datos = {c: A.banco_mundial(c, PAISES, DESDE, HASTA) for c in IND}
except A.SinConexion as e:
    aviso(f"SIN ACCESO A LA API ({e}).\nSE USAN DATOS SINTÉTICOS: SOLO PARA PROBAR EL CÓDIGO, NO SON CIFRAS REALES."); SINTETICO = True
    rng = np.random.default_rng(3); anios = range(DESDE, HASTA + 1); nom = {"PRY": "Paraguay", "ARG": "Argentina", "BRA": "Brasil", "URY": "Uruguay", "BOL": "Bolivia"}
    datos = {c: pd.DataFrame([{"pais": nom[p], "iso3": p, "anio": a, "valor": 30 + 8 * np.sin((a - 2000) / 4 + i) + rng.normal(0, 2), "indicador": IND[c], "codigo": c} for i, p in enumerate(PAISES) for a in anios]) for c in IND}
df = pd.concat(datos.values(), ignore_index=True); print(df.shape, "· sintético =", SINTETICO); df.head()

# %% [markdown]
# ## 2. Calidad: ¿hay datos faltantes? (el último año suele venir vacío)

# %%
ult = df.dropna(subset=["valor"]).groupby("codigo").anio.max(); print("Último año con dato por indicador:\n", ult.to_string())
df.groupby(["codigo"]).valor.apply(lambda s: round(s.isna().mean() * 100, 1)).rename("% de NA")

# %% [markdown]
# ## 3. Serie comparada con énfasis (Paraguay resaltado, resto en gris)

# %%
def serie(cod, ax=None, titulo=None):
    d = df[df.codigo == cod].dropna(subset=["valor"]); ax = ax or plt.subplots(figsize=(8, 4))[1]
    for p, g in d.groupby("iso3"):
        pry = p == "PRY"; ax.plot(g.anio, g.valor, color=NARANJA if pry else GRIS, lw=3 if pry else 1.3, zorder=3 if pry else 1)
        ax.text(g.anio.iloc[-1] + .3, g.valor.iloc[-1], g.pais.iloc[0], color=NARANJA if pry else "#8C8C8C", va="center", fontsize=9, fontweight="bold" if pry else "normal")
    ax.set_xlim(right=d.anio.max() + 4); ax.set_title(titulo or IND[cod], loc="left", fontweight="bold"); return ax
ax = serie("NE.EXP.GNFS.ZS", titulo="Exportaciones de bienes y servicios (% del PIB)"); ax.figure.text(.01, -.02, "Fuente: Banco Mundial (WDI). " + ("DATOS SINTÉTICOS" if SINTETICO else ""), fontsize=8, color="#8C8C8C"); estilo.guardar(ax.figure, "pr03_exportaciones.png")

# %% [markdown]
# ## 4. Small multiples: los cuatro indicadores

# %%
fig, axs = plt.subplots(2, 2, figsize=(11, 7)); [serie(c, a) for c, a in zip(IND, axs.ravel())]; fig.tight_layout(); estilo.guardar(fig, "pr03_multiples.png")

# %% [markdown]
# ## 5. Balanza comercial (exportaciones − importaciones, % del PIB)

# %%
b = df[df.codigo.isin(["NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"])].pivot_table(index=["iso3", "anio"], columns="codigo", values="valor").dropna(); b["saldo"] = b["NE.EXP.GNFS.ZS"] - b["NE.IMP.GNFS.ZS"]
s = b.xs("PRY", level="iso3").saldo; fig, ax = plt.subplots(figsize=(9, 3.6)); ax.bar(s.index, s.values, color=[VERDE if v >= 0 else NARANJA for v in s.values]); ax.axhline(0, color="k", lw=.8)
ax.set_title("Paraguay: saldo comercial de bienes y servicios (% del PIB)", loc="left", fontweight="bold"); estilo.guardar(fig, "pr03_saldo.png")

# %% [markdown]
# ## 6. Gráfico engañoso vs honesto (sesión 3)
# El **doble eje** permite “probar” cualquier relación. Compará.

# %%
x = df[(df.iso3 == "PRY") & df.codigo.isin(["NE.EXP.GNFS.ZS", "NY.GDP.PCAP.CD"])].pivot_table(index="anio", columns="codigo", values="valor").dropna()
fig, axs = plt.subplots(1, 2, figsize=(11, 3.8)); a1 = axs[0]; a1.plot(x.index, x["NE.EXP.GNFS.ZS"], color=AZUL); a2 = a1.twinx(); a2.plot(x.index, x["NY.GDP.PCAP.CD"], color=NARANJA); a1.set_title("❌ Doble eje: la escala la elige el autor", loc="left", fontweight="bold")
for c, col, l in [("NE.EXP.GNFS.ZS", AZUL, "Exportaciones % PIB"), ("NY.GDP.PCAP.CD", NARANJA, "PIB per cápita")]: axs[1].plot(x.index, x[c] / x[c].iloc[0] * 100, color=col, label=l)
axs[1].set_title("✅ Índice base 100 en un solo eje", loc="left", fontweight="bold"); axs[1].legend(frameon=False); estilo.guardar(fig, "pr03_doble_eje.png")

# %% [markdown]
# ## Tu turno
# 1. Elegí **otro indicador** (buscá códigos en https://api.worldbank.org/v2/indicator?format=json) y un grupo de países.
# 2. Respondé una pregunta con un gráfico y un **título-mensaje**; citá la fuente, el año del último dato y el indicador.
# 3. Si hubo NA, **explicá cómo los trataste**. Publicá (R: `r/pr03_banco_mundial.Rmd` → RPubs).
