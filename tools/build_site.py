"""Construye el sitio estático (GitHub Pages) en `site/`.
Convierte los .md a HTML, agrega la galería de salidas de cada lab y copia `salidas/`.
Uso: python tools/build_site.py   (ejecutar antes los labs para tener `salidas/`)
"""
import re, shutil, html
from pathlib import Path
import markdown

RAIZ = Path(__file__).resolve().parents[1]
SITE = RAIZ / "site"
REPO = "https://github.com/diegomezapy/curso_visualiza_datos_UNC"
shutil.rmtree(SITE, ignore_errors=True)

CSS = """:root{--bg:#fff;--fg:#1f2328;--mut:#656d76;--bd:#d8dee4;--ac:#0072B2;--cd:#f6f8fa}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--mut:#8b949e;--bd:#30363d;--ac:#56B4E9;--cd:#161b22}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}
header{border-bottom:1px solid var(--bd);background:var(--cd)}nav{max-width:960px;margin:auto;padding:.7rem 16px;display:flex;flex-wrap:wrap;gap:.4rem 1.1rem;align-items:center}
nav a{color:var(--fg);text-decoration:none;font-size:.9rem}nav a:hover{color:var(--ac)}nav .t{font-weight:700;margin-right:auto}
main{max-width:960px;margin:auto;padding:1rem 16px 4rem;overflow-wrap:anywhere}a{color:var(--ac)}
h1,h2,h3{line-height:1.25}h2{border-bottom:1px solid var(--bd);padding-bottom:.3rem;margin-top:2rem}
table{border-collapse:collapse;display:block;overflow-x:auto;max-width:100%}th,td{border:1px solid var(--bd);padding:.4rem .7rem;text-align:left;vertical-align:top}th{background:var(--cd)}
code{background:var(--cd);padding:.1rem .3rem;border-radius:4px;font-size:.9em}pre{background:var(--cd);border:1px solid var(--bd);border-radius:8px;padding:1rem;overflow-x:auto}pre code{background:none;padding:0}
blockquote{margin:1rem 0;padding:.1rem 1rem;border-left:4px solid var(--ac);color:var(--mut)}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}.gal figure{margin:0;border:1px solid var(--bd);border-radius:8px;padding:.5rem;background:#fff}
.gal img{width:100%;height:auto}.gal figcaption{font-size:.8rem;color:#555;padding-top:.3rem}
footer{max-width:960px;margin:auto;padding:1rem 16px 2rem;color:var(--mut);font-size:.85rem}"""

def raiz_rel(dest: Path) -> str:
    n = len(dest.relative_to(SITE).parts) - 1
    return "../" * n or "./"

def pagina(dest, titulo, cuerpo):
    r = raiz_rel(dest)
    nav = f'<a class="t" href="{r}index.html">Visualización de Datos · UNC</a>' + "".join(
        f'<a href="{r}{h}">{t}</a>' for t, h in [("Programa", "docs/programa.html"), ("Cronograma", "docs/cronograma.html"),
        ("Evaluación", "docs/evaluacion.html"), ("Rúbricas", "docs/rubricas.html"), ("Integrador", "docs/proyecto_integrador.html"),
        ("Quizzes", "docs/banco_quizzes.html"), ("Bibliografía", "docs/bibliografia.html")]) + f'<a href="{REPO}">GitHub</a>'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f"""<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} · Visualización de Datos UNC</title><style>{CSS}</style>
<header><nav>{nav}</nav></header><main>{cuerpo}</main>
<footer>Maestría en Ingeniería y Ciencia de Datos · FACET – Universidad Nacional de Concepción · Datos sintéticos con fines docentes.</footer></html>""", encoding="utf-8")

def md_a_html(md_path: Path, extra="") -> tuple[str, str]:
    txt = md_path.read_text(encoding="utf-8")
    titulo = (re.search(r"^#\s+(.+)$", txt, re.M) or [None, md_path.stem])[1]
    cuerpo = markdown.markdown(txt, extensions=["tables", "fenced_code", "toc"])
    # reescribir enlaces relativos
    def fix(m):
        url = m.group(1)
        if re.match(r"^(https?:|#|mailto:)", url): return m.group(0)
        base, _, frag = url.partition("#")
        if base.endswith("README.md"): base = base[:-9] + "index.html"
        elif base.endswith(".md"): base = base[:-3] + ".html"
        elif base.endswith(".py"):
            rel = (md_path.parent / base).resolve().relative_to(RAIZ).as_posix()
            return f'href="{REPO}/blob/main/{rel}"'
        return f'href="{base}{"#"+frag if frag else ""}"'
    return titulo, re.sub(r'href="([^"]+)"', fix, cuerpo) + extra

# salidas de los labs
salidas = RAIZ / "salidas"
if salidas.is_dir(): shutil.copytree(salidas, SITE / "salidas", ignore=shutil.ignore_patterns(".gitkeep"))

def galeria(md_path: Path, dest: Path) -> str:
    m = re.match(r"(\d\d)_", md_path.parent.name)
    if not m: return ""
    pref = f"lab{m.group(1)}_"; r = raiz_rel(dest)
    figs = sorted((SITE / "salidas").glob(f"{pref}*.png")) if (SITE / "salidas").is_dir() else []
    htmls = sorted((SITE / "salidas").glob(f"{pref}*.html")) + (sorted((SITE / "salidas").glob("informe_*.html")) if m.group(1) == "06" else [])
    out = ""
    if figs:
        out += "<h2>Resultados del laboratorio</h2><div class='gal'>" + "".join(
            f"<figure><a href='{r}salidas/{f.name}'><img loading='lazy' src='{r}salidas/{f.name}' alt='{f.stem}'></a><figcaption>{f.stem}</figcaption></figure>" for f in figs) + "</div>"
    if htmls:
        out += "<h2>Salidas interactivas</h2><ul>" + "".join(f"<li><a href='{r}salidas/{f.name}'>{f.name}</a></li>" for f in htmls) + "</ul>"
    return out

fuentes = [(RAIZ / "README.md", SITE / "index.html")]
fuentes += [(p, SITE / "docs" / (p.stem + ".html")) for p in sorted((RAIZ / "docs").glob("*.md"))]
fuentes += [(p, SITE / p.relative_to(RAIZ).parent / "index.html") for p in sorted(RAIZ.glob("sesiones/*/README.md"))]
fuentes += [(RAIZ / "datos/README.md", SITE / "datos" / "index.html")]
for src, dst in fuentes:
    t, c = md_a_html(src, galeria(src, dst) if "sesiones" in src.parts else "")
    pagina(dst, t, c)
(SITE / ".nojekyll").write_text("")
print("sitio generado:", len(fuentes), "páginas")
