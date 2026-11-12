# NotebookLM · protocolo para crear lecturas, audios y videos del curso

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
