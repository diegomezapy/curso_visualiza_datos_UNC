# Sesión 7 · Estructuras complejas: alta dimensionalidad, series y geodatos
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U3.
Resumen: Coordenadas paralelas, PCA y t-SNE; descomposición y heatmap de series; mapas de burbujas y coropletas.

## Objetivos
- Visualizar datos multivariados interpretando sus límites.
- Explorar series temporales y datos geográficos evitando lecturas erróneas.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 7 · Estructuras complejas: alta dimensionalidad, series y geodatos
**Unidad del programa:** U3 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Visualizar datos multivariados con coordenadas paralelas, PCA y t-SNE interpretando sus límites.
- Explorar series temporales (tendencia, estacionalidad, anomalías) y datos geográficos (burbujas vs. coropleta).

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-50 | Alta dimensionalidad: paralelas, matrices de correlación, PCA, t-SNE |
| 50-90 | Series temporales: descomposición, heatmap calendario, anomalías |
| 90-105 | Pausa |
| 105-150 | Geodatos: proyecciones, coropletas, tasas vs. conteos, MAUP |
| 150-205 | **Lab 7** guiado |
| 205-240 | Avance del integrador: prototipo y feedback |

## Trabajo asincrónico
- Lectura: Wilke caps. 13-16 (series, tendencias, geoespacial, incertidumbre); artículo *How to Use t-SNE Effectively* (Distill).
- **Mini-proyecto 3:** 3 vistas complementarias sobre un dataset real con dimensión temporal o geográfica.
- Quiz 7.

## Entrega y evaluación
**Mini-proyecto 3** (10 pts, R2) · Quiz 7 · Avance del integrador.

## Laboratorio
[`lab07_complejas.py`](lab07_complejas.py)

### Pista R (RStudio → RPubs)
[`r/07_estructuras_complejas.Rmd`](../../r/07_estructuras_complejas.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_07_complejas.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/7).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **En t-SNE, ¿qué NO es interpretable?** → Las distancias globales y el tamaño de los clústeres. t-SNE preserva vecindades locales; distancias entre clústeres y su tamaño dependen de parámetros como la perplejidad.
- **PCA se basa en…** → Una proyección lineal que maximiza la varianza explicada. Los componentes principales son combinaciones lineales ortogonales ordenadas por varianza explicada.
- **Regla básica de un mapa coroplético:** → Colorear tasas o densidades, no conteos absolutos. Los conteos reflejan el tamaño de la población y no la intensidad del fenómeno; normalizá.
- **El problema del área modificable (MAUP) indica que…** → El patrón observado depende de cómo se agregan o delimitan las áreas. Cambiar los límites o el nivel de agregación puede cambiar las conclusiones.
- **Para detectar estacionalidad en series diarias largas conviene…** → Un heatmap calendario, gráfico de subseries o descomposición. Esas vistas separan componentes (tendencia, ciclo, estacionalidad) y facilitan detectar anomalías.

## Actividades evaluadas
- Mini-proyecto 3: 3 vistas complementarias sobre un dataset REAL del catálogo de Datos abiertos (con ficha del dataset) · RPubs + Colab (10 pts)
- Hito: avance del integrador (prototipo con ≥ 2 vistas) · RPubs (0 pts)

## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Distill · How to Use t-SNE Effectively (artículo, en) · https://distill.pub/2016/misread-tsne/ · 
- Wilke · caps. 13-16 (series, tendencias, geoespacial, incertidumbre) (libro, en) · https://clauswilke.com/dataviz/ · 
- Portal de Datos Abiertos de Paraguay (datos, es) · https://www.datos.gov.py · 
- INE Paraguay · Instituto Nacional de Estadística (datos, es) · https://www.ine.gov.py · 
- GeoPandas · documentación (web, en) · https://geopandas.org · 
