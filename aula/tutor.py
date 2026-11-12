"""Perfil público del tutor ("El tutor"). Fuente: CV normalizado FACEN (25-10-2026), CV CONACYT y lista de artículos de LinkedIn, en el Drive del docente.
Se omiten a propósito datos personales: fecha de nacimiento, teléfono, domicilio y correos.
Enlaces a perfiles: LINKS (abajo) + aula/config.json -> "tutor_links" (opcional, para ORCID, Scholar, etc., que no figuran en el CV)."""
LI = "https://es.linkedin.com/pulse/"
LINKS = [
 {"t": "LinkedIn", "u": "https://www.linkedin.com/in/diego-meza/"},
 {"t": "CV completo en CONACYT", "u": "https://cv.conacyt.gov.py/publicar/cv?id=ea46989c3d19cb9063f3b98999d33ab8"},
]
TUTOR = {
 "nombre": "Diego Bernardo Meza Bogado",
 "cita": "Diego Meza",
 "rol": "Profesor Escalafonado Asistente · Departamento de Estadística (Muestreo e Inferencia Estadística) · FaCEN-UNA",
 "resumen": "Licenciado en Ciencias Matemáticas (mención Estadística) y Magíster en Estadística. Trabajo con estadística aplicada, economía laboral y seguridad social, con énfasis en registros administrativos y datos abiertos, y con flujos reproducibles en R y Excel avanzado, más Python cuando corresponde. Lideré cuatro estudios actuariales del Fondo de Jubilaciones y Pensiones del IPS y diseñé el Boletín Estadístico de Seguridad Social 2024. Esa mezcla de datos reales, reproducibilidad y comunicación para decidir es la que traigo a este curso.",
 "areas": ["Estadística y análisis de datos", "Economía laboral y seguridad social", "Cálculo actuarial", "Programación (R, Python) para ciencia de datos", "Educación virtual"],
 "formacion": [
  ("2025 – en curso", "Doctorado en Ciencias Exactas, Naturales y sus Aplicaciones", "FaCEN-UNA · Tesis: la presencia de R en la ciencia, del análisis crítico de su adopción al desarrollo de librerías · Becario CONACYT"),
  ("2018 – 2019", "Diploma en Técnicas Actuariales Aplicadas a las Políticas Públicas", "Universidad de Chile"),
  ("2012 – 2014", "Magíster en Estadística", "FaCEN-UNA · Tesis: determinantes de la probabilidad de cotización en el sistema de jubilación del Paraguay"),
  ("2010 – 2011", "Especialista en Estadística", "FaCEN-UNA"),
  ("2006 – 2009", "Licenciatura en Ciencias Matemáticas, mención Estadística", "FaCEN-UNA"),
 ],
 "experiencia": [
  ("2024 – actual", "Profesor Escalafonado Asistente; tutor del Programa de Iniciación Científica", "FaCEN-UNA"),
  ("2023 – actual", "Asistente de investigación, Laboratorio de Investigación en Estadística Teórica y Aplicada", "FaCEN-UNA"),
  ("2023 – 2024", "Consultor estadístico: indicadores de seguridad social con registros administrativos", "OIT"),
  ("2024", "Jefe del Dpto. de Investigación y Estudios Socio Laborales", "Ministerio de Trabajo, Empleo y Seguridad Social"),
  ("2011 – 2026", "Instituto de Previsión Social (IPS): Jefe del Dpto. de Estadística Actuarial (2011-2022) y Técnico en Apoyo Médico (2025-2026)", ""),
  ("2012 – actual", "Docencia en modalidad virtual; cursos de Excel y análisis estadístico", "FaCEN-UNA y otras instituciones"),
 ],
 "produccion": [
  ("Artículo", "Cañiza Zaldívar, M. P. y Meza, D. (2023). Estudio de las frecuencias de cotizaciones en el Instituto de Previsión Social (IPS). RADEE, 3(5), 17-36.", "https://doi.org/10.56216/radee012023jun.a02"),
  ("Libro", "Situación actual y proyecciones del desarrollo futuro de la población de origen croata en Paraguay. Paragvajska udruga Hrvata / IMIN, 2022. ISBN 978-953-6028-68-9."),
  ("Producto", "Boletín Estadístico de Seguridad Social 2024 (MTESS)."),
  ("Informe técnico", "Situación de las Mujeres en la Seguridad Social, 2022 (MTESS). Disponible en informacionpublica.paraguay.gov.py."),
  ("Informe técnico", "Principales indicadores sobre cobertura de inmunización de asegurados del IPS contra la COVID-19, 2022: cruce de registros del IPS con datos abiertos del PAI."),
  ("Informe técnico", "Afectación del reajuste del Salario Mínimo Legal en trabajadores asalariados formales del sector privado, 2022."),
  ("Estudios actuariales", "Fondo de Jubilaciones y Pensiones del IPS: 2012-2062, 2015-2100, 2018-2100 y 2022-2100."),
  ("Investigación", "Determinantes del desempleo juvenil: una revisión histórica con la EPH 2006-2015, 2017 (CIRD)."),
 ],
 "divulgacion": [
  ("2025-04-28", "La evidencia cuantitativa en Seguridad Social", "https://www.linkedin.com/pulse/la-evidencia-cuantitativa-en-seguridad-social-meza-bogado-dtevf"),
  ("2025-03-15", "¡Da el salto a la ciencia de datos con R! Simula datos y comparte resultados con RPubs", LI + "da-el-salto-la-ciencia-de-datos-con-r-simula-y-forma-meza-bogado-q2qsf"),
  ("2025-03-12", "Uso de datos abiertos sobre contrataciones públicas con Python en Visual Studio Code", LI + "uso-de-datos-abiertos-sobre-contrataciones-p%C3%BAblicas-con-meza-bogado-pp04f"),
  ("2025-02-01", "Un repositorio colaborativo para el aprovechamiento de datos abiertos en Paraguay", LI + "impulsando-la-transparencia-y-innovaci%C3%B3n-un-para-el-de-meza-bogado-dvxxe"),
  ("2025-01-18", "Explorando la distribución normal multivariada en 3D: un recurso interactivo", LI + "explorando-la-distribuci%C3%B3n-normal-multivariada-en-3d-un-meza-bogado-o7r5f"),
  ("2024-12-12", "Visualización interactiva de distribuciones: gráficos de cajas y de violín", LI + "visualizaci%C3%B3n-interactiva-de-distribuciones-datos-con-meza-bogado-j0stf"),
  ("2024-11-25", "Uso combinado de herramientas tecnológicas para la generación de documentos en entornos virtuales de aprendizaje", LI + "uso-combinado-de-herramientas-tecnol%C3%B3gicas-para-la-en-meza-bogado-p5lve"),
  ("2024-11-23", "Potenciando la enseñanza de estadística y probabilidad con IA y herramientas gratuitas", LI + "potenciando-la-ense%C3%B1anza-de-estad%C3%ADstica-y-con-meza-bogado-bkflf"),
  ("2024-11-22", "Análisis estadístico con R y Shiny: aplicación interactiva para tasas de participación y ocupación", LI + "potenciando-el-an%C3%A1lisis-estad%C3%ADstico-con-r-y-shiny-de-una-meza-bogado-do9qf"),
  ("2024-10-18", "La trayectoria salarial y la tasa implícita de retorno individual en un sistema de pensiones", LI + "la-trayectoria-salarial-y-tasa-impl%C3%ADcita-de-retorno-en-meza-bogado-jticf"),
 ],
 "premios": [
  "2022 · Segunda mención de honor, póster en Ciencias Sociales (Paraguay)",
  "2019 · Primera mención de honor, Sociedad Científica del Paraguay",
  "2016 · Ganador del concurso de investigación sobre empleo juvenil (MTESS)",
 ],
 "docencia_inv": ["Cotutor de trabajos de iniciación a la investigación (FaCEN-UNA)", "Tutor principal de tesis de Maestría en Estadística sobre modelos espaciales (SDM y GWR) con el Censo Agropecuario 2022 (en curso)"],
 "idiomas": "Español (nativo) · Guaraní · Inglés (lectura buena)",
}
