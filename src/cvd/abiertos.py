"""Herramientas para trabajar con datos abiertos reales (Python).
Todas las funciones son independientes del esquema de cada fuente: se adaptan a las columnas que existan."""
from __future__ import annotations
import io, json, re, urllib.request, urllib.error
import numpy as np, pandas as pd

UA = "curso-visualizacion-datos-unc/1.0"
class SinConexion(Exception):
    """No se pudo obtener el recurso (sin internet, fuente caída o URL cambiada)."""

# ------------------------------------------------------------------ descarga
def descargar(url: str, timeout: int = 30) -> bytes:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception as e:                      # red, DNS, HTTP, SSL…
        raise SinConexion(f"{type(e).__name__}: {e}") from e

def leer_tabla(origen, **kw) -> pd.DataFrame:
    """Lee CSV/XLSX/JSON desde una URL o ruta. Prueba separadores y codificaciones comunes en Paraguay (utf-8, latin-1)."""
    nombre = str(origen).lower().split("?")[0]
    datos = descargar(origen) if str(origen).startswith(("http://", "https://")) else open(origen, "rb").read()
    if nombre.endswith((".xlsx", ".xls")): return pd.read_excel(io.BytesIO(datos), **kw)
    if nombre.endswith(".json"): return pd.json_normalize(json.loads(datos.decode("utf-8", "replace")))
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try: txt = datos.decode(enc); break
        except UnicodeDecodeError: continue
    for sep in (",", ";", "\t", "|"):
        try:
            df = pd.read_csv(io.StringIO(txt), sep=sep, low_memory=False, **kw)
            if df.shape[1] > 1: return df
        except Exception: continue
    raise ValueError("No se pudo interpretar el archivo como tabla")

# ------------------------------------------------------------------ perfilado y gráficos sugeridos
def _tipo(s: pd.Series) -> str:
    n = len(s); nn = s.dropna()
    if nn.empty: return "vacía"
    nombre = str(s.name).lower()
    if pd.api.types.is_bool_dtype(s): return "categórica"
    if pd.api.types.is_datetime64_any_dtype(s): return "fecha"
    if pd.api.types.is_numeric_dtype(s):
        if re.search(r"(^|_)(lat|latitud)($|_)", nombre): return "latitud"
        if re.search(r"(^|_)(lon|lng|long|longitud)($|_)", nombre): return "longitud"
        if nn.nunique() <= 12 and (nn % 1 == 0).all() and nn.nunique() / max(n, 1) < 0.2: return "categórica"
        return "numérica"
    m = nn.astype(str).head(300)
    if re.search(r"fecha|date|periodo|período|dia|día|mes|anio|año", nombre) or m.str.match(r"^\d{4}-\d{2}(-\d{2})?").mean() > .8 or m.str.match(r"^\d{1,2}/\d{1,2}/\d{2,4}").mean() > .8:
        p = pd.to_datetime(m, errors="coerce", dayfirst=bool(m.str.match(r"^\d{1,2}/").mean() > .5))
        if p.notna().mean() > .85: return "fecha"
    u = nn.nunique()
    if u / max(len(nn), 1) > .9 and u > 30: return "identificador/texto"
    if u <= max(30, 0.05 * n): return "categórica"
    return "identificador/texto"

SUGERENCIA = {"numérica": "histograma / ECDF; caja o violín por grupo; dispersión contra otra numérica", "categórica": "barras ordenadas (top-N); barras apiladas al 100 % para proporciones",
  "fecha": "línea (serie por mes/año); heatmap año×mes si hay estacionalidad", "latitud": "mapa de puntos/burbujas (junto con longitud)", "longitud": "mapa de puntos/burbujas (junto con latitud)",
  "identificador/texto": "no graficar directamente: contar únicos, duplicados o extraer palabras clave", "vacía": "descartar"}

def perfilar(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen por columna: tipo inferido, nulos, únicos, ejemplo y gráfico recomendado (matriz de decisión de la sesión 2)."""
    filas = []
    for c in df.columns:
        t = _tipo(df[c])
        filas.append({"columna": c, "tipo": t, "nulos_%": round(df[c].isna().mean() * 100, 1), "únicos": int(df[c].nunique(dropna=True)),
                      "ejemplo": str(df[c].dropna().iloc[0])[:40] if df[c].notna().any() else "", "gráfico sugerido": SUGERENCIA[t]})
    return pd.DataFrame(filas)

def calidad(df: pd.DataFrame) -> dict:
    return {"filas": len(df), "columnas": df.shape[1], "filas_duplicadas": int(df.duplicated().sum()), "celdas_nulas_%": round(df.isna().mean().mean() * 100, 1),
            "columnas_vacías": [c for c in df.columns if df[c].isna().all()], "columnas_constantes": [c for c in df.columns if df[c].nunique(dropna=True) == 1]}

def primer_vistazo(df: pd.DataFrame, perfil: pd.DataFrame | None = None, max_graficos: int = 6, estilo=None):
    """Genera hasta `max_graficos` figuras de matplotlib elegidas según el tipo de cada columna."""
    import matplotlib.pyplot as plt
    perfil = perfil if perfil is not None else perfilar(df); figs = []
    azul, naranja = "#0072B2", "#D55E00"
    for _, r in perfil.iterrows():
        if len(figs) >= max_graficos: break
        c, t = r["columna"], r["tipo"]
        if t == "numérica" and df[c].notna().sum() > 5:
            fig, ax = plt.subplots(figsize=(6, 3)); x = df[c].dropna()
            x = x[(x >= x.quantile(.01)) & (x <= x.quantile(.99))] if len(x) > 50 else x
            ax.hist(x, bins=30, color=azul, edgecolor="white"); ax.set_title(f"{c}: distribución (1.º–99.º percentil)", loc="left", fontweight="bold")
        elif t == "categórica":
            fig, ax = plt.subplots(figsize=(6, 3.2)); v = df[c].astype(str).value_counts().head(10).sort_values()
            ax.barh(v.index, v.values, color=[naranja if i == len(v) - 1 else "#D9D9D9" for i in range(len(v))]); ax.set_title(f"{c}: top {len(v)}", loc="left", fontweight="bold")
        elif t == "fecha":
            f = pd.to_datetime(df[c], errors="coerce", dayfirst=True).dropna()
            if f.empty: continue
            fig, ax = plt.subplots(figsize=(6, 3)); s = f.dt.to_period("M").value_counts().sort_index(); s.index = s.index.to_timestamp()
            ax.plot(s.index, s.values, color=azul, lw=2); ax.set_title(f"{c}: registros por mes", loc="left", fontweight="bold")
        else: continue
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
        fig.tight_layout(); figs.append(fig)
    return figs

# ------------------------------------------------------------------ OCDS (contrataciones abiertas)
def _lista(o):
    if isinstance(o, dict):
        if "releases" in o: return o["releases"]
        if "records" in o: return [r.get("compiledRelease") or (r.get("releases") or [{}])[0] for r in o["records"]]
        if "list" in o: return o["list"]
        return [o]
    return o or []

def ocds_a_tabla(obj) -> pd.DataFrame:
    """Aplana releases OCDS (paquete de releases, records o un release) a una fila por proceso. Usa solo campos estándar y tolera ausentes."""
    filas = []
    for r in _lista(obj):
        if not isinstance(r, dict): continue
        t = r.get("tender") or {}; b = r.get("buyer") or {}; aw = r.get("awards") or []
        monto_adj = sum(float(((a or {}).get("value") or {}).get("amount") or 0) for a in aw)
        filas.append({"ocid": r.get("ocid"), "fecha": r.get("date"), "comprador": b.get("name"), "comprador_id": b.get("id"), "titulo": t.get("title"),
                      "estado": t.get("status"), "metodo": t.get("procurementMethodDetails") or t.get("procurementMethod"), "categoria": t.get("mainProcurementCategory"),
                      "monto_estimado": (t.get("value") or {}).get("amount"), "moneda": (t.get("value") or {}).get("currency"), "n_oferentes": t.get("numberOfTenderers"),
                      "n_adjudicaciones": len(aw), "monto_adjudicado": monto_adj if aw else np.nan,
                      "inicio_ofertas": (t.get("tenderPeriod") or {}).get("startDate")})
    df = pd.DataFrame(filas)
    for c in ("fecha", "inicio_ofertas"):
        if c in df: df[c] = pd.to_datetime(df[c], errors="coerce", utc=True).dt.tz_localize(None)
    for c in ("monto_estimado", "monto_adjudicado", "n_oferentes"):
        if c in df: df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def ocds_adjudicaciones(obj) -> pd.DataFrame:
    """Una fila por adjudicación × proveedor (para redes comprador–proveedor)."""
    filas = []
    for r in _lista(obj):
        if not isinstance(r, dict): continue
        for a in r.get("awards") or []:
            for s in (a or {}).get("suppliers") or [{}]:
                filas.append({"ocid": r.get("ocid"), "comprador": (r.get("buyer") or {}).get("name"), "proveedor": (s or {}).get("name"), "proveedor_id": (s or {}).get("id"),
                              "monto": pd.to_numeric(((a or {}).get("value") or {}).get("amount"), errors="coerce"), "fecha": (a or {}).get("date") or r.get("date")})
    df = pd.DataFrame(filas)
    if "fecha" in df: df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", utc=True).dt.tz_localize(None)
    return df

# ------------------------------------------------------------------ Banco Mundial
def parsear_banco_mundial(resp) -> pd.DataFrame:
    """La API devuelve [metadatos, [observaciones]]. Devuelve tabla ordenada: pais, iso3, anio, valor, indicador."""
    if not isinstance(resp, list) or len(resp) < 2 or resp[1] is None: return pd.DataFrame(columns=["pais", "iso3", "anio", "valor", "indicador"])
    return pd.DataFrame([{"pais": (o.get("country") or {}).get("value"), "iso3": o.get("countryiso3code"), "anio": int(o["date"]) if str(o.get("date", "")).isdigit() else None,
                          "valor": o.get("value"), "indicador": (o.get("indicator") or {}).get("value"), "codigo": (o.get("indicator") or {}).get("id")} for o in resp[1]]).sort_values(["iso3", "anio"]).reset_index(drop=True)

def banco_mundial(indicador: str, paises=("PRY", "ARG", "BRA", "URY", "BOL"), desde=2000, hasta=2024) -> pd.DataFrame:
    """Descarga un indicador del Banco Mundial (API v2, sin clave). Lanza SinConexion si no hay acceso."""
    url = f"https://api.worldbank.org/v2/country/{';'.join(paises)}/indicator/{indicador}?format=json&per_page=20000&date={desde}:{hasta}"
    return parsear_banco_mundial(json.loads(descargar(url).decode("utf-8")))

# ------------------------------------------------------------------ estadística ponderada (encuestas)
def media_ponderada(x, w) -> float:
    x, w = np.asarray(x, float), np.asarray(w, float); m = ~(np.isnan(x) | np.isnan(w)); return float(np.average(x[m], weights=w[m]))
def cuantil_ponderado(x, w, q: float) -> float:
    x, w = np.asarray(x, float), np.asarray(w, float); m = ~(np.isnan(x) | np.isnan(w)); x, w = x[m], w[m]
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w) - 0.5 * w; c /= w.sum(); return float(np.interp(q, c, x))
def proporcion_ponderada(df: pd.DataFrame, col: str, peso: str) -> pd.Series:
    return (df.groupby(col)[peso].sum() / df[peso].sum()).sort_values(ascending=False)

# ------------------------------------------------------------------ privacidad
PATRONES_IDENTIFICADORES = r"nombre|apellido|^ci$|cedula|cédula|documento|^doc|ruc|telefono|teléfono|celular|correo|email|direccion|dirección|domicilio"
def quitar_identificadores(df: pd.DataFrame, patron: str = PATRONES_IDENTIFICADORES):
    """Elimina columnas que parecen identificar personas. Devuelve (df_sin_ids, columnas_eliminadas)."""
    cols = [c for c in df.columns if re.search(patron, str(c), re.I)]
    return df.drop(columns=cols), cols
def suprimir_celdas_pequenas(tabla: pd.DataFrame, col_n: str = "n", k: int = 5, marca=np.nan) -> pd.DataFrame:
    """Reemplaza por `marca` las filas de una tabla agregada con menos de k personas (evita re-identificar a individuos)."""
    t = tabla.copy(); peq = t[col_n] < k
    for c in t.columns:
        if c != col_n and pd.api.types.is_numeric_dtype(t[c]): t.loc[peq, c] = marca
    t["suprimida"] = peq; return t
