# Foros de discusión del aula

Foro integrado en el aula (menú **💬 Foros**): un foro **General** y uno por **módulo** (1–8). Usa las mismas cuentas del aula y la misma base de datos (Firestore), con reglas de seguridad propias.

## Qué pueden hacer
| Rol | Acciones |
|---|---|
| **Estudiante** | Crear temas, responder, buscar, filtrar por módulo, marcar su tema como **resuelto**, marcar una respuesta como **solución** (solo el autor del tema), eliminar sus propias respuestas y sus temas sin respuestas. |
| **Docente** | Todo lo anterior **más**: **fijar** temas 📌, **cerrar** 🔒 (no admite respuestas), reabrir, marcar solución/resuelto en cualquier tema y **eliminar** cualquier tema o respuesta. Sus respuestas llevan la etiqueta *Docente* (no se puede falsificar). |

Cada módulo tiene un botón **“Foro del módulo N”**. Los enlaces `https://…` se vuelven clicables; el resto del texto se muestra como texto plano (sin HTML).

## Seguridad (reglas de Firestore)
Solo las cuentas con perfil (o docentes) pueden leer o escribir. Las reglas impiden: suplantar al autor, crear temas ya fijados/cerrados, fijar/cerrar/editar/borrar temas ajenos, falsificar la etiqueta de docente, responder en temas cerrados, marcar “solución” sin ser el autor del tema y alterar contadores. Se probaron 14 intentos de abuso contra los emuladores de Firebase (`tests/aula_e2e_foro.js`).

> ⚠️ **Hay que publicar las reglas nuevas:** copiá `firebase/firestore.rules` en **Firestore → Reglas → Publicar**. Sin eso el foro muestra “No tenés permiso”.

## Moderación y límites
- No hay filtro automático de contenido: moderá desde el rol docente (eliminar/cerrar). Títulos de 4–120 caracteres y mensajes de hasta 5.000.
- El **contador de respuestas** lo actualiza el cliente: un estudiante malintencionado podría sumar/restar 1 sin responder (efecto cosmético). 
- **Sin notificaciones por correo** por ahora (podría agregarse con Apps Script: avisar al autor cuando alguien responde).
- Todavía no se pueden **editar** mensajes ya publicados (se elimina y se vuelve a publicar).
- Las consultas leen hasta 300 temas: sobra para un curso; para uso masivo habría que paginar.
- El nombre visible es “Nombre + inicial del apellido” (p. ej. *Ana B.*).

## Alternativas (si no se quiere usar el foro del aula)
GitHub Discussions (exige cuenta de GitHub), Google Chat/Grupos de Google/Classroom (fuera del aula) o Giscus (depende de GitHub Discussions).
