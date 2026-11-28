# Guía de elaboración y entrega del trabajo final (30 %)

El trabajo final consiste en investigar una pregunta concreta con datos reales y comunicar una respuesta sustentada mediante un **documento de investigación** y un **tablero o reporte visual**. Cada estudiante prepara su propia carpeta de entrega y presenta y defiende el trabajo el **último día de clases**, con un máximo de **15 minutos en total**.

## 1. Elegir y documentar el problema

1. Formulá una pregunta que pueda responderse con datos. Identificá la audiencia y la decisión que podría tomar a partir de los resultados.
2. Elegí una base real del [catálogo de datos abiertos del curso](datos_abiertos_reales.md) o una fuente aprobada por el docente. Como referencia del proyecto integrador, la base debe contener **al menos 5.000 filas y 6 variables**, con dimensión temporal o geográfica. Si la pregunta exige otro tipo de base, acordá la excepción con el docente.
3. Registrá fuente, enlace original, institución responsable, fecha de descarga, cobertura, unidad de análisis, definición de variables, licencia y limitaciones. No subas datos personales ni información confidencial a la carpeta compartida.
4. Conservá una copia de la base original. Separá los datos originales de los procesados y explicá las transformaciones, los faltantes y los filtros.

## 2. Desarrollar el análisis y el producto visual

- Mostrá al menos cuatro vistas con propósito: **indicadores clave**, **tendencia o serie temporal**, **comparación** y **una estructura compleja** (por ejemplo, mapa, multivariable o red). Justificá por qué cada gráfico responde a la pregunta.
- Incorporá filtros funcionales en el tablero o un reporte automatizado y parametrizable. Comprobá que los indicadores, los gráficos y las conclusiones usan los mismos filtros.
- Explicá los hallazgos con cifras y unidades. Distinguí descripción de causalidad; no atribuyas causas que el diseño de los datos no permite demostrar.
- Revisá escalas, ejes, colores, etiquetas, contraste, accesibilidad y posibles lecturas engañosas. Indicá incertidumbre y límites del análisis.
- Conservá el código necesario para reproducir la preparación de datos y las visualizaciones. Podés trabajar en R, Python o ambos; incluí instrucciones y dependencias correspondientes.

## 3. Escribir el documento de investigación

Extensión orientativa: **6 a 10 páginas**, sin contar anexos. El documento debe contener:

1. Título, pregunta, objetivo, audiencia y relevancia.
2. Datos y método: procedencia, fecha, población o unidad de análisis, limpieza, transformaciones y definiciones de indicadores.
3. Decisiones de visualización: selección de gráficos, escalas, filtros y razones de diseño.
4. Resultados: hallazgos sustentados por gráficos y cifras, con su interpretación.
5. Limitaciones, consideraciones éticas y alcance de las conclusiones.
6. Instrucciones para reproducir el análisis, enlaces al tablero o reporte y referencias completas.

Cada tabla y figura debe indicar fuente, fecha, unidades y definición de la métrica. Declará el uso de herramientas de IA cuando hayan intervenido en el análisis o la redacción.

## 4. Crear la carpeta y entregar

1. Abrí la [carpeta de trabajos prácticos de la clase](https://drive.google.com/drive/folders/1spQXcXcYkMJY1RnCgnUsYdZ-l0DSAUt5?usp=sharing) y creá **tu propia subcarpeta**, por ejemplo `TP_APELLIDO_NOMBRE`. No edites ni muevas las carpetas de otras personas.
2. Depositá allí, con nombres reconocibles:
   - `datos/`: base original y versión procesada, o enlace a la fuente y script de descarga cuando la licencia o el tamaño impidan subirla; añadí una ficha breve de datos.
   - `codigo/`: scripts o notebook, `README` con pasos de ejecución y archivo de dependencias (`requirements.txt` para Python o listado de paquetes/`renv.lock` para R).
   - `informe.pdf` o un documento de Google con el desarrollo de la investigación.
   - Enlace o archivo del tablero/reporte y material de apoyo de la presentación.
3. Abrí desde el aula la actividad **Trabajo final: bases, investigación y tablero** de la unidad 8 y pegá el enlace de **tu subcarpeta** en el campo de entrega. El enlace debe abrir la carpeta correcta y sus archivos. Conservá una copia propia de todos los materiales.
4. Antes de presentar, comprobá que el documento se abre, que los datos y el código están disponibles, que el tablero funciona y que los enlaces no requieren permisos adicionales para el docente. La marca de entrega del aula confirma que se guardó el enlace; la revisión y la nota las realiza el docente.

El espacio de Drive está compartido para permitir la creación de carpetas. Por ello **no incluyas datos personales, credenciales ni bases restringidas**, y mantené una copia de respaldo. La fecha y hora exactas de cierre de la carpeta deben ser comunicadas por el docente; esta guía no fija una penalización por atraso.

## 5. Presentar y defender el último día de clases

Cada estudiante dispone de **hasta 10 minutos para exponer** y **hasta 5 minutos para responder preguntas**, sin superar **15 minutos**. Mostrá la pregunta, la procedencia de la base, dos o tres hallazgos principales, una demostración breve del tablero y una limitación relevante. Tené abierta tu carpeta antes de comenzar.

En la defensa, explicá cómo se calculó al menos un indicador, por qué elegiste una visualización, qué cambia al aplicar un filtro y qué conclusión no puede sostenerse con los datos. Respondé con precisión y reconocé las limitaciones cuando corresponda.

<a id="rubrica"></a>
## Criterios de evaluación del trabajo final (30 puntos)

| Entrega | Criterio | Puntos |
|---|---|---:|
| Documento, bases y tablero | Pregunta, audiencia y relevancia | 2 |
| Documento, bases y tablero | Fuente, calidad y tratamiento de los datos | 3 |
| Documento, bases y tablero | Elección, calidad y accesibilidad de las visualizaciones | 4 |
| Documento, bases y tablero | Análisis e interpretación de hallazgos | 2 |
| Documento, bases y tablero | Interacción o automatización funcional | 3 |
| Documento, bases y tablero | Reproducibilidad y documentación técnica | 2 |
| Documento, bases y tablero | Integridad visual, ética y limitaciones | 2 |
| **Subtotal producto** | | **18** |
| Presentación y defensa | Síntesis y claridad dentro del tiempo | 3 |
| Presentación y defensa | Demostración del tablero o reporte | 3 |
| Presentación y defensa | Justificación de datos, cálculos y decisiones visuales | 3 |
| Presentación y defensa | Respuestas fundamentadas a las preguntas | 3 |
| **Subtotal defensa** | | **12** |
| **Total trabajo final** | | **30** |

La presentación y defensa forman parte del mismo **30 %** del trabajo final. Los criterios se aplican a evidencias observables; los gráficos decorativos, los enlaces inaccesibles y las afirmaciones sin fuente no satisfacen el criterio correspondiente.

## Lista de comprobación antes de entregar

- [ ] Mi pregunta, audiencia y fuente están identificadas.
- [ ] La carpeta contiene base o método reproducible de descarga, documento, código y tablero/reporte.
- [ ] Los indicadores, las unidades, los filtros y las fuentes son consistentes.
- [ ] El documento explica hallazgos, límites, ética y reproducción.
- [ ] El enlace de mi subcarpeta está guardado en el aula y abre para el docente.
- [ ] La exposición cabe en 10 minutos y reservé hasta 5 para la defensa.
