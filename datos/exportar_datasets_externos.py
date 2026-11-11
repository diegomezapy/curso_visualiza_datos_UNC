"""Exporta a CSV los datasets que en Python vienen incluidos (scikit-learn y networkx),
para que las pistas de Python y R trabajen con los mismos archivos.
Uso: python datos/exportar_datasets_externos.py"""
from pathlib import Path
import pandas as pd, networkx as nx
from sklearn.datasets import load_wine

AQUI = Path(__file__).parent
w = load_wine(as_frame=True)
df = w.data.copy(); df["clase"] = w.target.map(dict(enumerate(w.target_names)))
df.to_csv(AQUI / "wine.csv", index=False)

L = nx.les_miserables_graph()
pd.DataFrame([(a, b, d["weight"]) for a, b, d in L.edges(data=True)], columns=["origen", "destino", "peso"]).to_csv(AQUI / "lesmis_aristas.csv", index=False)
K = nx.karate_club_graph()
pd.DataFrame([(a, b) for a, b in K.edges()], columns=["origen", "destino"]).to_csv(AQUI / "karate_aristas.csv", index=False)
pd.DataFrame([(n, d["club"]) for n, d in K.nodes(data=True)], columns=["nodo", "club"]).to_csv(AQUI / "karate_nodos.csv", index=False)
print("ok")
