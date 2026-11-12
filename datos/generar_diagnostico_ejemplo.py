"""Genera datos/diagnostico_ejemplo.csv: respuestas SINTÉTICAS del diagnóstico (mismo esquema que la hoja real).
Sirve para probar el tablero y para los laboratorios antes de tener respuestas reales."""
import sys, random, datetime as dt
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "diagnostico"))
import preguntas as Q

rng = random.Random(2026)
filas = []
base = dt.datetime(2026, 11, 12, 9, 0)
for i in range(72):
    area = rng.choices(Q.AREAS, [24, 12, 26, 14, 6, 8, 10])[0]
    inf = area.startswith("Informática"); ing = area == "Ingeniería"
    exp = rng.choices(Q.EXPERIENCIA, [30, 28, 26, 16])[0]
    base_skill = {"Ninguna": 0.9, "Menos de 1 año": 1.6, "1 a 3 años": 2.4, "Más de 3 años": 3.2}[exp] + (0.8 if inf else 0.4 if ing else 0)
    herr = [h for h in Q.HERRAMIENTAS if h != "Ninguna" and rng.random() < {"Excel / Google Sheets": .8, "Python": .35 + .1 * base_skill, "R / RStudio": .12 + .04 * base_skill,
            "SQL": .25 + .08 * base_skill, "Power BI / Tableau / Looker": .22, "Google Colab / Jupyter": .2 + .08 * base_skill}[h]] or ["Ninguna"]
    clip = lambda x: max(1, min(5, round(x)))
    au = {"au_python": clip(base_skill + rng.gauss(0.3, .8)), "au_r": clip(base_skill - 0.9 + rng.gauss(0, .8)), "au_datos": clip(base_skill + rng.gauss(0, .8)),
          "au_graf_py": clip(base_skill - .2 + rng.gauss(0, .8)), "au_graf_r": clip(base_skill - 1.1 + rng.gauss(0, .8)), "au_colab": clip(base_skill - .2 + rng.gauss(0, 1)),
          "au_rstudio": clip(base_skill - 1.0 + rng.gauss(0, .9)), "au_tablero": clip(base_skill - .6 + rng.gauss(0, .9)), "au_diseno": clip(base_skill - .4 + rng.gauss(0, .9))}
    a, ok = {}, {}
    for pid, tema, _, ops, c, _ in Q.PREGUNTAS:
        skill = {"viz": 0.35 + .12 * au["au_diseno"], "py": 0.2 + .13 * au["au_python"], "r": 0.15 + .12 * au["au_r"]}[tema]
        u = rng.random()
        if u < skill: let, good = Q.LETRAS[c], 1
        elif u < skill + .12: let, good = "NS", 0
        else: let, good = Q.LETRAS[rng.choice([k for k in range(4) if k != c])], 0
        a["a_" + pid] = let; ok["ok_" + pid] = good
    sv = sum(ok["ok_" + p[0]] for p in Q.PREGUNTAS if p[1] == "viz"); sp = sum(ok["ok_" + p[0]] for p in Q.PREGUNTAS if p[1] == "py"); sr = sum(ok["ok_" + p[0]] for p in Q.PREGUNTAS if p[1] == "r")
    fila = {"ts": (base + dt.timedelta(minutes=rng.randint(0, 70), seconds=rng.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S"), "pid": "", "area": area, "cohorte": "MICD 2026",
            "experiencia": exp, "herramientas": "; ".join(herr), **au, **a, **ok, "score_viz": sv, "score_py": sp, "score_r": sr, "score_total": sv + sp + sr, "nivel": Q.nivel(sv + sp + sr), "comentario": ""}
    filas.append(fila)
df = pd.DataFrame(filas)[Q.COLUMNAS].sort_values("ts")
df.drop(columns=["pid", "comentario"]).to_csv(Path(__file__).parent / "diagnostico_ejemplo.csv", index=False)
print(len(df), "filas →", "datos/diagnostico_ejemplo.csv"); print(df.score_total.describe().round(2).to_dict()); print(df.nivel.value_counts().to_dict())
