# Proyecto 1 — Data Science

**Universidad del Valle de Guatemala**  
Ingeniería en Ciencias de la Computación

## Integrantes

- Diego López — Carné 23242
- Luis González — Carné 23353
- Diego Rosales — Carné 23258

## Scraping MINEDUC

Extraccion reproducible de establecimientos educativos del portal MINEDUC para `Nivel Escolar = DIVERSIFICADO`.

## Requisitos

- Python 3
- Dependencias listadas en `requirements.txt`
- Navegador Chromium disponible para Playwright

Instalacion en un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
```

## Ejecucion

```bash
python scripts/scrape_mineduc_diversificado.py --output-dir data/raw
```

Para una prueba corta:

```bash
python scripts/scrape_mineduc_diversificado.py --output-dir data/test_run --department-limit 1
```

## Ejecucion reproducible completa

Ejecutar los notebooks desde JupyterLab, en este orden, con el directorio raiz del proyecto como directorio de trabajo:

1. `notebooks/01_diagnostico_inicial_mineduc.ipynb`
2. `notebooks/02_limpieza_mineduc.ipynb`
3. `python scripts/generar_libro_codigos.py`
4. `notebooks/03_validacion_informe_calidad.ipynb`

El paso 3 reemplaza el libro de codigos preliminar generado durante la limpieza por la version completa de entrega y genera `data/processed/tabla_transformaciones.{csv,md}` con los campos exigidos para documentar las transformaciones. La extraccion es opcional si se trabajara con los archivos crudos ya incluidos; para volver a obtener los datos desde MINEDUC, ejecutar primero el comando de la seccion anterior.

## Validacion e informe de calidad

El notebook `notebooks/03_validacion_informe_calidad.ipynb` ejecuta las pruebas automaticas del conjunto limpio y genera la comparacion antes y despues.

Salidas principales:

- `data/processed/resultados_validacion.csv`
- `data/processed/informe_calidad.csv`
- `data/processed/resumen_correcciones.csv`
- `data/processed/informe_calidad.md`

## Salidas

- `data/raw/establecimientos_diversificado_guatemala.csv`
- `data/raw/departamentos/*.csv`
- `data/raw/catalogos/departamentos.csv`
- `data/raw/catalogos/municipios.csv`
- `data/raw/catalogos/niveles.csv`
- `data/raw/catalogos/sectores.csv`
- `data/raw/catalogos/planes.csv`
- `data/raw/catalogos/modalidades.csv`
- `data/raw/catalogos/header_mapping.csv`
- `data/raw/extraction_log.csv`

## Notas

- El scraper usa navegador real porque el sitio funciona con ASP.NET WebForms.
- Los datos se guardan en estado crudo, sin limpieza ni deduplicacion.
