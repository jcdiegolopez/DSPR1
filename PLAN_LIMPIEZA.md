# Plan de limpieza del conjunto MINEDUC

**Curso:** CC3084 - Data Science  
**Fuente:** Portal de Busqueda de Establecimientos Educativos del MINEDUC  
**Cobertura:** establecimientos con nivel escolar `DIVERSIFICADO`, Guatemala  
**Estado del documento:** plan previo a la limpieza. Ninguna regla descrita aqui ha modificado el archivo crudo.

## Alcance y principios

El archivo de entrada es `data/raw/establecimientos_diversificado_guatemala.csv`, extraido el 14 de julio de 2026. El diagnostico inicial reporta 11,867 filas y 26 variables. La limpieza se ejecutara en una copia del archivo crudo y registrara cada transformacion, por lo que el archivo original no sera sobrescrito.

Las reglas generales seran las siguientes:

1. En campos de texto se eliminaran espacios al inicio y final, se reemplazaran espacios multiples por uno y se eliminaran caracteres invisibles. No se eliminaran tildes ni signos con posible significado semantico.
2. Los marcadores `""`, `--`, `N/A`, `NULL`, `-`, `.`, `Sin dato`, `SIN DATO`, `NA` y `N.D.` se convertiran a valores faltantes (`NA`) solo cuando representen ausencia de informacion. El valor `SIN ESPECIFICAR` se conservara porque es una categoria explicita de `area`.
3. Los valores de referencia, como codigos, telefonos y codigos de departamento, se manejaran como texto para conservar ceros iniciales y guiones significativos.
4. Ningun valor dudoso se corregira por inferencia. Se conservara el valor original, se marcara para revision y se documentara la cantidad afectada.
5. Los valores de ubicacion se validaran contra los catalogos extraidos del mismo portal. Las correcciones de categorias solo se aplicaran si hay una equivalencia unica y verificable en el catalogo.

## Plan por variable

| Variable | Problemas encontrados en el diagnostico | Regla de limpieza y justificacion | Riesgo asociado |
|---|---|---|---|
| `codigo` | No hay faltantes y los 11,867 valores cumplen el patron `NN-NN-NNNN-NN`. | Conservar como texto; aplicar solo limpieza de espacios y validar de nuevo el patron. Es un identificador, no una medida numerica. | Convertirlo a numero eliminaria guiones y podria perder ceros iniciales. |
| `distrito` | 532 faltantes y 70 valores con patrones distintos de los mas frecuentes. | Convertir marcadores a `NA`, normalizar espacios y conservar el texto como identificador. Crear una bandera `distrito_formato_revisar` para los 70 casos; no cambiar su contenido automaticamente. | Forzar todos los patrones a una sola estructura puede convertir distritos validos en valores incorrectos. |
| `departamento` | Sin faltantes; 23 categorias validas segun el catalogo. | Normalizar espacios y mayusculas; validar contra el catalogo de departamentos. No se anticipan unificaciones. | Una correccion basada solo en similitud podria confundir nombres parecidos. |
| `municipio` | Sin faltantes; 352 categorias y ninguna combinacion `departamento`-`municipio` fuera del catalogo. | Normalizar espacios y mayusculas; validar la combinacion con `departamento` mediante el catalogo. | Cambiar un municipio sin considerar su departamento puede asignarlo a otra localidad homonima. |
| `establecimiento` | 5 valores faltantes; es un nombre libre, con posibles variaciones de escritura. | Convertir marcadores a `NA`, normalizar espacios y caracteres invisibles. Mantener las tildes y puntuacion; generar una clave normalizada solo para detectar duplicados parciales, sin reemplazar el nombre original. | Homogeneizar agresivamente nombres puede juntar establecimientos diferentes con nombres similares. |
| `direccion` | 76 valores faltantes y campo de texto libre. | Convertir marcadores a `NA`, normalizar espacios y caracteres invisibles. Mantener abreviaturas, numeros, zonas y puntuacion. Usar una version normalizada solo para buscar duplicados parciales. | Estandarizar abreviaturas de forma automatica puede alterar direcciones validas. |
| `telefono` | 946 valores vacios y 201 no contienen exclusivamente digitos. | Convertir vacios y marcadores a `NA`. Crear `telefono_normalizado` removiendo espacios, guiones, parentesis y prefijo `+502` cuando deje exactamente ocho digitos; crear `telefono_valido` para indicar si el resultado tiene ocho digitos. Los casos que no cumplan se conservaran en `telefono` y quedaran marcados, no eliminados. | Algunos telefonos institucionales pueden usar extensiones o formatos no contemplados; por ello no se descartara el valor original. |
| `supervisor` | 535 valores faltantes; nombres de texto libre. | Convertir marcadores a `NA`, normalizar espacios y caracteres invisibles. No se corregiran nombres por similitud sin evidencia externa. | Dos personas diferentes pueden tener nombres muy parecidos. |
| `director` | 1,733 vacios y 41 valores `--` (1,774 ausencias o marcadores). | Convertir vacios y `--` a `NA`; normalizar espacios en nombres presentes. No imputar nombres. | Imputar el nombre de otra fila puede asignar una persona equivocada a un establecimiento. |
| `nivel` | Sin faltantes; una sola categoria: `DIVERSIFICADO`. | Normalizar texto y validar que todos los valores permanezcan en `DIVERSIFICADO`. Conservarlo por trazabilidad de la consulta. | Eliminarlo reduce contexto y dificulta verificar el alcance de la extraccion. |
| `sector` | Sin faltantes; cuatro categorias extraidas del portal. | Normalizar espacios y mayusculas; validar contra el catalogo de sectores. | Mapear categorias no presentes en el catalogo puede cambiar su significado administrativo. |
| `area` | Sin faltantes; contiene `URBANA`, `RURAL` y `SIN ESPECIFICAR`. | Normalizar espacios y mayusculas. Conservar `SIN ESPECIFICAR` como categoria valida, no como faltante. | Convertirla a faltante confundiria ausencia de dato con una clasificacion declarada por la fuente. |
| `status` | Sin faltantes; cinco categorias. | Normalizar espacios y mayusculas; conservar todas las categorias observadas. | Unificar estados sin un catalogo oficial podria modificar la situacion administrativa reportada. |
| `modalidad` | Sin faltantes; dos categorias y validas segun catalogo. | Normalizar espacios y mayusculas; validar contra el catalogo de modalidades. | Ninguno relevante mientras no se cambie el significado de la categoria. |
| `jornada` | Sin faltantes; seis categorias. | Normalizar espacios y mayusculas. Mantener categorias como `MATUTINA`, `VESPERTINA` y `NOCTURNA` sin recodificarlas. | Una recodificacion no documentada puede perder jornadas especiales. |
| `plan` | Sin faltantes; 13 categorias; algunas contienen puntuacion significativa, por ejemplo `DIARIO(REGULAR)`. | Normalizar solo espacios externos e invisibles. Mantener mayusculas y puntuacion interna; validar categorias observadas. | Quitar parentesis u otros signos puede fusionar planes educativos distintos. |
| `departamental` | Sin faltantes; difiere de `departamento` en 6,094 filas. | Conservar ambas columnas sin forzar igualdad. Crear una bandera `departamental_difiere_departamento` para documentar la diferencia. | Reemplazarla por `departamento` borraria una posible division administrativa valida. |
| `fecha_extraccion` | Sin faltantes; aparece como texto ISO 8601. | Convertir a fecha-hora con zona horaria UTC y validar la conversion. | Una conversion sin zona horaria puede desplazar la fecha o la hora. |
| `fuente_url` | Sin faltantes; una URL constante. | Eliminar espacios externos, validar que sea URL y conservarla como metadato de procedencia. Puede retirarse del dataset analitico y mantenerse en el libro de codigos. | Eliminarla sin documentarla reduce trazabilidad de la fuente. |
| `nivel_consulta` | Sin faltantes; constante `DIVERSIFICADO`. | Conservar como metadato de extraccion o moverlo a la documentacion; no es una variable independiente del establecimiento. | Eliminarla del conjunto analitico sin documentarla dificulta reproducir el filtro usado. |
| `sector_consulta` | Sin faltantes; constante `TODOS`. | Tratar como metadato; moverlo a la documentacion de extraccion o eliminarlo del conjunto analitico limpio. | Mantener una columna constante no aporta analisis; eliminarla sin registro pierde reproducibilidad. |
| `plan_consulta` | Sin faltantes; constante `TODOS`. | Tratar como metadato; moverlo a la documentacion de extraccion o eliminarlo del conjunto analitico limpio. | Igual que en `sector_consulta`. |
| `modalidad_consulta` | Sin faltantes; constante `TODOS`. | Tratar como metadato; moverlo a la documentacion de extraccion o eliminarlo del conjunto analitico limpio. | Igual que en `sector_consulta`. |
| `departamento_consulta` | Sin faltantes; 23 categorias, una por departamento procesado. | Normalizar y validar contra el catalogo. Mantenerlo durante la auditoria y comprobar que corresponde al departamento de la fila; despues evaluarlo como metadato redundante. | Eliminarlo antes de validar impediria detectar errores de extraccion por departamento. |
| `departamento_consulta_codigo` | Sin faltantes; 23 codigos de consulta. | Conservar como texto, validar contra el catalogo y comprobar su correspondencia con `departamento_consulta`. Puede pasar a metadato despues de la validacion. | Convertirlo a entero perderia el formato de codigo; eliminarlo antes de validar reduce trazabilidad. |
| `municipio_consulta` | Los 11,867 valores estan vacios. Corresponde a un filtro no utilizado en la extraccion. | Verificar que sea completamente vacia y eliminarla del conjunto analitico limpio; registrar la eliminacion en el log de transformaciones. | Si una futura ejecucion usa filtro municipal, la regla podria eliminar informacion; por eso se condicionara a que el campo este 100% vacio. |

## Tratamiento de duplicados

El diagnostico no encontro duplicados exactos, por lo que no se eliminara ninguna fila por este criterio. Se buscaran posibles duplicados parciales con una clave de comparacion formada por `establecimiento`, `direccion`, `municipio` y `telefono_normalizado`, aplicando similitud de cadenas solo dentro del mismo municipio. Cada pareja candidata se revisara y clasificara como duplicado confirmado, registros distintos o caso no concluyente. Ningun posible duplicado se eliminara automaticamente.

## Orden de ejecucion y validacion posterior

1. Crear una copia del archivo crudo y preservar identificadores de fila para auditoria.
2. Aplicar la normalizacion textual y convertir marcadores de ausencia a `NA`.
3. Convertir `fecha_extraccion` a fecha-hora y conservar identificadores y telefonos como texto.
4. Validar categorias y combinaciones de ubicacion con los catalogos del MINEDUC.
5. Crear banderas de revision para telefonos y distritos; no eliminar registros por estas banderas.
6. Revisar duplicados parciales y documentar cada decision.
7. Eliminar unicamente `municipio_consulta` si sigue 100% vacia y mover metadatos constantes a la documentacion.
8. Ejecutar pruebas automaticas: ausencia de duplicados exactos, textos sin espacios externos, codigos validos, telefonos normalizados con bandera de validez, tipos correctos y categorias dentro de sus catalogos.

Cada cambio se registrara en una tabla de transformaciones con: variable, problema detectado, transformacion, registros afectados, justificacion y riesgo. El resultado sera un conjunto limpio separado del archivo crudo, junto con su libro de codigos y la fecha de ejecucion.
