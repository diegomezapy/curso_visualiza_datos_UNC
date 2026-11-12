# %% [markdown]
# # Práctica 0 · Verificar las fuentes de datos (para el docente)
# Comprueba **hoy y desde Colab** qué fuentes responden y con qué estructura. Ejecutá todas las celdas y **guardá o copiá la tabla final**: sirve para decidir qué prácticas usar en clase y para ajustar el catálogo (`datos_reales/catalogo.py`).
# > Desde el entorno donde se armó el curso no se pudo abrir ninguna de estas fuentes, por eso esta verificación es necesaria.
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

import time, urllib.request, urllib.error, ssl
PRUEBAS = [
 ("DNCP · portal de datos abiertos", "https://www.contrataciones.gov.py/datos"),
 ("DNCP · documentación de la API v3", "https://contrataciones.gov.py/datos/api/v3/doc/"),
 ("Banco Mundial · API (indicador)", "https://api.worldbank.org/v2/country/PRY/indicator/NE.EXP.GNFS.ZS?format=json&per_page=5"),
 ("datos.gov.py · portal", "https://www.datos.gov.py"),
 ("datos.gov.py · ¿API CKAN?", "https://www.datos.gov.py/api/3/action/package_search?q=ephc&rows=3"),
 ("INE Paraguay · sitio", "https://www.ine.gov.py"),
 ("DNIT / Aduanas · sitio", "https://www.dnit.gov.py"),
 ("BCP · sitio", "https://www.bcp.gov.py"),
 ("MEF · sitio", "https://www.economia.gov.py"),
 ("MapBiomas Paraguay · sitio", "https://paraguay.mapbiomas.org"),
 ("Google Earth Engine · sitio", "https://earthengine.google.com"),
]
def probar(nombre, url, timeout=20):
    t0 = time.time(); r = {"fuente": nombre, "url": url, "estado": "", "ms": None, "tipo": "", "nota": ""}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": A.UA})
        with urllib.request.urlopen(req, timeout=timeout) as x:
            cuerpo = x.read(4000); r.update(estado=f"OK {x.status}", tipo=x.headers.get_content_type())
            if "json" in r["tipo"]:
                try: j = json.loads(cuerpo.decode("utf-8", "ignore")); r["nota"] = "JSON válido" if True else ""
                except Exception: r["nota"] = "JSON (vista parcial)"
    except urllib.error.HTTPError as e: r.update(estado=f"HTTP {e.code}", nota="el servidor respondió con error")
    except Exception as e: r.update(estado="SIN ACCESO", nota=f"{type(e).__name__}: {str(e)[:60]}")
    r["ms"] = int((time.time() - t0) * 1000); return r
res = pd.DataFrame([probar(n, u) for n, u in PRUEBAS])
pd.set_option("display.max_colwidth", 70); res[["fuente", "estado", "tipo", "ms", "nota"]]

# %% [markdown]
# ## Interpretación
# - **OK 200**: el sitio responde (eso **no** garantiza que haya datos descargables).
# - **HTTP 404/403**: la URL cambió o bloquea scripts → buscá la URL vigente en el sitio.
# - **SIN ACCESO**: red bloqueada, DNS o certificado.
# - En `datos.gov.py · ¿API CKAN?`, un JSON con `"success": true` indica que se puede buscar conjuntos por código.

# %%
print(res.estado.value_counts().to_string())
res.to_csv(estilo.salida("verificacion_fuentes.csv"), index=False)
print("\nTabla guardada. Copiala y enviala a quien mantiene el curso para ajustar el catálogo.")

# %% [markdown]
# ## Pasos manuales que NO se pueden automatizar
# 1. **Earth Engine / MapBiomas:** registrarse (https://earthengine.google.com), crear un proyecto de Google Cloud y probar `ee.Initialize(project=...)` (ver práctica 6). Confirmar el ID vigente del asset en paraguay.mapbiomas.org.
# 2. **EPHC (INE):** localizar la base vigente y su **diccionario de variables**; anotar el nombre de la columna del factor de expansión.
# 3. **Nómina de funcionarios:** localizar el conjunto en el portal de datos abiertos y revisar columnas; confirmar que se puede trabajar solo con agregados.
# 4. **Aduanas (DNIT):** confirmar si el portal de datos abiertos volvió a publicarse; si no, usar Banco Mundial/UN Comtrade/BCP.
