# Montaje del curso en Moodle (FACET-UNC)

Todo lo de esta carpeta se genera con `python tools/build_moodle.py`. **No se probó contra el Moodle de la FACET** (no hay acceso desde este entorno): si un menú se llama distinto según la versión, usá el equivalente.

## 1. Qué importar y qué pegar
| Archivo | Dónde va en Moodle |
|---|---|
| `preguntas/banco_completo.xml` | *Más → Banco de preguntas → Importar* → formato **Moodle XML**. Crea 8 categorías (Sesión 1…8) con 40 preguntas, con retroalimentación. |
| `preguntas/quiz_sesion_N.xml` | Igual, pero solo una sesión (si preferís ir de a una). |
| `glosario.xml` | Actividad **Glosario** → *Importar entradas* (XML). Activá el autoenlace. |
| `paginas/sesion_N.html` | Recurso **Página** (o Etiqueta) de la sesión N → editor HTML → botón `</>` → pegar. |

## 2. Estructura sugerida (un tema de Moodle por sesión)
Nombre del tema: `Sesión N · Título · fecha`. En cada uno, en este orden:
1. **Página** con `paginas/sesion_N.html` (objetivos, Colab, .Rmd, lecturas, videos).
2. **Reunión virtual**: BigBlueButton/Meet/Zoom según tenga la facultad. Horarios: viernes 18:00–22:00, sábados 08:00–12:00, del 13/11 al 05/12/2026.
3. **Cuestionario** de la sesión (importado en el paso 1): intentos 2, calificación = mejor intento, retroalimentación después del intento, sin límite de tiempo estricto.
4. **Tarea** de entrega (donde corresponda): activar *Enviar comentarios*, calificación con **Rúbrica** y finalización por entrega. Las entregas son enlaces a RPubs y Colab: usá *Texto en línea* y pedí los dos enlaces.
5. Carpeta de **Clases grabadas** (enlace a Drive o YouTube no listado); Moodle no es buen sitio para alojar videos largos.

Tema 0 (general): Anuncios, Programa y evaluación (`docs/programa.md`, `docs/evaluacion.md`), Foro de consultas (el foro de Moodle ya viene incluido), Glosario y Diagnóstico inicial (la actividad **Consulta/Cuestionario** de Moodle sirve para las 10–15 preguntas anónimas; o enlazá `diagnostico/index.html`).

## 3. Rúbricas y notas
- Rúbricas R1, R2 e INT: `docs/rubricas.md` → crear en cada **Tarea** (*Método de calificación → Rúbrica*).
- Ponderación: teoría 30 % (mejores 6 de 8 quizzes), práctica 50 %, integrador 20 %. En *Calificaciones → Configuración* usá **categorías**: *Teoría* (agregación: mejores 6 calificaciones), *Práctica*, *Integrador*.
- Escala sugerida: 1 (<60) · 2 (60–69) · 3 (70–80) · 4 (81–90) · 5 (≥91). Ajustar al reglamento vigente.

## 4. Asistencia y calendario
- **Asistencia:** actividad *Asistencia* (si la facultad tiene el plugin) o BigBlueButton con registro. Los envíos automáticos del Apps Script no se trasladan a Moodle.
- **Calendario:** cada reunión y tarea crea su evento solo. Opcional: importar el `.ics` del aula como calendario personal.

## 5. Qué conviene dejar fuera de Moodle
- **Aula virtual propia (GitHub Pages) y Firebase:** Moodle ya cubre cuentas, notas y progreso; mantenerlos duplica el trabajo. Dejá el sitio como **material de consulta** (enlace desde Moodle) y los laboratorios en Colab.
- Efectos visuales y panel docente: no se trasladan.

## 6. Datos personales
No subas a Moodle el listado de estudiantes con cédulas ni los resultados individuales del diagnóstico desde este repositorio; usá las matrículas de Moodle.
