"""Genera docs/datos_abiertos_reales.md desde datos_reales/catalogo.py (única fuente de verdad). Uso: python tools/build_datos_reales.py"""
import sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(RAIZ / "datos_reales"))
import catalogo as C

R_DISPONIBLE = {"pr01_explorador", "pr02_dncp", "pr03_banco_mundial"}
L = ["# Datos abiertos reales para las prácticas", "",
 "> *Generado por `tools/build_datos_reales.py` desde `datos_reales/catalogo.py`. No editar a mano.*", "",
 "Las prácticas del curso usan **datos abiertos reales de Paraguay y de fuentes globales** (compras públicas, encuestas de hogares, nómina estatal, imágenes satelitales, comercio exterior…) para dar a cada ejercicio una pregunta con sentido y una audiencia real.", "",
 "## ⚠️ Lea esto primero: estado real de cada fuente",
 "El catálogo se armó con búsquedas en noviembre de 2026; **desde el entorno de desarrollo no se pudo abrir ninguna fuente ni inspeccionar filas**. Por eso:",
 "- Cada fuente trae un **estado** (✅ documentada · 🔎 verificar acceso · ⚠️ incierto).",
 "- **No hay nombres de columnas “de memoria”**: las prácticas se adaptan al esquema real (perfilado automático) o piden mapear las columnas con el diccionario oficial.",
 "- Todas las prácticas **funcionan sin conexión con datos sintéticos claramente rotulados**, y se activan con datos reales al pegar la URL.",
 "- **Antes de la primera clase**, el docente debe ejecutar `practicas_reales/pr00_verificar_fuentes` en Colab y revisar los pasos manuales (registro en Earth Engine, diccionario de la EPHC, ID del asset de MapBiomas…).", "",
 "## Catálogo", "", "| Fuente | Estado | Sesiones | Práctica |", "|---|---|---|---|"]
for f in C.FUENTES:
    ic, tx = C.ESTADOS[f["estado"]]; L.append(f"| [{f['nombre']}](#{f['id']}) | {ic} {tx}{' · 🔒 datos personales' if f['sensible'] else ''} | {', '.join(map(str, f['sesiones']))} | `{f['practica']}` |")
L.append("")
for f in C.FUENTES:
    ic, tx = C.ESTADOS[f["estado"]]
    L += [f"### {f['nombre']} {{#{f['id']}}}", "", f"**{f['inst']}** · {ic} {tx} · {f['tipo']} · {f['formato']}", "", f["contiene"], "",
          f"- **Portal:** <{f['url']}> · **Documentación:** <{f['doc']}>",
          f"- **Práctica:** `{f['practica']}` — {f['titulo_practica']}" + (" (Python/Colab y R/RPubs)" if f["practica"] in R_DISPONIBLE else " (Python/Colab)"),
          "- **Ideas:** " + "; ".join(f["ideas"]), f"- **Cuidado:** {f['aviso']}", ""]
L += ["## Ruta de prácticas por sesión", "", "| Sesión | Práctica | Qué se aprende |", "|---|---|---|"]
for pid, nombre, desc, ses, rol in C.PRACTICAS:
    L.append(f"| {', '.join(map(str, ses))} | `{pid}` · {nombre}{' *(docente)*' if rol == 'docente' else ''} | {desc} |")
L += ["", "## Reglas de oro con datos reales",
 "1. **Citar** la fuente, la URL y la **fecha de descarga**; completar la *ficha del dataset* (práctica 1).",
 "2. **No confiar en un dato porque sea oficial**: perfilar, buscar nulos, duplicados y cambios de definición.",
 "3. **Datos personales:** trabajar solo con agregados; descartar nombres y documentos al cargar; suprimir grupos pequeños (práctica 5). Lo que se publica en RPubs es público.",
 "4. **Encuestas:** usar el factor de expansión (práctica 4).",
 "5. **Mapas:** tasas o densidades, no conteos (sesión 7).",
 "6. **Licencias:** verificar las condiciones de uso; MapBiomas (no comercial o interés público, citar), datos del VCHGO (reconocer la fuente y corroborar), etc.",
 "7. **Si una fuente cae o cambia**, el código lo avisa y usa datos sintéticos: nunca presentar esos resultados como reales.", "",
 "## Para el docente: lista de verificación previa",
 "- [ ] Ejecutar `pr00_verificar_fuentes` en Colab y guardar la tabla.",
 "- [ ] **Earth Engine:** que cada estudiante se registre y cree un proyecto de Cloud (puede demorar); verificar el ID del asset de MapBiomas.",
 "- [ ] **EPHC:** descargar la base vigente y su diccionario; anotar el nombre del factor de expansión; subir una **muestra** a la carpeta del curso (Drive).",
 "- [ ] **Nómina:** localizar el conjunto y confirmar que se puede usar solo con agregados.",
 "- [ ] **Aduanas:** confirmar si la DNIT volvió a publicar; si no, usar Banco Mundial / UN Comtrade / BCP.",
 "- [ ] **DNCP:** probar una descarga masiva OCDS (JSON) y pegar la URL o ruta en la práctica 2."]
(RAIZ / "docs" / "datos_abiertos_reales.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("docs/datos_abiertos_reales.md")
