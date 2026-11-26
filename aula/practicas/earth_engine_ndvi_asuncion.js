// FACET-UNC · Visualización de datos · Unidad 7
// Práctica: composición Sentinel-2 y NDVI en el área de Asunción.
// Pegá este archivo en https://code.earthengine.google.com/ y presioná Run.
// La fecha final de filterDate es exclusiva. Se analizan escenas de mayo a agosto de 2025.

var area = ee.Geometry.Rectangle([-57.59, -25.38, -57.43, -25.21], null, false);

var escenas = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(area)
  .filterDate('2025-05-01', '2025-09-01')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30));

print('Escenas candidatas', escenas.size());

function superficieVisible(imagen) {
  // SCL es una clasificación de 20 m. Se conservan vegetación (4) y suelo desnudo (5).
  // El porcentaje de nubosidad anterior se refiere a la escena, no solo al rectángulo.
  var scl = imagen.select('SCL');
  var mascara = scl.eq(4).or(scl.eq(5));
  return imagen.updateMask(mascara)
    .select(['B2', 'B3', 'B4', 'B8'])
    .multiply(0.0001);
}

var compuesto = escenas.map(superficieVisible).median().clip(area);
var ndvi = compuesto.normalizedDifference(['B8', 'B4']).rename('NDVI');

Map.centerObject(area, 11);
Map.addLayer(area, {color: 'f5b700'}, 'Área de estudio');
Map.addLayer(compuesto,
  {bands: ['B4', 'B3', 'B2'], min: 0.02, max: 0.30},
  'Color natural');
Map.addLayer(ndvi,
  {min: 0, max: 0.8,
   palette: ['440154', '3b528b', '21918c', '5ec962', 'fde725']},
  'NDVI');

var histograma = ui.Chart.image.histogram({
  image: ndvi,
  region: area,
  scale: 30,
  maxBuckets: 32,
  maxPixels: 1000000
}).setOptions({
  title: 'Distribución del NDVI en píxeles visibles',
  hAxis: {title: 'NDVI'},
  vAxis: {title: 'Cantidad de píxeles'}
});
print(histograma);

var ndviMedio = ndvi.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: area,
  scale: 30,
  maxPixels: 10000000
}).get('NDVI');
print('NDVI medio en píxeles visibles del área', ndviMedio);

// Preguntas de cierre: ¿cómo cambia el histograma si se altera la fecha o el área?
// ¿Qué píxeles se excluyeron? ¿Qué conclusión NO permite sostener el NDVI?
