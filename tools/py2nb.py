"""Convierte los laboratorios en formato percent (# %%) a notebooks .ipynb.
Uso: python tools/py2nb.py            # todos los labs en sesiones/*/lab*.py
"""
from pathlib import Path
import re, nbformat as nbf

RAIZ = Path(__file__).resolve().parents[1]
for py in sorted(RAIZ.glob("sesiones/*/lab*.py")):
    nb, cell = nbf.v4.new_notebook(), None
    bloques = re.split(r"^# %%", py.read_text(encoding="utf-8"), flags=re.M)
    for b in bloques:
        if not b.strip():
            continue
        if b.lstrip().startswith("[markdown]"):
            cuerpo = b.split("\n", 1)[1] if "\n" in b else ""
            md = "\n".join(re.sub(r"^# ?", "", l) for l in cuerpo.strip("\n").split("\n"))
            nb.cells.append(nbf.v4.new_markdown_cell(md))
        else:
            nb.cells.append(nbf.v4.new_code_cell(b.strip("\n")))
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    destino = py.with_suffix(".ipynb")
    nbf.write(nb, destino)
    print("→", destino.relative_to(RAIZ))
