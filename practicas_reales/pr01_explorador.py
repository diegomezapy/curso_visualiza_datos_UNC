# %% [markdown]
# # Práctica 1 · Explorador de datasets: el “primer vistazo” a cualquier tabla
# Funciona con **cualquier CSV/Excel** (datos.gov.py, BCP, MEF…). Hace tres cosas: **perfila** las columnas, **evalúa la calidad** y **propone gráficos** según el tipo de dato (la matriz de decisión de la sesión 2).
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
# ## 1. Elegí tu dataset
# Pegá la **URL de descarga** (CSV/XLSX/JSON) o una ruta. Si lo dejás vacío se usa un dataset de ejemplo **sintético**.
# En Colab también podés subir un archivo: `from google.colab import files; files.upload()`.

# %%
ORIGEN = ""            # p. ej. "https://.../recurso.csv"
if ORIGEN:
    try: df = A.leer_tabla(ORIGEN); print("Leído:", ORIGEN)
    except Exception as e: aviso(f"No se pudo leer ({e}). Se usa el ejemplo SINTÉTICO."); df = pd.read_csv(EJ / "ephc_demo.csv")
else:
    aviso("Sin ORIGEN: usando un dataset de ejemplo SINTÉTICO (ephc_demo.csv)."); df = pd.read_csv(EJ / "ephc_demo.csv")
df.head()

# %% [markdown]
# ## 2. Calidad: ¿qué tan confiable es?

# %%
q = A.calidad(df); pd.Series(q)

# %% [markdown]
# ## 3. Perfil de columnas y gráfico sugerido

# %%
perfil = A.perfilar(df); pd.set_option("display.max_colwidth", 90); perfil

# %% [markdown]
# ## 4. Primer vistazo (gráficos automáticos)
# Son un **punto de partida**, no un producto final: elegí uno y mejoralo (título-mensaje, color de énfasis, anotación).

# %%
figs = A.primer_vistazo(df, perfil, max_graficos=6)
for i, f in enumerate(figs): estilo.guardar(f, f"pr01_vistazo_{i+1}.png")

# %% [markdown]
# ## 5. Ficha del dataset (obligatoria en los mini-proyectos)
# Copiá y completá:
# ```
# Nombre:            Fuente / institución:
# URL y fecha de descarga:            Licencia / condiciones de uso:
# Período y cobertura:        Unidad de análisis (qué es una fila):
# Variables clave y su significado:
# Problemas de calidad detectados (nulos, duplicados, codificación):
# ¿Contiene datos personales? ¿Cómo los tratás?:
# Limitaciones para interpretar los resultados:
# ```
# ## 6. Tu turno
# 1. Elegí **una pregunta** que el dataset pueda responder y un gráfico de la matriz de decisión.
# 2. Construilo con matplotlib/plotly y escribí el **título-mensaje**.
# 3. Publicá en RPubs (versión R: `r/pr01_explorador.Rmd`) o compartí tu Colab.
