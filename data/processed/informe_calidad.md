# Informe de calidad del conjunto MINEDUC

## Resultados de validacion

| prueba | regla | incumplimientos | resultado |
| --- | --- | --- | --- |
| Duplicados exactos | No existen filas identicas | 0 | CUMPLE |
| Espacios externos | Los textos no tienen espacios iniciales o finales | 0 | CUMPLE |
| Telefonos | El telefono normalizado tiene ocho digitos o es NA y su bandera coincide | 0 | CUMPLE |
| Departamentos | Todos los departamentos pertenecen al catalogo | 0 | CUMPLE |
| Municipios | Cada par departamento-municipio pertenece al catalogo | 0 | CUMPLE |
| Tipos de dato | Textos, fecha y banderas usan el tipo esperado | 0 | CUMPLE |
| Categorias equivalentes | No hay categorias duplicadas por diferencias de escritura | 0 | CUMPLE |
| Invalidos del diagnostico | No quedan codigos, distritos, telefonos o categorias invalidas en los campos analiticos | 0 | CUMPLE |

## Comparacion antes y despues

| metrica | antes | despues | interpretacion |
| --- | --- | --- | --- |
| Registros | 11,867 | 11,867 | No se eliminaron filas. |
| Variables | 26 | 29 | Se elimino municipio_consulta y se agregaron cuatro variables derivadas. |
| Valores faltantes | 15,799 (5.12%) | 5,196 (1.51%) | Los marcadores se representan de forma uniforme como NA. |
| Variables con NA | 7 | 7 | Se contabilizan variables con al menos un valor faltante. |
| Duplicados exactos | 0 | 0 | No se encontraron filas identicas. |
| Posibles duplicados | 8,414 registros en 13,221 parejas | 8,414 conservados; 0 corregidos; 0 fusionados | La decision permanece pendiente de revision manual; no se eliminaron registros automaticamente. |
| Variables con formato inconsistente | 2 | 0 | Se trataron 248 telefonos y 70 distritos. |
| Variables con tipo incorrecto | 1 | 0 | fecha_extraccion se convirtio de texto a fecha-hora UTC. |
| Categorias inconsistentes | 0 | 0 | No se detectaron categorias equivalentes escritas de maneras distintas. |
| Errores corregidos | 423 casos detectados | 423 casos tratados | El detalle se presenta por tipo de correccion. |

## Correcciones aplicadas

| tipo_correccion | registros_afectados |
| --- | --- |
| Marcadores de ausencia convertidos a NA | 105 |
| Telefonos no normalizables retirados del campo analitico y marcados | 248 |
| Distritos incompletos convertidos a NA y marcados | 70 |

## Observaciones

- El numero de registros no cambio porque no habia duplicados exactos y los candidatos parciales requieren revision manual.
- La columna municipio_consulta se elimino porque estaba completamente vacia.
- Se agregaron telefono_normalizado, telefono_valido, distrito_formato_revisar y departamental_difiere_departamento.
- El telefono original se conserva para auditoria; telefono_normalizado es el campo que debe utilizarse para analisis.
- Los valores no verificables no se imputaron.