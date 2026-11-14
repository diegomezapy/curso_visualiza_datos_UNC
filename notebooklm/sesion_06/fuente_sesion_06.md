# Sesión 6 · Reporting automatizado
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U2.
Resumen: Informes parametrizados y reproducibles con Jinja2; papermill, Quarto y automatización con GitHub Actions.

## Objetivos
- Convertir un análisis en un reporte parametrizado y reproducible.
- Programar la generación periódica y alertas.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 6 · Reporting automatizado
**Unidad del programa:** U2 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Convertir un análisis en un reporte parametrizado y reproducible.
- Programar generación periódica y alertas.

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-40 | Reproducibilidad: del notebook al reporte; plantillas, parámetros, versionado |
| 40-90 | Jinja2, Quarto, papermill; automatización (cron, GitHub Actions) |
| 90-105 | Pausa |
| 105-180 | **Lab 6** guiado: informe por sucursal |
| 180-240 | Presentación breve de **propuestas del integrador** (2 min c/u) y feedback |

## Trabajo asincrónico
- Lectura: documentación de Quarto *Parameters*; Wilke caps. 21-22 (paneles, títulos y tablas).
- Ejercicio: alerta de margen + gráfico de contribución + exportación PDF.
- Redactar **propuesta del integrador** (1 página).
- Quiz 6.

## Entrega y evaluación
Ejercicio S6 (5 pts, R2) · Propuesta del integrador (hito) · Quiz 6.

## Laboratorio
[`lab06_reportes_automaticos.py`](lab06_reportes_automaticos.py) · `python tools/generar_reportes.py`

### Pista R (RStudio → RPubs)
[`r/06_reporting_automatizado.Rmd`](../../r/06_reporting_automatizado.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_06_reporting.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/6).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **Un reporte reproducible se define como…** → Plantilla + datos + parámetros, ejecutable sin pasos manuales. Si se puede regenerar con un comando, es reproducible y programable.
- **¿Qué herramienta permite ejecutar un notebook con parámetros?** → papermill (o Quarto con -P). papermill inyecta parámetros en una celda etiquetada y ejecuta el notebook; Quarto ofrece parámetros equivalentes.
- **¿Por qué incrustar imágenes en base64 dentro del HTML del informe?** → Genera un archivo autocontenido fácil de compartir. Un único .html sin dependencias externas se puede enviar por correo o archivar.
- **Una alerta automática útil debe tener…** → Un umbral explícito, contexto y destinatario. Sin umbral y contexto se generan falsas alarmas o se ignoran.
- **Automatizar elimina la necesidad de validar los datos.** → Falso. Al contrario: un error en los datos se replica automáticamente; agregá chequeos y pruebas.

## Actividades evaluadas
- Ejercicio S6: informe parametrizado con alerta de margen + gráfico de contribución · publicar en RPubs (5 pts)
- Hito: propuesta del proyecto integrador (1 página) · publicar en RPubs (0 pts)


## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- R Markdown: The Definitive Guide (Xie, Allaire, Grolemund) (libro, en) · https://bookdown.org/yihui/rmarkdown/ · gratuito en línea · parámetros: cap. 15
- Getting Started with RPubs (web, en) · https://rpubs.com/about/getting-started · 
- Manual ED-UCH · Introducción al uso de RMarkdown (libro, es) · https://bookdown.org/gboccardo/manual-ED-UCH/introduccion-al-uso-de-rmarkdown-para-la-compilacion-de-resultados-de-rstudio-en-diferentes-formatos.html · 
- Matías Andina · Comunicación (R Markdown) (libro, es) · https://bookdown.org/matiasandina/R-intro/comunicacion.html · 
- Posit · Galería de cheatsheets (R Markdown, con traducciones) (web, es/en) · https://posit.co/resources/cheatsheets/ · 
