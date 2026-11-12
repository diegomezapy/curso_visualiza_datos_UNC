# %% [markdown]
# # Práctica 4 · Datos de encuesta: por qué el peso muestral cambia la historia
# Las encuestas de hogares (como la **EPHC del INE**) son **muestras**: cada persona “representa” a otras. El **factor de expansión** corrige que algunas zonas estén sobre- o sub-muestreadas. Si lo ignorás, tus gráficos pueden **mentir**.
# > Esta práctica usa por defecto una encuesta **sintética** (con sobremuestreo rural) para ver el efecto; luego la aplicás a los **microdatos reales** (ver `datos_reales/catalogo.py`).
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
# ## 1. Cargar y mapear columnas
# Con datos reales, abrí el **diccionario de variables** y completá `COL` con los nombres exactos.

# %%
ORIGEN = ""   # URL o ruta de los microdatos reales (CSV)
COL = dict(peso="fex", ingreso="ingreso_laboral_gs", area="area", sexo="sexo", edad="edad", escolaridad="anios_estudio")
if ORIGEN:
    try: df = A.leer_tabla(ORIGEN)
    except Exception as e: aviso(f"No se pudo leer ({e}). Se usa la encuesta SINTÉTICA."); df = pd.read_csv(EJ / "ephc_demo.csv")
else:
    aviso("Usando encuesta SINTÉTICA de demostración (no son datos reales)."); df = pd.read_csv(EJ / "ephc_demo.csv")
faltan = [v for v in COL.values() if v not in df.columns]; assert not faltan, f"Columnas inexistentes: {faltan}. Revisá el diccionario y ajustá COL."
df = df.rename(columns={v: k for k, v in COL.items()}).dropna(subset=["peso"]); print(len(df), "filas; suma de pesos =", f"{df.peso.sum():,.0f}", "(población representada)")

# %% [markdown]
# ## 2. ¿A cuánta gente representa cada persona de la muestra?

# %%
fig, ax = plt.subplots(figsize=(8, 3.5)); ax.hist(df.peso, bins=40, color=AZUL, edgecolor="white"); ax.set_xlabel("Factor de expansión"); ax.set_title("No todas las personas de la muestra pesan lo mismo", loc="left", fontweight="bold"); estilo.guardar(fig, "pr04_pesos.png")

# %% [markdown]
# ## 3. Composición urbano/rural: muestra vs población

# %%
muestra = df.area.value_counts(normalize=True); poblacion = A.proporcion_ponderada(df, "area", "peso")
c = pd.DataFrame({"muestra (sin ponderar)": muestra, "población (ponderada)": poblacion}); ax = c.T.plot.barh(stacked=True, figsize=(8, 2.8), color=[AZUL, NARANJA], width=.6)
ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1)); ax.set_title("La muestra sobrerrepresenta a una zona", loc="left", fontweight="bold"); ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(.5, -.2)); estilo.guardar(ax.figure, "pr04_composicion.png"); c.round(3)

# %% [markdown]
# ## 4. Ingreso laboral: sin ponderar vs ponderado

# %%
sin = df.ingreso.mean(); con = A.media_ponderada(df.ingreso, df.peso); msin = df.ingreso.median(); mcon = A.cuantil_ponderado(df.ingreso, df.peso, .5)
t = pd.DataFrame({"sin ponderar": [sin, msin], "ponderado": [con, mcon]}, index=["media", "mediana"]) / 1e6; print("Millones de Gs.\n", t.round(2).to_string()); print(f"\nDiferencia de la media: {100*(con/sin-1):+.1f} %")

# %% [markdown]
# ## 5. Brecha de género con incertidumbre (bootstrap ponderado)
# Una cifra sin **margen de error** sugiere más precisión de la que hay (sesión 3).

# %%
rng = np.random.default_rng(1)
def razon(d): m = d[d.sexo == "Mujer"]; h = d[d.sexo == "Hombre"]; return A.media_ponderada(m.ingreso, m.peso) / A.media_ponderada(h.ingreso, h.peso)
b = np.array([razon(df.sample(len(df), replace=True, random_state=int(rng.integers(1e9)))) for _ in range(300)]); lo, hi = np.percentile(b, [2.5, 97.5])
fig, ax = plt.subplots(figsize=(7, 2.6)); ax.errorbar([razon(df)], [0], xerr=[[razon(df) - lo], [hi - razon(df)]], fmt="o", color=NARANJA, capsize=6, ms=9); ax.axvline(1, color="k", ls="--", lw=.8)
ax.set_yticks([]); ax.set_xlim(.6, 1.2); ax.set_xlabel("Ingreso medio de mujeres / hombres (IC 95 %)"); ax.set_title(f"Las mujeres ganan {razon(df):.0%} del ingreso de los hombres (IC {lo:.0%}–{hi:.0%})", loc="left", fontweight="bold", fontsize=10); estilo.guardar(fig, "pr04_brecha.png")

# %% [markdown]
# ## Tu turno
# 1. Con **datos reales**, ¿qué cambia al ponderar? Presentá **dos gráficos lado a lado** (con y sin peso) y explicá la diferencia.
# 2. Calculá un indicador por **departamento** y mostralo como **tasa o promedio ponderado**, nunca como conteo de filas de la muestra.
# 3. Citá la encuesta, el año/trimestre y el diccionario que usaste. Publicá (R/RPubs o Colab).
