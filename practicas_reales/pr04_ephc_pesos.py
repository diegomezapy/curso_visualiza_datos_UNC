# %% [markdown]
# # Práctica 4 · EPHC del INE: por qué el peso muestral cambia la historia
# La **Encuesta Permanente de Hogares Continua (EPHC)** es una **muestra**: cada persona encuestada “representa” a otras. El **factor de expansión (`FACTOR`)** corrige que algunas zonas estén sobre- o sub-muestreadas. Si lo ignorás, tus gráficos **mienten**.
# - **Datos reales**: se descarga el archivo de personas (`REG02`) del INE (≈27 MB). Fuente: https://www.ine.gov.py/microdatos/ · Diccionario: `diccionario_EPHC_ANUAL_2025.xls` (misma carpeta).
# - **Licencia** (Decreto 4064 / Ley 5282/2014): **citá la fuente y la fecha de actualización** y no sugieras patrocinio oficial.
# - Sin conexión se usa una **muestra real de 3.000 filas** incluida en el curso (no equivale al archivo completo).
# %%
import sys, io, json, warnings
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
# ## 1. Descargar y leer
# El archivo real tiene rarezas que veremos enseguida: separador `;`, UTF-8 con BOM, coma decimal y celdas en blanco con espacios.

# %%
ANIO = 2025
USAR = ["AÑO", "DPTO", "AREA", "P02", "P06", "añoest", "e01aimde", "PEAA", "FACTOR", "pobrezai", "quintili"]
NUM = [c for c in USAR]
try:
    raw = A.leer_ephc(ANIO, "REG02", columnas=USAR, numericas=NUM); FUENTE = f"INE · EPHC anual {ANIO} (REG02), descargada hoy"; REAL_COMPLETO = True
except A.SinConexion as e:
    aviso(f"No se pudo descargar del INE ({e}).\nSe usa la MUESTRA REAL de 3.000 filas incluida en el curso: sirve para practicar, pero NO equivale al archivo completo.")
    raw = A.leer_ephc(str(EJ / "ephc_2025_muestra.csv"), columnas=USAR, numericas=NUM); FUENTE = "INE · EPHC 2025 (muestra de 3.000 filas del curso)"; REAL_COMPLETO = False
print(FUENTE, "·", f"{len(raw):,} filas"); raw.head()

# %% [markdown]
# ## 2. Calidad: lo que NO te cuenta el archivo
# - `añoest` (años de estudio) tiene valores como **99**: parecen un código de “no responde”, no años reales. **Confirmalo en el diccionario.**
# - `e01aimde` (ingreso mensual de la ocupación principal) vale 0 para quien no trabaja y tiene **valores extremos**.

# %%
print("Nulos por columna (%):\n", (raw.isna().mean() * 100).round(1).to_string())
print("\nañoest: valores > 30 →", int((raw.añoest > 30).sum()), "filas (código especial)")
print("e01aimde: máximo =", f"{raw.e01aimde.max():,.0f}", "Gs.   |   percentil 99 =", f"{raw.e01aimde.quantile(.99):,.0f}", "Gs.")

# %% [markdown]
# ## 3. Etiquetar y limpiar
# Códigos del diccionario: `AREA` 1 = urbana, 6 = rural · `P06` 1 = hombre, 6 = mujer. Los **departamentos** (`DPTO` 0–15) siguen el orden oficial de códigos geográficos del INE (confirmalo en «Códigos geográficos»).

# %%
DEP = {0: "Asunción", 1: "Concepción", 2: "San Pedro", 3: "Cordillera", 4: "Guairá", 5: "Caaguazú", 6: "Caazapá", 7: "Itapúa", 8: "Misiones", 9: "Paraguarí", 10: "Alto Paraná", 11: "Central", 12: "Ñeembucú", 13: "Amambay", 14: "Canindeyú", 15: "Presidente Hayes"}
df = raw.assign(area=raw.AREA.map({1: "Urbana", 6: "Rural"}), sexo=raw.P06.map({1: "Hombre", 6: "Mujer"}), dpto=raw.DPTO.map(DEP), peso=raw.FACTOR,
                anios_est=raw.añoest.where(raw.añoest <= 30), ingreso=raw.e01aimde.where(raw.e01aimde > 0), ocupado=raw.PEAA == 1)
oc = df[df.ocupado & df.ingreso.notna()]; print(f"{len(oc):,} personas ocupadas con ingreso declarado ({len(oc)/len(df):.0%} de las filas)")

# %% [markdown]
# ## 4. ¿A cuánta gente representa cada persona de la muestra?

# %%
fig, ax = plt.subplots(figsize=(8, 3.5)); ax.hist(df.peso, bins=40, color=AZUL, edgecolor="white"); ax.set_xlabel("Factor de expansión (personas representadas)")
ax.set_title("No todas las personas de la muestra pesan lo mismo", loc="left", fontweight="bold"); estilo.guardar(fig, "pr04_pesos.png")
print(f"Suma de pesos: {df.peso.sum():,.0f} personas representadas" + ("" if REAL_COMPLETO else "  (¡solo de esta muestra! no es la población)"))

# %% [markdown]
# ## 5. Composición urbano/rural: muestra vs población

# %%
muestra = df.area.value_counts(normalize=True); poblacion = A.proporcion_ponderada(df, "area", "peso")
c = pd.DataFrame({"muestra (sin ponderar)": muestra, "población (ponderada)": poblacion}); ax = c.T.plot.barh(stacked=True, figsize=(8, 2.8), color=[AZUL, NARANJA], width=.6)
ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1)); ax.set_title("La muestra sobrerrepresenta a una zona", loc="left", fontweight="bold"); ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(.5, -.2)); estilo.guardar(ax.figure, "pr04_composicion.png"); c.round(3)

# %% [markdown]
# ## 6. Ingreso de la ocupación principal: sin ponderar vs ponderado
# Fijate también en **media vs mediana**: con valores extremos, la media se mueve mucho.

# %%
t = pd.DataFrame({"sin ponderar": [oc.ingreso.mean(), oc.ingreso.median()], "ponderado": [A.media_ponderada(oc.ingreso, oc.peso), A.cuantil_ponderado(oc.ingreso, oc.peso, .5)]}, index=["media", "mediana"]) / 1e6
print("Millones de Gs. por mes\n", t.round(2).to_string()); print(f"\nDiferencia de la media al ponderar: {100*(t.loc['media','ponderado']/t.loc['media','sin ponderar']-1):+.1f} %")

# %% [markdown]
# ## 7. Brecha de género con incertidumbre (bootstrap)
# Una cifra sin **margen de error** sugiere más precisión de la que hay (sesión 3). Remuestreamos para estimar un intervalo.

# %%
rng = np.random.default_rng(1)
def razon(d):
    m, h = d[d.sexo == "Mujer"], d[d.sexo == "Hombre"]; return A.media_ponderada(m.ingreso, m.peso) / A.media_ponderada(h.ingreso, h.peso)
b = np.array([razon(oc.sample(len(oc), replace=True, random_state=int(rng.integers(1e9)))) for _ in range(200)]); lo, hi = np.percentile(b, [2.5, 97.5]); r0 = razon(oc)
fig, ax = plt.subplots(figsize=(7, 2.6)); ax.errorbar([r0], [0], xerr=[[r0 - lo], [hi - r0]], fmt="o", color=NARANJA, capsize=6, ms=9); ax.axvline(1, color="k", ls="--", lw=.8)
ax.set_yticks([]); ax.set_xlim(min(.5, lo - .05), 1.15); ax.set_xlabel("Ingreso medio de mujeres / hombres ocupados (IC 95 %)")
ax.set_title(f"Las mujeres ocupadas ganan {r0:.0%} de lo que ganan los hombres (IC {lo:.0%}–{hi:.0%})", loc="left", fontweight="bold", fontsize=10); estilo.guardar(fig, "pr04_brecha.png")
ax.figure.text(.01, -.05, f"Fuente: {FUENTE}.", fontsize=8, color="#8C8C8C")

# %% [markdown]
# ## 8. Pobreza por departamento: una **tasa ponderada**, no un conteo
# `pobrezai`: 1 = pobre extremo, 2 = pobre no extremo, 3 = no pobre. Mostramos también el **n de la muestra** (con n pequeño, la estimación es frágil).

# %%
d = df.dropna(subset=["pobrezai", "dpto"]); g = d.groupby("dpto").apply(lambda x: pd.Series({"pobreza_%": 100 * x.loc[x.pobrezai.isin([1, 2]), "peso"].sum() / x.peso.sum(), "n": len(x)}), include_groups=False).sort_values("pobreza_%")
fig, ax = plt.subplots(figsize=(8, 5.5)); ax.barh(g.index, g["pobreza_%"], color=[NARANJA if v >= g["pobreza_%"].quantile(.75) else GRIS for v in g["pobreza_%"]])
for y, (v, n) in enumerate(zip(g["pobreza_%"], g.n)): ax.text(v + .4, y, f"{v:.0f} %  (n={int(n)})", va="center", fontsize=8)
ax.set_xlabel("% de personas en situación de pobreza (ponderado)"); ax.set_title("Pobreza por departamento (tasa ponderada)", loc="left", fontweight="bold"); ax.grid(False); estilo.guardar(fig, "pr04_pobreza.png")

# %% [markdown]
# ## Tu turno
# 1. Presentá **dos gráficos lado a lado** (con y sin peso) para otra variable (p. ej. años de estudio) y explicá la diferencia.
# 2. Calculá un indicador por **departamento o área** y mostralo como **tasa o promedio ponderado**, con su **n**. Nunca como conteo de filas de la muestra.
# 3. **Citá**: «Instituto Nacional de Estadística (INE), EPHC anual 2025, descargada el [fecha]» y revisá el diccionario para cada variable que uses.
# 4. Publicá (RPubs o Colab). No publiques filas individuales.
