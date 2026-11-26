/* Presentación editable de la práctica de la unidad 7.
   Ejecutar desde la raíz del repositorio con el runtime de presentaciones de Codex.
   Las capturas proceden de una ejecución real en el Code Editor el 2026-11-26.
   El script completo para estudiantes está en aula/practicas/earth_engine_ndvi_asuncion.js. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const root = process.cwd();
const asset = path.join(root, 'aula/media/unidad7_earth_engine/fuentes');
const crop = path.join(asset, 'recortes');
const out = path.join(asset, 'Visualizacion_georreferenciada_Earth_Engine_FACET_UNC.pptx');
const skill = '/Users/diegobernardomezabogado/.codex/plugins/cache/openai-primary-runtime/presentations/26.1119.11507/skills/presentations';
const python = '/Users/diegobernardomezabogado/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const W = 1280, H = 720;
const ink = '#17252F', muted = '#42515C', accent = '#AC7816';
const sans = 'Arial', serif = 'Arial';

const pres = Presentation.create({ slideSize: { width: W, height: H } });

function txt(slide, text, x, y, w, h, size=20, color=ink, bold=false, font=sans) {
  const s = slide.shapes.add({ geometry: 'textbox', position: {left:x,top:y,width:w,height:h},
    fill:'none', line:{style:'solid',fill:'none',width:0} });
  s.text = text;
  s.text.style = { fontFamily:font, fontSize:`${size}pt`, color, bold, verticalAlignment:'top' };
  return s;
}
async function img(slide, file, x, y, w, h, alt) {
  const b = await fs.readFile(path.join(crop,file));
  slide.images.add({ blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength), contentType:'image/png',
    alt, fit:'contain', position:{left:x,top:y,width:w,height:h} });
}
async function seal(slide, number) {
  const b=await fs.readFile(path.join(asset,'escudo_unc.png'));
  slide.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',
    alt:'Escudo de la Universidad Nacional de Concepción, extraído del programa de la asignatura',
    fit:'contain',position:{left:60,top:20,width:63,height:72}});
  txt(slide,'Universidad Nacional de Concepción',141,23,650,24,17,ink,false,serif);
  txt(slide,'Facultad de Ciencias Exactas y Tecnológicas · Maestría en Ingeniería y Ciencia de Datos',141,51,970,25,13,muted,false,serif);
  const line=slide.shapes.add({geometry:'rect',position:{left:60,top:103,width:1160,height:2},fill:ink,
    line:{style:'solid',fill:'none',width:0}});
  line.name='Línea del membrete institucional';
  txt(slide,'Visualización de datos · Unidad 7 · 2.º semestre de 2026',60,686,1020,20,11,muted);
  txt(slide,String(number).padStart(2,'0'),1168,684,50,23,11,muted);
}
async function slide(title, body, note='') {
  const s=pres.slides.add(); s.background.fill='#FFFFFF';
  await seal(s,pres.slides.items.length);
  txt(s,title,60,123,1160,64,30,ink,true);
  if(body) txt(s,body,62,198,1150,370,20,ink);
  s.speakerNotes.text=note;
  return s;
}
async function codeSlide(title, file, explanation, note) {
  const s=await slide(title,'',note);
  await img(s,file,62,205,1155,300,`Captura real del Code Editor: ${title}`);
  txt(s,explanation,62,523,1150,130,19,ink);
  return s;
}
async function pictureSlide(title, file, explanation, note) {
  const s=await slide(title,'',note);
  await img(s,file,73,195,570,467,`Captura real de Earth Engine: ${title}`);
  txt(s,explanation,687,224,507,366,20,ink);
  return s;
}

let s=await slide('Visualización georreferenciada con Google Earth Engine',
  'Práctica guiada con Sentinel-2\nAsunción y entorno · mayo a agosto de 2025\nColor natural, NDVI, Inspector e histograma',
  'Membrete y escudo: Programa de estudios Visualización de datos, FACET-UNC, facilitado por el docente. Google Earth Engine: https://developers.google.com/earth-engine/guides/quickstart_javascript');
txt(s,'Ejercicio formativo de la Unidad 7',62,578,850,35,16,accent,true);

s=await slide('Propósito y productos de la práctica',
  'Al terminar, cada estudiante podrá construir un mapa de color natural y un mapa NDVI sobre la misma área.\n\nTambién podrá inspeccionar píxeles, leer la distribución del NDVI y calcular una media espacial.\n\nProducto para el aula: dos capturas de mapa, una del histograma, una interpretación breve en el foro de la Unidad 7 y el quiz 7A.',
  'La actividad usa imágenes públicas del catálogo de Google Earth Engine. No se publican datos personales del docente ni de estudiantes.');

s=await slide('Datos y decisiones antes de abrir el editor',
  'Colección: COPERNICUS/S2_SR_HARMONIZED, reflectancia de superficie armonizada.\n\nÁrea: rectángulo [-57.59, -25.38, -57.43, -25.21] en longitud, latitud.\n\nPeriodo: 2025-05-01 al 2025-09-01. La fecha final es exclusiva.\n\nFiltro preliminar: menos de 30 % de nubosidad por escena. Después se aplica una máscara SCL por píxel.',
  'Fuente de bandas, escala y SCL: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED');

await codeSlide('Paso 1 · Acceso y área de estudio','02_area_filtros_codigo.png',
  'Abrí code.earthengine.google.com, seleccioná un proyecto habilitado y creá un script. El rectángulo usa longitud oeste, latitud sur, longitud este y latitud norte. El mapa se centra luego en esa geometría.',
  'Captura del Code Editor tomada durante la ejecución real del 2026-11-26. Referencia: https://developers.google.com/earth-engine/guides/quickstart_javascript');
await codeSlide('Paso 2 · Colección y filtros','03_mascara_codigo.png',
  'filterBounds(area) selecciona escenas que intersectan el rectángulo. filterDate fija el periodo y CLOUDY_PIXEL_PERCENTAGE elimina escenas demasiado nubladas. La consola mostró 48 escenas candidatas en esta ejecución.',
  'El valor de nubosidad es metadato de la escena, no una medida exclusiva del área. Fuente: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED');
await codeSlide('Paso 3 · Máscara de superficies visibles','03_mascara_detalle.png',
  'SCL 4 identifica vegetación y SCL 5 suelo desnudo o no vegetado. La función aplica esa máscara a cada escena y convierte las bandas B2, B3, B4 y B8 a reflectancia multiplicando por 0,0001.',
  'SCL tiene resolución nominal de 20 m; B2, B3, B4 y B8 de 10 m. Fuente: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED');
await codeSlide('Paso 4 · Compuesto y recorte','04_compuesto_ndvi_codigo.png',
  'map(superficieVisible) procesa cada escena. median() toma la mediana temporal por píxel y banda. clip(area) limita el resultado al rectángulo. Los píxeles sin observaciones válidas quedan transparentes.',
  'Fuente de API: https://developers.google.com/earth-engine/apidocs/ee-imagecollection-median');
await codeSlide('Paso 5 · Color natural y NDVI','05_color_ndvi_codigo.png',
  'Color natural asigna B4 al rojo, B3 al verde y B2 al azul. El NDVI usa (B8 − B4) / (B8 + B4), con B8 en infrarrojo cercano. La paleta y los límites min/max controlan solo la representación.',
  'Fuente de bandas: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED');
await pictureSlide('Paso 6 · Inspección del color natural','08_color_natural_mapa.png',
  'En Layers, desactivá NDVI para ver la composición RGB. La imagen recortada conserva patrones de ciudad, suelo y vegetación. Compará esta vista con el NDVI sin cambiar el área ni el periodo.',
  'Captura real en Earth Engine, 2026-11-26. Datos Sentinel-2 SR armonizados, Google Earth Engine.');
await pictureSlide('Paso 7 · Mapa NDVI','02_area_filtros_mapa.png',
  'Activá NDVI. La paleta viridis muestra valores entre 0 y 0,8; valores mayores quedan saturados en el extremo de la escala. El mapa revela patrones relativos dentro de los píxeles no enmascarados.',
  'Captura real en Earth Engine, 2026-11-26. Los colores no son clases de cobertura del suelo.');
await pictureSlide('Paso 8 · Inspector: píxel con NDVI alto','09_inspector_vegetacion_panel.png',
  'Hacé clic en un píxel visible. En la captura de ejemplo, B4 = 0,0143, B8 = 0,2958 y NDVI ≈ 0,908. Registrá las coordenadas y compará con el color natural. Son valores de un píxel del compuesto.',
  'Valores observados en el Inspector del Code Editor, 2026-11-26. Coordenadas aproximadas: −57.5752, −25.2422.');
await pictureSlide('Paso 9 · Inspector: contraste urbano','10_inspector_urbano_panel.png',
  'Elegí un segundo píxel. En la captura de ejemplo, B4 = 0,0993, B8 = 0,1877 y NDVI ≈ 0,308. Un contraste entre dos píxeles sirve para formular hipótesis, no para identificar especies o causas.',
  'Valores observados en el Inspector del Code Editor, 2026-11-26. Coordenadas aproximadas: −57.4997, −25.2863.');
await codeSlide('Paso 10 · Histograma de píxeles válidos','06_histograma_codigo_codigo.png',
  'ui.Chart.image.histogram agrupa los valores NDVI dentro del rectángulo a escala solicitada de 30 m. El eje horizontal es NDVI y el vertical, cantidad de píxeles válidos por intervalo. La máscara define qué entra.',
  'Referencia: https://developers.google.com/earth-engine/apidocs/ui-chart-image-histogram');
s=await slide('Paso 11 · Lectura de la distribución','',
  'Histograma obtenido en la ejecución real del 2026-11-26. La forma depende del periodo, área y máscara. Referencia: https://developers.google.com/earth-engine/apidocs/ui-chart-image-histogram');
await img(s,'12_histograma.png',62,199,1155,434,'Histograma real del NDVI en el Code Editor');
txt(s,'La mayor concentración de píxeles válidos se ubica aproximadamente entre NDVI 0,3 y 0,8.',67,638,1100,26,16,muted);
await codeSlide('Paso 12 · NDVI medio del área','07_media_codigo_codigo.png',
  'reduceRegion con ee.Reducer.mean calcula una media espacial de los píxeles válidos a escala de 30 m. En esta ejecución dio ≈ 0,509. No es el porcentaje de vegetación ni una calificación de su estado.',
  'Referencia: https://developers.google.com/earth-engine/apidocs/ee-image-reduceregion. Resultado de la ejecución real del 2026-11-26: 0.5087404393663842.');
s=await slide('Qué cambia en el mapa y qué cambia en los datos',
  'Si modificás solo la paleta o min/max de Map.addLayer, cambian los colores. El histograma y la media siguen calculándose sobre el mismo NDVI.\n\nSi cambiás área, periodo, filtro de escenas o máscara, pueden cambiar los píxeles incluidos, la distribución y la media.\n\nEl NDVI no identifica especies, no diagnostica por sí solo salud vegetal y no permite atribuir causalidad.',
  'La interpretación se limita al compuesto y a las clases SCL seleccionadas. Fuentes: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED y https://developers.google.com/earth-engine/apidocs/ee-image-normalizeddifference');
s=await slide('Entrega, foro y quiz 7A',
  '1. Guardá tu script y tomá una captura del color natural, una del NDVI y una del histograma. Excluí cualquier dato de tu cuenta.\n\n2. En el foro de la Unidad 7, indicá área, fechas, dos patrones observados y una limitación. Respondé a otra persona.\n\n3. Completá el quiz 7A del aula Git. El guion JavaScript completo está disponible para descarga junto a esta presentación.',
  'La práctica es formativa y no sustituye la evaluación oficial del curso. Enlace del aula: https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/index.html#/sesion/7');

await fs.mkdir(path.dirname(out),{recursive:true});
const staging=path.join(root,'.codex-ee-build');
await fs.mkdir(staging,{recursive:true});
const candidate=path.join(staging,'earth_engine_candidate.pptx');
await (await PresentationFile.exportPptx(pres)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const result=await finalizePresentation({
  workspaceDir:root,candidatePath:candidate,finalPath:out,pythonExecutable:python,
  integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
  requiredNativeTableOwnerSlides:[],fontPolicy:{basis:'design',families:[serif,sans]},
  verifyArtifactToolImport:true,
  receiptPath:path.join(staging,'earth_engine_validation.json'),
});
if(!result) throw new Error('La finalización no devolvió evidencia');
