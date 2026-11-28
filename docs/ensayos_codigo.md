# Ensayos de código del aula

Cada una de las ocho unidades contiene diez pasos breves. Cada paso puede resolverse en R o Python, y el estudiante puede repetirlo en el otro lenguaje. Los dos usan la misma consigna y una variable `respuesta` verificable. Los intentos son ilimitados y cada paso ofrece tres pistas progresivas. Los errores de sintaxis o ejecución no suman intentos.

La secuencia comienza con datos ingresados en el editor. Más adelante, el aula descarga CSV sintéticos desde `aula/datos-codigo/` y los monta como `datos.csv` en el entorno de ejecución. Continúa con barras, comparación de períodos, filtros, funciones reutilizables, puntos proporcionales con coordenadas y paneles comparativos. El ensayo publicado originalmente queda como paso 10 de cada unidad y conserva su progreso previo.

## Implementación

- `aula/codigo-pasos.mjs` y `aula/codigo-retos.mjs`: consignas, datos de inicio, respuestas y pistas.
- `aula/codigo.mjs`: interfaz de dos columnas, consola siempre visible, gráficos acotados, verificación y progreso.
- `aula/codigo-python-worker.mjs`: ejecución de Python en un worker mediante Pyodide 314.0.8.
- R se ejecuta mediante webR 0.6.1 en su worker interno.
- Los motores se descargan al ejecutar por primera vez y requieren conexión a internet. Los CSV se sirven desde el mismo sitio. El botón **Detener** y un límite de 35 segundos permiten reiniciar una ejecución bloqueada.

La comprobación es formativa: verifica el valor de `respuesta` y, cuando corresponde, la existencia del gráfico. No evalúa la calidad visual del gráfico. El estado por paso y lenguaje (`hecho`, `intentos`, `pistas`) se guarda en `progreso/{uid}` para estudiantes autenticados. Completar un paso en cualquiera de los lenguajes suma una vez al avance del módulo; no entra en la nota oficial. El código editado permanece en memoria durante la navegación de la página; al recargar se recupera el ejemplo inicial. La práctica de invitados no se guarda.

## Verificación local

```bash
node --test tests/codigo_retos.test.mjs
python3 tools/build_site.py
python3 tools/build_aula.py
python3 -m http.server 8765 --directory site
```

Abrir `http://localhost:8765/aula/index.html`, ingresar o explorar como invitado y probar un reto en cada lenguaje. El build de GitHub Pages ejecuta los mismos generadores y copia los módulos y CSV al sitio generado.
