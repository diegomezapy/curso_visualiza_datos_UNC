# Sesión 8 · Redes (opcional) y presentación del integrador
Curso: Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos · FACET–UNC. Unidad U4.
Resumen: Grafos, layouts, centralidad, comunidades y matrices de adyacencia. Presentaciones finales.

## Objetivos
- (Opcional) Representar redes con layouts, métricas y matrices.
- Comunicar el proyecto integrador a una audiencia técnica y de gestión.

## Guía de la sesión (agenda, trabajo asincrónico, evaluación)
# Sesión 8 · Redes (opcional) y presentación del integrador
**Unidad del programa:** U4 · **Duración:** 4 h sincrónicas + ≈2,75 h asincrónicas

## Resultados de aprendizaje
- (Opcional) Representar redes con layouts, métricas y matrices de adyacencia.
- Comunicar el proyecto integrador a una audiencia técnica y de gestión.

## Agenda sincrónica
| Min | Actividad |
|---|---|
| 0-60 | **Redes (opcional):** grafos, layouts, centralidad, comunidades, matriz vs. nodo-enlace; **Lab 8** |
| 60-75 | Pausa |
| 75-210 | **Presentaciones del integrador** (hasta 10 min + 5 min de preguntas por estudiante) y coevaluación |
| 210-240 | Cierre del curso, retroalimentación y encuesta |

## Trabajo asincrónico
- Entrega del **trabajo práctico final** en la subcarpeta personal de Drive, según el plazo comunicado por el docente.
- (Opcional) Ejercicio de redes como práctica, sin puntos adicionales.
- Quiz 8 opcional.

## Entrega y evaluación
**Trabajo práctico final** (30 puntos: producto 18 + presentación y defensa 12, hasta 15 minutos) · [Guía y rúbrica](../../docs/proyecto_integrador.md#rubrica). Además, foros 25 puntos, cuestionarios 25 y coedición 20.

## Laboratorio
[`lab08_redes.py`](lab08_redes.py)

### Pista R (RStudio → RPubs)
[`r/08_redes.Rmd`](../../r/08_redes.Rmd) — publicar con *Publish → RPubs* y pegar el enlace en el aula.

### Material de estudio
[Ficha de estudio (PDF)](../../materiales/pdf/ficha_08_redes.pdf) · videos y lecturas en el [aula virtual](../../aula/index.html#/sesion/8).

## Ideas clave verificables (de las preguntas de autoevaluación)
- **Un 'hairball' en visualización de redes es…** → Un grafo denso ilegible: filtrar aristas, agregar o usar matriz. Cuando hay demasiadas aristas el grafo no comunica; simplificá o cambiá de representación.
- **La centralidad de intermediación (betweenness) mide…** → Cuánto actúa un nodo como puente en los caminos más cortos. Nodos con alta intermediación conectan comunidades y su eliminación fragmenta la red.
- **Para redes muy densas suele ser mejor…** → Una matriz de adyacencia ordenada. La matriz evita el solapamiento de aristas y deja ver bloques de comunidades.
- **Una codificación recomendada para redes es…** → Tamaño = métrica, color = comunidad, pocas etiquetas. Codificar con propósito y etiquetar solo lo relevante mantiene la legibilidad.
- **En un layout de fuerzas, las distancias tienen significado cuantitativo exacto.** → Falso. Los layouts de fuerzas son heurísticos: la posición ayuda a ver estructura pero no es una medida exacta.

## Actividades evaluadas
- (Opcional) Ejercicio de redes: red de co-ocurrencias · RPubs (0 pts)
- Participación fundamentada en los foros de las ocho unidades (25 pts) (25 pts)
- Edición conjunta de documentos y tableros (20 pts) (20 pts)
- Trabajo final: bases, investigación y tablero (18 pts) (18 pts)
- Trabajo final: presentación y defensa (12 pts, máximo 15 minutos) (12 pts)


## Lecturas recomendadas (enlaces; subir el texto solo si la licencia lo permite)
- NetworkX · documentación (web, en) · https://networkx.org/documentation/stable/ · 
- igraph para R (web, en) · https://r.igraph.org · 
- Gephi · software de análisis de redes (web, en) · https://gephi.org · 
