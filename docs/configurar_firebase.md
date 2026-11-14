# Activar el aula en modo real (Firebase)

Mientras `aula/config.json` tenga `"firebase": {}`, el aula funciona en **modo demostración** (cuentas guardadas solo en el navegador). Para que cada estudiante tenga cuenta real, siga estos pasos (≈15 minutos, plan gratuito *Spark*).

## 1. Crear el proyecto
1. Entrar a <https://console.firebase.google.com> con la cuenta Google del docente → **Agregar proyecto** (p. ej. `curso-visualizacion-unc`). Google Analytics: desactivar.

## 2. Autenticación
1. **Build → Authentication → Comenzar**.
2. **Método de acceso**: habilitar **Correo electrónico/contraseña** y **Google** (elegir correo de soporte).
3. **Configuración → Dominios autorizados**: agregar `diegomezapy.github.io`.
4. **Plantillas** (verificación de correo, restablecer contraseña): cambiar el idioma a **Español** y, si desea, el nombre del remitente.

## 3. Base de datos
1. **Build → Firestore Database → Crear base de datos** → modo producción → región `southamerica-east1` (São Paulo).
2. Pestaña **Reglas** → pegar el contenido de [`firebase/firestore.rules`](https://github.com/diegomezapy/curso_visualiza_datos_UNC/blob/main/firebase/firestore.rules) → **Publicar**.

## 4. Registrar al docente
1. En Firestore: **Iniciar colección** `docentes` → ID del documento = **correo del docente, en minúsculas** → agregar un campo cualquiera (`activo` = true).
2. El docente debe crear su cuenta en el aula y **verificar su correo**; entonces aparece el menú **Panel docente**.
   (Un docente sin perfil de estudiante no necesita completar datos personales.)
3. Para mostrar y descargar en Excel las hojas externas en el panel, agregar al mismo documento un mapa `planillas` con los campos opcionales `diagnostico`, `agenda` y `entregas`. Cada valor debe ser la URL privada de una hoja de Google Sheets (`https://docs.google.com/spreadsheets/d/.../edit`). `agenda` corresponde a las pestañas **Asistencia** y **MiniEval** del libro de Apps Script. No poner estos enlaces en `aula/config.json`, porque ese archivo se publica en GitHub Pages. Conceder acceso al docente directamente en Google Sheets.

## 5. Conectar el sitio
1. **Configuración del proyecto → Tus apps → Web (`</>`)** → registrar app → copiar `firebaseConfig`.
2. Pegar en `aula/config.json`:
```json
"firebase": { "apiKey": "...", "authDomain": "TU-PROYECTO.firebaseapp.com", "projectId": "TU-PROYECTO", "appId": "..." }
```
   (La `apiKey` de Firebase web **no es un secreto**; la seguridad la dan las reglas.)
3. `git commit` + `git push`: el workflow vuelve a publicar el sitio.

## 6. Probar
Crear una cuenta de prueba → debe llegar el correo de verificación → ingresar → verificar en Firestore que existen `usuarios/{uid}` y `progreso/{uid}`.

## Qué se guarda y quién lo ve
| Colección | Contenido | Estudiante | Docente |
|---|---|---|---|
| `usuarios/{uid}` | datos personales (nombres, apellidos, cédula, fecha de nacimiento, sexo, residencia, contacto, consentimiento) | lee y edita lo suyo (**la cédula no**) | lee todo |
| `progreso/{uid}` | actividades hechas, quizzes, autoevaluaciones | lee/escribe lo suyo | lee todo |
| `calificaciones/{uid}` | notas oficiales | **solo lee** lo suyo | lee y escribe |
| `cedulas/{n}` | índice para impedir cédulas duplicadas | nadie lo lee | nadie lo lee |
| `docentes/{correo}` | lista de docentes | — | solo se edita en la consola |
| `respuestas_quiz/{id}` | respuestas de cada intento de quiz de práctica | lee las suyas | lee todas |

Las reglas de `firebase/firestore.rules` deben estar publicadas **antes** de activar en Pages una versión que guarda intentos en `respuestas_quiz`. Los intentos previos no tenían respuestas por pregunta y no se pueden reconstruir.

## Contraseñas y recuperación
- Cada estudiante elige su contraseña al registrarse (mínimo 8, con letras y números). **No se usa una contraseña inicial común** (p. ej. `123456`): cualquiera que conozca el nombre de un compañero podría entrar a su cuenta y ver su cédula y fecha de nacimiento.
- **Recuperación:** “¿Olvidaste tu contraseña?” envía un enlace por correo (Firebase). **Cambio:** *Mi perfil → Cambiar contraseña*. Quien ingresa con Google no maneja contraseña en el aula.
- Si un estudiante pierde acceso a su correo, el docente puede eliminar/restablecer su cuenta desde **Authentication** en la consola.

## Cuidado de los datos personales
- Los datos de cédula, fecha de nacimiento y sexo son **sensibles**: usar solo para fines del curso, exportar CSV o Excel únicamente si es necesario y no compartirlos en carpetas públicas de Drive.
- El formulario incluye una cláusula de consentimiento; ajústela al texto que exija la institución (`CONSENT` en `aula/aula.js`).
- Para eliminar a un estudiante: borrar su cuenta en Authentication y sus documentos en `usuarios`, `progreso`, `calificaciones` y `cedulas/{su cédula}`.

## Mantenimiento
- Regenerar el SDK empaquetado: `cd tools/firebase_vendor && npm install && npm run build` (genera `aula/vendor/firebase.js`).
- Pruebas locales con emuladores: ver [`tests/README.md`](https://github.com/diegomezapy/curso_visualiza_datos_UNC/blob/main/tests/README.md).
