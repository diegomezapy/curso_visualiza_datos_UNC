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

FXCSS = """
#fx-bg{position:fixed;inset:0;z-index:0;pointer-events:none}header,main,footer{position:relative;z-index:1}
header{backdrop-filter:blur(8px);background:color-mix(in srgb,var(--cd) 82%,transparent);position:sticky;top:0;z-index:5}
nav a{transition:color .15s,transform .15s}nav a:hover{transform:translateY(-1px)}
#fxbtn{cursor:pointer;background:none;color:var(--fg);border:1px solid var(--bd);border-radius:999px;padding:.15rem .7rem;font:inherit;font-size:.8rem}
.fx-reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s cubic-bezier(.2,.8,.2,1)}.fx-reveal.in{opacity:1;transform:none}
main{animation:viewin .5s cubic-bezier(.2,.8,.2,1)}
.gal figure{transition:transform .2s,box-shadow .2s}.gal figure:hover{transform:translateY(-3px);box-shadow:0 10px 28px color-mix(in srgb,var(--ac) 25%,transparent)}
main>h1{background:linear-gradient(90deg,var(--fg),var(--ac),var(--fg));background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shift 10s linear infinite}
.hero{display:grid;grid-template-columns:1.1fr 1fr;gap:1rem;align-items:center;padding:1.4rem 1.5rem;margin:1rem 0 1.5rem;border-radius:16px;border:1px solid var(--bd);overflow:hidden;background:radial-gradient(120% 140% at 0% 0%,color-mix(in srgb,var(--ac) 16%,var(--cd)),var(--cd) 62%)}
.hero-tag{display:inline-flex;gap:.45rem;align-items:center;font-size:.76rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--ac)}
.hero-tag i{width:8px;height:8px;border-radius:50%;background:#1a9f5b;animation:ping 1.8s infinite}
.hero-h{font-size:clamp(1.6rem,3.6vw,2.4rem);line-height:1.15;margin:.5rem 0}
.grad{background:linear-gradient(90deg,var(--ac),#009E73,#CC79A7,var(--ac));background-size:250% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shift 9s linear infinite}
.hero p{color:var(--mut);margin:.2rem 0 .9rem}.hero .cta{display:flex;flex-wrap:wrap;gap:.6rem}
.hero .cta a{display:inline-block;padding:.5rem 1rem;border-radius:8px;text-decoration:none;font-weight:600;border:1px solid var(--ac);color:var(--ac);transition:transform .12s,box-shadow .15s}
.hero .cta a.p{background:var(--ac);color:#fff}.hero .cta a:hover{transform:translateY(-1px);box-shadow:0 6px 18px color-mix(in srgb,var(--ac) 35%,transparent)}
.hero-viz{width:100%;height:auto;min-width:0}.hv-grid line{stroke:var(--bd);stroke-dasharray:3 5}
.hv-bars rect{fill:color-mix(in srgb,var(--ac) 55%,transparent);transform-box:fill-box;transform-origin:bottom;animation:barin .9s cubic-bezier(.2,.8,.2,1) both;animation-delay:calc(var(--i)*90ms)}
.hv-line{fill:none;stroke:var(--ac);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.8s .4s ease forwards}
.hv-area{opacity:0;animation:fadein 1s 1.6s forwards}
.hv-pt{fill:var(--cd);stroke:var(--ac);stroke-width:2;opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s both;animation-delay:calc(.5s + var(--i)*190ms)}
.hv-dot{fill:#1a9f5b;filter:drop-shadow(0 0 6px #1a9f5b)}.hv-lbl{fill:var(--mut);font:10px system-ui,sans-serif}
@media(max-width:760px){.hero{grid-template-columns:1fr}}
@keyframes ping{0%{box-shadow:0 0 0 0 rgba(26,159,91,.6)}80%,100%{box-shadow:0 0 0 9px transparent}}
@keyframes shift{to{background-position:250% 0}}@keyframes barin{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes draw{to{stroke-dashoffset:0}}@keyframes fadein{to{opacity:1}}@keyframes pop{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
@keyframes viewin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.fx-off #fx-bg{display:none}.fx-off main,.fx-off main>h1,.fx-off .grad,.fx-off .hero-tag i,.fx-off .hv-bars rect,.fx-off .hv-line,.fx-off .hv-area,.fx-off .hv-pt{animation:none!important}
.fx-off main>h1{background:none;-webkit-text-fill-color:initial;color:var(--fg)}.fx-off .grad{background:none;color:var(--ac)}
.fx-off .hv-line{stroke-dashoffset:0}.fx-off .hv-area,.fx-off .hv-pt{opacity:1}.fx-off .fx-reveal{opacity:1;transform:none;transition:none}
@media(prefers-reduced-motion:reduce){main,main>h1,.grad,.hero-tag i,.hv-bars rect,.hv-line,.hv-area,.hv-pt{animation:none!important}.hv-line{stroke-dashoffset:0}.hv-area,.hv-pt{opacity:1}.fx-reveal{opacity:1;transform:none;transition:none}}
@media print{#fx-bg,#fxbtn,.hero-viz{display:none!important}.fx-reveal{opacity:1!important;transform:none!important}}
"""

FXJS = """<script src="@R@aula/fxbg.js"></script><script>(function(){var d=document,h=d.documentElement,b=d.createElement('button');b.id='fxbtn';b.type='button';b.title='Activar o desactivar las animaciones';
function on(){return !h.classList.contains('fx-off')}function pint(){b.textContent=on()?'✨ Efectos: sí':'✨ Efectos: no';b.setAttribute('aria-pressed',on())}
b.onclick=function(){window.FXBG&&window.FXBG.set(!on());pint()};var n=d.querySelector('nav');n&&n.appendChild(b);pint();
if(on()&&'IntersectionObserver' in window){var els=[].slice.call(d.querySelectorAll('main h2,main table,main pre,main blockquote,.gal figure'));
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.05});
els.forEach(function(e,i){e.classList.add('fx-reveal');e.style.transitionDelay=Math.min(i%6,5)*50+'ms';io.observe(e)});setTimeout(function(){els.forEach(function(e){e.classList.add('in')})},1800)}})();</script>"""

def hero():
    barras = [38, 62, 45, 80, 58, 92, 70, 104]
    pts = [[12, 118], [52, 96], [92, 104], [132, 70], [172, 82], [212, 46], [252, 56], [292, 24]]
    ln = " ".join(("L" if i else "M") + f"{x} {y}" for i, (x, y) in enumerate(pts))
    rects = "".join(f'<rect style="--i:{i}" x="{12 + i * 38}" y="{140 - h}" width="22" height="{h}" rx="3"/><text class="hv-lbl" x="{23 + i * 38}" y="158" text-anchor="middle">S{i + 1}</text>' for i, h in enumerate(barras))
    puntos = "".join(f'<circle class="hv-pt" style="--i:{i}" cx="{x}" cy="{y}" r="3.6"/>' for i, (x, y) in enumerate(pts))
    grid = "".join(f'<line x1="8" x2="312" y1="{y}" y2="{y}"/>' for y in (30, 70, 110))
    return f'''<section class="hero"><div><span class="hero-tag"><i></i> Maestría en Ingeniería y Ciencia de Datos · FACET – UNC</span>
<h2 class="hero-h" style="border:0;margin-top:.5rem">Convertí datos en <span class="grad">decisiones que se entienden.</span></h2>
<p>8 sesiones de visualización de datos con Python y R: percepción, color, dashboards, redes y storytelling con datos reales de Paraguay. Clases virtuales desde el 13 de noviembre de 2026.</p>
<div class="cta"><a class="p" href="aula/index.html">🎓 Entrar al aula</a><a href="docs/programa.html">Ver el programa</a><a href="docs/cronograma.html">Cronograma</a></div></div>
<svg class="hero-viz" viewBox="0 0 320 170" role="img" aria-label="Ilustración animada: barras por sesión y línea de tendencia"><g class="hv-grid">{grid}</g>
<g class="hv-bars">{rects}</g><path class="hv-area" d="{ln} L292 140 L12 140 Z" fill="var(--ac)" fill-opacity=".14"/><path class="hv-line" d="{ln}" pathLength="1"/>{puntos}
<circle class="hv-dot" r="5"><animateMotion dur="7s" repeatCount="indefinite" path="{ln}"/></circle></svg></section>'''


def raiz_rel(dest: Path) -> str:
    n = len(dest.relative_to(SITE).parts) - 1
    return "../" * n or "./"

def pagina(dest, titulo, cuerpo):
    r = raiz_rel(dest)
    nav = f'<a class="t" href="{r}index.html">Visualización de Datos · UNC</a>' + "".join(
        f'<a href="{r}{h}">{t}</a>' for t, h in [("🎓 Aula virtual", "aula/index.html"), ("📝 Diagnóstico", "diagnostico/index.html"), ("Guía del aula", "docs/aula_virtual.html"), ("Programa", "docs/programa.html"), ("Cronograma", "docs/cronograma.html"),
        ("Evaluación", "docs/evaluacion.html"), ("Rúbricas", "docs/rubricas.html"), ("Integrador", "docs/proyecto_integrador.html"),
        ("Quizzes", "docs/banco_quizzes.html"), ("Bibliografía", "docs/bibliografia.html")]) + f'<a href="{REPO}">GitHub</a>'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f"""<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} · Visualización de Datos UNC</title><style>{CSS}{FXCSS}</style>
<canvas id="fx-bg" aria-hidden="true"></canvas><header><nav>{nav}</nav></header><main>{(hero() if dest == SITE / "index.html" else "") + cuerpo}</main>
<footer>Maestría en Ingeniería y Ciencia de Datos · FACET – Universidad Nacional de Concepción · Datos sintéticos con fines docentes.</footer>{FXJS.replace("@R@", r)}</html>""", encoding="utf-8")

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
