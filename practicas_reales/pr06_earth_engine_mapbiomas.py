# %% [markdown]
# # Práctica 6 · Earth Engine y MapBiomas: cambio de uso del suelo en Paraguay
# **Qué vas a hacer:** conectarte a Google Earth Engine desde Colab, dibujar un mapa y **medir cuánta superficie cambió** entre dos años usando los mapas anuales de MapBiomas Paraguay (30 m, 1985–2023, Colección 2).
#
# ## Antes de la clase (¡no se puede improvisar!)
# 1. **Registrate** en Earth Engine (https://earthengine.google.com): gratis para uso no comercial/investigación; la aprobación puede demorar.
# 2. Creá un **proyecto de Google Cloud** y asociálo a Earth Engine. Anotá su **ID** (p. ej. `mi-proyecto-123`).
# 3. Verificá en https://paraguay.mapbiomas.org el **ID vigente del asset** (ver abajo).
# > Esta práctica **no se pudo ejecutar** en el entorno donde se preparó el curso (requiere tu cuenta de Google). Si algo falla, el mensaje de error te dice qué revisar. **Alternativa sin Earth Engine:** descargá las *estadísticas* de MapBiomas Paraguay (hectáreas por clase, departamento y año) desde su sitio y usá la práctica 1.

# %%
import sys, warnings
warnings.filterwarnings("ignore")
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo
estilo.aplicar_tema()

PROYECTO = ""    # ← ID de tu proyecto de Google Cloud
# ID del asset: el sitio de MapBiomas Paraguay lo lista con la ruta «collection1» aunque lo rotula Colección 2. VERIFICAR antes de usar.
ASSET = "projects/mapbiomas-public/assets/paraguay/collection1/mapbiomas_paraguay_collection1_integration_v1"
ANIO_A, ANIO_B = None, None   # None = primer y último año disponibles en el asset
ESCALA = 300                  # metros: 300 para ir rápido; bajá a 30 para precisión (más lento)

# %% [markdown]
# ## 1. Conectarse a Earth Engine

# %%
try:
    import ee
    if not PROYECTO:
        try:
            from google.colab import userdata; PROYECTO = userdata.get("EE_PROYECTO")
        except Exception: pass
    if not PROYECTO: raise RuntimeError("Falta PROYECTO (ID de tu proyecto de Google Cloud). También podés guardarlo en Colab → Secretos como EE_PROYECTO.")
    try: ee.Initialize(project=PROYECTO)
    except Exception: ee.Authenticate(); ee.Initialize(project=PROYECTO)
    EE_OK = True; print("Conectado a Earth Engine con el proyecto", PROYECTO)
except Exception as e:
    EE_OK = False; print("\n" + "!" * 70 + f"\nNo se pudo usar Earth Engine: {e}\nLas celdas siguientes se omiten. Revisá los pasos «Antes de la clase».\n" + "!" * 70)

# %% [markdown]
# ## 2. Primer mapa: relieve (SRTM) y límite de Paraguay
# `USDOS/LSIB_SIMPLE/2017` contiene los límites de países; `USGS/SRTMGL1_003` es el modelo de elevación global de 30 m.

# %%
if EE_OK:
    import geemap
    pais = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq("country_na", "Paraguay"))
    Map = geemap.Map(center=[-23.4, -58.4], zoom=6)
    Map.addLayer(ee.Image("USGS/SRTMGL1_003").clip(pais), {"min": 0, "max": 700, "palette": ["#f7fbff", "#9ecae1", "#08519c"]}, "Elevación (m)")
    Map.addLayer(pais.style(color="#D55E00", fillColor="00000000", width=2), {}, "Paraguay"); display(Map)

# %% [markdown]
# ## 3. Cargar MapBiomas y descubrir sus años
# Las colecciones de MapBiomas guardan **una banda por año** (`classification_AAAA`). No fijamos el año: lo leemos del asset.

# %%
if EE_OK:
    mb = ee.Image(ASSET); bandas = mb.bandNames().getInfo(); anios = sorted(int(b.split("_")[-1]) for b in bandas if b.startswith("classification_"))
    ANIO_A = ANIO_A or anios[0]; ANIO_B = ANIO_B or anios[-1]; print(f"Años disponibles: {anios[0]}–{anios[-1]} · comparando {ANIO_A} vs {ANIO_B}")

# %% [markdown]
# ## 4. Mapa de los dos años
# **Leyenda:** los códigos de clase y sus colores oficiales están en el sitio de MapBiomas Paraguay; acá usamos una paleta genérica.

# %%
if EE_OK:
    vis = {"min": 0, "max": 70, "palette": ["#ffffff", "#1f8d49", "#7dc975", "#d6bc74", "#ffefc3", "#ea9999", "#2532e4", "#d5d5e5", "#e974ed", "#ff0000"] * 7}
    M2 = geemap.Map(center=[-23.4, -58.4], zoom=6)
    M2.addLayer(mb.select(f"classification_{ANIO_A}").clip(pais), vis, f"Clases {ANIO_A}"); M2.addLayer(mb.select(f"classification_{ANIO_B}").clip(pais), vis, f"Clases {ANIO_B}"); display(M2)

# %% [markdown]
# ## 5. Medir el cambio: hectáreas por clase en cada año

# %%
def area_por_clase(anio):
    img = ee.Image.pixelArea().divide(1e4).addBands(mb.select(f"classification_{anio}"))
    r = img.reduceRegion(reducer=ee.Reducer.sum().group(groupField=1, groupName="clase"), geometry=pais.geometry(), scale=ESCALA, maxPixels=1e13, bestEffort=True, tileScale=4).getInfo()
    return pd.Series({int(g["clase"]): g["sum"] for g in r["groups"]}, name=anio)
if EE_OK:
    t = pd.concat([area_por_clase(ANIO_A), area_por_clase(ANIO_B)], axis=1).fillna(0); t["cambio_ha"] = t[ANIO_B] - t[ANIO_A]; t["cambio_%"] = (t["cambio_ha"] / t[ANIO_A].replace(0, np.nan) * 100).round(1)
    t.index.name = "clase (código MapBiomas)"; t = t.sort_values("cambio_ha"); display(t.round(0))

# %% [markdown]
# ## 6. Gráfico: ¿qué ganó y qué perdió superficie? (paleta divergente)

# %%
if EE_OK:
    s = t["cambio_ha"] / 1e6; fig, ax = plt.subplots(figsize=(8, 6)); ax.barh([str(i) for i in s.index], s.values, color=["#D55E00" if v < 0 else "#0072B2" for v in s.values]); ax.axvline(0, color="k", lw=.8)
    ax.set_xlabel("Cambio de superficie (millones de hectáreas)"); ax.set_ylabel("Código de clase"); ax.set_title(f"Cambio de cobertura y uso del suelo, {ANIO_A}–{ANIO_B}", loc="left", fontweight="bold"); estilo.guardar(fig, "pr06_cambio.png")

# %% [markdown]
# ## Tu turno
# 1. Buscá en el sitio de MapBiomas Paraguay **qué significa cada código** y reemplazá los números por nombres en el gráfico.
# 2. Pasá de hectáreas a **proporción de la superficie del país** (no solo valores absolutos).
# 3. Repetí para **un departamento**: filtrá un límite administrativo (p. ej. `FAO/GAUL/2015/level1`, campo `ADM1_NAME`) en vez del país. ¿Mapa de cambio o de totales? Justificá con lo visto sobre coropletas y tasas.
# 4. Citá **MapBiomas Paraguay (colección y año)**, la fecha de consulta y respetá sus condiciones de uso.
