"""Genera los datasets sintéticos del curso (semilla fija => reproducible).
Uso:  python datos/generar_datos.py
"""
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).parent
rng = np.random.default_rng(2026)

# --- 1. Ventas retail (2 años, 5 sucursales, 4 categorías) -------------------
fechas = pd.date_range("2024-01-01", "2025-12-31", freq="D")
sucursales = {"Asunción": 1.5, "Ciudad del Este": 1.3, "Encarnación": 0.9,
              "Concepción": 0.6, "Pedro Juan Caballero": 0.5}
categorias = {"Electrónica": (900, 0.22), "Hogar": (400, 0.30),
              "Indumentaria": (250, 0.45), "Alimentos": (120, 0.18)}  # ticket, margen
filas = []
for f in fechas:
    estac = 1 + 0.25 * np.sin(2 * np.pi * (f.day_of_year - 330) / 365) + (0.5 if f.month == 12 else 0)
    finde = 1.2 if f.day_of_week >= 5 else 1.0
    tendencia = 1 + 0.15 * (f - fechas[0]).days / len(fechas)
    for s, w in sucursales.items():
        for c, (ticket, margen) in categorias.items():
            u = rng.poisson(max(1, 6 * w * estac * finde * tendencia))
            precio = ticket * rng.normal(1, 0.08)
            ventas = u * precio
            filas.append((f, s, c, u, round(ventas, 2), round(ventas * (1 - margen * rng.normal(1, 0.1)), 2)))
pd.DataFrame(filas, columns=["fecha", "sucursal", "categoria", "unidades", "ventas_gs_miles", "costo_gs_miles"]
             ).to_csv(AQUI / "ventas_retail.csv", index=False)

# --- 2. Notas de estudiantes (distribuciones, relaciones) ---------------------
n = 400
horas = rng.gamma(4, 2.5, n).clip(0, 40)
asist = np.clip(rng.normal(80, 12, n), 30, 100)
nota = np.clip(35 + 1.4 * horas + 0.25 * asist + rng.normal(0, 8, n), 0, 100)
pd.DataFrame({"estudiante": range(1, n + 1),
              "carrera": rng.choice(["Ingeniería", "Ciencias", "Informática"], n, p=[.4, .25, .35]),
              "horas_estudio_sem": horas.round(1), "asistencia_pct": asist.round(1),
              "nota_final": nota.round(1)}).to_csv(AQUI / "notas_estudiantes.csv", index=False)

# --- 3. Departamentos de Paraguay (coordenadas aprox. + indicador SINTÉTICO) --
deps = [("Asunción", -25.28, -57.63), ("Concepción", -23.40, -57.43), ("San Pedro", -24.10, -56.45),
        ("Cordillera", -25.20, -56.97), ("Guairá", -25.88, -56.23), ("Caaguazú", -25.45, -55.67),
        ("Caazapá", -26.20, -56.37), ("Itapúa", -26.90, -55.50), ("Misiones", -26.85, -57.10),
        ("Paraguarí", -25.90, -57.00), ("Alto Paraná", -25.45, -54.80), ("Central", -25.40, -57.35),
        ("Ñeembucú", -26.85, -58.00), ("Amambay", -23.00, -56.00), ("Canindeyú", -24.10, -55.20),
        ("Presidente Hayes", -24.00, -58.50), ("Boquerón", -22.00, -60.50), ("Alto Paraguay", -20.50, -58.50)]
d = pd.DataFrame(deps, columns=["departamento", "lat", "lon"])
d["poblacion_miles"] = (rng.lognormal(5.2, 0.8, len(d))).round(0)
d.loc[d.departamento == "Central", "poblacion_miles"] = 2200
d.loc[d.departamento == "Asunción", "poblacion_miles"] = 520
d["indice_acceso_internet"] = np.clip(rng.normal(55, 15, len(d)), 15, 95).round(1)
d.to_csv(AQUI / "departamentos_py.csv", index=False)

# --- 4. Cuarteto de Anscombe ---------------------------------------------------
x123 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
a = pd.concat([
    pd.DataFrame({"dataset": "I", "x": x123, "y": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]}),
    pd.DataFrame({"dataset": "II", "x": x123, "y": [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]}),
    pd.DataFrame({"dataset": "III", "x": x123, "y": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]}),
    pd.DataFrame({"dataset": "IV", "x": [8]*7 + [19] + [8]*3, "y": [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]}),
])
a.to_csv(AQUI / "anscombe.csv", index=False)

# --- 5. Demanda diaria de energía (serie con tendencia + estacionalidades) -----
dias = pd.date_range("2022-01-01", "2025-12-31", freq="D")
t = np.arange(len(dias))
y = np.asarray(1000 + 0.12 * t + 180 * np.sin(2 * np.pi * (dias.day_of_year - 20) / 365)
     - 90 * (dias.day_of_week >= 5) + rng.normal(0, 40, len(t)), dtype=float)
y[rng.choice(len(t), 8, replace=False)] += rng.choice([-300, 350], 8)   # anomalías
pd.DataFrame({"fecha": dias, "demanda_mwh": y.round(1)}).to_csv(AQUI / "demanda_energia.csv", index=False)
print("Datasets generados en", AQUI)
