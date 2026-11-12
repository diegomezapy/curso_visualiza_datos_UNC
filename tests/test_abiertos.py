"""Pruebas de src/cvd/abiertos.py con datos sintéticos y respuestas simuladas.  python tests/test_abiertos.py"""
import sys, json
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd
from cvd import abiertos as A
E = RAIZ / "datos" / "ejemplos_abiertos"

# perfilado
df = pd.DataFrame({"id": [f"X{i}" for i in range(200)], "fecha": pd.date_range("2024-01-01", periods=200).astype(str), "monto": np.random.default_rng(1).lognormal(10, 1, 200),
                   "tipo": ["a", "b", "c", "d"] * 50, "lat": np.linspace(-27, -20, 200), "lon": np.linspace(-62, -54, 200), "vacia": [None] * 200, "nivel": [1, 2, 3, 4, 5] * 40})
p = A.perfilar(df).set_index("columna")["tipo"].to_dict()
assert p == {"id": "identificador/texto", "fecha": "fecha", "monto": "numérica", "tipo": "categórica", "lat": "latitud", "lon": "longitud", "vacia": "vacía", "nivel": "categórica"}, p
print("✔ perfilar: detecta numérica, categórica, fecha, id, lat/lon y columnas vacías")
q = A.calidad(pd.concat([df, df.iloc[:5]])); assert q["filas_duplicadas"] == 5 and q["columnas_vacías"] == ["vacia"]; print("✔ calidad: duplicados y columnas vacías")
import matplotlib; matplotlib.use("Agg"); figs = A.primer_vistazo(df, max_graficos=4); assert 1 <= len(figs) <= 4; print("✔ primer_vistazo genera", len(figs), "figuras")

# lectura de CSV con ; y latin-1
tmp = Path("/tmp/prueba_latin1.csv"); tmp.write_bytes("año;departamento;valor\n2024;Ñeembucú;3,5\n2023;Asunción;4,1\n".encode("latin-1")); t = A.leer_tabla(str(tmp))
assert t.shape == (2, 3) and "Ñeembucú" in t["departamento"].values; print("✔ leer_tabla: separador ; y codificación latin-1")

# OCDS
o = json.load(open(E / "ocds_ejemplo.json", encoding="utf-8")); T = A.ocds_a_tabla(o); assert len(T) == 420 and T["monto_estimado"].notna().all() and str(T["fecha"].dtype).startswith("datetime")
assert T["monto_adjudicado"].notna().sum() > 200; Adj = A.ocds_adjudicaciones(o); assert {"comprador", "proveedor", "monto"} <= set(Adj.columns) and len(Adj) > 250; print("✔ OCDS: 420 procesos →", len(Adj), "adjudicaciones")
assert len(A.ocds_a_tabla({"records": [{"compiledRelease": o["releases"][0]}]})) == 1 and len(A.ocds_a_tabla(o["releases"][0])) == 1 and A.ocds_a_tabla({"releases": []}).empty; print("✔ OCDS tolera records, un release suelto y vacío")
assert len(A.ocds_a_tabla({"releases": [{"ocid": "x"}]})) == 1; print("✔ OCDS tolera campos ausentes")

# Banco Mundial (respuesta simulada con la estructura documentada)
resp = [{"page": 1, "total": 3}, [{"indicator": {"id": "NE.EXP.GNFS.ZS", "value": "Exportaciones (% del PIB)"}, "country": {"id": "PY", "value": "Paraguay"}, "countryiso3code": "PRY", "date": "2023", "value": 33.1},
                                  {"indicator": {"id": "NE.EXP.GNFS.ZS", "value": "Exportaciones (% del PIB)"}, "country": {"id": "PY", "value": "Paraguay"}, "countryiso3code": "PRY", "date": "2024", "value": None},
                                  {"indicator": {"id": "NE.EXP.GNFS.ZS", "value": "Exportaciones (% del PIB)"}, "country": {"id": "AR", "value": "Argentina"}, "countryiso3code": "ARG", "date": "2023", "value": 17.0}]]
w = A.parsear_banco_mundial(resp); assert list(w.columns[:5]) == ["pais", "iso3", "anio", "valor", "indicador"] and len(w) == 3 and w.valor.isna().sum() == 1 and w.iso3.tolist() == ["ARG", "PRY", "PRY"]
assert A.parsear_banco_mundial([{"message": [{"id": "120"}]}]).empty; print("✔ Banco Mundial: parser de la estructura [meta, datos], tolera NA y errores")
try: A.descargar("http://127.0.0.1:9/inexistente", timeout=2); raise SystemExit("debía fallar")
except A.SinConexion: print("✔ descargar: sin conexión lanza SinConexion (los labs usan datos de ejemplo)")

# ponderación
x = np.array([1., 2., 3., 4.]); wt = np.array([1., 1., 1., 7.]); assert abs(A.media_ponderada(x, wt) - 3.4) < 1e-9; assert A.cuantil_ponderado(x, wt, .5) > 3; print("✔ media y mediana ponderadas")
ep = pd.read_csv(E / "ephc_demo.csv"); simple = ep.ingreso_laboral_gs.mean(); pond = A.media_ponderada(ep.ingreso_laboral_gs, ep.fex); assert abs(simple - pond) / pond > .03
assert abs(A.proporcion_ponderada(ep, "area", "fex").sum() - 1) < 1e-9 and A.proporcion_ponderada(ep, "area", "fex")["Urbana"] > .7; print(f"✔ ponderar cambia la conclusión: media simple {simple/1e6:.2f} M vs ponderada {pond/1e6:.2f} M; urbano {A.proporcion_ponderada(ep,'area','fex')['Urbana']:.0%} (no 50 %)")

# privacidad
pr = pd.DataFrame({"Nombre y Apellido": ["a"], "CI": [1], "teléfono": [2], "salario": [3], "entidad": ["x"], "ruc": ["r"]}); sin, quitadas = A.quitar_identificadores(pr)
assert set(quitadas) == {"Nombre y Apellido", "CI", "teléfono", "ruc"} and list(sin.columns) == ["salario", "entidad"]; print("✔ quitar_identificadores:", quitadas)
nm = pd.read_csv(E / "nomina_demo.csv"); g = nm.groupby("entidad").agg(n=("salario_gs", "size"), salario_medio=("salario_gs", "mean")).reset_index(); g.loc[0, "n"] = 3
s = A.suprimir_celdas_pequenas(g, "n", 5); assert s.loc[0, "suprimida"] and np.isnan(s.loc[0, "salario_medio"]) and not s.loc[1, "suprimida"]; print("✔ suprimir_celdas_pequenas: grupos con n < 5 ocultos")

# EPHC real (muestra de 3.000 filas del archivo REG02 2025 del INE)
assert A.url_ephc(2025, "REG02") == "https://www.ine.gov.py/microdatos/register/EPHC-ANUAL/EPHC_2025_ANUAL/REG02_EPHC_ANUAL_2025.csv"
r = A.leer_ephc(str(E / "ephc_2025_muestra.csv"), numericas=["FACTOR", "e01aimde", "añoest", "P02", "AREA", "P06", "PEAA"]); assert len(r) == 3000 and r["FACTOR"].notna().all() and r["e01aimde"].dtype.kind == "f"
oc = r[(r.PEAA == 1) & (r.e01aimde > 0)]; assert len(oc) > 500 and A.media_ponderada(oc.e01aimde, oc.FACTOR) != oc.e01aimde.mean(); print(f"✔ EPHC real (muestra): {len(r)} filas, {len(oc)} ocupados con ingreso; coma decimal y blancos convertidos")
assert abs(A.a_numerico(pd.Series(["4917667,813", " ", "12", None])).fillna(-1).tolist()[0] - 4917667.813) < 1e-6 and A.a_numerico(pd.Series([" "])).isna().all(); print("✔ a_numerico: coma decimal y espacios")
# DNIT
html = '<a href="/documents/20123/3872761/5.+Recaudaci%C3%B3n_Por_Impuesto_Departamento_Distrito_Actividad_Economica_2025.xlsx/ba8c07fb?t=17925" download>Descargar</a><a href="/documents/x/Departamento_Distrito_Actividad_Economica_2024.xlsx/aa?t=1">d</a>'
u = A.buscar_url_dnit_recaudacion(2025, html); assert u.startswith("https://www.dnit.gov.py/documents/") and "2025.xlsx" in u and "?t=17925" in u
try: A.buscar_url_dnit_recaudacion(2019, html); raise SystemExit("debía fallar")
except A.SinConexion: pass
print("✔ buscar_url_dnit_recaudacion: encuentra el enlace del año aunque cambie el identificador")
dm = pd.read_csv(E / "dnit_recaudacion_2025_muestra.csv"); sucio = pd.concat([dm, pd.DataFrame({"Mes": ["Tributos Internos:", None], "Recaudacion": [None, None]})], ignore_index=True); sucio["Año"] = sucio["Año"].astype(object)
L = A.limpiar_recaudacion(sucio); assert len(L) == len(dm) and L["fecha"].min().month == 1 and L["Año"].dtype.name == "Int64" and (L["Recaudacion"] > 0).all(); print(f"✔ limpiar_recaudacion: elimina notas al pie ({len(sucio)-len(L)} filas) y crea fecha")
import zipfile, io
b = io.BytesIO(); z = zipfile.ZipFile(b, "w"); z.writestr("datos.csv", "a,b\n1,2\n3,4\n"); z.close(); Path("/tmp/prueba.zip").write_bytes(b.getvalue()); assert A.leer_tabla("/tmp/prueba.zip").shape == (2, 2); print("✔ leer_tabla: archivos ZIP")
print("\nTodas las pruebas de abiertos.py pasaron.")
