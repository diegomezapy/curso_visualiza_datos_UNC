"""Catálogo curado de datos abiertos REALES para las prácticas del curso.
Fuente de verdad: de aquí salen la página «Datos abiertos» del aula, docs/datos_abiertos_reales.md y las prácticas.

CAMPO `estado` (honestidad sobre lo que se pudo comprobar al armar el catálogo, noviembre de 2026):
  "documentado"  → la fuente y su acceso aparecen en documentación oficial o en varias fuentes; no se pudo abrir desde el entorno de desarrollo.
  "verificar"    → hay indicios de que existe pero su disponibilidad o URL vigente es incierta: comprobar con practicas_reales/pr00_verificar_fuentes.
  "incierto"     → hubo cambios o bajas recientes (ver `aviso`).
Ninguna fila fue descargada ni inspeccionada aquí: los nombres de columnas se confirman con el diccionario de datos de cada fuente."""

FUENTES = [
 dict(id="dncp", nombre="Contrataciones públicas abiertas (DNCP)", inst="Dirección Nacional de Contrataciones Públicas", estado="documentado", sensible=False, tipo="API + descargas masivas",
  formato="OCDS (JSON) · CSV · Excel", url="https://www.contrataciones.gov.py/datos", doc="https://contrataciones.gov.py/datos/api/v3/doc/",
  contiene="Procesos de compra del Estado: planificación, convocatorias, adjudicaciones y contratos, con compradores y proveedores. Sigue el estándar internacional OCDS.",
  sesiones=[2, 4, 5, 6, 8], practica="pr02_dncp", titulo_practica="¿Quién compra qué, a quién y cuánto?",
  ideas=["KPIs de compras por entidad (S4)", "Tablero por método de contratación (S5)", "Informe parametrizado por entidad compradora (S6)", "Red comprador–proveedor y concentración (S8)"],
  aviso="Paraguay figura entre los países de la región con mayor disponibilidad de datos abiertos de compras públicas (La Nación, 2025). Los montos están en guaraníes y hay procesos sin adjudicar o cancelados: limpiar antes de sumar."),
 dict(id="bm", nombre="Banco Mundial · Indicadores de desarrollo (WDI)", inst="Banco Mundial", estado="documentado", sensible=False, tipo="API pública (sin clave)",
  formato="JSON / XML", url="https://data.worldbank.org", doc="https://datahelpdesk.worldbank.org/knowledgebase/articles/898581",
  contiene="Miles de indicadores por país y año (economía, comercio exterior, población, educación…). Permite comparar Paraguay con la región.",
  sesiones=[2, 3, 7], practica="pr03_banco_mundial", titulo_practica="Paraguay en la región: comercio exterior y economía",
  ideas=["Series temporales comparadas (S2–S3)", "Engaños: ejes y escalas (S3)", "Small multiples por país (S4)"],
  aviso="Los años más recientes suelen venir sin dato (NA). Es la alternativa estable para comercio exterior mientras se aclara el estado del portal de Aduanas."),
 dict(id="ephc", nombre="Encuesta Permanente de Hogares Continua (EPHC)", inst="Instituto Nacional de Estadística (INE)", estado="verificar", sensible=True, tipo="Microdatos de encuesta",
  formato="CSV / SPSS / Stata (según publicación)", url="https://www.ine.gov.py", doc="https://www.bancomundial.org/es/news/press-release/2022/03/17/banco-mundial-apoya-desarrollo-del-primer-cat-logo-de-metadatos-y-microdatos-del-paraguay",
  contiene="Hogares y personas: ingresos, empleo, educación, vivienda. Es una muestra: se necesita el factor de expansión para estimar a la población.",
  sesiones=[2, 3, 7], practica="pr04_ephc_pesos", titulo_practica="Datos de encuesta: por qué el peso muestral cambia la historia",
  ideas=["Distribuciones ponderadas vs sin ponderar (S2)", "Gráficos honestos con incertidumbre (S3)", "Mapas por departamento con tasas (S7)"],
  aviso="El INE presentó en 2022 un catálogo de microdatos (7 de 13 operativos con acceso). Algunas bases se descargan directo y otras requieren solicitud. Hay subconjuntos publicados en datos.gov.py. Confirmar el acceso vigente y leer el diccionario de variables."),
 dict(id="nomina", nombre="Nómina de funcionarios públicos", inst="Viceministerio de Capital Humano y Gestión Organizacional (MEF)", estado="verificar", sensible=True, tipo="Portal de datos abiertos",
  formato="CSV (a confirmar)", url="https://www.datos.gov.py", doc="https://www.datos.gov.py",
  contiene="Registros del personal permanente y contratado de las entidades del Estado (SICCA). La información no es completa: depende de lo que cada entidad reporta.",
  sesiones=[2, 3, 4, 8], practica="pr05_nomina_privacidad", titulo_practica="Datos personales: visualizar sin exponer personas",
  ideas=["Distribución salarial por entidad y brecha de género (S2–S3)", "KPIs de plantilla (S4)", "Ética: agregación y supresión de celdas pequeñas (S3)"],
  aviso="⚠️ Contiene datos personales de personas identificables aunque sean públicos por ley. En el curso se trabaja SOLO con agregados: se descartan nombres y documentos al cargar y se suprimen grupos pequeños. Citar la fuente es obligatorio y los datos deben ser corroborados por quien los usa (aviso del propio VCHGO). Esta práctica usa datos sintéticos por defecto."),
 dict(id="aduanas", nombre="Comercio exterior · Aduanas (DNIT)", inst="Dirección Nacional de Ingresos Tributarios (absorbió a la Aduana)", estado="incierto", sensible=False, tipo="Portal (en revisión)",
  formato="a confirmar", url="https://www.dnit.gov.py", doc="https://www.abc.com.py/economia/2024/12/20/dnit-actualizara-portal-de-datos-abiertos/",
  contiene="Operaciones de importación y exportación. Su portal de datos abiertos fue retirado a fines de 2024 y la DNIT lo declaró «en revisión» (la ley restringe algunos datos). No se pudo confirmar si volvió a publicarse.",
  sesiones=[4, 5, 7], practica="pr03_banco_mundial", titulo_practica="Comercio exterior (con alternativas)",
  ideas=["Si el portal está activo: series de importaciones/exportaciones por producto y país", "Alternativas: Banco Mundial (WITS/WDI), UN Comtrade, Reporte de Comercio Exterior del BCP"],
  aviso="NO asumir que hay datos aduaneros disponibles. Verificar con pr00_verificar_fuentes o consultar a la DNIT; mientras tanto usar las alternativas."),
 dict(id="mapbiomas", nombre="MapBiomas Paraguay · Cobertura y uso del suelo", inst="MapBiomas Paraguay", estado="documentado", sensible=False, tipo="Ráster en Google Earth Engine + estadísticas descargables",
  formato="Ráster 30 m anual (1985–2023, Colección 2) · tablas de estadísticas", url="https://paraguay.mapbiomas.org", doc="https://paraguay.mapbiomas.org/en/productos/",
  contiene="Mapas anuales de cobertura y uso del suelo. Las estadísticas en hectáreas por departamento y distrito se pueden descargar sin usar Earth Engine.",
  sesiones=[7], practica="pr06_earth_engine_mapbiomas", titulo_practica="Cambio de uso del suelo en Paraguay (1985–2023)",
  ideas=["Series de área por clase y departamento (S7)", "Mapas de cambio (S7)", "Coropletas con tasas, no conteos (S7)"],
  aviso="El sitio indica usar siempre la versión más reciente. El ID del asset en Earth Engine que figura en el sitio contiene «collection1» aunque se rotula como Colección 2: VERIFICAR el ID vigente en paraguay.mapbiomas.org antes de la clase. Uso libre para fines no comerciales o de interés público; citar a MapBiomas."),
 dict(id="gee", nombre="Google Earth Engine · Catálogo global", inst="Google", estado="documentado", sensible=False, tipo="Plataforma (requiere cuenta y proyecto Cloud)",
  formato="Imágenes y tablas vectoriales", url="https://earthengine.google.com", doc="https://developers.google.com/earth-engine/guides/python_install",
  contiene="Petabytes de imágenes satelitales y datos geoespaciales (elevación, temperatura, vegetación, límites). En Colab, `ee` y `geemap` ya vienen instalados.",
  sesiones=[7], practica="pr06_earth_engine_mapbiomas", titulo_practica="Primer mapa con Earth Engine y geemap",
  ideas=["Relieve (SRTM) y límites del país", "Combinar con MapBiomas"],
  aviso="Gratis para uso no comercial y de investigación, pero requiere REGISTRARSE y crear un proyecto de Google Cloud ANTES de la clase (la aprobación puede demorar). En Colab: ee.Authenticate() y ee.Initialize(project=…)."),
 dict(id="datosgov", nombre="Portal de Datos Abiertos de Paraguay", inst="Gobierno de Paraguay", estado="verificar", sensible=False, tipo="Portal / catálogo",
  formato="CSV, XLS, JSON, PDF (según conjunto)", url="https://www.datos.gov.py", doc="https://www.datos.gov.py",
  contiene="Catálogo de conjuntos de varias instituciones (incluye subconjuntos del INE, como estadísticas vitales o EPHC). La calidad y la actualización varían mucho.",
  sesiones=[1, 2, 7], practica="pr01_explorador", titulo_practica="Explorador de datasets: perfilar y graficar cualquier tabla",
  ideas=["Elegir un conjunto y hacer el «primer vistazo» (S2)", "Dataset del proyecto integrador"],
  aviso="No se pudo confirmar desde aquí si el portal ofrece una API (tipo CKAN); descargar los archivos manualmente y pegar la URL del recurso."),
 dict(id="bcp", nombre="Banco Central del Paraguay · Estadísticas", inst="Banco Central del Paraguay (BCP)", estado="verificar", sensible=False, tipo="Descargas en el sitio (API no confirmada)",
  formato="Excel / PDF", url="https://www.bcp.gov.py", doc="https://www.bcp.gov.py",
  contiene="Series monetarias y financieras, tipo de cambio, sector externo (incluye el Reporte de Comercio Exterior mensual), cuentas nacionales.",
  sesiones=[3, 4, 7], practica="pr01_explorador", titulo_practica="Series macro desde Excel",
  ideas=["Serie de tipo de cambio o inflación (S3 y S7)", "KPIs macro (S4)"],
  aviso="No se confirmó una API oficial; existen republicadores de terceros (p. ej. Alphacast) con sus propios términos. Los Excel cambian de formato: revisar a mano."),
 dict(id="mef", nombre="Presupuesto General de la Nación · Ejecución", inst="Ministerio de Economía y Finanzas (MEF)", estado="verificar", sensible=False, tipo="Informes (PDF) y reportes",
  formato="PDF / Excel (datasets a confirmar)", url="https://www.economia.gov.py", doc="https://www.economia.gov.py",
  contiene="Presupuesto aprobado y ejecutado por entidad. Los datos provienen del sistema contable (SICO).",
  sesiones=[4, 5], practica="pr01_explorador", titulo_practica="Ejecución presupuestaria",
  ideas=["KPIs de ejecución por entidad (S4)", "Tablero de gasto (S5)"],
  aviso="No se encontró un catálogo de datos abiertos abierto/estructurado: muchos informes están en PDF. Evaluar si conviene extraer tablas o usar otra fuente."),
]

POR_ID = {f["id"]: f for f in FUENTES}
ESTADOS = {"documentado": ("✅", "Documentada"), "verificar": ("🔎", "Verificar acceso"), "incierto": ("⚠️", "Estado incierto")}
PRACTICAS = [
 ("pr00_verificar_fuentes", "Verificar fuentes (docente)", "Comprueba en Colab cuáles fuentes responden hoy y qué estructura tienen.", [1], "docente"),
 ("pr01_explorador", "Explorador de datasets", "Perfila cualquier CSV/Excel y propone gráficos según el tipo de dato.", [1, 2], "estudiante"),
 ("pr02_dncp", "Contrataciones públicas (DNCP)", "OCDS → tabla ordenada → KPIs, series y red comprador–proveedor.", [4, 5, 8], "estudiante"),
 ("pr03_banco_mundial", "Paraguay en la región (Banco Mundial)", "API pública: series, comparaciones y gráficos honestos.", [2, 3], "estudiante"),
 ("pr04_ephc_pesos", "Encuestas y pesos muestrales", "Por qué ponderar cambia las conclusiones.", [2, 3], "estudiante"),
 ("pr05_nomina_privacidad", "Datos personales y agregación", "Visualizar sin exponer: anonimizar, agregar, suprimir celdas pequeñas.", [3, 4], "estudiante"),
 ("pr06_earth_engine_mapbiomas", "Earth Engine y MapBiomas", "Cambio de uso del suelo con geemap.", [7], "estudiante"),
]
