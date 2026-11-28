# Aula virtual: guía de uso

**URL:** https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/ · **Drive:** carpeta `AULA_VIRTUAL_CURSO_VISUALIZA_DATOS_UNC`

## Qué incluye
- 8 módulos con objetivos, recursos, laboratorio en Google Colab, actividades con casilla de avance y **autoevaluación con rúbrica**.
- 8 quizzes autocorregidos (40 preguntas) con retroalimentación; reintentos ilimitados (cuenta el mejor).
- **Mis notas:** cuestionarios (25), foros (25), trabajo final (30), coedición (20), total y escala sugerida 1-5 una vez cargadas todas las notas.
- **Recursos:** carpetas de Drive, datasets, documentos, glosario (25 términos).
- **Panel docente:** consulta registros, respuestas de quizzes y autoevaluaciones; registra notas y descarga cada planilla en CSV o Excel (.xlsx).

## Foro y calendario

- Los **ocho foros por unidad** se abren desde Inicio, el menú lateral o cada unidad: `#/foros`. El foro de prensa de la Unidad 3 conserva `#/foro/prensa` y sus mensajes. Quien visita como invitado ve las consignas y puede iniciar sesión desde cada foro; los mensajes requieren una cuenta verificada.
- El calendario incluye las ocho clases sincrónicas y las aperturas confirmadas de la tarea S3 y los ocho foros. La tarea y los foros enlazan a sus espacios propios del aula Git; la ficha de cada evento sigue disponible mediante «Detalles». El acceso a la videollamada de las clases aún usa el recurso de reunión institucional configurado en Moodle.
- Las aperturas de la tarea S3 y de los ocho foros se muestran como eventos de día completo, **sin fecha de vencimiento**. No se asignan plazos a tareas o quizzes que no tengan uno confirmado. Si se configura la agenda de Apps Script, sus eventos se agregan a la agenda base y pueden actualizar eventos existentes por ID.
- La actividad S3 se entrega dentro del aula Git mediante un enlace a RPubs o a un PDF en Google Drive compartido con el docente. El foro muestra las imágenes originales de los dos artículos, servidas por los medios y atribuidas con enlace a cada publicación.

## Cuentas y acceso
- **Primer acceso:** el estudiante elige *Crear cuenta*, completa sus datos (nombres y apellidos, cédula, fecha de nacimiento, sexo, nacionalidad, departamento y ciudad, dirección, teléfono, institución, profesión, cohorte) y elige su propia contraseña; recibe un correo de verificación. También puede **ingresar con Google** y completar los datos la primera vez.
- **Recuperación:** “¿Olvidaste tu contraseña?” → enlace por correo. **Cambio de contraseña:** en *Mi perfil*.
- **Cédula única:** no se permiten dos cuentas con la misma cédula. La cédula no se puede editar (solo el docente puede corregirla).
- Requiere conectar Firebase: ver [configurar_firebase.md](configurar_firebase.md). Sin eso, el aula corre en **modo demostración** (solo navegador).

## Flujo del estudiante
1. Crea su cuenta y entra. 2. Estudia el módulo, abre el lab en Colab, hace el quiz. 3. Entrega sus trabajos en `ENTREGAS_ESTUDIANTES` (Drive) o por formulario, con el nombre sugerido. 4. Consulta sus notas en *Mis notas* (se actualizan cuando el docente las carga).

## Flujo del docente
1. Crea su cuenta (su correo debe estar en la colección `docentes`). 2. **Panel docente** lista a los estudiantes con su avance y quizzes. 3. Descarga por separado en CSV o Excel el registro de usuarios, las respuestas de los quizzes de práctica, las autoevaluaciones y las calificaciones. 4. Abre o descarga en Excel las hojas externas configuradas para diagnóstico, asistencia, mini evaluaciones y otros formularios. 5. Carga las notas de cada actividad (se guardan al instante). La evaluación formal se administra en Moodle.

Las respuestas por pregunta se conservan desde la activación de esta función. Los intentos anteriores solo guardaron fecha y porcentaje; la exportación los marca como `histórico sin detalle`.

## Configuración (`aula/config.json`)
- `firebase`: credenciales web del proyecto (ver guía). `formulario_entregas`: URL de un Google Form con subida de archivos. `fechas`: fecha de cada módulo. IDs de carpetas de Drive.
- Luego: `python tools/build_aula.py` (se ejecuta solo en el workflow de Pages).

## Limitaciones y recomendaciones
- **Integridad de los quizzes:** se corrigen en el navegador y sus respuestas están en el código de la página. Para evaluación formal, aplicarlos en sesión sincrónica o con Google Forms.
- **Privacidad de Drive:** la carpeta de trabajos prácticos actualmente permite editar a cualquier persona con el vínculo para que los estudiantes creen sus subcarpetas. Esa configuración también permite ver o alterar carpetas ajenas. No guardar calificaciones, datos personales, credenciales ni bases restringidas allí; conservar una copia independiente. Si se requiere privacidad por estudiante, usar un mecanismo de entrega con permisos individuales antes de cambiar el acceso.
- **Hojas externas:** los enlaces se leen del documento `docentes/{correo}` en Firestore y se muestran solo en el panel docente. Google Sheets conserva su propio control de acceso; el docente debe tener permiso directo a cada hoja.

## Clases grabadas

Menú **🎥 Clases grabadas** (`#/clases`). El aula **no aloja videos**: el docente sube la grabación a Google Drive (carpeta con acceso solo para el grupo) o a YouTube como *no listado* y carga el enlace desde esa misma pantalla (formulario visible solo para docentes).

- Acepta enlaces de YouTube (reproductor incrustado, capítulos clicables), de Drive (`/file/d/…`, vista previa incrustada) y cualquier otro `https` (botón "Abrir grabación").
- Capítulos: una línea por capítulo, `12:40 Título`.
- Cada alumno marca "Ya la vi"; se guarda en su progreso (`rec_<id>`).
- "Ocultar" es solo de interfaz: la regla de Firestore deja leer la colección a cualquier usuario con sesión. El control real de acceso es el del video en Drive/YouTube.
- **Hay que volver a publicar las reglas** (`firebase/firestore.rules`) en Firebase → Firestore → Reglas para habilitar la colección `clases`.

## Ocultar y mostrar elementos (docente)

Con la sesión de docente aparece el botón **👁 Edición** en la barra superior. Al activarlo, cada sección, tarjeta, ítem de lista y opción del menú lateral muestra un botón 👁 para ocultarlo o mostrarlo a los estudiantes.
- Por defecto **todo está visible**. Lo oculto se ve atenuado y con 🚫 para el docente; los estudiantes no lo ven (y si abren la dirección de una sección oculta, ven «Contenido no disponible»).
- La barra de edición muestra cuántos elementos hay ocultos, la lista y **Mostrar todo**.
- Se guarda en Firestore (`ajustes/visibilidad`); **hay que republicar `firebase/firestore.rules`**. Los estudiantes ven el cambio al navegar o recargar (se consulta cada minuto como máximo).
- Los elementos se identifican por la ruta y el título; si cambia el título de un bloque, hay que volver a ocultarlo.
- **Eliminar (🗑):** además de ocultar, el docente puede eliminar cualquier elemento (con confirmación). Deja de verse **para todos, también para el docente**, y va a la **Papelera** del modo edición, de donde se restaura uno por uno o todo junto. Para los elementos del aula es una eliminación *lógica* (el contenido sigue en los archivos del sitio; para quitarlo de verdad hay que borrarlo del repositorio).
- **Clases grabadas:** el botón «🗑 Eliminar» de cada clase la **borra de verdad** de Firestore (no se puede deshacer; el video en Drive/YouTube no se toca).
- Hay que republicar `firebase/firestore.rules` (se agregó el campo `eliminados` y el borrado de clases al docente).
- No es un control de seguridad: el contenido sigue en los archivos públicos del sitio.

## Orden de una sesión
Objetivos → Presentación (con su **Quiz de lectura pegado debajo**) → Infografía → Videos → Lecturas → Materiales → Actividades → Datos reales → Quiz de teoría → Para profundizar.

## Acceso como invitado

Cualquier persona puede **ver el curso sin cuenta**: en la pantalla de ingreso hay un botón «Entrar como invitado», y el enlace directo es `…/aula/index.html#/invitado` (también está en la portada del sitio).
- **Puede ver:** inicio, módulos (objetivos, presentación, infografía, videos, lecturas, materiales, actividades como lista), recursos, calendario, datos abiertos y «El tutor». Respeta lo que el docente ocultó con el modo edición.
- **No puede:** responder quizzes, marcar o entregar actividades, completar formularios (autoevaluaciones, diagnóstico, entregas), ver calificaciones, clases grabadas, perfil ni panel docente. Esas rutas muestran «Solo para estudiantes registrados». Tampoco ve la carpeta de entregas ni el tablero del diagnóstico.
- Al ingresar o crear cuenta se sale del modo invitado.
- **Límite:** el modo invitado es de solo lectura en la interfaz, no un control de seguridad: los materiales del aula son archivos públicos del sitio. Lo que sí se protege con reglas es la escritura (los invitados no tienen sesión, así que Firestore les niega cualquier lectura o escritura salvo `ajustes/visibilidad`, que es público).
- **Hay que republicar `firebase/firestore.rules`** para que los invitados respeten lo oculto. Sin eso ven todo.
- Las carpetas de Drive tienen sus propios permisos: revisá con quién está compartida cada una.

## Presentaciones incrustadas
Cada sesión puede tener una presentación con visor propio (diapositivas, texto accesible, PDF y PowerPoint). Hoy: sesión 1 (percepción gráfica, con infografía y Quiz 1B), sesión 2 (**elección de gráficos**, 20 diapositivas con datos reales de la EPHC 2025 y Quiz 2A; se regenera con `tools/eleccion_datos.R`, `tools/eleccion_figuras.R` y `tools/eleccion_pptx.py`) sesión 5 con **tres presentaciones** (la sesión admite varias: `PRESENTACIONES[n]` puede ser una lista; cada quiz de lectura indica `deck`): (1) **dashboards** con datos de aduanas, 17 diapositivas, código Python en RStudio y tableros plotly interactivos; Quiz 5A; se regenera con `tools/dashboards_datos.py`, `dashboards_figuras.py`, `dashboards_pptx.py` y `dashboards_rmd.py`) y (2) **tablero dinámico en RStudio con Shiny**, 14 diapositivas con capturas reales de la app en cada paso (`tools/tablero_capturas.py`, `tools/tablero_pptx.py`; app en `r/app_tablero_aduanas/`; Quiz 5B) y (3) **Looker Studio con el Censo Agropecuario Nacional 2022** (MAG, Volumen I), 17 diapositivas con maquetas de datos reales, datos en `aula/media/unidad5_looker/fuentes/datos/` y guía en `docs/looker_studio_can2022.md` (`tools/can_datos.py`, `looker_figuras.py`, `looker_pptx.py`; Quiz 5C) y sesión 4, primera de la Unidad 2 (**ggplot2, capa por capa**, 24 diapositivas con datos reales de la EPHC; con el ejercicio de la EPHC y los quizzes 4A y 4B).
- Se registran en `PRESENTACIONES` de `tools/build_aula.py`; los archivos están en `aula/media/<carpeta>/`.
- Para regenerar una: `python tools/procesar_presentacion.py <carpeta>` (requiere LibreOffice, `pdftoppm` y Pillow) a partir del `.pptx` de `fuentes/`.
- La de ggplot2 se construye con código: `tools/ggplot_spec.py` (contenido y código de cada paso) → `tools/ggplot_pasos_a_archivos.py` → `Rscript tools/ggplot_figuras.R` (ejecuta ese mismo código y guarda las figuras) → `python tools/ggplot_pptx.py`. Los datos agregados salen de `tools/ggplot_datos.R` (requiere los CSV del INE).
