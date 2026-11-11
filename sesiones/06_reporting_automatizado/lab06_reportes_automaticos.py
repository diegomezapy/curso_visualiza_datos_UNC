# %% [markdown]
# # Lab 6 · Reporting automatizado
# Idea: **un reporte = plantilla + datos + parámetros**. Generamos un informe HTML por sucursal con `jinja2`, sin tocar nada a mano.
# %%
import sys
from pathlib import Path
RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())
sys.path.insert(0, str(RAIZ / "src"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from cvd import estilo, datos
estilo.aplicar_tema()

import base64, io, datetime as dt
from jinja2 import Template
v = datos.ventas(); v["mes"] = v.fecha.dt.to_period("M").dt.to_timestamp(); v["anio"] = v.fecha.dt.year

# %% [markdown]
# ## 1. Función que convierte una figura en imagen embebida (HTML autocontenido)

# %%
def fig_a_base64(fig):
    buf = io.BytesIO(); fig.savefig(buf, format="png", bbox_inches="tight", dpi=130); plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

# %% [markdown]
# ## 2. Plantilla

# %%
PLANTILLA = Template("""<!doctype html><html lang="es"><meta charset="utf-8">
<title>Informe {{ sucursal }}</title>
<style>body{font-family:system-ui,sans-serif;max-width:820px;margin:2rem auto;color:#222}
.kpis{display:flex;gap:1rem}.kpi{flex:1;border:1px solid #ddd;border-radius:8px;padding:.8rem}
.kpi b{font-size:1.6rem;display:block}.up{color:#009E73}.down{color:#D55E00}small{color:#777}</style>
<h1>Informe comercial · {{ sucursal }}</h1>
<p><small>Generado {{ fecha }} · Fuente: ventas_retail (sintético)</small></p>
<div class="kpis">{% for k in kpis %}
<div class="kpi">{{ k.nombre }}<b>{{ k.valor }}</b><span class="{{ 'up' if k.delta>=0 else 'down' }}">{{ '▲' if k.delta>=0 else '▼' }} {{ '%.1f'|format(k.delta|abs) }}% vs {{ anio_prev }}</span></div>{% endfor %}</div>
<h2>{{ titulo }}</h2><img src="data:image/png;base64,{{ img }}" style="width:100%">
<h2>Detalle por categoría</h2>{{ tabla|safe }}
<p><small>Nota: valores en millones de Gs. Margen = (ventas−costo)/ventas.</small></p></html>""")

# %% [markdown]
# ## 3. Generador parametrizado

# %%
def reporte(sucursal, anio=2025):
    d = v[v.sucursal == sucursal]; a, p = d[d.anio == anio], d[d.anio == anio - 1]
    f = lambda x, col: x[col].sum()
    kp = [("Ventas (MM Gs.)", f(a, "ventas_gs_miles") / 1e3, f(p, "ventas_gs_miles") / 1e3),
          ("Unidades", f(a, "unidades"), f(p, "unidades"))]
    kpis = [dict(nombre=n, valor=f"{x:,.0f}", delta=(x / y - 1) * 100) for n, x, y in kp]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    for an, col in [(anio - 1, estilo.GRIS), (anio, estilo.ENFASIS)]:
        s = d[d.anio == an].groupby(d.mes.dt.month).ventas_gs_miles.sum() / 1e3
        ax.plot(s.index, s.values, color=col, lw=2.2, label=str(an))
    ax.set_xticks(range(1, 13)); ax.legend(); ax.set_xlabel("Mes"); ax.set_ylabel("MM Gs.")
    tabla = (a.groupby("categoria").agg(ventas=("ventas_gs_miles", lambda s: s.sum() / 1e3),
             margen=("ventas_gs_miles", "sum"), costo=("costo_gs_miles", "sum")))
    tabla["margen_%"] = (1 - tabla.costo / tabla.margen) * 100
    tabla = tabla[["ventas", "margen_%"]].round(1).sort_values("ventas", ascending=False)
    crec = kpis[0]["delta"]
    titulo = f"Las ventas {'crecieron' if crec >= 0 else 'cayeron'} {abs(crec):.1f}% en {anio}"
    return PLANTILLA.render(sucursal=sucursal, fecha=dt.date.today().isoformat(), kpis=kpis, anio_prev=anio - 1,
                            titulo=titulo, img=fig_a_base64(fig), tabla=tabla.to_html(classes="t"))

# %%
for s in v.sucursal.unique():
    ruta = estilo.salida(f"informe_{s.replace(' ', '_')}.html"); ruta.write_text(reporte(s), encoding="utf-8"); print("→", ruta.name)

# %% [markdown]
# ## 4. Pipeline reproducible
# - **Script**: `python tools/generar_reportes.py` (programable con `cron` / GitHub Actions).
# - **Notebook parametrizado**: `papermill nb.ipynb out.ipynb -p sucursal "Asunción"`.
# - **Quarto** (opcional): `quarto render informe.qmd -P sucursal:Asunción` → HTML/PDF/Word.
#
# ## 5. Ejercicio
# Agregá al informe (a) una alerta automática si el margen cae > 2 pp, (b) un gráfico de contribución por categoría, y (c) generá un PDF (`weasyprint` o imprimir desde navegador).
