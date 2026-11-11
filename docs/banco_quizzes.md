# Banco de quizzes (uso docente)
Respuestas correctas marcadas con ✔. Cada quiz: 5 preguntas de este banco (rotar por cohorte).

## Quiz 1 · Principios y percepción
1. Según Cleveland-McGill, ¿qué codificación se decodifica con mayor precisión? a) Área · b) **✔ Posición sobre escala común** · c) Ángulo · d) Saturación de color
2. El cuarteto de Anscombe demuestra que: a) La correlación implica causalidad · b) **✔ Estadísticos idénticos pueden ocultar estructuras muy distintas** · c) La regresión es robusta · d) Los outliers son siempre errores
3. Un atributo *preatentivo* es: a) Uno que requiere leyenda · b) **✔ Uno detectado por el sistema visual en < 250 ms sin atención serial** · c) Un tipo de gráfico · d) Un error de diseño
4. *Data-ink ratio* (Tufte) propone: a) Maximizar adornos · b) **✔ Maximizar la proporción de tinta que representa datos** · c) Usar 3D · d) Eliminar ejes siempre
5. V/F: Una torta es la mejor opción para comparar 8 categorías de valores similares. **✔ Falso** (barras ordenadas).

## Quiz 2 · Elección del gráfico
1. Para ver la forma de una distribución con n=400 conviene: **✔ histograma/ECDF/violín** · b) torta · c) área apilada · d) radar
2. Un diagrama de dispersión con 50 000 puntos sufre de: **✔ overplotting; usar transparencia, hexbin o densidad**
3. Ranking de categorías con etiquetas largas: **✔ barras horizontales ordenadas**
4. Partes de un todo en el tiempo con muchas categorías: **✔ barras apiladas 100 % o small multiples** (no tortas múltiples)
5. V/F: Las barras pueden empezar en un valor distinto de cero si se anota el eje. **✔ Falso** (la longitud codifica el valor).

## Quiz 3 · Color, diseño y ética
1. ¿Qué paleta usar para una variable continua con punto neutro (p. ej. variación vs. meta)? **✔ Divergente centrada en el punto neutro**
2. ~8 % de varones tiene daltonismo rojo-verde. ¿Qué hacer? **✔ Usar paleta segura (Okabe-Ito/viridis) y redundar con forma/etiqueta**
3. Un doble eje Y es problemático porque: **✔ la relación visual depende de escalas arbitrarias del autor**
4. Mejor título: a) "Ventas" · b) **✔ "Las ventas crecieron 7 % en 2025, impulsadas por Asunción"** · c) "Gráfico de ventas 2025"
5. Cherry-picking temporal consiste en: **✔ Elegir una ventana de tiempo que favorece una conclusión**

## Quiz 4 · Visual analytics y KPIs
1. Un buen KPI incluye: **✔ definición, unidad, periodo y comparación/meta**
2. *Small multiples* sirve para: **✔ comparar muchas series con la misma escala sin saturar**
3. Estructura narrativa de storytelling: **✔ contexto → conflicto → resolución/llamado a la acción**
4. V/F: Más gráficos en un panel siempre aumentan la comprensión. **✔ Falso**
5. Métrica de vanidad vs. accionable: **✔ la accionable permite decidir/cambiar algo**

## Quiz 5 · Dashboards
1. Mantra de Shneiderman: **✔ overview first, zoom and filter, then details on demand**
2. ¿Dónde ubicar los KPIs principales? **✔ Arriba a la izquierda (zona de mayor atención)**
3. Un filtro global debe: **✔ afectar de forma coherente y visible a todas las vistas indicadas**
4. Interacción *decorativa* es: **✔ aquella que no ayuda a responder la pregunta de la audiencia**
5. Indicador de rendimiento razonable de un tablero web: **✔ carga inicial < 3 s; agregar/pre-calcular datos**

## Quiz 6 · Reporting automatizado
1. Un reporte reproducible = **✔ plantilla + datos + parámetros, ejecutable sin pasos manuales**
2. Herramienta para ejecutar notebooks con parámetros: **✔ papermill (o Quarto con `-P`)**
3. ¿Por qué incrustar imágenes en base64 en HTML? **✔ Genera un archivo autocontenido fácil de compartir**
4. Una alerta automática útil debe: **✔ tener umbral explícito, contexto y destinatario**
5. V/F: Automatizar elimina la necesidad de validar los datos. **✔ Falso** (agregar pruebas/chequeos)

## Quiz 7 · Estructuras complejas
1. En t-SNE, ¿qué NO es interpretable? **✔ Distancias globales y tamaño de los clústeres**
2. PCA se basa en: **✔ proyección lineal que maximiza la varianza explicada**
3. Regla del coroplético: **✔ colorear tasas/densidades, no conteos absolutos**
4. El MAUP (*modifiable areal unit problem*) indica que: **✔ el patrón depende de cómo se agregan las áreas**
5. Para detectar estacionalidad en series diarias largas: **✔ heatmap calendario / gráfico de subseries / descomposición**

## Quiz 8 (opcional) · Redes
1. *Hairball* es: **✔ un grafo denso ilegible; filtrar aristas, agregar o usar matriz**
2. Centralidad de intermediación (*betweenness*) mide: **✔ cuánto un nodo actúa de puente en caminos más cortos**
3. Para redes densas conviene: **✔ matriz de adyacencia ordenada**
4. Codificación recomendada: **✔ tamaño = métrica, color = comunidad, pocas etiquetas**
5. V/F: Un layout de fuerzas tiene distancias con significado cuantitativo exacto. **✔ Falso**
