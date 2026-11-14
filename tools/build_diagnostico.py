"""Genera los artefactos del diagnóstico a partir de diagnostico/preguntas.py:
 - appsscript/Preguntas.gs        (constantes y clave de respuestas para Apps Script)
 - appsscript/Tablero.html         (tablero para Apps Script)
 - site/diagnostico/*              (cuestionario, tablero y datos de ejemplo para GitHub Pages)
Uso: python tools/build_diagnostico.py   (después de tools/build_site.py)"""
import hashlib, json, shutil, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "diagnostico"))
import preguntas as Q

cfg = json.loads((RAIZ / "aula" / "config.json").read_text(encoding="utf-8"))
dg = cfg.get("diagnostico", {})
ENDPOINT = dg.get("endpoint", "")

# 1) Preguntas.gs
clave = {p[0]: {"t": p[1], "c": Q.LETRAS[p[4]]} for p in Q.PREGUNTAS}
gs = ["// GENERADO por tools/build_diagnostico.py a partir de diagnostico/preguntas.py. No editar a mano.",
      f"const AREAS = {json.dumps(Q.AREAS, ensure_ascii=False)};",
      f"const EXPERIENCIA = {json.dumps(Q.EXPERIENCIA, ensure_ascii=False)};",
      f"const HERRAMIENTAS = {json.dumps(Q.HERRAMIENTAS, ensure_ascii=False)};",
      f"const AUTO_IDS = {json.dumps([a for a, _ in Q.AUTO])};",
      f"const CLAVE_IDS = {json.dumps([p[0] for p in Q.PREGUNTAS])};",
      f"const CLAVE = {json.dumps(clave)};",
      f"const COLUMNAS = {json.dumps(Q.COLUMNAS)};",
      f"const PUBLICAS = {json.dumps(Q.PUBLICAS)};"]
(RAIZ / "appsscript" / "Preguntas.gs").write_text("\n".join(gs) + "\n", encoding="utf-8")

# 1b) Banco.gs: preguntas de mini-evaluación por sesión (tomadas de los quizzes del aula)
sys.path.insert(0, str(RAIZ / "aula"))
import contenido as CT
banco = {str(n): [{"q": q["q"], "o": q["o"], "c": q["c"], "why": q["why"]} for q in v[1]] for n, v in CT.QUIZZES.items()}
(RAIZ / "appsscript" / "Banco.gs").write_text("// GENERADO por tools/build_diagnostico.py a partir de aula/contenido.py. No editar a mano.\nconst BANCO = " + json.dumps(banco, ensure_ascii=False) + ";\n", encoding="utf-8")

# 2) datos para páginas
DIAG = {"areas": Q.AREAS, "experiencia": Q.EXPERIENCIA, "herramientas": Q.HERRAMIENTAS, "auto": Q.AUTO, "temas": Q.TEMAS,
        "preguntas": [{"id": p[0], "tema": p[1], "q": p[2], "o": p[3], "c": p[4], "why": p[5]} for p in Q.PREGUNTAS],
        "columnas": Q.COLUMNAS, "publicas": Q.PUBLICAS}
meta = json.dumps({"auto": Q.AUTO, "temas": Q.TEMAS, "herramientas": Q.HERRAMIENTAS, "areas": Q.AREAS, "experiencia": Q.EXPERIENCIA,
                   "preguntas": [{"id": p[0], "tema": p[1], "q": p[2]} for p in Q.PREGUNTAS]}, ensure_ascii=False)
tab = (RAIZ / "diagnostico" / "tablero.template.html").read_text(encoding="utf-8")
generador_xlsx = (RAIZ / "aula" / "xlsx.mjs").read_text(encoding="utf-8")
generador_xlsx = generador_xlsx.replace("export const XLSX_MIME", "const XLSX_MIME").replace("export function xlsxPlanilla", "function xlsxPlanilla")
generador_xlsx = generador_xlsx.replace("http://", '${"http:" + String.fromCharCode(47, 47)}')
tab = tab.replace("/*XLSX_INLINE*/", "(() => {\n" + generador_xlsx + "\nwindow.CVD_XLSX = { xlsxPlanilla, XLSX_MIME };\n})();")
(RAIZ / "appsscript" / "Tablero.html").write_text(tab.replace("/*META*/null", meta).replace("/*ENDPOINT*/''", "''"), encoding="utf-8")

site = RAIZ / "site" / "diagnostico"; site.mkdir(parents=True, exist_ok=True)
(site / "tablero.html").write_text(tab.replace("/*META*/null", meta).replace("/*ENDPOINT*/''", json.dumps(ENDPOINT)), encoding="utf-8")
(site / "preguntas.js").write_text("window.DIAG=" + json.dumps(DIAG, ensure_ascii=False) + ";window.DIAG_CFG=" + json.dumps({"endpoint": ENDPOINT, "tablero_url": dg.get("tablero_url", "")}) + ";", encoding="utf-8")
version = hashlib.sha256((site / "preguntas.js").read_bytes()).hexdigest()[:12]
index = (RAIZ / "diagnostico" / "index.html").read_text(encoding="utf-8")
(site / "index.html").write_text(index.replace('src="preguntas.js"', f'src="preguntas.js?v={version}"'), encoding="utf-8")
shutil.copy(RAIZ / "datos" / "diagnostico_ejemplo.csv", site / "ejemplo.csv")
print("diagnóstico generado → appsscript/ y", site)
