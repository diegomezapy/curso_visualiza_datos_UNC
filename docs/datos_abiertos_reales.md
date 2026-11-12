# Datos abiertos reales para las prácticas

> *Generado por `tools/build_datos_reales.py` desde `datos_reales/catalogo.py`. No editar a mano.*

Las prácticas del curso usan **datos abiertos reales de Paraguay y de fuentes globales** (compras públicas, encuestas de hogares, nómina estatal, imágenes satelitales, comercio exterior…) para dar a cada ejercicio una pregunta con sentido y una audiencia real.

## ⚠️ Lea esto primero: estado real de cada fuente
El catálogo se armó con búsquedas en noviembre de 2026; **desde el entorno de desarrollo no se pudo abrir ninguna fuente ni inspeccionar filas**. Por eso:
- Cada fuente trae un **estado** (✅ documentada · 🔎 verificar acceso · ⚠️ incierto).
- **No hay nombres de columnas “de memoria”**: las prácticas se adaptan al esquema real (perfilado automático) o piden mapear las columnas con el diccionario oficial.
- Todas las prácticas **funcionan sin conexión con datos sintéticos claramente rotulados**, y se activan con datos reales al pegar la URL.
- **Antes de la primera clase**, el docente debe ejecutar `practicas_reales/pr00_verificar_fuentes` en Colab y revisar los pasos manuales (registro en Earth Engine, diccionario de la EPHC, ID del asset de MapBiomas…).

## Catálogo

| Fuente | Estado | Sesiones | Práctica |
|---|---|---|---|
| [Contrataciones públicas abiertas (DNCP)](#dncp) | ✅ Documentada | 2, 4, 5, 6, 8 | `pr02_dncp` |
| [Banco Mundial · Indicadores de desarrollo (WDI)](#bm) | ✅ Documentada | 2, 3, 7 | `pr03_banco_mundial` |
| [Encuesta Permanente de Hogares Continua (EPHC)](#ephc) | 🔎 Verificar acceso · 🔒 datos personales | 2, 3, 7 | `pr04_ephc_pesos` |
| [Nómina de funcionarios públicos](#nomina) | 🔎 Verificar acceso · 🔒 datos personales | 2, 3, 4, 8 | `pr05_nomina_privacidad` |
| [Comercio exterior · Aduanas (DNIT)](#aduanas) | ⚠️ Estado incierto | 4, 5, 7 | `pr03_banco_mundial` |
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

### Encuesta Permanente de Hogares Continua (EPHC) {#ephc}

**Instituto Nacional de Estadística (INE)** · 🔎 Verificar acceso · Microdatos de encuesta · CSV / SPSS / Stata (según publicación)

Hogares y personas: ingresos, empleo, educación, vivienda. Es una muestra: se necesita el factor de expansión para estimar a la población.

- **Portal:** <https://www.ine.gov.py> · **Documentación:** <https://www.bancomundial.org/es/news/press-release/2022/03/17/banco-mundial-apoya-desarrollo-del-primer-cat-logo-de-metadatos-y-microdatos-del-paraguay>
- **Práctica:** `pr04_ephc_pesos` — Datos de encuesta: por qué el peso muestral cambia la historia (Python/Colab)
- **Ideas:** Distribuciones ponderadas vs sin ponderar (S2); Gráficos honestos con incertidumbre (S3); Mapas por departamento con tasas (S7)
- **Cuidado:** El INE presentó en 2022 un catálogo de microdatos (7 de 13 operativos con acceso). Algunas bases se descargan directo y otras requieren solicitud. Hay subconjuntos publicados en datos.gov.py. Confirmar el acceso vigente y leer el diccionario de variables.

### Nómina de funcionarios públicos {#nomina}

**Viceministerio de Capital Humano y Gestión Organizacional (MEF)** · 🔎 Verificar acceso · Portal de datos abiertos · CSV (a confirmar)

Registros del personal permanente y contratado de las entidades del Estado (SICCA). La información no es completa: depende de lo que cada entidad reporta.

- **Portal:** <https://www.datos.gov.py> · **Documentación:** <https://www.datos.gov.py>
- **Práctica:** `pr05_nomina_privacidad` — Datos personales: visualizar sin exponer personas (Python/Colab)
- **Ideas:** Distribución salarial por entidad y brecha de género (S2–S3); KPIs de plantilla (S4); Ética: agregación y supresión de celdas pequeñas (S3)
- **Cuidado:** ⚠️ Contiene datos personales de personas identificables aunque sean públicos por ley. En el curso se trabaja SOLO con agregados: se descartan nombres y documentos al cargar y se suprimen grupos pequeños. Citar la fuente es obligatorio y los datos deben ser corroborados por quien los usa (aviso del propio VCHGO). Esta práctica usa datos sintéticos por defecto.

### Comercio exterior · Aduanas (DNIT) {#aduanas}

**Dirección Nacional de Ingresos Tributarios (absorbió a la Aduana)** · ⚠️ Estado incierto · Portal (en revisión) · a confirmar

Operaciones de importación y exportación. Su portal de datos abiertos fue retirado a fines de 2024 y la DNIT lo declaró «en revisión» (la ley restringe algunos datos). No se pudo confirmar si volvió a publicarse.

- **Portal:** <https://www.dnit.gov.py> · **Documentación:** <https://www.abc.com.py/economia/2024/12/20/dnit-actualizara-portal-de-datos-abiertos/>
- **Práctica:** `pr03_banco_mundial` — Comercio exterior (con alternativas) (Python/Colab y R/RPubs)
- **Ideas:** Si el portal está activo: series de importaciones/exportaciones por producto y país; Alternativas: Banco Mundial (WITS/WDI), UN Comtrade, Reporte de Comercio Exterior del BCP
- **Cuidado:** NO asumir que hay datos aduaneros disponibles. Verificar con pr00_verificar_fuentes o consultar a la DNIT; mientras tanto usar las alternativas.

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
| 2, 3 | `pr04_ephc_pesos` · Encuestas y pesos muestrales | Por qué ponderar cambia las conclusiones. |
| 3, 4 | `pr05_nomina_privacidad` · Datos personales y agregación | Visualizar sin exponer: anonimizar, agregar, suprimir celdas pequeñas. |
| 7 | `pr06_earth_engine_mapbiomas` · Earth Engine y MapBiomas | Cambio de uso del suelo con geemap. |

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
- [ ] **EPHC:** descargar la base vigente y su diccionario; anotar el nombre del factor de expansión; subir una **muestra** a la carpeta del curso (Drive).
- [ ] **Nómina:** localizar el conjunto y confirmar que se puede usar solo con agregados.
- [ ] **Aduanas:** confirmar si la DNIT volvió a publicar; si no, usar Banco Mundial / UN Comtrade / BCP.
- [ ] **DNCP:** probar una descarga masiva OCDS (JSON) y pegar la URL o ruta en la práctica 2.
