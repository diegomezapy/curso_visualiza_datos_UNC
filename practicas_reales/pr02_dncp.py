# %% [markdown]
# # Práctica 2 · Contrataciones públicas (DNCP, estándar OCDS)
# **Pregunta guía:** ¿quién compra qué, a quién y cuánto? Aprenderás a pasar de un JSON anidado (OCDS) a una **tabla ordenada**, calcular **KPIs**, ver **series** y dibujar la **red comprador–proveedor**.
# > Fuente: https://www.contrataciones.gov.py/datos · API: https://contrataciones.gov.py/datos/api/v3/doc/
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

import networkx as nx

# %% [markdown]
# ## 1. Cargar los datos
# Opción A (recomendada): bajá un archivo **JSON OCDS** (descarga masiva) y pegá su URL o ruta.
# Opción B: un endpoint de la API (consultá su documentación). Si lo dejás vacío: **datos sintéticos** con la misma estructura.

# %%
ORIGEN_JSON = ""
def cargar():
    if ORIGEN_JSON:
        try:
            datos = A.descargar(ORIGEN_JSON) if ORIGEN_JSON.startswith("http") else open(ORIGEN_JSON, "rb").read()
            return json.loads(datos.decode("utf-8")), True
        except Exception as e: aviso(f"No se pudo leer ORIGEN_JSON ({e}).")
    aviso("USANDO DATOS SINTÉTICOS (entidades y proveedores ficticios, estructura OCDS).")
    return json.load(open(EJ / "ocds_ejemplo.json", encoding="utf-8")), False
bruto, REAL = cargar()
procesos = A.ocds_a_tabla(bruto); adj = A.ocds_adjudicaciones(bruto)
print(f"{len(procesos):,} procesos · {len(adj):,} adjudicaciones · real={REAL}"); procesos.head()

# %% [markdown]
# ## 2. Limpiar antes de sumar
# Montos en guaraníes; hay procesos cancelados o sin adjudicar. **Definí qué contás** y escribilo.

# %%
print(procesos.estado.value_counts(dropna=False).to_string())
vigentes = procesos[~procesos.estado.isin(["cancelled", "unsuccessful"])]
print(f"\nProcesos no cancelados/desiertos: {len(vigentes):,} de {len(procesos):,}")

# %% [markdown]
# ## 3. KPIs (con definición y comparación)

# %%
k = {"Procesos": len(procesos), "Tasa de cancelación/desierto": 1 - len(vigentes) / len(procesos), "Monto adjudicado (miles de millones de Gs.)": adj.monto.sum() / 1e9,
     "% por contratación directa": procesos.metodo.fillna("").str.contains("Directa", case=False).mean(), "Mediana de oferentes": procesos.n_oferentes.median()}
pd.Series(k).round(3)

# %% [markdown]
# ## 4. Compradores: ¿dónde se concentra el gasto?

# %%
top = adj.groupby("comprador").monto.sum().sort_values().tail(10) / 1e9
fig, ax = plt.subplots(figsize=(8, 4)); ax.barh(top.index, top.values, color=[NARANJA if i == len(top) - 1 else GRIS for i in range(len(top))])
ax.set_xlabel("Monto adjudicado (miles de millones de Gs.)"); ax.set_title(f"{top.index[-1]} concentra la mayor parte del gasto", loc="left", fontweight="bold"); ax.grid(False); estilo.guardar(fig, "pr02_compradores.png")

# %% [markdown]
# ## 5. Métodos de contratación y su evolución

# %%
p = procesos.dropna(subset=["fecha"]).assign(mes=lambda d: d.fecha.dt.to_period("Q").dt.to_timestamp())
pv = p.pivot_table(index="mes", columns="metodo", values="ocid", aggfunc="count", fill_value=0); pv = pv.div(pv.sum(axis=1), axis=0); pv.index = [f"{d.year}-T{(d.month - 1) // 3 + 1}" for d in pv.index]   # etiquetas de texto: evita el formateador de fechas de pandas
fig, ax = plt.subplots(figsize=(9, 4)); pv.plot.bar(stacked=True, ax=ax, color=estilo.OKABE_ITO[:len(pv.columns)], width=.85)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right"); ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1))
ax.set_title("Mezcla de métodos de contratación por trimestre", loc="left", fontweight="bold"); ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1, 1)); ax.set_xlabel(""); estilo.guardar(fig, "pr02_metodos.png")

# %% [markdown]
# ## 6. Concentración de proveedores (índice de Herfindahl por comprador)
# HHI = Σ (cuota del proveedor)². Cerca de 1: depende de pocos proveedores.

# %%
def hhi(g): s = g.groupby("proveedor").monto.sum(); s = s / s.sum(); return (s ** 2).sum()
h = adj.groupby("comprador").apply(hhi, include_groups=False).sort_values(); n = adj.groupby("comprador").size()
fig, ax = plt.subplots(figsize=(8, 4)); ax.scatter(n[h.index], h.values, color=AZUL, s=60)
for c in h.index[-3:]: ax.annotate(c, (n[c], h[c]), xytext=(5, 5), textcoords="offset points", fontsize=8)
ax.set_xlabel("N.º de adjudicaciones"); ax.set_ylabel("HHI de proveedores"); ax.set_title("¿Qué entidades dependen de pocos proveedores?", loc="left", fontweight="bold"); estilo.guardar(fig, "pr02_hhi.png")

# %% [markdown]
# ## 7. Red comprador–proveedor (sesión 8)
# Nodos: compradores (naranja) y proveedores (azul); grosor = monto. **Filtramos aristas débiles** para evitar el *hairball*.

# %%
e = adj.groupby(["comprador", "proveedor"]).monto.sum().reset_index(); e = e[e.monto >= e.monto.quantile(.6)]
G = nx.Graph(); [G.add_edge("C:" + r.comprador, "P:" + r.proveedor, w=r.monto) for r in e.itertuples()]
pos = nx.spring_layout(G, seed=7, k=.6); cols = [NARANJA if n.startswith("C:") else AZUL for n in G]
fig, ax = plt.subplots(figsize=(8, 6)); nx.draw_networkx_edges(G, pos, ax=ax, edge_color=GRIS, width=[.5 + 3 * d["w"] / e.monto.max() for *_, d in G.edges(data=True)])
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=cols, node_size=[30 + 25 * G.degree(n) for n in G], edgecolors="white")
nx.draw_networkx_labels(G, pos, {n: n[2:] for n in G if n.startswith("C:")}, ax=ax, font_size=7); ax.axis("off"); ax.set_title("Red comprador–proveedor (aristas fuertes)", loc="left", fontweight="bold"); estilo.guardar(fig, "pr02_red.png")

# %% [markdown]
# ## Tu turno
# 1. Elegí **una entidad compradora** y respondé: ¿qué método usa más? ¿depende de pocos proveedores?
# 2. Construí **un gráfico** y escribí el título-mensaje. Documentá **qué procesos excluiste y por qué**.
# 3. Con datos reales: completá la **ficha del dataset** (práctica 1) y no saques conclusiones sobre personas o empresas sin contrastar con la fuente.
# 4. Publicá (R: `r/pr02_dncp.Rmd` → RPubs; Python: tu Colab).
