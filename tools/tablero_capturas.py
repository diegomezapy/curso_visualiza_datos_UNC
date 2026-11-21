"""Escribe cada app Shiny de tablero_spec.py, la ejecuta con R y captura la pantalla REAL (Playwright).
Uso: python tools/tablero_capturas.py   (requiere R con shiny, bslib, plotly, DT y node con playwright; datos: tools/dashboards_datos.py)"""
import shutil, subprocess, sys, time, socket, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import tablero_spec as T
RAIZ = Path(__file__).resolve().parents[1]; M = RAIZ / "aula" / "media" / "unidad5_tablero_shiny" / "fuentes"
(M / "apps").mkdir(parents=True, exist_ok=True); (M / "capturas").mkdir(exist_ok=True); (M / "datos").mkdir(exist_ok=True)
shutil.copy(RAIZ / "aula" / "media" / "unidad5_dashboards" / "fuentes" / "datos" / "cubo_importaciones.csv", M / "datos" / "cubo_importaciones.csv")
JS = RAIZ / "tools" / "tablero_captura.cjs"
for i, (k, codigo) in enumerate(T.APPS.items()):
    d = M / "apps" / k; d.mkdir(exist_ok=True); (d / "app.R").write_text(codigo, encoding="utf-8"); shutil.copy(M / "datos" / "cubo_importaciones.csv", d / "cubo_importaciones.csv")
    port = 4100 + i
    p = subprocess.Popen(["Rscript", "-e", f"shiny::runApp('{d}', port={port}, launch.browser=FALSE)"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for _ in range(60):
        try: socket.create_connection(("127.0.0.1", port), 1).close(); break
        except OSError: time.sleep(1)
    else: p.kill(); print(p.stderr.read().decode()[-800:]); raise SystemExit(f"{k}: la app no inició")
    r = subprocess.run(["node", str(JS), k, str(port), str(M / "capturas")], capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    p.terminate(); p.wait(timeout=20)
