# Log de transformaciones (Punto 5)

| inciso | tema | accion | registros_afectados | justificacion |
|---|---|---|---:|---|
| a | Valores faltantes y NA | Marcadores de ausencia normalizados a NA sin tocar SIN ESPECIFICAR en area. | 5196 | Uniformar ausencias para analisis reproducible y conservar categorias validas. |
| b | Tipos de dato | Dataset cargado como texto; fecha_extraccion convertida a datetime UTC. | 11867 | Preservar codigos y telefonos; garantizar tipo temporal correcto. |
| c | Normalizacion de texto | Trim, colapso de espacios y eliminacion de invisibles. | 11867 | Evitar diferencias espurias de escritura sin perder semantica. |
| d | Consistencia de categorias | Validacion contra catalogos oficiales de departamento, municipio, sector y modalidad. | 0 | Detectar categorias fuera de dominio sin corregir por inferencia. |
| e | Formatos | Validacion de codigo, normalizacion de telefono y bandera de distrito. | 318 | Aislar formatos problematicos para revision transparente. |
| f | Valores invalidos | Conteo de fuera de dominio en categorias, codigos, telefonos y distritos. | 318 | Resolver formatos incompletos sin inferir valores que no aparecen en la fuente. |
| g | Registros duplicados | Busqueda de duplicados exactos y candidatos parciales con similitud de cadenas. | 13221 | No se elimina automaticamente; se deja evidencia para decision manual. |
| h | Consistencia entre variables | Revision de coherencia entre departamental, departamento y metadatos de consulta. | 6094 | Hacer visibles contradicciones entre columnas relacionadas. |
| i | Variables derivadas | Creacion de telefono_normalizado, telefono_valido, distrito_formato_revisar y departamental_difiere_departamento. | 11867 | Permiten auditar calidad sin perder el dato original. |