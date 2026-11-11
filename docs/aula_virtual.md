# Aula virtual: guía de uso

**URL:** https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/ · **Drive:** carpeta `AULA_VIRTUAL_CURSO_VISUALIZA_DATOS_UNC`

## Qué incluye
- 8 módulos con objetivos, recursos, laboratorio en Google Colab, actividades con casilla de avance y **autoevaluación con rúbrica**.
- 8 quizzes autocorregidos (40 preguntas) con retroalimentación; reintentos ilimitados (cuenta el mejor).
- **Mis notas:** teoría (30), práctica (50), integrador (20), total y escala sugerida 1-5.
- **Recursos:** carpetas de Drive, datasets, documentos, glosario (25 términos).
- **Panel docente:** importa reportes de estudiantes, registra notas, calcula la final y exporta CSV.

## Flujo del estudiante
1. Completa su **perfil** (nombre, C.I.). 2. Estudia el módulo, abre el lab en Colab, hace el quiz. 3. Entrega sus trabajos en `ENTREGAS_ESTUDIANTES` (Drive) con el nombre sugerido. 4. Descarga su **reporte (.json)** en *Mis notas* y lo sube a la carpeta de entregas. 5. Importa la **hoja de calificaciones** que le devuelve el docente.

## Flujo del docente
1. Descarga los `reporte_*.json` de Drive. 2. En **Panel docente** los arrastra (la huella ✔ indica que no fueron editados). 3. Carga las notas de cada actividad calificada con las rúbricas. 4. **Exporta CSV** (planilla oficial) y, por estudiante, la **Hoja** (`calificaciones_*.json`) para devolverla.
5. Respaldo: *Exportar copia* del panel (los datos se guardan solo en el navegador del docente).

## Configuración (`aula/config.json`)
- `formulario_entregas`: URL de un Google Form con campo de subir archivo (recomendado, ver abajo).
- `fechas`: fecha límite/sesión por módulo (texto libre).
- IDs de las carpetas de Drive.
Luego: `python tools/build_aula.py` (se ejecuta solo en el workflow de Pages).

## Limitaciones y recomendaciones
- **Sin servidor:** el progreso vive en el navegador de cada estudiante; se comparte mediante el reporte. No hay inicio de sesión.
- **Integridad:** los quizzes se resuelven en el navegador y sus respuestas están en el código de la página; la huella detecta ediciones accidentales, no manipulación deliberada. Para evaluación formal, aplicar quizzes en sesión sincrónica o con Google Forms.
- **Privacidad de Drive:** si la carpeta raíz está compartida con “cualquiera con el enlace puede *editar*”, cualquiera puede borrar o ver todas las entregas. Recomendado: compartir la raíz como **Lector** y usar un **Google Form** (con subida de archivos) para recibir entregas de forma privada. No guardar calificaciones en un Drive compartido.
