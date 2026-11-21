"""Maquetas (con datos REALES del CAN 2022) de los gráficos del informe de Looker Studio. No son capturas de Looker: muestran qué se construye en cada paso.
Uso: python tools/looker_figuras.py   (datos: python tools/can_datos.py <Volumen I>)"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
RAIZ = Path(__file__).resolve().parents[1]; M = RAIZ / "aula" / "media" / "unidad5_looker" / "fuentes"; OUT = M / "figuras"; OUT.mkdir(exist_ok=True)
d = pd.read_csv(M / "datos" / "can2022_departamentos.csv"); e = pd.read_csv(M / "datos" / "can2022_estratos.csv")
coord = pd.read_csv(RAIZ / "datos" / "departamentos_py.csv")[["departamento", "lat", "lon"]]
d = d.merge(coord, on="departamento", how="left")
AZ, NA, GR, VE, OSC = "#4285F4", "#D55E00", "#9AA0A6", "#0F9D58", "#202124"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#DADCE0", "axes.titleweight": "bold", "axes.titlesize": 12.5, "axes.titlelocation": "left"})
W, H = 6.4, 3.9
def guardar(fig, n): fig.savefig(OUT / f"{n}.png", dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
mill = lambda x: f"{x:,.0f}".replace(",", ".")

# F1 · tarjetas de resultados (scorecards)
fig, ax = plt.subplots(figsize=(W, H)); ax.axis("off"); ax.set_xlim(0, 2); ax.set_ylim(0, 2)
tarjetas = [("Fincas agropecuarias", mill(d.fincas_2022.sum()), "+0,6 % vs. 2008", VE), ("Superficie de fincas (ha)", f"{d.superficie_2022_ha.sum()/1e6:.1f} M".replace(".", ","), "−2,2 % vs. 2008", NA),
            ("Cabezas de ganado vacuno", f"{d.vacunos_cabezas.sum()/1e6:.1f} M".replace(".", ","), "+26,0 % vs. 2008", VE), ("Productoras mujeres", f"{100*d.productores_mujeres.sum()/d.productores_residentes.sum():.1f} %".replace(".", ","), "de los productores residentes", GR)]
for i, (t, v, s, c) in enumerate(tarjetas):
    x, y = (i % 2), 1 - (i // 2)
    ax.add_patch(FancyBboxPatch((x + .04, y + .06), .92, .84, boxstyle="round,pad=0.01,rounding_size=0.04", fc="white", ec="#DADCE0", lw=1.2))
    ax.text(x + .1, y + .76, t, fontsize=11, color="#5F6368", va="center"); ax.text(x + .1, y + .46, v, fontsize=28, fontweight="bold", color=OSC, va="center"); ax.text(x + .1, y + .19, s, fontsize=10.5, color=c, va="center", fontweight="bold")
ax.set_title("CAN 2022 · Paraguay", loc="left", y=1.0)
guardar(fig, "l1")

# F2 · burbujas sobre coordenadas (el mapa de Looker usa el código ISO del departamento)
fig, ax = plt.subplots(figsize=(W, H))
colores = np.where(d.region == "Oriental", AZ, "#F29900")
ax.scatter(d.lon, d.lat, s=d.superficie_2022_ha / 1e6 * 330, c=colores, alpha=.55, edgecolor="white", lw=1)
for _, r in d.iterrows():
    if r.departamento in ("Presidente Hayes", "Boquerón", "Alto Paraguay", "Concepción", "Itapúa", "San Pedro", "Alto Paraná"): ax.annotate(r.departamento, (r.lon, r.lat), fontsize=8, ha="center", va="center", color=OSC, xytext=(0, -3 if r.departamento != "Concepción" else 14), textcoords="offset points")
ax.margins(.18); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.spines[:].set_visible(False)
ax.set_title("Superficie de fincas por departamento (ha)")
ax.text(.5, -.04, "azul: Región Oriental · naranja: Occidental · área ∝ hectáreas", transform=ax.transAxes, fontsize=8.5, color="#5F6368", ha="center")
guardar(fig, "l2")

# F3 · ranking de superficie
fig, ax = plt.subplots(figsize=(W, H)); s = d.sort_values("superficie_2022_ha")
ax.barh(s.departamento, s.superficie_2022_ha / 1e6, color=[NA if x == "Concepción" else AZ for x in s.departamento])
ax.set_xlabel("Millones de hectáreas"); ax.set_title("Superficie de fincas por departamento, 2022"); ax.tick_params(axis="y", labelsize=9)
for y, v in enumerate(s.superficie_2022_ha / 1e6): ax.text(v + .05, y, f"{v:.1f}".replace(".", ","), va="center", fontsize=8.5, color="#5F6368")
guardar(fig, "l3")

# F4 · variación de fincas 2008–2022
fig, ax = plt.subplots(figsize=(W, H)); s = d.sort_values("var_fincas_pct")
ax.barh(s.departamento, s.var_fincas_pct, color=[AZ if v >= 0 else NA for v in s.var_fincas_pct]); ax.axvline(0, color="#5F6368", lw=.8)
ax.set_xlabel("Variación de la cantidad de fincas, 2008 → 2022 (%)"); ax.set_title("¿Dónde crecieron y dónde cayeron las fincas?"); ax.tick_params(axis="y", labelsize=9)
guardar(fig, "l4")

# F5 · concentración de la tierra
fig, ax = plt.subplots(figsize=(W, H)); x = np.arange(len(e)); w = .4
etiq = ["<1", "1–5", "5–10", "10–20", "20–50", "50–100", "100–200", "200–500", "500–1.000", "1.000–5.000", "5.000–10.000", "≥10.000"]
ax.bar(x - w / 2, e.pct_fincas_2022, w, color=AZ, label="% de las fincas"); ax.bar(x + w / 2, e.pct_superficie_2022, w, color=NA, label="% de la superficie")
ax.set_xticks(x); ax.set_xticklabels(etiq, rotation=40, ha="right", fontsize=8.5); ax.set_xlabel("Tamaño de finca (ha)"); ax.set_ylabel("%"); ax.legend(frameon=False, fontsize=9.5)
ax.set_title("Pocas fincas muy grandes concentran la tierra")
guardar(fig, "l5")

# F6 · uso de la tierra: Paraguay vs Concepción
cols = [("sup_cultivos_temporales_ha", "Cultivos temporales", AZ), ("sup_cultivos_permanentes_ha", "Cultivos permanentes", "#0B5394"), ("sup_pastura_natural_ha", "Pastura natural", "#34A853"), ("sup_pastura_cultivada_ha", "Pastura cultivada", "#A8D5A2"), ("sup_montes_naturales_ha", "Montes naturales", "#7F6000"), ("sup_forestales_plantados_ha", "Forestales plantados", "#F9AB00")]
tot = d[[c for c, _, _ in cols]].sum(); con = d[d.departamento == "Concepción"][[c for c, _, _ in cols]].iloc[0]
fig, ax = plt.subplots(figsize=(W, H)); izq = np.zeros(2)
for c, n, col in cols:
    v = np.array([100 * tot[c] / tot.sum(), 100 * con[c] / con.sum()]); ax.barh(["Paraguay", "Concepción"], v, left=izq, color=col, label=n)
    for i, (a, b) in enumerate(zip(izq, v)):
        if b > 6: ax.text(a + b / 2, i, f"{b:.0f} %", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    izq += v
ax.set_xlim(0, 100); ax.set_xlabel("% de la superficie con estos usos"); ax.legend(ncol=3, frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(.5, -.2)); ax.set_title("Uso de la tierra en las fincas, 2022")
guardar(fig, "l6")

# F7 · informe completo (maqueta)
fig = plt.figure(figsize=(W * 1.15, H * 1.15)); gs = fig.add_gridspec(3, 4, height_ratios=[.55, 1.5, .08], hspace=.45, wspace=.55)
fig.suptitle("Censo Agropecuario Nacional 2022 · MAG", x=.02, ha="left", fontsize=13, fontweight="bold")
fig.text(.62, .93, "Región: Todas ▾   Departamento: Todos ▾", fontsize=9, color="#5F6368", bbox=dict(boxstyle="round,pad=.3", fc="#F1F3F4", ec="#DADCE0"))
for i, (t, v, s_, c) in enumerate(tarjetas):
    a = fig.add_subplot(gs[0, i]); a.axis("off"); a.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.0,rounding_size=0.06", fc="white", ec="#DADCE0", transform=a.transAxes, clip_on=False))
    a.text(.06, .76, t, fontsize=7.5, color="#5F6368", transform=a.transAxes); a.text(.06, .38, v, fontsize=16, fontweight="bold", color=OSC, transform=a.transAxes); a.text(.06, .1, s_, fontsize=7, color=c, transform=a.transAxes)
a = fig.add_subplot(gs[1, :2]); a.scatter(d.lon, d.lat, s=d.superficie_2022_ha / 1e6 * 150, c=colores, alpha=.55, edgecolor="white"); a.margins(.15); a.set_aspect("equal"); a.axis("off"); a.set_title("Superficie por departamento", fontsize=10)
a = fig.add_subplot(gs[1, 2:]); s = d.sort_values("fincas_2022").tail(8); a.barh(s.departamento, s.fincas_2022 / 1e3, color=[NA if x == "Concepción" else AZ for x in s.departamento]); a.set_title("Fincas (miles) · 8 mayores", fontsize=10); a.tick_params(labelsize=8)
guardar(fig, "l7")
print("figuras:", sorted(p.name for p in OUT.glob("l*.png")))
