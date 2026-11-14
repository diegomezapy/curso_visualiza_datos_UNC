"""Genera notebooklm/: fuentes (.md para subir) y prompts listos para pegar en NotebookLM, uno por sesión.
Uso: python tools/build_notebooklm.py   (lee aula/contenido.py, aula/recursos.py y sesiones/*/README.md)"""
import sys, re, shutil
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "aula"))
import contenido as c, recursos as rc

OUT = RAIZ / "notebooklm"
shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir()
DIRS = {1: "01_principios", 2: "02_eleccion_graficos", 3: "03_color_diseno_etica", 4: "04_visual_analytics_kpis", 5: "05_dashboards_interactivos", 6: "06_reporting_automatizado", 7: "07_estructuras_complejas", 8: "08_redes_e_integrador"}

PERSONA = ("Sos un docente universitario de visualización de datos para una maestría en ciencia de datos en Paraguay. Explicá en español neutro, claro y preciso, "
 "con ejemplos de datos reales de Paraguay cuando la fuente los traiga. Usá SOLO lo que dicen las fuentes: si algo no está, decí que no está en las fuentes y no lo inventes. "
 "No des cifras, fechas ni citas que no figuren en las fuentes. Nombrá la fuente de cada afirmación importante.")

def limpiar(t):  # quita encabezado de unidad/duración para que la fuente sea autocontenida
    return t.strip()

def fuente_sesion(s):
    n = s["n"]; d = DIRS[n]
    readme = (RAIZ / "sesiones" / d / "README.md").read_text(encoding="utf-8")
    quiz = c.QUIZZES.get(n)
    puntos = ""
    if quiz:
        puntos = "\n## Ideas clave verificables (de las preguntas de autoevaluación)\n" + "\n".join(
            f"- **{q['q']}** → {q['o'][q['c']]}. {q['why']}" for q in quiz[1])
    lects = "\n".join(f"- {l['t']} ({l['tipo']}, {l['idioma']}) · {l['u']} · {l.get('nota','')}" for l in rc.LECTURAS.get(n, []))
    acts = "\n".join(f"- {a['titulo']} ({a['pts']} pts)" for a in s["actividades"])
    ppt = ""
    sj = RAIZ / "aula" / "media" / "unidad1" / "slides.json"
    if n == 1 and sj.exists():
        import json
        ppt = "\n## Texto de la presentación de la unidad (Ciencia de la percepción gráfica)\n" + "\n".join(
            f"### Diapositiva {d['n']} · {d['titulo']}\n" + "\n".join(f"- {t}" for t in d["texto"]) for d in json.loads(sj.read_text(encoding="utf-8")))
    return f"""# Sesión {n} · {s['titulo']}
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad {s['unidad']}.
Resumen: {s['resumen']}

## Objetivos
""" + "\n".join(f"- {o}" for o in s["objetivos"]) + f"""

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
{limpiar(readme)}
{puntos}

## Actividades evaluadas
{acts}
{ppt}

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
{lects}
"""

def glosario():
    return "# Glosario del curso de Visualización de Datos\n\n" + "\n".join(f"- **{a}:** {b}" for a, b in c.GLOSARIO) + "\n"

def prompts(s):
    n, t = s["n"], s["titulo"]; obj = "; ".join(o.rstrip(". ") for o in s["objetivos"])
    DEBATE = "**Debate** (sobre cuándo un gráfico manipula y cuándo solo simplifica);" if n == 3 else "**Debate** (solo si el tema admite posturas: planteá la pregunta en el prompt);"
    return f"""# Prompts de NotebookLM · Sesión {n}: {t}

**Cuaderno:** `VD · Sesión {n} · {t}`. **Fuentes a subir (en este orden):**
1. `fuente_sesion_{n:02d}.md` (esta carpeta)
2. `../fuente_glosario.md`
3. La ficha PDF de la sesión: `materiales/pdf/ficha_*.pdf` (repositorio) — opcional
4. Enlaces **de acceso abierto** de las lecturas (p. ej. el libro de Wilke en clauswilke.com/dataviz). No subas libros o artículos con derechos de autor sin permiso.

> Antes de generar nada, en **Chat → Configurar (lápiz)** elegí *Personalizado* y pegá el bloque «Rol del chat» de abajo. Así todas las respuestas del cuaderno mantienen el tono y la regla de no inventar.

## 0 · Rol del chat (pegar en la configuración del chat)
```
{PERSONA}
Tema del cuaderno: Sesión {n}, «{t}». Objetivos: {obj}.
Audiencia: estudiantes de maestría con base en estadística y programación.
```

## 1 · Material de lectura (Informes → Crear informe personalizado)
```
Escribí una lectura de estudio sobre «{t}» para estudiantes de maestría, de 1.500 a 2.000 palabras, en español.
Estructura: (1) por qué importa, con un ejemplo concreto de las fuentes; (2) los 4 o 5 conceptos centrales, cada uno con definición breve, un ejemplo y un error común;
(3) un mini-caso paso a paso; (4) cinco errores típicos y cómo evitarlos; (5) glosario de 8 a 10 términos; (6) 5 preguntas de reflexión; (7) qué leer a continuación (solo lo que figure en las fuentes).
Cubrí exactamente estos objetivos: {obj}.
Reglas: nada que no esté en las fuentes; marcá con «[no está en las fuentes]» lo que falte; frases cortas; sin relleno.
```
Variantes rápidas: *Guía de estudio* (nativa), *Documento de resumen* y *Preguntas frecuentes*; revisá siempre contra la ficha PDF.

## 2 · Audio (Resumen de audio → Personalizar)
Formato **Análisis profundo** · idioma **Español** · duración **Larga** (pedí 12–15 min).
```
Conversación entre dos docentes para estudiantes de maestría que escuchan antes de la clase de la Sesión {n}: «{t}».
Abrí con una pregunta que los intrigue, no con un saludo largo. Recorré: {obj}.
Alterná explicación y ejemplo concreto de las fuentes; usá analogías cotidianas una sola vez por concepto; nombrá un error común y cómo corregirlo.
Cerrá con tres ideas para recordar y la tarea que viene. Ritmo pausado, tono cercano y riguroso, sin chistes forzados.
No inventes datos ni nombres: si no está en las fuentes, no lo digas. Mencioná el nombre de la fuente cuando cites algo.
```
Variantes: **Resumen breve** (3–5 min, «repaso de 3 minutos»); {DEBATE} **Crítica** (subí un gráfico de un trabajo del grupo, con permiso).

## 3 · Video (Resumen de video → Personalizar)
Estilo **sobrio** (Pizarra/Clásico si está disponible) · idioma **Español** · formato explicativo.
```
Video explicativo de 5 a 8 minutos sobre «{t}» para estudiantes de maestría, previo a la clase.
Estructura: problema → idea clave → ejemplo visual paso a paso → error común → resumen en tres puntos.
Mostrá gráficos y diagramas simples que ilustren lo que dicen las fuentes; letras grandes y alto contraste; una sola idea por pantalla.
Español neutro, sin adornos. No incluyas datos que no estén en las fuentes.
```

## 4 · Cuestionario y tarjetas
```
Generá 10 preguntas de opción múltiple (4 opciones) de nivel maestría sobre «{t}», con respuesta correcta y una explicación de una línea. 3 fáciles, 4 medias, 3 difíciles. Basate solo en las fuentes.
```
Tarjetas: pedí *Tarjetas didácticas* con 15 términos del glosario de esta sesión. Mapa mental: *Mapa mental* sobre los objetivos.

## 5 · Control de calidad antes de publicar (obligatorio)
- [ ] Escuchá o mirá el material completo contra la ficha PDF y la guía; corregí o regenerá si hay errores.
- [ ] Verificá cifras, nombres, fechas y citas (NotebookLM puede equivocarse o inventar).
- [ ] Si usaste un dato real de Paraguay, comprobá la fuente (ver `docs/datos_abiertos_reales.md`).
- [ ] Agregá en la descripción: «Material generado con NotebookLM a partir de fuentes del curso; revisado por el docente».
- [ ] Subí el archivo a Drive (carpeta de la sesión) y cargá el enlace en el aula (**Recursos** o **Clases grabadas**).
"""

LEEME = f"""# NotebookLM · protocolo para crear lecturas, audios y videos del curso

Esta carpeta se genera con `python tools/build_notebooklm.py` desde el contenido del repositorio. Contiene, por sesión, (a) **una fuente lista para subir** y (b) **prompts listos para pegar**.

## Resumen del flujo (45–60 min por sesión)
1. En NotebookLM creá un **cuaderno por sesión**: `VD · Sesión N · Título`. Más un cuaderno general «VD · Curso completo» con los 8 `fuente_sesion_*` y el glosario (para repasos y consultas de estudiantes).
2. Subí las fuentes indicadas en `sesion_NN/prompts_sesion_N.md`. Una fuente = un tema; evitá subir material duplicado.
3. Pegá el **Rol del chat** (configuración del chat) antes de generar.
4. Generá, en este orden: **lectura → audio → video → cuestionario/tarjetas**. Si la lectura sale mal, corregí las fuentes antes de generar audio y video.
5. **Revisá todo** (checklist de la sección 5 de cada archivo) y subí a la carpeta de Drive de la sesión; enlazá desde el aula.

## Buenas prácticas
- **Fuentes limpias = materiales buenos.** Texto propio y verificado primero; libros abiertos (Wilke) y documentación oficial después. No subas obras con derechos reservados sin autorización.
- **Una instrucción, un objetivo.** Los prompts son cortos y con estructura; si NotebookLM rechaza uno por longitud, quitá los ejemplos y dejá la estructura.
- **Idioma.** Elegí español en el generador de audio y video; confirmá con una escucha de 30 s antes de esperar el resultado completo.
- **Iterá.** Regenerá con una frase de corrección concreta («más ejemplos de Paraguay», «explicá el Gestalt con un ejemplo antes de la definición») en lugar de reescribir todo el prompt.
- **Accesibilidad.** Publicá junto al audio/video la **transcripción o el resumen de lectura** y comprobá subtítulos.
- **Privacidad.** Nunca subas datos personales de estudiantes (cédulas, notas, correos) ni resultados del diagnóstico individual.

## Qué conviene verificar en tu cuenta (puede cambiar)
Los nombres de menús, estilos de video, formatos de audio, idiomas, límites diarios y el plan (gratis o de pago) los define Google y se actualizan seguido. Este protocolo se escribió sin poder abrir NotebookLM: si algún botón se llama distinto, usá el equivalente.

## Contenido
- `fuente_glosario.md` · 26 términos del curso.
- `sesion_01/` … `sesion_08/`: `fuente_sesion_NN.md` y `prompts_sesion_N.md`.
"""

(OUT / "LEEME.md").write_text(LEEME, encoding="utf-8")
(OUT / "fuente_glosario.md").write_text(glosario(), encoding="utf-8")
for s in c.SESIONES:
    n = s["n"]; d = OUT / f"sesion_{n:02d}"; d.mkdir()
    (d / f"fuente_sesion_{n:02d}.md").write_text(fuente_sesion(s), encoding="utf-8")
    (d / f"prompts_sesion_{n}.md").write_text(prompts(s), encoding="utf-8")
print("notebooklm generado en", OUT, "·", len(list(OUT.rglob('*.md'))), "archivos")
