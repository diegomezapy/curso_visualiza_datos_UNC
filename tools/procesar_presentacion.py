"""Procesa una presentación del aula (PPTX) para incrustarla: PDF + diapositivas .webp + slides.json (títulos y texto) y, si existe, la infografía.
Uso: python tools/procesar_presentacion.py unidad1            (o unidad2_ggplot)
Entrada: aula/media/<carpeta>/fuentes/*.pptx  (y opcional fuentes/infografia_original.png)
Requiere LibreOffice (soffice), pdftoppm y Pillow. Se ejecuta a mano cuando cambian las fuentes; la salida se versiona."""
import json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image
RAIZ = Path(__file__).resolve().parents[1]
carpeta = sys.argv[1] if len(sys.argv) > 1 else "unidad1"
M = RAIZ / "aula" / "media" / carpeta; F = M / "fuentes"; D = M / "diapositivas"
shutil.rmtree(D, ignore_errors=True); D.mkdir(parents=True)
pptx = sorted(F.glob("*.pptx"))[0]
shutil.copy(pptx, M / "presentacion.pptx")
with tempfile.TemporaryDirectory() as t:
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", t, str(pptx)], check=True, capture_output=True, timeout=600)
    pdf = next(Path(t).glob("*.pdf")); shutil.copy(pdf, M / "presentacion.pdf")
    subprocess.run(["pdftoppm", "-r", "110", "-png", str(pdf), str(Path(t) / "s")], check=True)
    for i, p in enumerate(sorted(Path(t).glob("s-*.png")), 1):
        Image.open(p).convert("RGB").save(D / f"{i:02d}.webp", "WEBP", quality=82, method=6)
# texto por diapositiva (del XML del .pptx: limpio y en orden)
NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
z = zipfile.ZipFile(pptx)
nombres = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=lambda n: int(re.findall(r"\d+", n)[0]))
slides = []
for i, n in enumerate(nombres, 1):
    raiz = ET.fromstring(z.read(n)); parr = []
    for p in raiz.iter(NS + "p"):
        tx = "".join(x.text or "" for x in p.iter(NS + "t")).strip()
        if tx and not re.fullmatch(r"[\d.,%\s]+", tx): parr.append(tx)
    slides.append({"n": i, "img": f"{i:02d}.webp", "titulo": re.sub(r"([a-záéíóú])([A-ZÁÉÍÓÚ])", r"\1 \2", parr[0]) if parr else f"Diapositiva {i}", "texto": parr[1:]})
(M / "slides.json").write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
info = F / "infografia_original.png"
if info.exists(): Image.open(info).convert("RGB").save(M / "infografia.webp", "WEBP", quality=90, method=6)
print(carpeta, len(slides), "diapositivas;", round(sum(p.stat().st_size for p in D.glob("*.webp")) / 1024), "KB en diapositivas;", round((M / "presentacion.pdf").stat().st_size / 1024), "KB de PDF")
