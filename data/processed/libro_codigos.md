# Libro de codigos - Limpieza Punto 5

Variables derivadas y justificacion:
- telefono_normalizado: estandariza telefono para validacion y deteccion de duplicados.
- telefono_valido: identifica telefonos con estructura de 8 digitos.
- distrito_formato_revisar: identifica distritos fuera del patron esperado para revision manual.
- departamental_difiere_departamento: identifica posibles inconsistencias administrativas.

| variable | tipo_dato | nulos | es_derivada | descripcion |
|---|---|---:|---|---|
| codigo | str | 0 | False |  |
| distrito | str | 532 | False |  |
| departamento | string | 0 | False |  |
| municipio | string | 0 | False |  |
| establecimiento | str | 5 | False |  |
| direccion | str | 82 | False |  |
| telefono | str | 946 | False |  |
| supervisor | str | 535 | False |  |
| director | str | 1832 | False |  |
| nivel | string | 0 | False |  |
| sector | string | 0 | False |  |
| area | string | 0 | False |  |
| status | string | 0 | False |  |
| modalidad | string | 0 | False |  |
| jornada | string | 0 | False |  |
| plan | string | 0 | False |  |
| departamental | string | 0 | False |  |
| fecha_extraccion | datetime64[us, UTC] | 0 | False |  |
| fuente_url | str | 0 | False |  |
| nivel_consulta | string | 0 | False |  |
| sector_consulta | string | 0 | False |  |
| plan_consulta | string | 0 | False |  |
| modalidad_consulta | string | 0 | False |  |
| departamento_consulta | string | 0 | False |  |
| departamento_consulta_codigo | string | 0 | False |  |
| telefono_normalizado | str | 946 | True | Telefono con limpieza de formato para comparacion y validacion. |
| telefono_valido | boolean | 0 | True | Bandera booleana: telefono_normalizado tiene 8 digitos. |
| distrito_formato_revisar | boolean | 0 | True | Bandera booleana: distrito no cumple patron esperado NN-NN. |
| departamental_difiere_departamento | boolean | 0 | True | Bandera booleana: departamental difiere de departamento. |