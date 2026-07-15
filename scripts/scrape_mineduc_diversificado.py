from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from playwright.sync_api import Page, TimeoutError, sync_playwright


BASE_URL = "https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/"
QUERY_LEVEL_VALUE = "46"
QUERY_LEVEL_LABEL = "DIVERSIFICADO"
DEFAULT_WAIT_MS = 120_000
META_HEADERS = [
    "fecha_extraccion",
    "fuente_url",
    "nivel_consulta",
    "sector_consulta",
    "plan_consulta",
    "modalidad_consulta",
    "departamento_consulta",
    "departamento_consulta_codigo",
    "municipio_consulta",
]


DEPARTMENT_SELECTOR = "#_ctl0_ContentPlaceHolder1_cmbDepartamento"
MUNICIPALITY_SELECTOR = "#_ctl0_ContentPlaceHolder1_cmbMunicipio"
LEVEL_SELECTOR = "#_ctl0_ContentPlaceHolder1_cmbNivel"
SECTOR_SELECTOR = "#_ctl0_ContentPlaceHolder1_cmbSector"
PLAN_SELECTOR = "#_ctl0_ContentPlaceHolder1_ddlplan"
MODALITY_SELECTOR = "#_ctl0_ContentPlaceHolder1_ddlModalidad"
SEARCH_BUTTON_SELECTOR = "#_ctl0_ContentPlaceHolder1_IbtnConsultar"
RESULT_TABLE_SELECTOR = "#_ctl0_ContentPlaceHolder1_dgResultado"


def normalize_cell_text(value: str | None) -> str:
    if value is None:
        return ""
    value = value.replace("\xa0", " ")
    value = value.replace("\u200b", "")
    value = value.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def slugify_filename(value: str) -> str:
    cleaned = strip_accents(normalize_cell_text(value)).lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    return cleaned.strip("_") or "sin_nombre"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: Iterable[dict[str, str]], fieldnames: list[str]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def extract_select_options(page: Page, selector: str) -> list[dict[str, str]]:
    script = """
    (selector) => {
      const select = document.querySelector(selector);
      if (!select) return [];
      return Array.from(select.options).map((option, index) => ({
        index: String(index),
        value: option.value ?? "",
        label: (option.textContent ?? "").replace(/\\u00a0/g, " ").trim(),
      }));
    }
    """
    return page.evaluate(script, selector)


def wait_for_municipality_options(page: Page) -> None:
    page.wait_for_function(
        """(selector) => {
            const select = document.querySelector(selector);
            return !!select && select.options.length > 0;
        }""",
        arg=MUNICIPALITY_SELECTOR,
        timeout=DEFAULT_WAIT_MS,
    )


def wait_for_results_table(page: Page) -> None:
    page.wait_for_selector(RESULT_TABLE_SELECTOR, timeout=DEFAULT_WAIT_MS)
    page.wait_for_function(
        """(selector) => {
            const table = document.querySelector(selector);
            return !!table && table.querySelectorAll("tr").length > 1;
        }""",
        arg=RESULT_TABLE_SELECTOR,
        timeout=DEFAULT_WAIT_MS,
    )


def snake_case_headers(headers: list[str]) -> list[str]:
    normalized: list[str] = []
    used: dict[str, int] = {}
    for raw_header in headers:
        header = strip_accents(normalize_cell_text(raw_header)).lower()
        header = re.sub(r"[^a-z0-9]+", "_", header).strip("_")
        if not header:
            header = "columna"
        count = used.get(header, 0) + 1
        used[header] = count
        normalized.append(header if count == 1 else f"{header}_{count}")
    return normalized


@dataclass
class DepartmentResult:
    department_code: str
    department_name: str
    municipalities: list[dict[str, str]]
    raw_headers: list[str]
    normalized_headers: list[str]
    rows: list[dict[str, str]]


def extract_result_rows(page: Page, extraction_timestamp: str) -> tuple[list[str], list[str], list[dict[str, str]]]:
    script = """
    (selector) => {
      const table = document.querySelector(selector);
      if (!table) return null;
      const rows = Array.from(table.querySelectorAll("tr"));
      if (rows.length === 0) return null;

      const headers = Array.from(rows[0].querySelectorAll("td, th")).map((cell) => (cell.textContent || "").replace(/\\u00a0/g, " ").trim());
      const dataRows = rows.slice(1).map((row) =>
        Array.from(row.querySelectorAll("td")).map((cell) => (cell.textContent || "").replace(/\\u00a0/g, " ").trim())
      );

      return { headers, dataRows };
    }
    """
    payload = page.evaluate(script, RESULT_TABLE_SELECTOR)
    if not payload:
        return [], [], []

    raw_headers = [normalize_cell_text(item) for item in payload["headers"]]
    data_rows = payload["dataRows"]
    if not raw_headers or len(raw_headers) < 2:
        return [], [], []

    # The first column is the action button.
    table_headers = raw_headers[1:]
    normalized_headers = snake_case_headers(table_headers)

    extracted_rows: list[dict[str, str]] = []
    for row in data_rows:
        trimmed = [normalize_cell_text(item) for item in row]
        if not any(trimmed):
            continue
        values = trimmed[1:]
        if len(values) < len(normalized_headers):
            values.extend([""] * (len(normalized_headers) - len(values)))
        record = dict(zip(normalized_headers, values[: len(normalized_headers)]))
        record["fecha_extraccion"] = extraction_timestamp
        record["fuente_url"] = BASE_URL
        record["nivel_consulta"] = QUERY_LEVEL_LABEL
        record["sector_consulta"] = "TODOS"
        record["plan_consulta"] = "TODOS"
        record["modalidad_consulta"] = "TODOS"
        extracted_rows.append(record)

    return table_headers, normalized_headers, extracted_rows


def scrape_department(page: Page, department_code: str, department_name: str, extraction_timestamp: str) -> DepartmentResult:
    page.goto(BASE_URL, wait_until="networkidle", timeout=DEFAULT_WAIT_MS)

    page.select_option(DEPARTMENT_SELECTOR, department_code)
    wait_for_municipality_options(page)
    municipalities = extract_select_options(page, MUNICIPALITY_SELECTOR)

    page.select_option(LEVEL_SELECTOR, QUERY_LEVEL_VALUE)
    page.select_option(SECTOR_SELECTOR, "TODOS")
    page.select_option(PLAN_SELECTOR, "TODOS")
    page.select_option(MODALITY_SELECTOR, "TODOS")
    page.click(SEARCH_BUTTON_SELECTOR)

    wait_for_results_table(page)
    raw_headers, normalized_headers, rows = extract_result_rows(page, extraction_timestamp)
    for row in rows:
        row["departamento_consulta"] = department_name
        row["departamento_consulta_codigo"] = department_code
        row["municipio_consulta"] = ""

    return DepartmentResult(
        department_code=department_code,
        department_name=department_name,
        municipalities=municipalities,
        raw_headers=raw_headers,
        normalized_headers=normalized_headers,
        rows=rows,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape MINEDUC establishments for Nivel Diversificado.")
    parser.add_argument(
        "--output-dir",
        default="data/raw",
        help="Output directory for raw CSV files.",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Run the browser with a visible window.",
    )
    parser.add_argument(
        "--department-limit",
        type=int,
        default=None,
        help="Optional limit for departments, useful for dry runs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    departments_dir = output_dir / "departamentos"
    catalog_dir = output_dir / "catalogos"
    ensure_dir(departments_dir)
    ensure_dir(catalog_dir)

    extraction_timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    extraction_log: list[dict[str, str]] = []
    municipality_catalog: list[dict[str, str]] = []
    consolidated_rows: list[dict[str, str]] = []
    header_map_rows: list[dict[str, str]] = []
    normalized_headers: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not args.headful)
        page = browser.new_page(viewport={"width": 1600, "height": 2400})
        page.goto(BASE_URL, wait_until="networkidle", timeout=DEFAULT_WAIT_MS)

        departments = extract_select_options(page, DEPARTMENT_SELECTOR)
        levels = extract_select_options(page, LEVEL_SELECTOR)
        sectors = extract_select_options(page, SECTOR_SELECTOR)
        plans = extract_select_options(page, PLAN_SELECTOR)
        modalities = extract_select_options(page, MODALITY_SELECTOR)

        selected_departments = [
            item for item in departments if item["value"] and item["value"] != "SELECCIONE UNO"
        ]
        if args.department_limit is not None:
            selected_departments = selected_departments[: args.department_limit]

        for department in selected_departments:
            code = department["value"]
            name = department["label"]
            status = "ok"
            error_message = ""
            try:
                result = scrape_department(page, code, name, extraction_timestamp)
                consolidated_rows.extend(result.rows)

                department_fieldnames = sorted({key for row in result.rows for key in row.keys()})
                if result.rows and not normalized_headers:
                    data_headers = [field for field in result.normalized_headers if field not in META_HEADERS]
                    normalized_headers = data_headers
                    header_map_rows = [
                        {
                            "encabezado_original": raw_header,
                            "nombre_variable": normalized_header,
                        }
                        for raw_header, normalized_header in zip(result.raw_headers, result.normalized_headers)
                    ]

                if result.rows:
                    fieldnames = (normalized_headers + META_HEADERS) if normalized_headers else department_fieldnames
                else:
                    fieldnames = (normalized_headers + META_HEADERS) if normalized_headers else META_HEADERS

                write_csv(
                    departments_dir / f"{code}_{slugify_filename(name)}.csv",
                    result.rows,
                    fieldnames,
                )

                for municipality in result.municipalities:
                    municipality_catalog.append(
                        {
                            "departamento_codigo": code,
                            "departamento": name,
                            "municipio_indice": municipality["index"],
                            "municipio_codigo": municipality["value"],
                            "municipio": municipality["label"],
                            "fecha_extraccion": extraction_timestamp,
                            "fuente_url": BASE_URL,
                        }
                    )
            except TimeoutError as exc:
                status = "timeout"
                error_message = str(exc)
            except Exception as exc:  # noqa: BLE001
                status = "error"
                error_message = str(exc)

            extraction_log.append(
                {
                    "departamento_codigo": code,
                    "departamento": name,
                    "estado": status,
                    "filas_extraidas": str(len([row for row in consolidated_rows if row.get("departamento_consulta_codigo") == code])),
                    "error": error_message,
                    "fecha_extraccion": extraction_timestamp,
                    "fuente_url": BASE_URL,
                }
            )

        browser.close()

    consolidated_fieldnames = sorted({key for row in consolidated_rows for key in row.keys()})
    if normalized_headers:
        consolidated_fieldnames = normalized_headers + META_HEADERS

    write_csv(
        output_dir / "establecimientos_diversificado_guatemala.csv",
        consolidated_rows,
        consolidated_fieldnames or ["fecha_extraccion", "fuente_url"],
    )
    write_csv(output_dir / "extraction_log.csv", extraction_log, list(extraction_log[0].keys()) if extraction_log else [])
    write_csv(catalog_dir / "departamentos.csv", selected_departments, ["index", "value", "label"])
    write_csv(catalog_dir / "niveles.csv", levels, ["index", "value", "label"])
    write_csv(catalog_dir / "sectores.csv", sectors, ["index", "value", "label"])
    write_csv(catalog_dir / "planes.csv", plans, ["index", "value", "label"])
    write_csv(catalog_dir / "modalidades.csv", modalities, ["index", "value", "label"])
    write_csv(
        catalog_dir / "municipios.csv",
        municipality_catalog,
        [
            "departamento_codigo",
            "departamento",
            "municipio_indice",
            "municipio_codigo",
            "municipio",
            "fecha_extraccion",
            "fuente_url",
        ],
    )
    write_csv(
        catalog_dir / "header_mapping.csv",
        header_map_rows,
        ["encabezado_original", "nombre_variable"],
    )

    print(f"Departamentos procesados: {len(selected_departments)}")
    print(f"Filas consolidadas: {len(consolidated_rows)}")
    print(f"Salida: {output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
