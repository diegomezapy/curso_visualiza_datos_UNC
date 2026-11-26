# Seguimiento semanal del aula Git

El panel docente muestra, por estudiante, los intentos de quiz, el promedio formativo de esos intentos, los temas y respuestas de los foros y la última actividad de la semana en curso. El resumen se descarga en Excel. Se usan únicamente eventos con fecha registrada; la marca general de progreso no permite reconstruir lo ocurrido en una semana. Las calificaciones oficiales siguen en la planilla de notas y en Moodle.

Cada lunes por la mañana, un proyecto **privado e independiente** de Google Apps Script puede enviar al correo registrado un resumen de la semana anterior y una invitación a continuar. El estudiante desactiva esos correos desde «Mi perfil». El docente pausa la programación y fija la fecha final desde el panel. Ningún token, credencial ni dato personal se publica en GitHub Pages.

## Activación

1. Publicar `firebase/firestore.rules` del repositorio. Las rutas `seguimiento/configuracion` y `seguimiento_envios/*` solo son legibles para el docente verificado. El navegador del estudiante no puede acceder a esos registros.
2. Crear o actualizar un proyecto privado de Apps Script con los dos archivos de `appsscript_seguimiento/`. El manifiesto solicita solo Firestore, solicitudes HTTP, envío de correo y gestión de activadores. El script debe ejecutarse con una cuenta que tenga permiso IAM sobre el proyecto Firestore `cursovisualizadatosunc`.
3. En el editor de Apps Script ejecutar `diagnosticarSeguimiento()`. Debe devolver `accesoFirestore: true` y el número esperado de estudiantes. Luego ejecutar `enviarPruebaSeguimiento()`, que envía un ejemplo sintético únicamente al docente.
4. Ejecutar `instalarSeguimientoSemanal()` una sola vez. Crea un activador los lunes dentro de la franja de las 08:00, en `America/Asuncion`.
5. En el panel docente, activar «Enviar resúmenes semanales» y guardar la fecha final. La configuración inicial es inactiva. Revisar en el mismo panel el estado de los correos de la semana anterior.

Cada envío crea primero un registro con clave `semana_inicio + uid`. Un segundo intento omite esa clave para evitar duplicados. Si un envío queda en «preparando», debe revisarse manualmente antes de volver a procesar la semana. La cuota diaria de MailApp detiene el lote cuando no quedan destinatarios disponibles. El registro guarda conteos y estado, no el cuerpo del correo.

## Verificación

- `node tests/seguimiento_test.mjs` comprueba resumen, exclusión voluntaria, activador y que una segunda ejecución no reenvíe.
- `node --check aula/aula.js && node --check aula/backend.js && node --check aula/seguimiento.mjs` comprueba sintaxis del panel.
- El despliegue se considera operativo solo al confirmar el diagnóstico, la prueba al docente y la presencia del activador en Apps Script. Un cambio guardado en el panel por sí solo no programa envíos.

Fuentes: [activadores de Apps Script](https://developers.google.com/apps-script/guides/triggers/installable), [MailApp](https://developers.google.com/apps-script/reference/mail/mail-app), [API REST de Firestore](https://firebase.google.com/docs/firestore/use-rest-api).
