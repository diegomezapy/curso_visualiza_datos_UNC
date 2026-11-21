"""Extrae del «VOLUMEN I - CAN 2022» (MAG, Censo Agropecuario Nacional 2022) las tablas por departamento que usa la presentación de Looker Studio.
Entrada: el Excel oficial (hojas «Cuadro N»). Salida: aula/media/unidad5_looker/fuentes/datos/can2022_departamentos.csv y can2022_estratos.csv
Uso: python tools/can_datos.py <VOLUMEN I - CAN 2022 _final.xlsx>"""
import re, sys
from pathlib import Path
import openpyxl, pandas as pd
RAIZ = Path(__file__).resolve().parents[1]; OUT = RAIZ / "aula" / "media" / "unidad5_looker" / "fuentes" / "datos"; OUT.mkdir(parents=True, exist_ok=True)
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
def num(x):
    if isinstance(x, (int, float)): return float(x)
    s = str(x).strip().replace(".", "").replace(",", ".") if isinstance(x, str) else ""
    try: return float(s)
    except ValueError: return None
def filas(hoja):
    """Filas de la hoja sin celdas vacías (el censo deja columnas en blanco entre bloques)."""
    for r in wb[hoja].iter_rows(values_only=True):
        v = [c for c in r if c not in (None, "")]
        if v: yield v
def deptos(hoja):
    out = {}
    for v in filas(hoja):
        m = re.match(r"^(\d{2})\.\s*(.+)$", str(v[0]).strip())
        if m: out[m.group(1)] = (m.group(2).strip(), v[1:])
    return out
ISO = {"00": "PY-ASU", "01": "PY-1", "02": "PY-2", "03": "PY-3", "04": "PY-4", "05": "PY-5", "06": "PY-6", "07": "PY-7", "08": "PY-8", "09": "PY-9", "10": "PY-10",
       "11": "PY-11", "12": "PY-12", "13": "PY-13", "14": "PY-14", "15": "PY-15", "16": "PY-19", "17": "PY-16"}   # códigos del CAN → ISO 3166-2
titulo = lambda s: " ".join(w.capitalize() if w.lower() not in ("de",) else w.lower() for w in s.lower().split())
c1, c19, c27, c52, c5 = deptos("Cuadro 1"), deptos("Cuadro 19"), deptos("Cuadro 27"), deptos("Cuadro 52"), deptos("Cuadro 5")
filas_out = []
for cod, (nombre, v) in c1.items():
    def n(tab, i):   # celda ausente = el censo no registra fincas con ese cultivo en el departamento → 0
        v = tab[cod][1] if cod in tab else []
        return num(v[i]) if i < len(v) else 0.0
    filas_out.append(dict(
        dpto_cod=cod, departamento=titulo(nombre).replace("Ñ", "ñ") if False else titulo(nombre), iso_3166_2=ISO[cod], region="Oriental" if int(cod) <= 14 else "Occidental",
        fincas_2008=num(v[0]), superficie_2008_ha=num(v[1]), fincas_2022=num(v[2]), superficie_2022_ha=num(v[3]), var_fincas_pct=num(v[4]), var_superficie_pct=num(v[5]),
        superficie_promedio_2022_ha=num(v[7]),
        sup_cultivos_temporales_ha=n(c19, 3), sup_cultivos_permanentes_ha=n(c19, 5), sup_pastura_natural_ha=n(c19, 8), sup_pastura_cultivada_ha=n(c19, 10),
        sup_montes_naturales_ha=n(c19, 12), sup_forestales_plantados_ha=n(c19, 15),
        soja_fincas=n(c27, 1), soja_sup_ha=n(c27, 2), soja_produccion_tn=n(c27, 4),
        vacunos_fincas=n(c52, 1), vacunos_cabezas=n(c52, 2),
        productores_residentes=n(c5, 2), productores_hombres=n(c5, 3), productores_mujeres=n(c5, 4)))
df = pd.DataFrame(filas_out)
df["pct_superficie_2022"] = (100 * df.superficie_2022_ha / df.superficie_2022_ha.sum()).round(2)
df["pct_productoras_mujeres"] = (100 * df.productores_mujeres / df.productores_residentes).round(1)
df["vacunos_por_100_ha"] = (100 * df.vacunos_cabezas / df.superficie_2022_ha).round(1)
df.to_csv(OUT / "can2022_departamentos.csv", index=False)
# estratos de tamaño (total país), cuadro 1
est = []
for v in filas("Cuadro 1"):
    t = str(v[0]); 
    if re.match(r"^(Menos de|De\s)", t) and len(v) >= 9: est.append(dict(estrato=re.sub(r"\s+", " ", t).strip(), fincas_2008=num(v[1]), superficie_2008_ha=num(v[2]), fincas_2022=num(v[3]), superficie_2022_ha=num(v[4])))
e = pd.DataFrame(est); e["pct_fincas_2022"] = (100 * e.fincas_2022 / e.fincas_2022.sum()).round(2); e["pct_superficie_2022"] = (100 * e.superficie_2022_ha / e.superficie_2022_ha.sum()).round(2)
e.insert(0, "orden", range(1, len(e) + 1)); e.to_csv(OUT / "can2022_estratos.csv", index=False)
print(len(df), "departamentos; fincas 2022:", int(df.fincas_2022.sum()), "| sup 2022:", round(df.superficie_2022_ha.sum(), 1), "ha")
print(df[["departamento", "iso_3166_2", "fincas_2022", "superficie_2022_ha", "soja_sup_ha", "vacunos_cabezas", "productores_mujeres"]].to_string())
print(e.to_string())
