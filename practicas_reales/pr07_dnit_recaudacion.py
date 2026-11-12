# %% [markdown]
# # Práctica 7 · ¿Quién paga y dónde? Recaudación tributaria en Paraguay (DNIT)
# Datos **reales y “sucios”**: 652.021 filas en el archivo de 2025 (mes × actividad económica × departamento × distrito × impuesto). Aprenderás a **limpiar**, a **resumir** con criterio y a dibujar **series, Pareto y concentración**.
# - Fuente: https://www.dnit.gov.py/web/portal-institucional/estadisticas (Excel «Recaudación por impuesto, departamento, distrito y actividad económica»).
# - El enlace del archivo cambia: la práctica lo **busca en la página**. Descargar el Excel (≈35 MB) y leerlo toma 1–3 minutos.
# - Sin conexión se usa una **muestra real de 6.000 filas** (solo para practicar: los totales NO son los reales).
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

# %%
ANIO = 2025
try:
    url = A.buscar_url_dnit_recaudacion(ANIO); print("Archivo:", url[:110], "…")
    try: import python_calamine
    except ImportError: import subprocess; subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-calamine"], check=False)
    contenido = io.BytesIO(A.descargar(url, timeout=300))
    try: crudo = pd.read_excel(contenido, engine="calamine")      # rápido
    except Exception: contenido.seek(0); crudo = pd.read_excel(contenido)  # más lento pero universal
    FUENTE = f"DNIT · Recaudación {ANIO} (descargada hoy)"; COMPLETO = True
except Exception as e:
    aviso(f"No se pudo descargar de la DNIT ({e}).\nSe usa una MUESTRA REAL de 6.000 filas: las PROPORCIONES son orientativas, los TOTALES NO son los reales.")
    crudo = pd.read_csv(EJ / "dnit_recaudacion_2025_muestra.csv"); FUENTE = "DNIT · Recaudación 2025 (muestra de 6.000 filas del curso)"; COMPLETO = False
print(FUENTE, "·", f"{len(crudo):,} filas"); crudo.tail(3)

# %% [markdown]
# ## 2. Limpiar: mirá el final de la tabla
# Al pie del Excel hay **notas explicativas escritas en la columna `Mes`** y el año viene como texto. Si no las sacás, ensucian cualquier agregación.

# %%
n0 = len(crudo); df = A.limpiar_recaudacion(crudo)
print(f"Filas descartadas (notas al pie y vacías): {n0 - len(df)} · filas válidas: {len(df):,}")
print("\nValores nulos (%):\n", (df.isna().mean() * 100).round(1)[lambda s: s > 0].to_string())
df.head(3)

# %% [markdown]
# ## 3. KPIs con definición
# Recaudación en **guaraníes**. Mostramos miles de millones de Gs. (para el archivo completo, la unidad cómoda es **billones**).

# %%
T = df.Recaudacion.sum(); ad = df[df["Tipo Impuesto"] == "ADUANEROS"].Recaudacion.sum()
pd.Series({"Recaudación (miles de millones de Gs.)": T / 1e9, "% por tributos aduaneros": ad / T, "N.º de actividades económicas": df["Des Act Economica Princ"].nunique(), "N.º de distritos": df.Distrito.nunique(), "% sin departamento": df.Departamento.isna().mean()}).round(3)

# %% [markdown]
# ## 4. Serie mensual: internos vs aduaneros

# %%
m = df.pivot_table(index="fecha", columns="Tipo Impuesto", values="Recaudacion", aggfunc="sum").fillna(0) / 1e9
fig, ax = plt.subplots(figsize=(9, 4)); ax.bar(m.index.strftime("%b"), m.get("INTERNOS", 0), color=AZUL, label="Internos"); ax.bar(m.index.strftime("%b"), m.get("ADUANEROS", 0), bottom=m.get("INTERNOS", 0), color=NARANJA, label="Aduaneros")
ax.set_ylabel("Miles de millones de Gs."); ax.legend(frameon=False); ax.set_title("Recaudación mensual por tipo de tributo", loc="left", fontweight="bold"); ax.grid(axis="x", visible=False); estilo.guardar(fig, "pr07_mensual.png")

# %% [markdown]
# ## 5. ¿Qué impuestos aportan más?

# %%
i = (df.groupby("Impuesto Asignado").Recaudacion.sum().sort_values() / T)
fig, ax = plt.subplots(figsize=(8, 4)); ax.barh(i.index, i.values, color=[NARANJA if k == i.index[-1] else GRIS for k in i.index]); ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1)); ax.grid(False)
for y, v in enumerate(i.values): ax.text(v + .005, y, f"{v:.1%}", va="center", fontsize=8)
ax.set_title(f"{i.index[-1]} es el principal aporte", loc="left", fontweight="bold"); estilo.guardar(fig, "pr07_impuestos.png")

# %% [markdown]
# ## 6. Pareto: pocas actividades concentran mucho

# %%
a = df.groupby("Des Act Economica Princ").Recaudacion.sum().sort_values(ascending=False); acum = a.cumsum() / a.sum(); n15 = a.head(15)
fig, ax = plt.subplots(figsize=(9, 5)); import textwrap
ax.barh([textwrap.shorten(s, 52, placeholder="…") for s in n15.index][::-1], (n15 / 1e9).values[::-1], color=AZUL); ax.set_xlabel("Miles de millones de Gs."); ax.grid(False)
ax.set_title(f"Las 15 actividades principales concentran el {acum.iloc[14]:.0%} de la recaudación (de {len(a)})", loc="left", fontweight="bold", fontsize=10); estilo.guardar(fig, "pr07_pareto.png")

# %% [markdown]
# ## 7. Departamentos: ¡cuidado con qué mide!
# El departamento es el del **domicilio fiscal** del contribuyente, no el lugar donde se genera la actividad. Una empresa con sede en Asunción aparece en **CAPITAL** aunque produzca en el interior. Por eso es **un conteo/monto absoluto**, no una “tasa de actividad” (sesión 7: tasas, no conteos).

# %%
d = df.groupby("Departamento").Recaudacion.sum().sort_values() / T
fig, ax = plt.subplots(figsize=(8, 5)); ax.barh(d.index, d.values, color=[NARANJA if v == d.max() else GRIS for v in d.values]); ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1)); ax.grid(False)
ax.set_title("Participación en la recaudación por departamento (domicilio fiscal)", loc="left", fontweight="bold", fontsize=10); estilo.guardar(fig, "pr07_departamentos.png")

# %% [markdown]
# ## 8. Concentración por distrito: curva de Lorenz y Gini

# %%
v = np.sort(df.groupby(["Departamento", "Distrito"]).Recaudacion.sum().values); L = np.insert(np.cumsum(v) / v.sum(), 0, 0); x = np.linspace(0, 1, len(L)); gini = 1 - 2 * np.trapezoid(L, x)
fig, ax = plt.subplots(figsize=(5.2, 5.2)); ax.plot(x, L, color=NARANJA, lw=2.5); ax.plot([0, 1], [0, 1], color="k", ls="--", lw=.8); ax.fill_between(x, L, x, color=NARANJA, alpha=.12)
ax.set_xlabel("Proporción acumulada de distritos (de menor a mayor)"); ax.set_ylabel("Proporción acumulada de la recaudación"); ax.set_title(f"Concentración por distrito (Gini = {gini:.2f})", loc="left", fontweight="bold"); estilo.guardar(fig, "pr07_lorenz.png")

# %% [markdown]
# ## 9. Mapa de calor: mes × impuesto

# %%
h = df.pivot_table(index="Impuesto Asignado", columns="mes_n", values="Recaudacion", aggfunc="sum").fillna(0) / 1e9
fig, ax = plt.subplots(figsize=(9, 4)); im = ax.imshow(h.values, aspect="auto", cmap="YlOrRd"); ax.set_yticks(range(len(h))); ax.set_yticklabels(h.index); ax.set_xticks(range(len(h.columns))); ax.set_xticklabels(h.columns); ax.grid(False)
fig.colorbar(im, label="Miles de millones de Gs."); ax.set_xlabel("Mes"); ax.set_title("Estacionalidad de cada impuesto", loc="left", fontweight="bold"); estilo.guardar(fig, "pr07_heatmap.png")

# %% [markdown]
# ## Tu turno
# 1. Descargá **otro año** (`ANIO = 2023`) y comparalo: ¿cambió la mezcla entre tributos internos y aduaneros? ¿hay un mes atípico?
# 2. Elegí **una actividad económica** (por ejemplo, agricultura o comercio) y mostrá su serie mensual y en qué departamentos se declara.
# 3. Escribí **qué NO se puede concluir** de estos datos (¿dónde ocurre la actividad? ¿quién paga realmente?).
# 4. Citá: «Dirección Nacional de Ingresos Tributarios (DNIT), Recaudación [año], descargada el [fecha]». Publicá en RPubs o Colab.
