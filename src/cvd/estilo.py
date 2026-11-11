"""Estilo visual común: paleta accesible (Okabe-Ito) y helpers de matplotlib/plotly."""
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt

# Paleta Okabe-Ito: segura para daltonismo
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00",
             "#CC79A7", "#56B4E9", "#F0E442", "#000000"]
GRIS = "#8C8C8C"
GRIS_CLARO = "#D9D9D9"
ENFASIS = "#D55E00"   # color de resalte
BASE = "#0072B2"

def raiz_proyecto() -> Path:
    """Sube desde el directorio actual hasta encontrar la carpeta `datos/`."""
    return next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos").is_dir())

def salida(nombre: str) -> Path:
    """Ruta dentro de `salidas/` (se crea si no existe)."""
    d = raiz_proyecto() / "salidas"
    d.mkdir(exist_ok=True)
    return d / nombre

def aplicar_tema():
    """Tema limpio para matplotlib: poca tinta, sin marcos innecesarios."""
    mpl.rcParams.update({
        "figure.figsize": (8, 4.5), "figure.dpi": 110,
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.labelsize": 11, "axes.grid": True, "grid.color": "#EAEAEA",
        "grid.linewidth": 0.8, "axes.axisbelow": True,
        "font.size": 11, "legend.frameon": False,
    })

def guardar(fig, nombre: str):
    ruta = salida(nombre)
    fig.savefig(ruta, bbox_inches="tight", dpi=150)
    print("guardado:", ruta)
    return ruta

PLOTLY_TEMPLATE = "simple_white"
