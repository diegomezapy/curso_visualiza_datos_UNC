# Datos abiertos reales para las prácticas

> *Generado por `tools/build_datos_reales.py` desde `datos_reales/catalogo.py`. No editar a mano.*

Las prácticas del curso usan **datos abiertos reales de Paraguay y de fuentes globales** (compras públicas, encuestas de hogares, nómina estatal, imágenes satelitales, comercio exterior…) para dar a cada ejercicio una pregunta con sentido y una audiencia real.

## ⚠️ Lea esto primero: estado real de cada fuente
El catálogo se armó en noviembre de 2026. **Dos fuentes se descargaron e inspeccionaron de verdad** (🟢 EPHC del INE y recaudación de la DNIT); **las demás solo se documentaron con búsquedas** porque desde el entorno de desarrollo no fue posible abrirlas. Por eso:
- Cada fuente trae un **estado** (🟢 verificada · ✅ documentada · 🔎 verificar acceso · ⚠️ incierto).
- En las fuentes no verificadas **no hay nombres de columnas “de memoria”**: las prácticas se adaptan al esquema real (perfilado automático) o piden mapear las columnas con el diccionario oficial.
- Todas las prácticas **funcionan sin conexión con datos sintéticos claramente rotulados**, y se activan con datos reales al pegar la URL.
- **Antes de la primera clase**, el docente debe ejecutar `practicas_reales/pr00_verificar_fuentes` en Colab y revisar los pasos manuales (registro en Earth Engine, diccionario de la EPHC, ID del asset de MapBiomas…).

## Catálogo

| Fuente | Estado | Sesiones | Práctica |
|---|---|---|---|
| [Contrataciones públicas abiertas (DNCP)](#dncp) | ✅ Documentada | 2, 4, 5, 6, 8 | `pr02_dncp` |
| [Banco Mundial · Indicadores de desarrollo (WDI)](#bm) | ✅ Documentada | 2, 3, 7 | `pr03_banco_mundial` |
| [Encuesta Permanente de Hogares Continua (EPHC) anual](#ephc) | 🟢 Verificada (descargada e inspeccionada) · 🔒 datos personales | 2, 3, 7 | `pr04_ephc_pesos` |
| [Funcionarios públicos (SFP)](#nomina) | 🔎 Verificar acceso · 🔒 datos personales | 2, 3, 4, 8 | `pr05_nomina_privacidad` |
| [Recaudación tributaria por impuesto, departamento, distrito y actividad (DNIT)](#dnit) | 🟢 Verificada (descargada e inspeccionada) | 2, 4, 5, 7 | `pr07_dnit_recaudacion` |
| [Comercio exterior · Aduanas (importaciones y exportaciones)](#aduanas) | ⚠️ Estado incierto | 4, 5, 7 | `pr03_banco_mundial` |
| [MapBiomas Paraguay · Cobertura y uso del suelo](#mapbiomas) | ✅ Documentada | 7 | `pr06_earth_engine_mapbiomas` |
| [Google Earth Engine · Catálogo global](#gee) | ✅ Documentada | 7 | `pr06_earth_engine_mapbiomas` |
| [Portal de Datos Abiertos de Paraguay](#datosgov) | 🔎 Verificar acceso | 1, 2, 7 | `pr01_explorador` |
| [Banco Central del Paraguay · Estadísticas](#bcp) | 🔎 Verificar acceso | 3, 4, 7 | `pr01_explorador` |
| [Presupuesto General de la Nación · Ejecución](#mef) | 🔎 Verificar acceso | 4, 5 | `pr01_explorador` |

### Contrataciones públicas abiertas (DNCP) {#dncp}

**Dirección Nacional de Contrataciones Públicas** · ✅ Documentada · API + descargas masivas · OCDS (JSON) · CSV · Excel

Procesos de compra del Estado: planificación, convocatorias, adjudicaciones y contratos, con compradores y proveedores. Sigue el estándar internacional OCDS.

- **Portal:** <https://www.contrataciones.gov.py/datos> · **Documentación:** <https://contrataciones.gov.py/datos/api/v3/doc/>
- **Práctica:** `pr02_dncp` — ¿Quién compra qué, a quién y cuánto? (Python/Colab y R/RPubs)
- **Ideas:** KPIs de compras por entidad (S4); Tablero por método de contratación (S5); Informe parametrizado por entidad compradora (S6); Red comprador–proveedor y concentración (S8)
- **Cuidado:** Paraguay figura entre los países de la región con mayor disponibilidad de datos abiertos de compras públicas (La Nación, 2025). Los montos están en guaraníes y hay procesos sin adjudicar o cancelados: limpiar antes de sumar.

### Banco Mundial · Indicadores de desarrollo (WDI) {#bm}

**Banco Mundial** · ✅ Documentada · API pública (sin clave) · JSON / XML

Miles de indicadores por país y año (economía, comercio exterior, población, educación…). Permite comparar Paraguay con la región.

- **Portal:** <https://data.worldbank.org> · **Documentación:** <https://datahelpdesk.worldbank.org/knowledgebase/articles/898581>
- **Práctica:** `pr03_banco_mundial` — Paraguay en la región: comercio exterior y economía (Python/Colab y R/RPubs)
- **Ideas:** Series temporales comparadas (S2–S3); Engaños: ejes y escalas (S3); Small multiples por país (S4)
- **Cuidado:** Los años más recientes suelen venir sin dato (NA). Es la alternativa estable para comercio exterior mientras se aclara el estado del portal de Aduanas.

### Encuesta Permanente de Hogares Continua (EPHC) anual {#ephc}

**Instituto Nacional de Estadística (INE)** · 🟢 Verificada (descargada e inspeccionada) · Microdatos de encuesta (descarga directa) · CSV (;) · SAV · diccionario XLS/DOC

Personas, viviendas e ingreso familiar de hogares paraguayos, años 2022–2025 (tablas REG02 personas, REG01 viviendas, INGREFAM). El archivo de personas 2025 tiene 55.934 filas y 213 variables. Es una muestra: se necesita el factor de expansión (variable FACTOR) para estimar a la población.

- **Portal:** <https://www.ine.gov.py/microdatos/> · **Documentación:** <https://www.ine.gov.py/microdatos/register/EPHC-ANUAL/EPHC_2025_ANUAL/diccionario_EPHC_ANUAL_2025.xls>
- **Práctica:** `pr04_ephc_pesos` — Encuestas: por qué el peso muestral cambia la historia (Python/Colab)
- **Ideas:** Distribuciones ponderadas vs sin ponderar (S2); Brecha de ingreso con intervalo de confianza (S3); Pobreza por departamento como tasa ponderada (S7)
- **Cuidado:** Verificada: archivo REG02 2025 descargado e inspeccionado. Particularidades reales: separador «;», UTF-8 con BOM, coma decimal, celdas en blanco como espacio, códigos especiales (p. ej. añoest = 99) y valores extremos de ingreso. Variables útiles: FACTOR, AREA (1 urbana, 6 rural), P06 (1 hombre, 6 mujer), P02 (edad), DPTO (0–15), añoest, e01aimde (ingreso mensual de la ocupación principal), PEAA (1 ocupados), pobrezai (1 extrema, 2 no extrema, 3 no pobre), ipcm, quintili. Licencia (Decreto 4064/Ley 5282/2014): citar la fuente y la fecha de actualización y no sugerir patrocinio oficial. Los microdatos están anonimizados pero describen personas: trabajar con agregados. La práctica incluye una muestra real de 3.000 filas para uso sin conexión.

### Funcionarios públicos (SFP) {#nomina}

**Secretaría de la Función Pública (SFP) · datos del SICCA** · 🔎 Verificar acceso · Portal de datos abiertos (descarga) · a confirmar (CSV/ZIP)

Registros del personal permanente y contratado de las entidades del Estado. Según constancias del MEF, la información no es completa: depende de lo que cada entidad reporta, y los datos deben ser corroborados por quien los usa.

- **Portal:** <https://datos.sfp.gov.py> · **Documentación:** <https://datos.sfp.gov.py/data/funcionarios/download>
- **Práctica:** `pr05_nomina_privacidad` — Datos personales: visualizar sin exponer personas (Python/Colab)
- **Ideas:** Distribución salarial por entidad y brecha de género (S2–S3); KPIs de plantilla (S4); Ética: agregación y supresión de celdas pequeñas (S3)
- **Cuidado:** ⚠️ No se pudo conectar a datos.sfp.gov.py desde el entorno de desarrollo (el servidor cierra la conexión TLS durante el handshake), por eso NO se inspeccionó el archivo ni se conocen sus columnas. Probar desde Colab (pr00) o descargarlo con el navegador y subirlo. Contiene datos personales de personas identificables aunque sean públicos por ley: en el curso se trabaja SOLO con agregados (se descartan nombres y documentos al cargar y se suprimen grupos pequeños). Esta práctica usa datos sintéticos por defecto.

### Recaudación tributaria por impuesto, departamento, distrito y actividad (DNIT) {#dnit}

**Dirección Nacional de Ingresos Tributarios (DNIT)** · 🟢 Verificada (descargada e inspeccionada) · Excel por año (descarga directa) · XLSX (≈35 MB por año) · 2016–2026

Recaudación mensual por tipo de impuesto (internos y aduaneros), categoría y tipo de contribuyente, actividad económica principal (694 actividades), departamento y distrito (247). El archivo de 2025 tiene 652.021 filas y suma ≈ 42,3 billones de Gs. También hay detalle de contribuyentes por estado, departamento y obligación, y reportes mensuales en PDF.

- **Portal:** <https://www.dnit.gov.py/web/portal-institucional/estadisticas> · **Documentación:** <https://www.dnit.gov.py/web/portal-institucional/estadisticas>
- **Práctica:** `pr07_dnit_recaudacion` — ¿Quién paga y dónde? Recaudación tributaria en Paraguay (Python/Colab)
- **Ideas:** Serie mensual y estacionalidad (S2, S7); Pareto de actividades económicas (S2); KPIs de recaudación (S4); Concentración por distrito: curva de Lorenz (S7)
- **Cuidado:** Verificada: archivo 2025 descargado e inspeccionado. Hay que limpiar: al pie del Excel hay notas explicativas dentro de la columna Mes y el año viene como texto. El departamento es el del DOMICILIO FISCAL del contribuyente, no el lugar donde ocurre la actividad (CAPITAL concentra más de la mitad). Los datos son agregados (no personas). El enlace de descarga cambia (lleva identificador y marca de tiempo): la práctica lo busca en la página de Estadísticas. Citar la fuente y la fecha; la DNIT puede restringir datos por ley.

### Comercio exterior · Aduanas (importaciones y exportaciones) {#aduanas}

**Dirección Nacional de Ingresos Tributarios (absorbió a la Aduana)** · ⚠️ Estado incierto · Sin conjunto descargable verificado · —

Verificado en noviembre de 2026: la página «Datos abiertos» de la DNIT NO lista conjuntos descargables y su sección «Estadísticas» publica recaudación (ver arriba), no flujos de importación/exportación. El portal de datos aduaneros fue retirado a fines de 2024 y la DNIT lo declaró «en revisión».

- **Portal:** <https://www.dnit.gov.py/web/portal-institucional/datos-abiertos> · **Documentación:** <https://www.abc.com.py/economia/2024/12/20/dnit-actualizara-portal-de-datos-abiertos/>
- **Práctica:** `pr03_banco_mundial` — Comercio exterior (con alternativas) (Python/Colab y R/RPubs)
- **Ideas:** Alternativas: Banco Mundial (WDI/WITS), UN Comtrade, Reporte de Comercio Exterior del BCP; Recaudación aduanera por departamento/actividad (práctica DNIT)
- **Cuidado:** NO asumir que hay datos de comercio exterior por producto o país en la DNIT. Consultar a la institución o usar las alternativas.

### MapBiomas Paraguay · Cobertura y uso del suelo {#mapbiomas}

**MapBiomas Paraguay** · ✅ Documentada · Ráster en Google Earth Engine + estadísticas descargables · Ráster 30 m anual (1985–2023, Colección 2) · tablas de estadísticas

Mapas anuales de cobertura y uso del suelo. Las estadísticas en hectáreas por departamento y distrito se pueden descargar sin usar Earth Engine.

- **Portal:** <https://paraguay.mapbiomas.org> · **Documentación:** <https://paraguay.mapbiomas.org/en/productos/>
- **Práctica:** `pr06_earth_engine_mapbiomas` — Cambio de uso del suelo en Paraguay (1985–2023) (Python/Colab)
- **Ideas:** Series de área por clase y departamento (S7); Mapas de cambio (S7); Coropletas con tasas, no conteos (S7)
- **Cuidado:** El sitio indica usar siempre la versión más reciente. El ID del asset en Earth Engine que figura en el sitio contiene «collection1» aunque se rotula como Colección 2: VERIFICAR el ID vigente en paraguay.mapbiomas.org antes de la clase. Uso libre para fines no comerciales o de interés público; citar a MapBiomas.

### Google Earth Engine · Catálogo global {#gee}

**Google** · ✅ Documentada · Plataforma (requiere cuenta y proyecto Cloud) · Imágenes y tablas vectoriales

Petabytes de imágenes satelitales y datos geoespaciales (elevación, temperatura, vegetación, límites). En Colab, `ee` y `geemap` ya vienen instalados.

- **Portal:** <https://earthengine.google.com> · **Documentación:** <https://developers.google.com/earth-engine/guides/python_install>
- **Práctica:** `pr06_earth_engine_mapbiomas` — Primer mapa con Earth Engine y geemap (Python/Colab)
- **Ideas:** Relieve (SRTM) y límites del país; Combinar con MapBiomas
- **Cuidado:** Gratis para uso no comercial y de investigación, pero requiere REGISTRARSE y crear un proyecto de Google Cloud ANTES de la clase (la aprobación puede demorar). En Colab: ee.Authenticate() y ee.Initialize(project=…).

### Portal de Datos Abiertos de Paraguay {#datosgov}

**Gobierno de Paraguay** · 🔎 Verificar acceso · Portal / catálogo · CSV, XLS, JSON, PDF (según conjunto)

Catálogo de conjuntos de varias instituciones (incluye subconjuntos del INE, como estadísticas vitales o EPHC). La calidad y la actualización varían mucho.

- **Portal:** <https://www.datos.gov.py> · **Documentación:** <https://www.datos.gov.py>
- **Práctica:** `pr01_explorador` — Explorador de datasets: perfilar y graficar cualquier tabla (Python/Colab y R/RPubs)
- **Ideas:** Elegir un conjunto y hacer el «primer vistazo» (S2); Dataset del proyecto integrador
- **Cuidado:** No se pudo confirmar desde aquí si el portal ofrece una API (tipo CKAN); descargar los archivos manualmente y pegar la URL del recurso.

### Banco Central del Paraguay · Estadísticas {#bcp}

**Banco Central del Paraguay (BCP)** · 🔎 Verificar acceso · Descargas en el sitio (API no confirmada) · Excel / PDF

Series monetarias y financieras, tipo de cambio, sector externo (incluye el Reporte de Comercio Exterior mensual), cuentas nacionales.

- **Portal:** <https://www.bcp.gov.py> · **Documentación:** <https://www.bcp.gov.py>
- **Práctica:** `pr01_explorador` — Series macro desde Excel (Python/Colab y R/RPubs)
- **Ideas:** Serie de tipo de cambio o inflación (S3 y S7); KPIs macro (S4)
- **Cuidado:** No se confirmó una API oficial; existen republicadores de terceros (p. ej. Alphacast) con sus propios términos. Los Excel cambian de formato: revisar a mano.

### Presupuesto General de la Nación · Ejecución {#mef}

**Ministerio de Economía y Finanzas (MEF)** · 🔎 Verificar acceso · Informes (PDF) y reportes · PDF / Excel (datasets a confirmar)

Presupuesto aprobado y ejecutado por entidad. Los datos provienen del sistema contable (SICO).

- **Portal:** <https://www.economia.gov.py> · **Documentación:** <https://www.economia.gov.py>
- **Práctica:** `pr01_explorador` — Ejecución presupuestaria (Python/Colab y R/RPubs)
- **Ideas:** KPIs de ejecución por entidad (S4); Tablero de gasto (S5)
- **Cuidado:** No se encontró un catálogo de datos abiertos abierto/estructurado: muchos informes están en PDF. Evaluar si conviene extraer tablas o usar otra fuente.

## Ruta de prácticas por sesión

| Sesión | Práctica | Qué se aprende |
|---|---|---|
| 1 | `pr00_verificar_fuentes` · Verificar fuentes (docente) *(docente)* | Comprueba en Colab cuáles fuentes responden hoy y qué estructura tienen. |
| 1, 2 | `pr01_explorador` · Explorador de datasets | Perfila cualquier CSV/Excel y propone gráficos según el tipo de dato. |
| 4, 5, 8 | `pr02_dncp` · Contrataciones públicas (DNCP) | OCDS → tabla ordenada → KPIs, series y red comprador–proveedor. |
| 2, 3 | `pr03_banco_mundial` · Paraguay en la región (Banco Mundial) | API pública: series, comparaciones y gráficos honestos. |
| 2, 3 | `pr04_ephc_pesos` · EPHC (INE): encuestas y pesos muestrales | Microdatos reales: por qué ponderar cambia las conclusiones. |
| 3, 4 | `pr05_nomina_privacidad` · Datos personales y agregación | Visualizar sin exponer: anonimizar, agregar, suprimir celdas pequeñas. |
| 7 | `pr06_earth_engine_mapbiomas` · Earth Engine y MapBiomas | Cambio de uso del suelo con geemap. |
| 2, 4, 7 | `pr07_dnit_recaudacion` · Recaudación tributaria (DNIT) | Datos reales sucios: limpiar, tidy, Pareto, series y concentración. |

## Reglas de oro con datos reales
1. **Citar** la fuente, la URL y la **fecha de descarga**; completar la *ficha del dataset* (práctica 1).
2. **No confiar en un dato porque sea oficial**: perfilar, buscar nulos, duplicados y cambios de definición.
3. **Datos personales:** trabajar solo con agregados; descartar nombres y documentos al cargar; suprimir grupos pequeños (práctica 5). Lo que se publica en RPubs es público.
4. **Encuestas:** usar el factor de expansión (práctica 4).
5. **Mapas:** tasas o densidades, no conteos (sesión 7).
6. **Licencias:** verificar las condiciones de uso; MapBiomas (no comercial o interés público, citar), datos del VCHGO (reconocer la fuente y corroborar), etc.
7. **Si una fuente cae o cambia**, el código lo avisa y usa datos sintéticos: nunca presentar esos resultados como reales.

## Para el docente: lista de verificación previa
- [ ] Ejecutar `pr00_verificar_fuentes` en Colab y guardar la tabla.
- [ ] **Earth Engine:** que cada estudiante se registre y cree un proyecto de Cloud (puede demorar); verificar el ID del asset de MapBiomas.
- [x] **EPHC (INE):** verificada (archivo REG02 2025). Revisar cada año que se use y el diccionario de variables.
- [x] **Recaudación (DNIT):** verificada (Excel 2025). Su enlace cambia: la práctica lo busca en la página de Estadísticas.
- [ ] **Funcionarios (SFP):** el servidor no pudo abrirse desde el entorno de desarrollo (falla la verificación del certificado TLS). Probar desde Colab; si falla, descargar con el navegador, subir el archivo y mapear las columnas (práctica 5).
- [ ] **Aduanas:** la DNIT no publica importaciones/exportaciones en su página de datos abiertos (verificado); usar Banco Mundial / UN Comtrade / BCP.
- [ ] **DNCP:** probar una descarga masiva OCDS (JSON) y pegar la URL o ruta en la práctica 2.
