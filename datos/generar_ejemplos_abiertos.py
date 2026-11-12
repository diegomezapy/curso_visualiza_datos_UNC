"""Genera datos SINTÉTICOS (no reales) con la misma estructura que algunas fuentes abiertas, para practicar y probar sin conexión:
  - ocds_ejemplo.json : procesos de compra en formato OCDS estándar (entidades y proveedores ficticios)
  - ephc_demo.csv     : encuesta con factor de expansión y sobremuestreo rural (demostración de ponderación)
  - nomina_demo.csv   : plantilla de personal SIN nombres ni documentos
Uso: python datos/generar_ejemplos_abiertos.py"""
import json, datetime as dt
from pathlib import Path
import numpy as np, pandas as pd
out = Path(__file__).parent / "ejemplos_abiertos"; out.mkdir(exist_ok=True); rng = np.random.default_rng(2026)

compradores = [f"Entidad compradora {chr(65+i)}" for i in range(12)]; proveedores = [f"Proveedor {i:03d}" for i in range(1, 61)]
metodos = ["Licitación Pública Nacional", "Contratación Directa", "Concurso de Ofertas", "Licitación por Concurso de Ofertas"]; cats = ["goods", "services", "works"]
pesoC = rng.dirichlet(np.ones(12) * 0.6); pesoP = rng.dirichlet(np.ones(60) * 0.35); rel = []
for i in range(420):
    c = rng.choice(12, p=pesoC); f = dt.datetime(2024, 1, 1) + dt.timedelta(days=int(rng.integers(0, 700)), hours=int(rng.integers(0, 24)))
    monto = float(np.round(np.exp(rng.normal(19.3, 1.6)), -3)); est = rng.choice(["complete", "active", "cancelled", "unsuccessful"], p=[.62, .14, .14, .10])
    r = {"ocid": f"ocds-demo-{i:05d}", "id": f"{i:05d}-1", "date": f.isoformat() + "Z", "tag": ["tender"], "buyer": {"id": f"E{c:02d}", "name": compradores[c]},
         "tender": {"id": f"T{i:05d}", "title": f"Proceso de ejemplo {i:05d}", "status": est, "procurementMethodDetails": str(rng.choice(metodos, p=[.3, .2, .3, .2])),
                    "mainProcurementCategory": str(rng.choice(cats, p=[.5, .35, .15])), "value": {"amount": monto, "currency": "PYG"}, "numberOfTenderers": int(rng.integers(1, 9)),
                    "tenderPeriod": {"startDate": f.isoformat() + "Z"}}, "awards": []}
    if est in ("complete", "active"):
        for _ in range(int(rng.choice([1, 1, 1, 2]))):
            p = rng.choice(60, p=pesoP)
            r["awards"].append({"id": f"A{i}", "date": (f + dt.timedelta(days=20)).isoformat() + "Z", "value": {"amount": float(np.round(monto * rng.uniform(.7, 1.05), -3)), "currency": "PYG"}, "suppliers": [{"id": f"P{p:03d}", "name": proveedores[p]}]})
    rel.append(r)
json.dump({"uri": "SINTETICO", "publisher": {"name": "Datos sintéticos del curso (NO son reales)"}, "releases": rel}, open(out / "ocds_ejemplo.json", "w", encoding="utf-8"), ensure_ascii=False)

n = 3000; area = rng.choice(["Urbana", "Rural"], n, p=[.5, .5]); dep = rng.choice(["Asunción", "Central", "Alto Paraná", "Itapúa", "San Pedro", "Caaguazú", "Concepción", "Canindeyú"], n)
sexo = rng.choice(["Mujer", "Hombre"], n); edad = np.clip(rng.normal(36, 16, n), 15, 80).round().astype(int); esc = np.clip(rng.normal(np.where(area == "Urbana", 11, 7.5), 3.2, n), 0, 18).round(1)
ing = np.exp(rng.normal(np.where(area == "Urbana", 14.9, 14.3) + 0.07 * (esc - 9) + np.where(sexo == "Mujer", -0.18, 0), 0.55, n)).round(-3)
fex = np.where(area == "Urbana", rng.uniform(320, 520, n), rng.uniform(90, 160, n)).round(1)
pd.DataFrame({"departamento": dep, "area": area, "sexo": sexo, "edad": edad, "anios_estudio": esc, "ingreso_laboral_gs": ing, "fex": fex}).to_csv(out / "ephc_demo.csv", index=False)

m = 4000; ent = rng.choice([f"Entidad {i:02d}" for i in range(1, 26)], m, p=rng.dirichlet(np.ones(25) * .7)); cat = rng.choice(["Permanente", "Contratado"], m, p=[.62, .38]); sx = rng.choice(["Mujer", "Hombre"], m, p=[.54, .46])
niv = rng.choice(["Operativo", "Técnico", "Profesional", "Directivo"], m, p=[.3, .3, .32, .08]); base = np.select([niv == "Operativo", niv == "Técnico", niv == "Profesional"], [3.2e6, 4.5e6, 7.5e6], 13e6)
sal = (base * np.exp(rng.normal(0, .25, m)) * np.where(sx == "Mujer", .94, 1)).round(-4)
pd.DataFrame({"entidad": ent, "categoria": cat, "nivel": niv, "sexo": sx, "salario_gs": sal, "antiguedad_anios": np.clip(rng.gamma(3, 3, m), 0, 40).round(1)}).to_csv(out / "nomina_demo.csv", index=False)
print("ejemplos sintéticos generados en", out)
