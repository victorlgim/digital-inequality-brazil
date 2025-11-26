import pandas as pd
import numpy as np
import os

# ---------------------------------------------------------------------
# Region mapping by Brazilian Federative Units
# ---------------------------------------------------------------------
# Dictionary grouping Brazilian states into official macro-regions.
# This is used to enrich the dataset with a "region" column for
# higher-level analysis (North, Northeast, etc.).
REGIONS = {
    "N":  ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "NE": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "SE": ["ES", "MG", "RJ", "SP"],
    "S":  ["PR", "RS", "SC"],
    "CO": ["DF", "GO", "MS", "MT"],
}


def map_region(uf: str) -> str:
    """
    Map a Brazilian state (UF) to its macro-region.
    Returns region code (N, NE, SE, S, CO) or None if the UF is unknown.
    """
    for region, states in REGIONS.items():
        if uf in states:
            return region
    return None


# ---------------------------------------------------------------------
# Fiber category mapping (0, 50, 100 → none, partial, full)
# ---------------------------------------------------------------------
def map_fiber_category(value):
    """
    Convert fiber coverage numeric values into readable categories.
    - 0   → no fiber coverage
    - 50  → partial fiber coverage
    - 100 → full fiber coverage
    Any unknown or missing value is categorized as "unknown".
    """
    if pd.isna(value):
        return "unknown"
    if value == 0:
        return "none"
    if value == 50:
        return "partial"
    if value == 100:
        return "full"
    return "unknown" 


# ---------------------------------------------------------------------
# Create annual IBC deciles using NTILE logic
# ---------------------------------------------------------------------
def add_ibc_deciles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ranked deciles (1–10) for the IBC indicator,
    computed *within each year*.

    Logic:
    - Rank municipalities by IBC inside each year
    - Use qcut to split into 10 equal buckets
    - Labels 1..10, where 10 = highest IBC group
    """
    df = df.copy()
    df["ibc_decile"] = (
        df.groupby("year")["ibc"]
          .transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False) + 1)
    )
    return df


# ---------------------------------------------------------------------
# Main dataset preparation function
# ---------------------------------------------------------------------
def prepare_dataset(raw_path: str, processed_path: str):
    """
    Full ETL pipeline for preparing the connectivity dataset.

    Steps:
    1. Load raw CSV
    2. Standardize column names
    3. Rename columns into English
    4. Enrich with region and fiber category
    5. Convert numeric columns
    6. Remove invalid rows
    7. Compute IBC deciles
    8. Save processed dataset
    """

    df = pd.read_csv(raw_path)

    # ---------------------------------------------------------------
    # Standardize column names to lowercase_with_underscores
    # Removes spaces, hyphens, and ensures consistency.
    # ---------------------------------------------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # ---------------------------------------------------------------
    # Rename raw columns into canonical English names.
    # This makes downstream analysis cleaner and more maintainable.
    # ---------------------------------------------------------------
    rename_map = {
        "ano": "year",
        "sigla_uf": "state",
        "sigla_uf_nome": "state_name",
        "id_municipio": "municipality_id",
        "id_municipio_nome": "municipality_name",
        "cobertura_pop_4g5g": "coverage_4g5g",
        "densidade_smp": "density_smp",
        "densidade_scm": "density_scm",
        "hhi_smp": "hhi_smp",
        "hhi_scm": "hhi_scm",
        "adensamento_estacoes": "stations_density",
    }

    df = df.rename(columns=rename_map)

    # ---------------------------------------------------------------
    # Map each state to its macro-region
    # ---------------------------------------------------------------
    df["region"] = df["state"].apply(map_region)

    # ---------------------------------------------------------------
    # Map fiber numeric values into "none", "partial", "full"
    # ---------------------------------------------------------------
    df["fiber_cat"] = df["fibra"].apply(map_fiber_category)

    # ---------------------------------------------------------------
    # Convert relevant columns to numeric
    # Coerce errors → NaN ensures safe stats operations.
    # ---------------------------------------------------------------
    numeric_cols = [
        "ibc",
        "coverage_4g5g",
        "fibra",
        "density_smp",
        "density_scm",
        "hhi_smp",
        "hhi_scm",
        "stations_density",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------------------------------------------
    # Remove rows missing critical fields
    # IBC, year, and state cannot be null for meaningful analysis.
    # ---------------------------------------------------------------
    df = df.dropna(subset=["ibc", "year", "state"])

    # ---------------------------------------------------------------
    # Compute IBC deciles by year (stratified NTILE-like grouping)
    # ---------------------------------------------------------------
    df = add_ibc_deciles(df)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)

    # Save processed CSV
    df.to_csv(processed_path, index=False)


if __name__ == "__main__":
    RAW_PATH = "data/raw/municipalities_connectivity_raw.csv"
    PROCESSED_PATH = "data/processed/municipalities_connectivity_processed.csv"

    prepare_dataset(RAW_PATH, PROCESSED_PATH)
