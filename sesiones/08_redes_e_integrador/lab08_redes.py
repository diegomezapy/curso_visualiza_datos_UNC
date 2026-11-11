# %% [markdown]
# # Lab 8 · Redes (opcional): grafos y su visualización
# Datos: *Zachary Karate Club* y *Les Misérables* (incluidos en `networkx`, sin descargas).
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

import networkx as nx
from networkx.algorithms import community

# %% [markdown]
# ## 1. Layouts: el mismo grafo, lecturas distintas

# %%
G = nx.karate_club_graph()
fig, axs = plt.subplots(1, 3, figsize=(14, 4.3))
for ax, (nombre, pos) in zip(axs, [("Spring (fuerzas)", nx.spring_layout(G, seed=7)), ("Circular", nx.circular_layout(G)),
                                   ("Kamada-Kawai", nx.kamada_kawai_layout(G))]):
    nx.draw_networkx(G, pos, ax=ax, node_size=90, node_color=estilo.BASE, edge_color=estilo.GRIS_CLARO, with_labels=False)
    ax.set_title(nombre); ax.axis("off")
estilo.guardar(fig, "lab08_layouts.png")

# %% [markdown]
# ## 2. Codificar métricas: tamaño = centralidad, color = comunidad

# %%
cent = nx.betweenness_centrality(G); com = community.greedy_modularity_communities(G)
col = {n: estilo.OKABE_ITO[i] for i, c in enumerate(com) for n in c}
pos = nx.spring_layout(G, seed=7)
fig, ax = plt.subplots(figsize=(7, 5.5))
nx.draw_networkx_edges(G, pos, ax=ax, edge_color=estilo.GRIS_CLARO)
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=[200 + 3000 * cent[n] for n in G], node_color=[col[n] for n in G], edgecolors="white")
top = sorted(cent, key=cent.get, reverse=True)[:3]
nx.draw_networkx_labels(G, pos, {n: str(n) for n in top}, ax=ax, font_color="white", font_weight="bold")
ax.set_title(f"{len(com)} comunidades; los nodos {top} son puentes clave"); ax.axis("off")
estilo.guardar(fig, "lab08_metricas.png")

# %% [markdown]
# ## 3. Cuando el "hairball" falla: matriz de adyacencia (Les Misérables)

# %%
L = nx.les_miserables_graph(); orden = sorted(L.nodes, key=lambda n: -L.degree(n, weight="weight"))[:35]
M = nx.to_numpy_array(L, nodelist=orden, weight="weight")
fig, ax = plt.subplots(figsize=(7.5, 7)); ax.imshow(M, cmap="Blues"); ax.grid(False)
ax.set_xticks(range(35)); ax.set_xticklabels(orden, rotation=90, fontsize=7); ax.set_yticks(range(35)); ax.set_yticklabels(orden, fontsize=7)
ax.set_title("Matriz de adyacencia: los 35 personajes más conectados"); estilo.guardar(fig, "lab08_matriz.png")

# %% [markdown]
# ## Reglas para redes
# Layout con propósito · filtrar aristas débiles · no saturar etiquetas · si >500 nodos, agregar o usar matriz/arc-diagram · reportar métricas, no solo "se ve bonito".
# Herramientas: `networkx`, `pyvis` (interactivo), `Gephi`, `Cytoscape`.
#
# ## Ejercicio opcional
# Construí una red de **co-ocurrencias** a partir de un texto o de la tabla `ventas` (productos comprados juntos) y presentá 2 hallazgos.
