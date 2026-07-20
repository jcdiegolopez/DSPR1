# Libro de codigos — establecimientos Diversificado MINEDUC

## Metadatos

- **Version:** 1.0.0
- **Fuente:** https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/
- **Fecha de extraccion:** 2026-07-14 23:53:06+00:00
- **Cobertura:** establecimientos educativos de Guatemala con nivel `DIVERSIFICADO`.
- **Conjunto descrito:** `data/processed/establecimientos_diversificado_guatemala_limpio.csv`.
- **Convencion de ausencias:** `NA` representa un valor faltante o no verificable.

## Variables

| Variable | Descripcion | Tipo de dato | Dominio | Valores posibles | Tratamiento aplicado | Derivada |
|---|---|---|---|---|---|---|
| codigo | Identificador unico del establecimiento educativo. | string | Texto con patron NN-NN-NNNN-NN | Codigos que cumplen el patron; sin NA. | Se conserva como texto y se valida el patron NN-NN-NNNN-NN. | No |
| distrito | Codigo o identificador de distrito reportado por MINEDUC. | string | Texto con patrones NN-NNN, NN-NN-NNN o NN-NN-NNNN; NA si no es verificable | Codigos de distrito validos o NA. | Se normalizan espacios; los formatos no verificables se convierten a NA y se marcan. | No |
| departamento | Departamento donde se ubica el establecimiento. | string | Categoria controlada | ALTA VERAPAZ; BAJA VERAPAZ; CHIMALTENANGO; CHIQUIMULA; CIUDAD CAPITAL; EL PROGRESO; ESCUINTLA; GUATEMALA; HUEHUETENANGO; IZABAL; JALAPA; JUTIAPA; PETEN; QUETZALTENANGO; QUICHE; RETALHULEU; SACATEPEQUEZ; SAN MARCOS; SANTA ROSA; SOLOLA; SUCHITEPEQUEZ; TOTONICAPAN; ZACAPA | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| municipio | Municipio donde se ubica el establecimiento. | string | Categoria controlada por par departamento-municipio | Catalogo completo: data/raw/catalogos/municipios.csv. | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| establecimiento | Nombre del establecimiento educativo. | string | Texto libre o NA | Valores textuales reportados por la fuente. | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| direccion | Direccion reportada para el establecimiento. | string | Texto libre o NA | Valores textuales reportados por la fuente. | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| telefono | Telefono original reportado por la fuente. | string | Texto; telefono_normalizado tiene exactamente 8 digitos o NA | Telefono reportado; 8 digitos o NA en el campo normalizado. | Se conserva para auditoria; marcadores de ausencia se convierten a NA. | No |
| supervisor | Nombre del supervisor reportado por la fuente. | string | Texto libre o NA | Valores textuales reportados por la fuente. | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| director | Nombre del director reportado por la fuente. | string | Texto libre o NA | Valores textuales reportados por la fuente. | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| nivel | Nivel educativo del establecimiento. | string | Categoria controlada | DIVERSIFICADO | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| sector | Sector administrativo del establecimiento. | string | Categoria controlada | COOPERATIVA; MUNICIPAL; OFICIAL; PRIVADO | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| area | Clasificacion geografica del establecimiento. | string | Categoria controlada | RURAL; SIN ESPECIFICAR; URBANA | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| status | Estado administrativo reportado por MINEDUC. | string | Categoria controlada | ABIERTA; CERRADA DEFINITIVAMENTE; CERRADA TEMPORALMENTE; TEMPORAL NOMBRAMIENTO; TEMPORAL TITULOS | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| modalidad | Modalidad educativa reportada por MINEDUC. | string | Categoria controlada | BILINGUE; MONOLINGUE | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| jornada | Jornada de funcionamiento del establecimiento. | string | Categoria controlada | DOBLE; INTERMEDIA; MATUTINA; NOCTURNA; SIN JORNADA; VESPERTINA | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| plan | Plan educativo reportado por MINEDUC. | string | Categoria controlada | A DISTANCIA; DIARIO(REGULAR); DOMINICAL; FIN DE SEMANA; INTERCALADO; IRREGULAR; MIXTO; SABATINO; SEMIPRESENCIAL; SEMIPRESENCIAL (DOS DÍAS A LA SEMANA); SEMIPRESENCIAL (FIN DE SEMANA); SEMIPRESENCIAL (UN DÍA A LA SEMANA); VIRTUAL A DISTANCIA | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| departamental | Direccion departamental administrativa reportada por MINEDUC. | string | Categoria controlada | ALTA VERAPAZ; BAJA VERAPAZ; CHIMALTENANGO; CHIQUIMULA; EL PROGRESO; ESCUINTLA; GUATEMALA NORTE; GUATEMALA OCCIDENTE; GUATEMALA ORIENTE; GUATEMALA SUR; HUEHUETENANGO; IZABAL; JALAPA; JUTIAPA; PETÉN; QUETZALTENANGO; QUICHÉ; QUICHÉ NORTE; RETALHULEU; SACATEPÉQUEZ; SAN MARCOS; SANTA ROSA; SOLOLÁ; SUCHITEPÉQUEZ; TOTONICAPÁN; ZACAPA | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| fecha_extraccion | Fecha y hora UTC en que se obtuvo el registro. | string | Fecha-hora UTC | Marca temporal ISO 8601 con zona UTC. | Se convierte a fecha-hora UTC. | No |
| fuente_url | URL de procedencia de los datos. | string | URL | URL del portal MINEDUC utilizado. | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| nivel_consulta | Filtro de nivel utilizado durante la extraccion. | string | Categoria controlada | DIVERSIFICADO | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| sector_consulta | Filtro de sector utilizado durante la extraccion. | string | Categoria controlada | TODOS | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| plan_consulta | Filtro de plan utilizado durante la extraccion. | string | Categoria controlada | TODOS | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| modalidad_consulta | Filtro de modalidad utilizado durante la extraccion. | string | Categoria controlada | TODOS | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| departamento_consulta | Departamento seleccionado durante la extraccion. | string | Categoria controlada | ALTA VERAPAZ; BAJA VERAPAZ; CHIMALTENANGO; CHIQUIMULA; CIUDAD CAPITAL; EL PROGRESO; ESCUINTLA; GUATEMALA; HUEHUETENANGO; IZABAL; JALAPA; JUTIAPA; PETEN; QUETZALTENANGO; QUICHE; RETALHULEU; SACATEPEQUEZ; SAN MARCOS; SANTA ROSA; SOLOLA; SUCHITEPEQUEZ; TOTONICAPAN; ZACAPA | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| departamento_consulta_codigo | Codigo del departamento seleccionado durante la extraccion. | string | Categoria controlada | 00; 01; 02; 03; 04; 05; 06; 07; 08; 09; 10; 11; 12; 13; 14; 15; 16; 17; 18; 19; 20; 21; 22 | Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico. | No |
| telefono_normalizado | Telefono de ocho digitos apto para analisis; NA si no pudo verificarse. | string | Texto; telefono_normalizado tiene exactamente 8 digitos o NA | Telefono reportado; 8 digitos o NA en el campo normalizado. | Derivada al remover separadores y prefijo +502; solo se conserva si tiene ocho digitos. | Si |
| telefono_valido | Indica si se obtuvo un telefono normalizado valido de ocho digitos. | string | Booleano | True, False. | Bandera derivada de telefono_normalizado. | Si |
| distrito_formato_revisar | Indica que el formato original del distrito no pudo verificarse. | string | Booleano | True, False. | Bandera derivada para formatos de distrito no verificables. | Si |
| departamental_difiere_departamento | Indica que la direccion departamental difiere del departamento geografico. | string | Booleano | True, False. | Bandera derivada para diferencias entre columnas administrativas. | Si |

## Variables derivadas

- `telefono_normalizado` permite analizar telefonos verificados sin modificar el valor original.
- `telefono_valido` identifica los registros con un telefono normalizado de ocho digitos.
- `distrito_formato_revisar` conserva la trazabilidad de los distritos cuyo formato no pudo validarse.
- `departamental_difiere_departamento` hace visible una diferencia administrativa sin sobrescribir ninguno de los dos campos.
