# Pruebas del aula virtual (extremo a extremo)

Requieren Node 18+, `playwright` y (para Firebase) Java 11+ y `firebase-tools`.

```bash
python tools/build_site.py && python tools/build_aula.py     # genera site/
cd site && python -m http.server 8765 &                      # sirve el aula en http://localhost:8765/aula/

# 1) Modo demostración (sin servidor)
node tests/aula_e2e_demo.js

# 2) Modo real contra los emuladores de Firebase (usa firebase/firestore.rules)
cd firebase && firebase emulators:start --only auth,firestore --project demo-cvd &
node tests/aula_e2e_firebase.js
```
La prueba de Firebase cubre: registro con datos personales, verificación de correo, persistencia, cédula duplicada,
recuperación y cambio de contraseña, panel docente y los intentos de acceso indebido a las reglas de Firestore (deben dar 403).
No cubre el ingreso con Google (requiere un proyecto real).
