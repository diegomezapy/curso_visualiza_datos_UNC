# Sesión 3 · Color, tipografía, anotación y ética visual
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U1.
Resumen: Paletas accesibles, etiquetado directo, títulos-mensaje y galería de gráficos engañosos con su corrección.

## Objetivos
- Seleccionar paletas cualitativas, secuenciales y divergentes accesibles.
- Detectar y corregir gráficos engañosos con un checklist ético.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 3 · Color, tipografía, anotación y ética visual
**Unidad del programa:** U1 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- Seleccionar paletas cualitativas, secuenciales y divergentes accesibles.
- Detectar y corregir gráficos engañosos con un checklist ético.

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-45 | Color: teoría, daltonismo, Okabe-Ito/viridis/ColorBrewer |
| 45-90 | Tipografía, anotación, etiquetado directo, títulos-mensaje |
| 90-105 | Pausa |
| 105-170 | **Ética visual:** ejes truncados, doble eje, cherry-picking, áreas 3D, mapas engañosos; casos reales |
| 170-240 | **Lab 3:** corregir la galería de engaños + debate (¿cuándo es manipulación?) |

## Trabajo asincrónico
- Lectura: Wilke caps. 17, 19-20 y 29; Cairo, *How Charts Lie* (selección).
- Ejercicio: corregir un gráfico "malo" + 150 palabras sobre su daño potencial.
- Quiz 3.

## Entrega y evaluación
Ejercicio S3 (5 pts, R1) · Quiz 3.

## Laboratorio
[`lab03_color_diseno_etica.py`](lab03_color_diseno_etica.py)

### Pista R (RStudio → RPubs)
[`r/03_color_diseno_etica.Rmd`](../../r/03_color_diseno_etica.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_03_color_etica.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/3).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **Para una variable continua con punto neutro (p. ej., variación respecto a una meta) se recomienda una paleta…** → Divergente centrada en el punto neutro. La paleta divergente separa lo positivo de lo negativo alrededor de un valor neutro significativo.
- **Aproximadamente 8 % de los varones tiene daltonismo rojo-verde. ¿Qué conviene hacer?** → Usar paletas seguras (Okabe-Ito, viridis) y redundar con etiquetas o formas. Las paletas seguras y la codificación redundante hacen el gráfico accesible.
- **Un doble eje Y es problemático porque…** → La relación visual depende de escalas que elige arbitrariamente el autor. Cambiando las escalas se puede fabricar cualquier correlación aparente; mejor un índice base 100 o paneles separados.
- **¿Cuál es el mejor título para un gráfico de ventas?** → Las ventas crecieron 7 % en 2025, impulsadas por Asunción. Un título-mensaje afirma un hallazgo que el gráfico sostiene; los demás solo etiquetan.
- **Cherry-picking temporal consiste en…** → Elegir una ventana de tiempo que favorece la conclusión deseada. Recortar el periodo a conveniencia puede invertir la tendencia aparente; hay que mostrar el contexto completo.

## Actividades evaluadas
- Ejercicio S3: corregir un gráfico 'malo' + 150 palabras sobre su daño potencial · publicar en RPubs (5 pts)


## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- Google · Trampas de visualización (guía de datos) (web, es) · https://developers.google.com/machine-learning/guides/data-traps/visualization-traps?hl=es-419 · 
- datos.gob.es · Diseñar visualizaciones de datos con integridad (web, es) · https://datos.gob.es/es/blog/disenar-visualizaciones-de-datos-con-integridad-mas-alla-de-los-graficos-bonitos · 
- IJNet · ¿Y si tu visualización de datos es engañosa? Consejos para evitarlo (web, es) · https://ijnet.org/es/story/%C2%BFy-si-tu-visualizaci%C3%B3n-de-datos-es-enga%C3%B1osa-consejos-para-evitarlo · 
- Okabe & Ito · Color Universal Design (paleta apta para daltonismo) (web, en) · https://jfly.uni-koeln.de/color/ · 
- ColorBrewer · paletas para mapas y gráficos (web, en) · https://colorbrewer2.org · 
- Wilke · caps. 17, 19-20 y 29 (libro, en) · https://clauswilke.com/dataviz/ · 
