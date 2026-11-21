# Guía paso a paso · Informe de Looker Studio con el Censo Agropecuario Nacional 2022

Material de la **sesión 5** (presentación 3 del aula). Looker Studio (antes Google Data Studio) es gratuito con una cuenta de Google. Los nombres de los menús pueden variar según el idioma y la versión.

## 1. Datos

Fuente: **Ministerio de Agricultura y Ganadería (MAG), Censo Agropecuario Nacional 2022, Volumen I** (78 cuadros por tamaño de finca y departamento).

| Archivo | Contenido |
|---|---|
| [`can2022_departamentos.csv`](../aula/media/unidad5_looker/fuentes/datos/can2022_departamentos.csv) | Una fila por departamento (17): fincas y superficie 2008 y 2022, variación, usos de la tierra, soja, vacunos y productores por sexo. Incluye el código **ISO 3166-2** para los mapas. |
| [`can2022_estratos.csv`](../aula/media/unidad5_looker/fuentes/datos/can2022_estratos.csv) | Una fila por tamaño de finca (12): fincas y superficie 2008 y 2022, y porcentajes de 2022. |

Se generan con `python tools/can_datos.py "VOLUMEN I - CAN 2022 _final.xlsx"` (cuadros 1, 5, 19, 27 y 52). **Verificación:** los totales reproducen los oficiales: 291.497 fincas, 30.401.660 ha, 13.221.039 cabezas de vacunos y 245.002 productores residentes.

| Campo | Significado |
|---|---|
| `dpto_cod`, `departamento`, `iso_3166_2`, `region` | Identificación (el código ISO de Boquerón es PY-19 y el de Alto Paraguay, PY-16; no coinciden con la numeración del censo) |
| `fincas_2008`, `superficie_2008_ha`, `fincas_2022`, `superficie_2022_ha` | Cantidad y superficie de fincas (Cuadro 1) |
| `var_fincas_pct`, `var_superficie_pct`, `superficie_promedio_2022_ha` | Variación 2008–2022 y tamaño promedio |
| `sup_cultivos_temporales_ha` … `sup_forestales_plantados_ha` | Superficie por uso de la tierra (Cuadro 19) |
| `soja_fincas`, `soja_sup_ha`, `soja_produccion_tn` | Soja de zafra normal (Cuadro 27); celda vacía en el censo = 0 |
| `vacunos_fincas`, `vacunos_cabezas` | Ganado vacuno (Cuadro 52) |
| `productores_residentes`, `productores_hombres`, `productores_mujeres` | Productores residentes en finca por sexo (Cuadro 5) |
| `pct_superficie_2022`, `pct_productoras_mujeres`, `vacunos_por_100_ha` | Indicadores calculados |

## 2. Pasos

1. **Hoja de cálculo.** En Google Drive, *Nuevo → Hojas de cálculo de Google*; importá `can2022_departamentos.csv` en una pestaña `departamentos` y `can2022_estratos.csv` en otra `estratos`. Números sin separador de miles.
2. **Informe.** Entrá a `lookerstudio.google.com` → *Crear → Informe* → *Agregar datos* → conector **Hojas de cálculo de Google** → elegí el archivo y la pestaña `departamentos` → *Agregar*.
3. **Campos.** En el editor de la fuente de datos: `iso_3166_2` como **Geografía → Región de país (ISO 3166-2)**; porcentajes y promedios con agregación *promedio*, conteos y hectáreas con *suma*.
4. **Campos calculados** (razón de sumas, no promedio de porcentajes):
   - Superficie promedio por finca: `SUM(superficie_2022_ha) / SUM(fincas_2022)`
   - Productoras mujeres (%): `SUM(productores_mujeres) / SUM(productores_residentes)`
5. **Tarjetas de resultados** (KPI): fincas, superficie, vacunos y % de productoras, con comparación con 2008 donde exista.
6. **Mapa** de burbujas o coroplético: dimensión `iso_3166_2`, métrica `superficie_2022_ha`.
7. **Barras**: ranking de superficie por departamento (orden descendente, un color de énfasis) y variación de fincas 2008–2022 (`var_fincas_pct`, colores condicionales).
8. **Segunda fuente** (`estratos`): barras agrupadas de `pct_fincas_2022` y `pct_superficie_2022` por estrato (ordenado por `orden`).
9. **Controles:** lista desplegable de `region` y de `departamento`; activá el filtrado cruzado.
10. **Diseño:** título que enuncia el mensaje, pie con la fuente («MAG, CAN 2022, Volumen I»), una gama de colores coherente, una página.
11. **Compartir:** botón *Compartir* (permiso de lector o enlace); *Archivo → Incorporar informe* para obtener la URL de incrustación (para una web propia). En el aula se entrega el **enlace** del informe con permiso de lector.

## 3. Hallazgos para comentar

- **Concentración:** 4.524 fincas de **1.000 ha o más** (1,6 % del total) manejan 23,46 millones de ha (**77,2 %** de la superficie). Las fincas de menos de 20 ha son el 82 % y manejan el 4,2 %.
- **Región Occidental:** Presidente Hayes, Boquerón y Alto Paraguay suman 17,0 millones de ha (55,9 %).
- **2008 → 2022:** el total de fincas casi no cambió (+0,6 %), pero Boquerón (+30 %) y San Pedro (+29 %) crecieron, y Central (−52 %), Amambay (−41 %) y Misiones (−33 %) cayeron.
- **Concepción:** 16.670 fincas y 1,52 millones de ha; 77 % de la superficie en pasturas (49 % natural y 28 % cultivada) frente al 59 % del país; 45,8 % de los productores residentes son mujeres (país: 38,3 %).

## 4. Límites

Los cuadros del Volumen I son resultados oficiales agregados: sirven para describir, no para inferir a nivel de finca. Las imágenes de la presentación son **maquetas con los datos reales**, no capturas de Looker Studio.
