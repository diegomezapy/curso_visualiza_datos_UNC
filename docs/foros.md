# Foros de discusión por unidad

El aula Git ofrece ocho foros en `#/foros`, uno por cada sección numerada de la interfaz. Cada foro plantea una decisión concreta, pide sustentarla con evidencia y requiere una réplica que ponga a prueba otra propuesta. Las consignas se mantienen en `aula/foros.json` y se publican mediante `tools/build_aula.py`. Hay enlaces al foro en Inicio, el menú y la página de cada unidad.

La Unidad 3 conserva `#/foro/prensa` y los mensajes existentes en `foro_prensa`. Muestra, con atribución y enlace al artículo, las imágenes originales servidas por Última Hora y ABC Color. Su consigna propia está en `aula/tareas/ejercicio_s3_prensa_paraguaya.html`.

La entrega evaluada se registra en la actividad S3 de `#/sesion/3`: cada estudiante guarda el enlace HTTPS de su informe en RPubs o de su PDF compartido en Google Drive. El enlace queda en su progreso y se abre desde la ficha del estudiante en el panel docente; la calificación se carga en el mismo panel. La planilla de entregas S3 se descarga en CSV y Excel. Esta entrega del aula Git no requiere Moodle.

Cada estudiante con cuenta de Firebase verificada y perfil completo puede publicar un análisis inicial **por unidad** y responder a otros temas. El nombre visible procede del perfil; el correo y la cédula no aparecen en los foros. El docente puede eliminar mensajes desde la interfaz. Las unidades 1, 2 y 4 a 8 usan `foros/{unidad}/mensajes/{id}`; la Unidad 3 mantiene `foro_prensa`. Las reglas están en `firebase/firestore.rules` y deben publicarse antes del frontend.

Los foros nuevos se muestran como aperturas sin fecha de cierre en el calendario. La publicación del foro no genera automáticamente correos por cada respuesta nueva.

Para futuras publicaciones o cambios de acceso, volver a desplegar `firebase/firestore.rules` antes de publicar la web. El sitio se construye con `tools/build_aula.py` y se despliega con el flujo de GitHub Pages.
