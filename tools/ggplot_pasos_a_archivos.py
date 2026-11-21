"""Escribe el código de cada paso (sin marcas) en aula/media/unidad2_ggplot/fuentes/pasos/*.R para que R lo ejecute."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ggplot_spec as S
PASOS = Path(__file__).resolve().parents[1] / "aula" / "media" / "unidad2_ggplot" / "fuentes" / "pasos"
PASOS.mkdir(parents=True, exist_ok=True)
for p in S.PASOS: (PASOS / f"{p['id']}.R").write_text("\n".join(S.sin_marcas(p["codigo"])) + "\n", encoding="utf-8")
for k, c in S.EXTRA.items(): (PASOS / f"{k}.R").write_text("\n".join(S.sin_marcas(c)) + "\n", encoding="utf-8")
print(len(list(PASOS.glob("*.R"))), "archivos de pasos")
