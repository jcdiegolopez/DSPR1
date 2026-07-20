"""Genera el libro de codigos del conjunto limpio del Proyecto 1."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "processed" / "establecimientos_diversificado_guatemala_limpio.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "libro_codigos.md"
LOG_PATH = ROOT / "data" / "processed" / "log_transformaciones.csv"
DELIVERY_LOG_CSV_PATH = ROOT / "data" / "processed" / "tabla_transformaciones.csv"
DELIVERY_LOG_MD_PATH = ROOT / "data" / "processed" / "tabla_transformaciones.md"
VERSION = "1.0.0"

DESCRIPTIONS = {
    "codigo": "Identificador unico del establecimiento educativo.",
    "distrito": "Codigo o identificador de distrito reportado por MINEDUC.",
    "departamento": "Departamento donde se ubica el establecimiento.",
    "municipio": "Municipio donde se ubica el establecimiento.",
    "establecimiento": "Nombre del establecimiento educativo.",
    "direccion": "Direccion reportada para el establecimiento.",
    "telefono": "Telefono original reportado por la fuente.",
    "supervisor": "Nombre del supervisor reportado por la fuente.",
    "director": "Nombre del director reportado por la fuente.",
    "nivel": "Nivel educativo del establecimiento.",
    "sector": "Sector administrativo del establecimiento.",
    "area": "Clasificacion geografica del establecimiento.",
    "status": "Estado administrativo reportado por MINEDUC.",
    "modalidad": "Modalidad educativa reportada por MINEDUC.",
    "jornada": "Jornada de funcionamiento del establecimiento.",
    "plan": "Plan educativo reportado por MINEDUC.",
    "departamental": "Direccion departamental administrativa reportada por MINEDUC.",
    "fecha_extraccion": "Fecha y hora UTC en que se obtuvo el registro.",
    "fuente_url": "URL de procedencia de los datos.",
    "nivel_consulta": "Filtro de nivel utilizado durante la extraccion.",
    "sector_consulta": "Filtro de sector utilizado durante la extraccion.",
    "plan_consulta": "Filtro de plan utilizado durante la extraccion.",
    "modalidad_consulta": "Filtro de modalidad utilizado durante la extraccion.",
    "departamento_consulta": "Departamento seleccionado durante la extraccion.",
    "departamento_consulta_codigo": "Codigo del departamento seleccionado durante la extraccion.",
    "telefono_normalizado": "Telefono de ocho digitos apto para analisis; NA si no pudo verificarse.",
    "telefono_valido": "Indica si se obtuvo un telefono normalizado valido de ocho digitos.",
    "distrito_formato_revisar": "Indica que el formato original del distrito no pudo verificarse.",
    "departamental_difiere_departamento": "Indica que la direccion departamental difiere del departamento geografico.",
}

TREATMENTS = {
    "codigo": "Se conserva como texto y se valida el patron NN-NN-NNNN-NN.",
    "distrito": "Se normalizan espacios; los formatos no verificables se convierten a NA y se marcan.",
    "telefono": "Se conserva para auditoria; marcadores de ausencia se convierten a NA.",
    "fecha_extraccion": "Se convierte a fecha-hora UTC.",
    "telefono_normalizado": "Derivada al remover separadores y prefijo +502; solo se conserva si tiene ocho digitos.",
    "telefono_valido": "Bandera derivada de telefono_normalizado.",
    "distrito_formato_revisar": "Bandera derivada para formatos de distrito no verificables.",
    "departamental_difiere_departamento": "Bandera derivada para diferencias entre columnas administrativas.",
}

CATEGORY_COLUMNS = {
    "departamento", "municipio", "nivel", "sector", "area", "status", "modalidad", "jornada",
    "plan", "departamental", "nivel_consulta", "sector_consulta", "plan_consulta",
    "modalidad_consulta", "departamento_consulta", "departamento_consulta_codigo",
}


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def domain_and_values(frame: pd.DataFrame, column: str) -> tuple[str, str]:
    if column == "codigo":
        return "Texto con patron NN-NN-NNNN-NN", "Codigos que cumplen el patron; sin NA."
    if column == "distrito":
        return "Texto con patrones NN-NNN, NN-NN-NNN o NN-NN-NNNN; NA si no es verificable", "Codigos de distrito validos o NA."
    if column in {"telefono", "telefono_normalizado"}:
        return "Texto; telefono_normalizado tiene exactamente 8 digitos o NA", "Telefono reportado; 8 digitos o NA en el campo normalizado."
    if column in {"telefono_valido", "distrito_formato_revisar", "departamental_difiere_departamento"}:
        return "Booleano", "True, False."
    if column == "fecha_extraccion":
        return "Fecha-hora UTC", "Marca temporal ISO 8601 con zona UTC."
    if column == "fuente_url":
        return "URL", "URL del portal MINEDUC utilizado."
    if column in {"establecimiento", "direccion", "supervisor", "director"}:
        return "Texto libre o NA", "Valores textuales reportados por la fuente."
    if column == "municipio":
        return "Categoria controlada por par departamento-municipio", "Catalogo completo: data/raw/catalogos/municipios.csv."
    if column in CATEGORY_COLUMNS:
        values = sorted(frame[column].dropna().astype(str).unique())
        return "Categoria controlada", "; ".join(values)
    return "Texto o NA", "Valores textuales reportados por la fuente."


def main() -> None:
    clean = pd.read_csv(CLEAN_PATH, dtype="string", keep_default_na=True)
    extraction_date = clean["fecha_extraccion"].dropna().iloc[0]
    source = clean["fuente_url"].dropna().iloc[0]

    lines = [
        "# Libro de codigos — establecimientos Diversificado MINEDUC",
        "",
        "## Metadatos",
        "",
        f"- **Version:** {VERSION}",
        f"- **Fuente:** {source}",
        f"- **Fecha de extraccion:** {extraction_date}",
        "- **Cobertura:** establecimientos educativos de Guatemala con nivel `DIVERSIFICADO`.",
        "- **Conjunto descrito:** `data/processed/establecimientos_diversificado_guatemala_limpio.csv`.",
        "- **Convencion de ausencias:** `NA` representa un valor faltante o no verificable.",
        "",
        "## Variables",
        "",
        "| Variable | Descripcion | Tipo de dato | Dominio | Valores posibles | Tratamiento aplicado | Derivada |",
        "|---|---|---|---|---|---|---|",
    ]

    for column in clean.columns:
        domain, values = domain_and_values(clean, column)
        treatment = TREATMENTS.get(column, "Se normalizan espacios y marcadores de ausencia; se conserva el valor semantico.")
        derived = "Si" if column in {"telefono_normalizado", "telefono_valido", "distrito_formato_revisar", "departamental_difiere_departamento"} else "No"
        lines.append(
            f"| {column} | {esc(DESCRIPTIONS[column])} | {clean[column].dtype} | {esc(domain)} | {esc(values)} | {esc(treatment)} | {derived} |"
        )

    lines.extend([
        "",
        "## Variables derivadas",
        "",
        "- `telefono_normalizado` permite analizar telefonos verificados sin modificar el valor original.",
        "- `telefono_valido` identifica los registros con un telefono normalizado de ocho digitos.",
        "- `distrito_formato_revisar` conserva la trazabilidad de los distritos cuyo formato no pudo validarse.",
        "- `departamental_difiere_departamento` hace visible una diferencia administrativa sin sobrescribir ninguno de los dos campos.",
    ])
    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    log = pd.read_csv(LOG_PATH)
    variables = {
        "a": "Todas las variables de texto; area (excepcion SIN ESPECIFICAR)",
        "b": "fecha_extraccion; codigos y telefonos",
        "c": "Todas las variables de texto",
        "d": "departamento, municipio, sector, modalidad",
        "e": "codigo, telefono, distrito",
        "f": "codigo, departamento, municipio, sector, modalidad, telefono, distrito",
        "g": "Registro completo; establecimiento, direccion, municipio, telefono_normalizado",
        "h": "departamental, departamento, departamento_consulta, departamento_consulta_codigo",
        "i": "telefono_normalizado, telefono_valido, distrito_formato_revisar, departamental_difiere_departamento",
    }
    problems = {
        "a": "Vacios y marcadores de ausencia heterogeneos.",
        "b": "Fecha en texto y riesgo de perder formato en identificadores.",
        "c": "Espacios externos, multiples o invisibles.",
        "d": "Categorias potencialmente fuera de catalogo.",
        "e": "Patrones de codigo, telefono y distrito inconsistentes.",
        "f": "Valores no verificables o fuera de dominio.",
        "g": "Posibles registros duplicados exactos o parciales.",
        "h": "Discrepancias potenciales entre variables relacionadas.",
        "i": "Necesidad de campos analiticos y de auditoria derivados.",
    }
    delivery_log = pd.DataFrame({
        "variable": log["inciso"].map(variables),
        "problema_detectado": log["inciso"].map(problems),
        "transformacion": log["accion"],
        "registros_afectados": log["registros_afectados"],
        "justificacion": log["justificacion"],
    })
    delivery_log.to_csv(DELIVERY_LOG_CSV_PATH, index=False, encoding="utf-8")
    log_lines = [
        "# Tabla de transformaciones",
        "",
        "| Variable | Problema detectado | Transformacion | Registros afectados | Justificacion |",
        "|---|---|---|---:|---|",
    ]
    for row in delivery_log.itertuples(index=False):
        log_lines.append("| " + " | ".join(esc(value) for value in row) + " |")
    DELIVERY_LOG_MD_PATH.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(f"Libro de codigos generado: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Tabla de transformaciones generada: {DELIVERY_LOG_MD_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
