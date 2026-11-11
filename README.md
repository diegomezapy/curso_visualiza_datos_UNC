# Visualización de Datos · Maestría en Ingeniería y Ciencia de Datos (FACET – UNC)

Materiales del módulo **1.2.3 Visualización de datos (Obligatoria)** · Semestre 2º 2026 · 8 sesiones · 60 h (30 sincrónicas / 30 asincrónicas).
Universidad Nacional de Concepción · Facultad de Ciencias Exactas y Tecnológicas · Concepción, Paraguay.

> **Fundamentación.** La visualización es central para explorar datos, comunicar resultados y apoyar decisiones. El módulo entrena criterios de diseño, ética visual y construcción de productos (dashboards/reportes).

## Competencias
1. Diseñar visualizaciones efectivas según objetivo, audiencia y tipo de dato.
2. Construir reportes y tableros con criterios de claridad, integridad y ética.

## Mapa del curso

| # | Sesión | Unidad del programa | Lab |
|---|--------|--------------------|-----|
| 1 | [Principios: percepción y por qué visualizar](sesiones/01_principios/) | U1 | `lab01_percepcion.py` |
| 2 | [Elección de gráficos](sesiones/02_eleccion_graficos/) | U1 | `lab02_eleccion_graficos.py` |
| 3 | [Color, diseño y ética visual](sesiones/03_color_diseno_etica/) | U1 | `lab03_color_diseno_etica.py` |
| 4 | [Visual analytics, KPIs y storytelling](sesiones/04_visual_analytics_kpis/) | U2 | `lab04_kpis_storytelling.py` |
| 5 | [Dashboards interactivos](sesiones/05_dashboards_interactivos/) | U2 | `lab05_dashboards_plotly.py`, `app_dash.py` |
| 6 | [Reporting automatizado](sesiones/06_reporting_automatizado/) | U2 | `lab06_reportes_automaticos.py` |
| 7 | [Alta dimensionalidad, series y geodatos](sesiones/07_estructuras_complejas/) | U3 | `lab07_complejas.py` |
| 8 | [Redes (opcional) + presentación del integrador](sesiones/08_redes_e_integrador/) | U4 | `lab08_redes.py` |

🎓 **Aula virtual:** https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/

🌐 **Sitio web:** https://diegomezapy.github.io/curso_visualiza_datos_UNC/

Documentos: [aula virtual (guía)](docs/aula_virtual.md) · [activar cuentas (Firebase)](docs/configurar_firebase.md) · [programa](docs/programa.md) · [cronograma](docs/cronograma.md) · [evaluación](docs/evaluacion.md) · [rúbricas](docs/rubricas.md) · [proyecto integrador](docs/proyecto_integrador.md) · [banco de quizzes](docs/banco_quizzes.md) · [bibliografía y recursos](docs/bibliografia.md)

## Evaluación (sugerida en el programa)
**Teoría 30 %** (quizzes y lecturas guiadas) · **Práctica 50 %** (laboratorios y mini-proyectos) · **Integrador 20 %** (informe técnico + presentación). Detalle en [docs/evaluacion.md](docs/evaluacion.md).

## Cómo empezar
```bash
git clone https://github.com/diegomezapy/curso_visualiza_datos_UNC.git
cd curso_visualiza_datos_UNC
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python datos/generar_datos.py                           # (opcional) regenera los datasets
python tools/py2nb.py                                   # convierte los labs a notebooks .ipynb
jupyter lab                                             # o abrí los .py en VS Code (celdas `# %%`)
```
Los laboratorios están escritos en formato *percent* (`# %%`): se ejecutan como script o como notebook. Las figuras se guardan en `salidas/` (ignorada por git).

## Estructura
```
datos/        datasets sintéticos y reproducibles (+ generar_datos.py)
src/cvd/      estilo (paleta accesible Okabe-Ito) y cargadores de datos
sesiones/     una carpeta por sesión: README (guía) + laboratorio
docs/         programa, cronograma, evaluación, rúbricas, integrador, quizzes
tools/        conversión a notebooks y generación de reportes
```

## Datos
Los datasets del curso son **sintéticos** (semilla fija) para garantizar reproducibilidad sin conexión. Los coeficientes y valores no representan información real. Para los mini-proyectos y el integrador se usarán **datos reales** (ver [docs/bibliografia.md](docs/bibliografia.md#fuentes-de-datos)).

## Licencia
Contenido docente: CC BY-NC-SA 4.0 · Código: MIT.
