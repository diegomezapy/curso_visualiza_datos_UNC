"""Procesa los recursos de la Unidad 1 (PPT + infografía) para incrustarlos en el aula.
Entrada:  aula/media/unidad1/fuentes/*.pptx y infografia_original.png
Salida:   aula/media/unidad1/diapositivas/NN.webp, presentacion.pdf, presentacion.pptx, infografia.webp, slides.json (títulos y texto)
Requiere LibreOffice (soffice), pdftoppm y Pillow. Se ejecuta a mano cuando cambian las fuentes; la salida se versiona."""
import json, re, shutil, subprocess, tempfile, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image
RAIZ = Path(__file__).resolve().parents[1]
M = RAIZ / "aula" / "media" / "unidad1"; F = M / "fuentes"; D = M / "diapositivas"
shutil.rmtree(D, ignore_errors=True); D.mkdir(parents=True)
pptx = next(F.glob("*.pptx"))
shutil.copy(pptx, M / "presentacion.pptx")
with tempfile.TemporaryDirectory() as t:
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", t, str(pptx)], check=True, capture_output=True, timeout=300)
    pdf = next(Path(t).glob("*.pdf")); shutil.copy(pdf, M / "presentacion.pdf")
    subprocess.run(["pdftoppm", "-r", "110", "-png", str(pdf), str(Path(t) / "s")], check=True)
    for i, p in enumerate(sorted(Path(t).glob("s-*.png")), 1):
        Image.open(p).convert("RGB").save(D / f"{i:02d}.webp", "WEBP", quality=82, method=6)
# texto por diapositiva (del XML del .pptx: limpio y en orden)
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
z = zipfile.ZipFile(pptx)
nombres = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=lambda n: int(re.findall(r"\d+", n)[0]))
slides = []
for i, n in enumerate(nombres, 1):
    raiz = ET.fromstring(z.read(n)); parr = []
    for p in raiz.iter("{%s}p" % NS["a"]):
        tx = "".join(x.text or "" for x in p.iter("{%s}t" % NS["a"])).strip()
        if tx and not re.fullmatch(r"[\d.,%\s]+", tx): parr.append(tx)   # sin etiquetas numéricas de ejes
    slides.append({"n": i, "img": f"{i:02d}.webp", "titulo": re.sub(r"([a-záéíóú])([A-ZÁÉÍÓÚ])", r"\1 \2", parr[0]) if parr else f"Diapositiva {i}", "texto": parr[1:]})
(M / "slides.json").write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
im = Image.open(F / "infografia_original.png").convert("RGB")
im.save(M / "infografia.webp", "WEBP", quality=90, method=6)
print(len(slides), "diapositivas;", {p.name: round(p.stat().st_size / 1024) for p in [M / "infografia.webp", M / "presentacion.pdf", M / "presentacion.pptx"]}, "KB;", round(sum(p.stat().st_size for p in D.glob("*.webp")) / 1024), "KB en diapositivas")
