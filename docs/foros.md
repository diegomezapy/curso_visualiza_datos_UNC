# Foro de discusión de la Unidad 3

El aula Git tiene un foro integrado en `#/foro/prensa` para discutir las visualizaciones de prensa paraguaya del ejercicio S3. Muestra, con atribución y enlace al artículo, las imágenes originales servidas por los medios. La consigna propia del aula Git está en `aula/tareas/ejercicio_s3_prensa_paraguaya.html` y se publica mediante `tools/build_aula.py`.

La entrega evaluada se registra en la actividad S3 de `#/sesion/3`: cada estudiante guarda el enlace HTTPS de su informe en RPubs o de su PDF compartido en Google Drive. El enlace queda en su progreso y se abre desde la ficha del estudiante en el panel docente; la calificación se carga en el mismo panel. La planilla de entregas S3 se descarga en CSV y Excel. Esta entrega del aula Git no requiere Moodle.

Cada estudiante con cuenta de Firebase verificada y perfil completo puede publicar un análisis inicial y responder a los temas de otras personas. El nombre visible procede del perfil; el correo y la cédula no aparecen en el foro. El docente puede eliminar mensajes desde la interfaz. Los datos se guardan en `foro_prensa` y las reglas están en `firebase/firestore.rules`.

El aviso inicial a los estudiantes se envía de forma individual a los correos de los usuarios matriculados en Moodle después de comprobar que la página y las reglas están publicadas. La publicación del foro no genera automáticamente avisos por cada respuesta nueva.

Para futuras publicaciones o cambios de acceso, volver a desplegar `firebase/firestore.rules` antes de publicar la web. El sitio se construye con `tools/build_aula.py` y se despliega con el flujo de GitHub Pages.
