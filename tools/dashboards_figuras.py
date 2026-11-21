"""Ejecuta el código REAL de cada figura (dashboards_spec.py) y guarda PNG en aula/media/unidad5_dashboards/fuentes/figuras/ y los HTML interactivos.
Uso: python tools/dashboards_figuras.py   (requiere pandas, plotly y kaleido; datos: tools/dashboards_datos.py)"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import dashboards_spec as S
import pandas as pd
RAIZ = Path(__file__).resolve().parents[1]; M = RAIZ / "aula" / "media" / "unidad5_dashboards"; F = M / "fuentes"
(F / "figuras").mkdir(exist_ok=True); (F / "pasos").mkdir(exist_ok=True)
sin = lambda ls: [l[1:] if l.startswith("§") else l for l in ls]
(F / "pasos" / "00_setup.py").write_text("\n".join(S.SETUP) + "\n", encoding="utf-8")
for f in S.FIGS: (F / "pasos" / f"{f['id']}.py").write_text("\n".join(sin(f["codigo"])) + "\n", encoding="utf-8")
os.chdir(F / "datos")
env = {}
exec("\n".join(S.SETUP), env)
env["sub"] = pd.read_csv("subitems_muestra.csv")
import plotly.io as pio
pio.templates["plotly_white"].layout.font.size = 14
for f in S.FIGS:
    exec("\n".join(sin(f["codigo"])), env)
    fig = env["fig"]
    fig.update_layout(margin=dict(l=60, r=30, t=70, b=50), font_size=14)
    fig.write_image(str(F / "figuras" / f"{f['id']}.png"), width=960, height=585, scale=2)
    if f["id"] in ("i1", "d1"):
        fig.write_html(str(M / f"tablero_{f['id']}.html"), include_plotlyjs="cdn", full_html=True)
    print("✔", f["id"])
