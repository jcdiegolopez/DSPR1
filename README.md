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
- `playwright` para Python
- Navegador Chromium disponible para Playwright

## Ejecucion

```bash
python scripts/scrape_mineduc_diversificado.py --output-dir data/raw
```

Para una prueba corta:

```bash
python scripts/scrape_mineduc_diversificado.py --output-dir data/test_run --department-limit 1
```

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
