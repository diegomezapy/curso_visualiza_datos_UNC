# Aula virtual: guía de uso

**URL:** https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/ · **Drive:** carpeta `AULA_VIRTUAL_CURSO_VISUALIZA_DATOS_UNC`

## Qué incluye
- 8 módulos con objetivos, recursos, laboratorio en Google Colab, actividades con casilla de avance y **autoevaluación con rúbrica**.
- 8 quizzes autocorregidos (40 preguntas) con retroalimentación; reintentos ilimitados (cuenta el mejor).
- **Mis notas:** teoría (30), práctica (50), integrador (20), total y escala sugerida 1-5.
- **Recursos:** carpetas de Drive, datasets, documentos, glosario (25 términos).
- **Foros de discusión:** general y por módulo, con respuestas, “resuelto”/solución y moderación ([foros.md](foros.md)).
- **Panel docente:** importa reportes de estudiantes, registra notas, calcula la final y exporta CSV.

## Cuentas y acceso
- **Primer acceso:** el estudiante elige *Crear cuenta*, completa sus datos (nombres y apellidos, cédula, fecha de nacimiento, sexo, nacionalidad, departamento y ciudad, dirección, teléfono, institución, profesión, cohorte) y elige su propia contraseña; recibe un correo de verificación. También puede **ingresar con Google** y completar los datos la primera vez.
- **Recuperación:** “¿Olvidaste tu contraseña?” → enlace por correo. **Cambio de contraseña:** en *Mi perfil*.
- **Cédula única:** no se permiten dos cuentas con la misma cédula. La cédula no se puede editar (solo el docente puede corregirla).
- Requiere conectar Firebase: ver [configurar_firebase.md](configurar_firebase.md). Sin eso, el aula corre en **modo demostración** (solo navegador).

## Flujo del estudiante
1. Crea su cuenta y entra. 2. Estudia el módulo, abre el lab en Colab, hace el quiz. 3. Entrega sus trabajos en `ENTREGAS_ESTUDIANTES` (Drive) o por formulario, con el nombre sugerido. 4. Consulta sus notas en *Mis notas* (se actualizan cuando el docente las carga).

## Flujo del docente
1. Crea su cuenta (su correo debe estar en la colección `docentes`). 2. **Panel docente** lista a todos los estudiantes con su avance y quizzes. 3. Carga las notas de cada actividad (se guardan al instante). 4. **Exporta la planilla CSV** con datos personales y notas.

## Configuración (`aula/config.json`)
- `firebase`: credenciales web del proyecto (ver guía). `formulario_entregas`: URL de un Google Form con subida de archivos. `fechas`: fecha de cada módulo. IDs de carpetas de Drive.
- Luego: `python tools/build_aula.py` (se ejecuta solo en el workflow de Pages).

## Limitaciones y recomendaciones
- **Integridad de los quizzes:** se corrigen en el navegador y sus respuestas están en el código de la página. Para evaluación formal, aplicarlos en sesión sincrónica o con Google Forms.
- **Privacidad de Drive:** si la carpeta raíz permite “cualquiera con el enlace puede *editar*”, cualquiera puede borrar o ver entregas. Compartir como **Lector** y recibir entregas por **Google Form**. No guardar calificaciones ni datos personales en un Drive compartido.
