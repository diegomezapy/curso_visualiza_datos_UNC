# Diagnóstico, agenda, asistencia y mini-evaluaciones (Google Apps Script)

Un solo proyecto de **Google Apps Script**, vinculado a **una hoja de cálculo**, hace cuatro cosas:

| Función | Cómo funciona |
|---|---|
| **Diagnóstico inicial** | El cuestionario (`/diagnostico/`) envía cada respuesta al script, que la valida, calcula el puntaje **en el servidor** y la guarda en la hoja. |
| **Tablero en vivo** | El mismo script publica un tablero interactivo y una API de datos anonimizados (`?action=datos` / `?action=csv`). |
| **Agenda y calendario** | La pestaña *Agenda* alimenta el calendario del aula (`?action=agenda`). |
| **Asistencia y mini-evaluación** | Un activador de tiempo envía, **a la hora de cada clase/tutoría**, un correo con un enlace **personal** de asistencia (válido solo en el horario del evento) y, **al terminar la clase**, otro con una mini-evaluación de 3 preguntas **que no suma puntos**. |

```
Cuestionario web ─POST→ Apps Script ─→ Hoja "Respuestas" ─┬→ Tablero en vivo
                                                           ├→ Looker Studio (pestaña "Looker")
                                                           ├→ R → RPubs  (r/00_diagnostico.Rmd)
                                                           └→ Python → Colab (lab00_diagnostico)
Hoja "Agenda" + "Estudiantes" ─→ activador (cada minuto) ─→ correos de asistencia y mini-evaluación
                              └→ API ?action=agenda ─→ Calendario del aula
```

## 1. Instalación (≈15 minutos)

1. **Hoja de cálculo:** usá la hoja creada en tu Drive (*Diagnóstico inicial · Respuestas*) o una nueva. Debe ser **privada** (no la guardes en la carpeta compartida del aula).
2. En la hoja: **Extensiones → Apps Script**. Creá estos archivos y pegá el contenido de la carpeta [`appsscript/`](https://github.com/diegomezapy/curso_visualiza_datos_UNC/tree/main/appsscript) del repositorio:
   `Code.gs`, `Preguntas.gs`, `Banco.gs`, `Agenda.gs` (tipo *Script*) y `Tablero.html`, `Asistencia.html`, `MiniEval.html` (tipo *HTML*). En **Configuración del proyecto** activá *Mostrar el archivo de manifiesto* y reemplazá `appsscript.json`.
3. **Configuración del proyecto → Propiedades del script → Agregar:** `CODIGO_CLASE` = el código que anunciarás en clase (sin él, el servidor **rechaza** todos los envíos).
4. Ejecutá **`configurarTodo`** (botón ▶). Google pedirá permisos: hoja de cálculo, enviar correos y activadores. Esto crea las pestañas, un secreto para firmar los enlaces y el activador que corre cada minuto.
5. **Implementar → Nueva implementación → Aplicación web:** *Ejecutar como:* **Yo** · *Quién tiene acceso:* **Cualquier usuario**. Copiá la **URL** (`https://script.google.com/macros/s/…/exec`).
6. En el repositorio, `aula/config.json`:
```json
"diagnostico": { "endpoint": "URL_DE_LA_APP_WEB", "tablero_url": "URL_DE_LA_APP_WEB", "looker_url": "", "looker_embed": "" },
"agenda": { "endpoint": "" }
```
   Si publicás también las funciones de agenda en el mismo proyecto, copiá esa URL a `agenda.endpoint`. Si queda vacío, el calendario usa la agenda base del aula. Hacé *commit* + *push* y el sitio se republica.
7. **Probá:** abrí `/diagnostico/`, respondé con el código de clase y verificá que aparece una fila en *Respuestas* y en el tablero.

> Cada vez que cambies el código del script: **Implementar → Administrar implementaciones → editar → Nueva versión**.

## 2. Agenda: tutorías, clases y entregas
Pestaña **Agenda** (una fila por evento):

| id | fecha | inicio | fin | tipo | titulo | sesion | enlace | descripcion | asistencia | mini |
|---|---|---|---|---|---|---|---|---|---|---|
| clase-1 | 2026-11-20 | 19:00 | 21:00 | clase | Sesión 1 · Principios | 1 | https://meet… | | SI | SI |
| tut-1 | 2026-11-25 | 18:00 | 19:00 | tutoria | Tutoría virtual S1 | 1 | https://meet… | Dudas | SI | NO |
| entrega-1 | 2026-11-27 | 23:00 | 23:59 | entrega | Entrega S1 | 1 | | RPubs + Colab | NO | NO |

- `tipo`: `clase`, `tutoria`, `entrega`, `evaluacion`, `otro`. Fecha `aaaa-mm-dd` y horas `HH:MM` **como texto** (la pestaña ya viene con ese formato). Hora de Paraguay.
- `asistencia = SI` → correo de asistencia a la hora de inicio. `mini = SI` → correo de mini-evaluación al terminar.
- **Atajo:** en la pestaña *Config* escribí las fechas `clase_1 … clase_8` y ejecutá **`generarAgendaBase`**: crea cada clase (con asistencia y mini-evaluación) y su entrega a +7 días. Para una sesión con otro horario, agregá en *Config* `hora_inicio_N` y `hora_fin_N` (por ejemplo, los sábados `08:00`–`12:00`). Un *Config* nuevo ya viene con el calendario del módulo (vie 13/11/2026 en adelante: viernes 18:00–22:00 y sábados 08:00–12:00); ajustá si cambia.
- Los enlaces de Meet **no se publican** en el calendario del aula salvo que pongas `PUBLICAR_ENLACES = SI` en *Config*; siempre llegan en el correo de asistencia.

## 3. Estudiantes
Pestaña **Estudiantes**: `email`, `nombre`, `activo` (SI/NO). Copiá los correos desde el **Panel docente → Exportar CSV** del aula. Solo los correos de esta lista pueden registrar asistencia y reciben los envíos.

## 4. Cómo funciona el control de horario
- El enlace del correo lleva un **token firmado** (HMAC) ligado al estudiante y al evento: no sirve para otra persona ni para otro evento.
- El **servidor** (no el navegador) compara la hora actual con la del evento: acepta desde el inicio hasta **15 minutos después del fin**. Antes o después: “fuera de horario”.
- Cada persona registra una sola vez por evento. Se guarda en la pestaña *Asistencia*; **`calcularResumen`** arma la matriz estudiante × evento y el % de asistencia (pestaña *Resumen*).
- La **mini-evaluación** toma 3 preguntas del banco de la sesión, se **corrige en el servidor** (las respuestas correctas nunca llegan al navegador antes de enviar), solo cuenta el primer intento y está abierta 72 h. **No suma puntos**; el docente ve el % de aciertos por clase en *Resumen*.
- **`enviarPrueba`** te manda los dos correos a vos para verlos antes de la primera clase.

## 5. Límites importantes de Google (lea antes de la primera clase)
- **Cuota de correos de Apps Script:** ≈ **100 destinatarios/día** con una cuenta Gmail personal y ≈ **1500/día** con Google Workspace (cuenta institucional). Con 2 correos por clase (asistencia + mini-evaluación) y N estudiantes, **N×2 debe ser menor que la cuota**. Si se agota, el script envía los que pueda, lo anota en la columna `enviado_*` (p. ej. `2/3`) y no reintenta. Soluciones: usar una cuenta Workspace, repartir en varios días, o dejar solo uno de los dos correos.
- **Puntualidad:** el activador corre **cada minuto**; el correo llega entre 0 y ~1-2 minutos después de la hora (Google no garantiza segundos exactos).
- **Tiempo de ejecución:** los activadores tienen un límite diario de ejecución (≈90 min en cuentas personales); revisar cada minuto consume muy poco.
- **Entregabilidad:** los correos salen de tu cuenta; pueden caer en *spam* las primeras veces. Pedí que agreguen tu dirección a contactos.
- El endpoint es público: cualquiera con la URL puede **leer** los datos anonimizados y **intentar** enviar; por eso se exige `CODIGO_CLASE` y se valida cada campo. No es un control de acceso fuerte: para evaluación formal usar Google Forms con inicio de sesión.

## 6. Looker Studio (cuarta vía de visualización)
`configurarTodo` crea la pestaña **Looker**: una vista **anonimizada** (sin código de participante ni comentarios) de *Respuestas*.
1. <https://lookerstudio.google.com> → **Crear → Informe → Agregar datos → Hojas de cálculo de Google** → elegí la hoja → pestaña **Looker** → marcá *Usar la primera fila como encabezados* → **Agregar**.
2. Tipos de campo: `ts` como *Texto* (o campo calculado `PARSE_DATETIME("%Y-%m-%d %H:%M:%S", ts)`), `score_*` y `au_*` como *Número*, `area`, `experiencia`, `nivel` como *Texto*. Agregá controles de filtro por `area`, `experiencia`, `nivel` y `cohorte`.
3. Gráficos sugeridos: **tarjetas** (n de registros, promedio de `score_total`), **barras** del promedio de `score_viz`, `score_py`, `score_r`; **columnas apiladas** por `nivel`; **mapa de calor** de `au_*` (tabla con formato condicional); **barras** de `ok_*` (aciertos por pregunta).
4. **Compartir** el informe (*Cualquier persona con el enlace puede ver*). Para insertarlo en el aula: **Archivo → Insertar informe** → activar incrustación → copiar la URL de inserción en `aula/config.json` (`looker_embed`); el enlace normal va en `looker_url`.
5. Para que se actualice solo: **Recurso → Administrar fuentes de datos → Frecuencia de actualización de datos** (mín. 15 min en la conexión de Hojas).

## 7. Privacidad
- El cuestionario es **anónimo** (código aleatorio de 10 caracteres después de `P-`, sin nombre ni cédula). El comentario libre no se publica en la API ni en Looker.
- El tablero permite exportar la vista filtrada en CSV y Excel. La hoja privada conserva todas las respuestas y puede descargarse en Excel desde el panel docente; las respuestas enviadas mientras el formulario estuvo en modo práctica no se guardaron y no pueden recuperarse.
- *Estudiantes*, *Asistencia* y *MiniEval* sí contienen correos y nombres: mantené la hoja **privada** y compartila solo con docentes.
- No guardes esta hoja dentro de la carpeta de Drive del aula (permite edición a quien tenga el enlace).

## 8. Pruebas automáticas
`node tests/appsscript_test.js` y `node tests/agenda_test.js` ejecutan el código del script contra servicios simulados de Google (validaciones, cuota, ventana horaria, tokens, calificación en el servidor). No reemplazan una prueba real: hacé una clase de ensayo con 2 o 3 personas.
