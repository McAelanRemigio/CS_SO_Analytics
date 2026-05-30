import re
from pathlib import Path

import pandas as pd

from plm_config import (
    ACADEMIC_YEAR_COL,
    ACADEMIC_YEAR_START_MONTH,
    DATE_COL,
    MONTH_COL,
    MONTH_ORDER,
)


def clean_column_names(df):
    df = df.copy()
    new_columns = []

    for col in df.columns:
        col = str(col).strip().lower()
        col = re.sub(r"[^a-z0-9]+", "_", col)
        col = col.strip("_")
        new_columns.append(col)

    df.columns = new_columns
    return df


def load_csv(path):
    df = pd.read_csv(path)
    return clean_column_names(df)


def load_many_csvs(folder_path, pattern="*.csv"):
    folder = Path(folder_path)
    files = sorted(folder.glob(pattern))

    all_files = []
    for file in files:
        df = load_csv(file)
        df["source_file"] = file.name
        all_files.append(df)

    if len(all_files) == 0:
        return pd.DataFrame()

    return pd.concat(all_files, ignore_index=True)


def add_time_columns(df, date_col=DATE_COL):
    """
    Add date, month, and academic_year columns.

    Example:
    A date in September 2024 becomes academic year 2024-2025.
    A date in February 2025 also becomes academic year 2024-2025.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    df[MONTH_COL] = df[date_col].dt.month_name()

    year = df[date_col].dt.year
    month_number = df[date_col].dt.month

    start_year = year.where(month_number >= ACADEMIC_YEAR_START_MONTH, year - 1)
    end_year = start_year + 1

    df[ACADEMIC_YEAR_COL] = start_year.astype("Int64").astype(str) + "-" + end_year.astype("Int64").astype(str)
    df.loc[df[date_col].isna(), ACADEMIC_YEAR_COL] = pd.NA

    df[MONTH_COL] = pd.Categorical(df[MONTH_COL], categories=MONTH_ORDER, ordered=True)
    return df


def fill_missing_text(df, columns, fill_value="Unknown"):
    """Fill blank text values in selected columns."""
    df = df.copy()

    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(["", " ", "NA", "N/A", "na", "n/a"], pd.NA)
            df[col] = df[col].fillna(fill_value)

    return df


def make_numeric(df, columns):
    """Convert selected columns to numbers."""
    df = df.copy()

    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df
