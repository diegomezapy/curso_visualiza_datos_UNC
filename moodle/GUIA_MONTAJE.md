# Montaje del curso en Moodle (FACET-UNC)

Las páginas de esta carpeta se generan con `python tools/build_moodle.py`. El 2026-11-24 se publicaron en el curso FACET-UNC 271 la página de recursos generales y una página de recursos por unidad. El generador elimina caracteres fuera del plano básico Unicode: esa instalación rechazó una versión con emojis al guardar en su base de datos.

| Sección de Moodle | Página publicada |
|---|---|
| Inicio y presentación | [Recursos generales del curso](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6814) |
| Unidad 1 | [Recursos de la unidad 1](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6816) |
| Unidad 2 | [Recursos de la unidad 2](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6817) |
| Unidad 3 | [Recursos de la unidad 3](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6818) |
| Unidad 4 | [Recursos de la unidad 4](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6819) |
| Unidad 5 | [Recursos de la unidad 5](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6820) |
| Unidad 6 | [Recursos de la unidad 6](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6821) |
| Unidad 7 | [Recursos de la unidad 7](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6822) |
| Unidad 8 | [Recursos de la unidad 8](https://www.facet-unc.edu.py/moodle/mod/page/view.php?id=6823) |

La réplica usa enlaces a las mismas fichas, presentaciones, laboratorios, prácticas, lecturas y videos recomendados que el aula Git. Las cinco grabaciones presentes en Moodle se enlazan desde el aula Git mediante `aula/clases_moodle.json`, con el control de acceso del recurso Moodle.

## 1. Qué importar y qué pegar
| Archivo | Dónde va en Moodle |
|---|---|
| `preguntas/banco_completo.xml` | *Más → Banco de preguntas → Importar* → formato **Moodle XML**. Crea 8 categorías (Sesión 1…8) con 40 preguntas, con retroalimentación. |
| `preguntas/quiz_sesion_N.xml` | Igual, pero solo una sesión (si preferís ir de a una). |
| `glosario.xml` | Actividad **Glosario** → *Importar entradas* (XML). Activá el autoenlace. |
| `paginas/sesion_N.html` | Recurso **Página** (o Etiqueta) de la sesión N → editor HTML → botón `</>` → pegar. |
| `paginas/recursos_generales.html` | Página de recursos de la sección **Inicio y presentación**. |

## 2. Estructura sugerida (un tema de Moodle por sesión)
Nombre del tema: `Sesión N · Título · fecha`. En cada uno, en este orden:
1. **Página** con `paginas/sesion_N.html` (objetivos, Colab, .Rmd, lecturas, videos).
2. **Reunión virtual**: BigBlueButton/Meet/Zoom según tenga la facultad. Horarios: viernes 18:00–22:00, sábados 08:00–12:00, del 13/11 al 05/12/2026.
3. **Cuestionario** de la sesión (importado en el paso 1): intentos 2, calificación = mejor intento, retroalimentación después del intento, sin límite de tiempo estricto.
4. **Tarea** de entrega (donde corresponda): activar *Enviar comentarios*, calificación con **Rúbrica** y finalización por entrega. Para los laboratorios, usar los enlaces a RPubs y Colab indicados en cada consigna. Para el trabajo final, pedir el enlace a la subcarpeta personal en [Drive](https://drive.google.com/drive/folders/1spQXcXcYkMJY1RnCgnUsYdZ-l0DSAUt5?usp=sharing); registrar el producto y la defensa por separado (18 y 12 puntos).
5. Carpeta de **Clases grabadas** (enlace a Drive o YouTube no listado); Moodle no es buen sitio para alojar videos largos.

Tema 0 (general): Anuncios, Programa y evaluación (`docs/programa.md`, `docs/evaluacion.md`), Foro de consultas (el foro de Moodle ya viene incluido), Glosario y Diagnóstico inicial (la actividad **Consulta/Cuestionario** de Moodle sirve para las 10–15 preguntas anónimas; o enlazá `diagnostico/index.html`).

## 3. Rúbricas y notas
- Rúbricas R1 y R2: `docs/rubricas.md`; criterios del trabajo final: `docs/proyecto_integrador.md`; foros y coedición: `docs/evaluacion.md`. Configurá la rúbrica correspondiente en cada tarea calificada.
- Ponderación: cuestionarios 25 % (promedio de los seis mejores porcentajes disponibles), foros 25 %, trabajo práctico final 30 % (producto 18 + defensa 12) y coedición 20 %. En *Calificaciones → Configuración* creá estas cuatro categorías. Los laboratorios y mini proyectos previos quedan como actividades formativas y no se suman a la nota final.
- Escala sugerida: 1 (<60) · 2 (60–69) · 3 (70–80) · 4 (81–90) · 5 (≥91). Ajustar al reglamento vigente.

## 4. Asistencia y calendario
- **Asistencia:** actividad *Asistencia* (si la facultad tiene el plugin) o BigBlueButton con registro. Los envíos automáticos del Apps Script no se trasladan a Moodle.
- **Calendario:** cada reunión y tarea crea su evento solo. Opcional: importar el `.ics` del aula como calendario personal.

## 5. Qué conviene dejar fuera de Moodle
- **Aula virtual propia (GitHub Pages) y Firebase:** Moodle ya cubre cuentas, notas y progreso; mantenerlos duplica el trabajo. Dejá el sitio como **material de consulta** (enlace desde Moodle) y los laboratorios en Colab.
- Efectos visuales y panel docente: no se trasladan.

## 6. Datos personales
No subas a Moodle el listado de estudiantes con cédulas ni los resultados individuales del diagnóstico desde este repositorio; usá las matrículas de Moodle.
