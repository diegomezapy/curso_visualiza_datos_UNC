# %% [markdown]
# # Práctica 5 · Datos personales: visualizar sin exponer personas
# Algunos datos abiertos (p. ej. la **nómina de funcionarios**) describen a **personas identificables**. Que sean públicos por ley **no** significa que puedas publicarlos de cualquier forma. Regla del curso: **solo agregados**, nunca registros individuales.
# > Por defecto se usa una plantilla **sintética** sin nombres ni documentos.
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
# ## 1. Cargar y descartar identificadores **inmediatamente**

# %%
ORIGEN = ""   # URL o ruta del archivo real (si lo usás, trabajá solo con el resultado de las celdas siguientes)
if ORIGEN:
    try: crudo = A.leer_tabla(ORIGEN)
    except Exception as e: aviso(f"No se pudo leer ({e}). Se usa la plantilla SINTÉTICA."); crudo = pd.read_csv(EJ / "nomina_demo.csv")
else:
    aviso("Usando plantilla SINTÉTICA (sin nombres ni documentos)."); crudo = pd.read_csv(EJ / "nomina_demo.csv")
df, eliminadas = A.quitar_identificadores(crudo); del crudo
print("Columnas eliminadas por identificar personas:", eliminadas or "(ninguna detectada: revisá a mano)"); print("Columnas conservadas:", list(df.columns))

# %% [markdown]
# ## 2. Mapear columnas (ajustá con datos reales)

# %%
COL = dict(entidad="entidad", sexo="sexo", salario="salario_gs", nivel="nivel", categoria="categoria")
assert all(v in df.columns for v in COL.values()), "Ajustá COL a las columnas reales."
d = df.rename(columns={v: k for k, v in COL.items()}); d["salario"] = pd.to_numeric(d["salario"], errors="coerce"); print(d.salario.describe().round(0).to_string())

# %% [markdown]
# ## 3. Agregar y **suprimir celdas pequeñas** (k-anonimato simple)
# Un grupo de 1–4 personas puede permitir **identificar** a alguien. Ocultamos los grupos con menos de `K`.

# %%
K = 5
g = d.groupby("entidad").agg(n=("salario", "size"), mediana=("salario", "median"),
        mediana_mujeres=("salario", lambda s: s[d.loc[s.index, "sexo"] == "Mujer"].median()), mediana_hombres=("salario", lambda s: s[d.loc[s.index, "sexo"] == "Hombre"].median())).reset_index()
g["brecha"] = g.mediana_mujeres / g.mediana_hombres; seg = A.suprimir_celdas_pequenas(g, "n", K)
print(f"Entidades con menos de {K} personas (ocultas): {int(seg.suprimida.sum())}"); seg.head(8).round(2)

# %% [markdown]
# ## 4. Distribución salarial por nivel (agregada)

# %%
niveles = [n for n in ["Operativo", "Técnico", "Profesional", "Directivo"] if n in d.nivel.unique()]
fig, ax = plt.subplots(figsize=(8, 4)); ax.violinplot([d[d.nivel == n].salario.dropna() / 1e6 for n in niveles], showmedians=True); ax.set_xticks(range(1, len(niveles) + 1)); ax.set_xticklabels(niveles)
ax.set_ylabel("Salario (millones de Gs.)"); ax.set_title("Distribución salarial por nivel", loc="left", fontweight="bold"); estilo.guardar(fig, "pr05_violin.png")

# %% [markdown]
# ## 5. Brecha salarial por entidad (solo grupos grandes)

# %%
s = seg[~seg.suprimida].dropna(subset=["brecha"]).sort_values("brecha"); fig, ax = plt.subplots(figsize=(8, 5.5)); ax.barh(s.entidad, s.brecha, color=[NARANJA if b < .95 else GRIS for b in s.brecha]); ax.axvline(1, color="k", lw=.8)
ax.set_xlim(.8, 1.1); ax.set_xlabel("Mediana de mujeres / mediana de hombres"); ax.set_title(f"Brecha salarial por entidad (solo n ≥ {K})", loc="left", fontweight="bold"); ax.grid(False); estilo.guardar(fig, "pr05_brecha.png")

# %% [markdown]
# ## 6. Checklist ético de datos personales
# - [ ] ¿Descarté nombres, documentos y contactos al cargar? - [ ] ¿Muestro solo agregados? - [ ] ¿Suprimí grupos pequeños (n < K)?
# - [ ] ¿Evité rankings o “listas” de personas? - [ ] ¿Cité la fuente y aclaré que los datos pueden estar incompletos? - [ ] ¿Revisé la licencia y las condiciones de uso?
# - [ ] Antes de publicar en RPubs: ¿algún gráfico o tabla permite reconocer a una persona?
#
# ## Tu turno
# Elegí un indicador agregado (p. ej. **proporción de mujeres en cargos directivos por entidad**), construí el gráfico con supresión de celdas pequeñas y escribí **una nota ética** de 5 líneas.
