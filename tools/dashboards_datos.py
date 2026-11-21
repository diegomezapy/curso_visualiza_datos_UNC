"""Prepara los datos AGREGADOS de la presentación de la sesión 5 (Dashboards) a partir de la base de aduanas (DNIT).
Entrada: parquet/CSV de importaciones con las columnas originales de la DNIT (aquí: importaciones_electronica_2024_2025.parquet).
Salida (aula/media/unidad5_dashboards/fuentes/datos/): cubo_importaciones.csv (año, mes, aduana, país, medio) y subitems_muestra.csv.
Uso: python tools/dashboards_datos.py <archivo.parquet|csv> [separador del CSV, por defecto ;]"""
import sys, re
from pathlib import Path
import pandas as pd
RAIZ = Path(__file__).resolve().parents[1]; OUT = RAIZ / "aula" / "media" / "unidad5_dashboards" / "fuentes" / "datos"; OUT.mkdir(parents=True, exist_ok=True)
ruta = Path(sys.argv[1]); sep = sys.argv[2] if len(sys.argv) > 2 else ";"
cols = ["DESPACHO CIFRADO", "ITEM", "OPERACION", "ADUANA", "anio", "mes", "PAIS ORIGEN", "MEDIO TRANSPORTE", "FOB DOLAR", "KILO NETO"]
df = pd.read_parquet(ruta, columns=cols) if ruta.suffix == ".parquet" else pd.read_csv(ruta, sep=sep, usecols=cols, dtype=str)
num = lambda s: pd.to_numeric(s.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")   # miles con punto, decimales con coma
df = df[df.OPERACION == "IMPORTACION"].copy()
df["fob_usd"] = num(df["FOB DOLAR"]); df["kilo_neto"] = num(df["KILO NETO"])
df["pais"] = df["PAIS ORIGEN"].str.replace(r"^[A-Z]{2}\s*-\s*", "", regex=True).str.strip().str.upper()
df = df.rename(columns={"DESPACHO CIFRADO": "despacho", "ITEM": "item", "ADUANA": "aduana", "MEDIO TRANSPORTE": "medio"})
muestra_desp = df.despacho.drop_duplicates().sample(300, random_state=2026)
df[df.despacho.isin(muestra_desp)][["despacho", "item", "aduana", "pais", "medio", "fob_usd", "kilo_neto"]].to_csv(OUT / "subitems_muestra.csv", index=False)
it = df.drop_duplicates(["despacho", "item"])   # una fila por ítem: los subítems repiten los valores del ítem
cubo = it.groupby(["anio", "mes", "aduana", "pais", "medio"], as_index=False).agg(items=("item", "size"), fob_usd=("fob_usd", "sum"), kilo_neto=("kilo_neto", "sum"))
cubo["fob_usd"] = cubo.fob_usd.round(2); cubo["kilo_neto"] = cubo.kilo_neto.round(1)
cubo.to_csv(OUT / "cubo_importaciones.csv", index=False)
print(len(df), "filas (subítems) →", len(it), "ítems →", len(cubo), "filas del cubo; FOB total", round(cubo.fob_usd.sum() / 1e6, 1), "M USD")
print(cubo.groupby("anio").fob_usd.sum().div(1e6).round(1).to_dict(), cubo.pais.nunique(), "países;", cubo.aduana.nunique(), "aduanas")
