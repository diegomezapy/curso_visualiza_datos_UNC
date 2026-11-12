# %% [markdown]
# # Lab 0 · Del dato a la visualización: resultados del diagnóstico inicial (Python → Colab)
# **Objetivo:** ver, con datos que *ustedes mismos generaron*, cómo se conecta la **captura de datos** con la **visualización de resultados**.
# Esta es la **vía Python → Colab** (la vía R → RPubs está en `r/00_diagnostico.Rmd` y el tablero en vivo en el aula).
#
# ```
# Cuestionario web → Google Apps Script → Hoja de Google Sheets → ┬→ Tablero en vivo (Apps Script)
#    (captura)         (valida y guarda)      (fuente única)      ├→ Looker Studio
#                                                                 ├→ R Markdown → RPubs
#                                                                 └→ Python → Google Colab  ← estás acá
# ```

# %%
import sys, json, urllib.request
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo
estilo.aplicar_tema()
RAW = "https://raw.githubusercontent.com/diegomezapy/curso_visualiza_datos_UNC/main"

# %% [markdown]
# ## 1. Leer los datos
# Si el docente configuró el endpoint de Apps Script, leemos la hoja **en vivo** (`?action=csv`); si no, usamos datos de ejemplo.

# %%
def leer_diagnostico():
    try:
        cfg = json.loads((RAIZ / "aula" / "config.json").read_text(encoding="utf-8")) if (RAIZ / "aula" / "config.json").exists() \
              else json.load(urllib.request.urlopen(f"{RAW}/aula/config.json", timeout=15))
        ep = cfg.get("diagnostico", {}).get("endpoint", "")
        if ep:
            d = pd.read_csv(f"{ep}?action=csv")
            if len(d): return d, "hoja de Google Sheets (en vivo vía Apps Script)"
    except Exception as e:
        print("No se pudo leer la hoja en vivo:", e)
    return pd.read_csv(RAIZ / "datos" / "diagnostico_ejemplo.csv"), "datos de ejemplo (sintéticos)"

d, fuente = leer_diagnostico()
print(f"Fuente: {fuente} · {len(d)} respuestas")
d.head(3)

# %% [markdown]
# Cada fila es una persona y cada columna una variable (**datos ordenados / *tidy***). Las columnas `ok_*` valen 1 si la respuesta fue correcta y `score_*` suman aciertos por área.

# %%
AZUL, NARANJA, VERDE = "#0072B2", "#D55E00", "#009E73"
d[["score_viz", "score_py", "score_r", "score_total"]].describe().round(2)

# %% [markdown]
# ## 2. ¿Qué sabemos de Python y de R?
# ### 2.1 Puntaje por área temática

# %%
tema = {"score_viz": ("Visualización (conceptos)", VERDE), "score_py": ("Python", AZUL), "score_r": ("R", NARANJA)}
m = d[list(tema)].mean()
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.barh([tema[k][0] for k in m.index][::-1], m.values[::-1], color=[tema[k][1] for k in m.index][::-1], height=.6)
for y, v in enumerate(m.values[::-1]): ax.text(v + .05, y, f"{v:.1f} / 4", va="center")
ax.set_xlim(0, 4.6); ax.grid(False); ax.set_xlabel("Promedio de aciertos (máx. 4)")
ax.set_title("El grupo llega más fuerte en unas áreas que en otras"); estilo.guardar(fig, "lab00_area.png")

# %% [markdown]
# ### 2.2 Python vs R: ¿cómo se distribuyen los aciertos?

# %%
ks = range(5)
py = d.score_py.value_counts(normalize=True).reindex(ks, fill_value=0); r = d.score_r.value_counts(normalize=True).reindex(ks, fill_value=0)
x = np.arange(5); fig, ax = plt.subplots(figsize=(8, 3.8))
ax.bar(x - .2, py, .4, color=AZUL, label="Python"); ax.bar(x + .2, r, .4, color=NARANJA, label="R")
ax.set_xticks(x); ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1)); ax.legend()
ax.set_xlabel("Aciertos (de 4)"); ax.set_title("Más gente se concentra en pocos aciertos en R que en Python"); estilo.guardar(fig, "lab00_dist.png")

# %% [markdown]
# ### 2.3 Niveles del grupo

# %%
orden = ["Inicial", "Intermedio", "Avanzado"]; cols = ["#c2410c", AZUL, "#1a7f4b"]
c = d.nivel.value_counts(normalize=True).reindex(orden, fill_value=0)
fig, ax = plt.subplots(figsize=(8, 1.6)); izq = 0
for n, v, col in zip(orden, c, cols):
    ax.barh([0], [v], left=izq, color=col); ax.text(izq + v / 2, 0, f"{n}\n{v:.0%}", ha="center", va="center", color="white", fontweight="bold", fontsize=9); izq += v
ax.axis("off"); ax.set_title("Composición del grupo por nivel", loc="left", fontweight="bold"); estilo.guardar(fig, "lab00_niveles.png")

# %% [markdown]
# ### 2.4 Autoevaluación y calibración

# %%
etq = {"au_python": "Programar en Python", "au_r": "Programar en R", "au_datos": "Manipular datos (pandas / dplyr)", "au_graf_py": "Graficar con matplotlib / seaborn / plotly",
       "au_graf_r": "Graficar con ggplot2", "au_colab": "Usar Google Colab / Jupyter", "au_rstudio": "Usar RStudio y R Markdown", "au_tablero": "Construir tableros", "au_diseno": "Criterios de diseño visual"}
col = lambda k: NARANJA if k in ("au_r", "au_graf_r", "au_rstudio") else AZUL if k in ("au_python", "au_graf_py", "au_colab") else "#8C8C8C"
a = d[list(etq)].mean().sort_values()
fig, axs = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw={"width_ratios": [1.2, 1]})
axs[0].barh([etq[k] for k in a.index], a.values, color=[col(k) for k in a.index]); axs[0].set_xlim(0, 5.4); axs[0].grid(False)
for y, v in enumerate(a.values): axs[0].text(v + .05, y, f"{v:.1f}", va="center")
axs[0].set_title("Autoevaluación promedio (1–5)")
auto = (d.au_python + d.au_r) / 2; ac = d.score_py + d.score_r; rng = np.random.default_rng(1)
axs[1].scatter(auto + rng.uniform(-.12, .12, len(d)), ac + rng.uniform(-.12, .12, len(d)), color=AZUL, alpha=.6)
b = np.polyfit(auto, ac, 1); xs = np.array([1, 5]); axs[1].plot(xs, b[0] * xs + b[1], color=NARANJA)
axs[1].set_xlabel("Autoevaluación media (Python y R)"); axs[1].set_ylabel("Aciertos en Python + R (de 8)"); axs[1].set_title("¿Se calibran bien?")
fig.tight_layout(); estilo.guardar(fig, "lab00_autoeval.png")

# %% [markdown]
# ### 2.5 Aciertos por pregunta

# %%
ok = d.filter(like="ok_").mean().sort_values(); ok.index = ok.index.str.replace("ok_", "")
cc = {"V": VERDE, "P": AZUL, "R": NARANJA}
fig, ax = plt.subplots(figsize=(8, 4.6)); ax.barh(ok.index, ok.values, color=[cc[i[0]] for i in ok.index])
for y, v in enumerate(ok.values): ax.text(v + .01, y, f"{v:.0%}", va="center")
ax.set_xlim(0, 1.1); ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1)); ax.grid(False)
ax.set_title("De la pregunta más difícil a la más fácil"); estilo.guardar(fig, "lab00_preguntas.png")

# %% [markdown]
# ## 3. Tablero interactivo con Plotly (filtro por área)
# Un archivo HTML autocontenido que podés compartir o abrir en el navegador.

# %%
import plotly.graph_objects as go
from plotly.subplots import make_subplots
areas = ["Todas"] + sorted(d.area.unique())
def vistas(df):
    p = df[["score_viz", "score_py", "score_r"]].mean().values
    h = df.nivel.value_counts().reindex(orden, fill_value=0).values
    return p, h
fig = make_subplots(rows=1, cols=2, subplot_titles=("Aciertos promedio por área temática (de 4)", "Participantes por nivel"), column_widths=[.55, .45])
for i, a_ in enumerate(areas):
    df = d if a_ == "Todas" else d[d.area == a_]; p, h = vistas(df)
    fig.add_trace(go.Bar(x=["Visualización", "Python", "R"], y=p, marker_color=[VERDE, AZUL, NARANJA], visible=(i == 0), name=a_, hovertemplate="%{x}: %{y:.1f}/4"), row=1, col=1)
    fig.add_trace(go.Bar(x=orden, y=h, marker_color=cols, visible=(i == 0), name=a_, hovertemplate="%{x}: %{y}"), row=1, col=2)
botones = [dict(label=f"{a_} ({len(d) if a_ == 'Todas' else (d.area == a_).sum()})", method="update",
                args=[{"visible": [j // 2 == i for j in range(2 * len(areas))]}]) for i, a_ in enumerate(areas)]
fig.update_layout(template=estilo.PLOTLY_TEMPLATE, showlegend=False, height=430, title=f"Diagnóstico inicial · {fuente}", yaxis=dict(range=[0, 4]),
                  updatemenus=[dict(buttons=botones, x=0, y=1.25, xanchor="left")])
fig.write_html(estilo.salida("lab00_tablero.html"))
if "ipykernel" in sys.modules: fig.show()   # en Colab/Jupyter se muestra aquí; como script solo guarda el HTML

# %% [markdown]
# ## 4. Tu turno
# 1. **¿En qué área está la mayor brecha entre Python y R?** Calculá `d.groupby("area")[["score_py","score_r"]].mean()` y graficala.
# 2. Elegí una visualización y mejorala (título-mensaje, color de énfasis, anotación). Explicá tu decisión en 5 líneas.
# 3. Guardá una copia en tu Drive, compartila (*cualquier persona con el enlace → Lector*) y pegá el enlace en la actividad del aula.
