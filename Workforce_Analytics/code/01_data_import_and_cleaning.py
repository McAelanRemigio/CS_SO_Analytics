# Setup
from pathlib import Path
import pandas as pd
import numpy as np
import re

RAW_XLSX = Path(".../Research Grant Project - Manufacturing Jobs.xlsx")
OUT_CSV  = Path(".../Research Grant Project - Manufacturing Jobs - Manufacturing Information.csv")

RAW_XLSX.exists(), RAW_XLSX

# Load
xls = pd.ExcelFile(RAW_XLSX)
xls.sheet_names

DATA_SHEET = "Manufacturing Information"

df_raw = pd.read_excel(RAW_XLSX, sheet_name=DATA_SHEET)
df_raw.shape, df_raw.head(3)

EXPECTED_COLS = [
    "employer_name",
    "job_title",
    "salary_raw",
    "salary_min",
    "salary_max",
    "platform",
    "position_link",
    "career_website"
]

missing = [c for c in EXPECTED_COLS if c not in df_raw.columns]
extra   = [c for c in df_raw.columns if c not in EXPECTED_COLS]

print("Missing columns:", missing)
print("Extra columns:", extra)

assert not missing, "Dataset is missing required columns."

def clean_string(s):
    """Trim whitespace, normalize internal spaces, keep NaN as NaN."""
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)
    return s if s != "" else np.nan

def parse_currency(x):
    """
    Convert currency-like strings to float.
    Handles cases like:
      '$164,200.00' -> 164200.0
      '164,200' -> 164200.0
      '211.600.00' -> 211600.0   (fixes extra dot thousands sep)
      NaN/'' -> NaN
    """
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if s == "":
        return np.nan

    # remove $ and commas
    s = s.replace("$", "").replace(",", "")

    # keep only digits, dot, minus
    s = re.sub(r"[^0-9.\-]", "", s)

    if s in {"", ".", "-"}:
        return np.nan

    # If there are multiple dots, treat all but the last as thousand separators
    if s.count(".") > 1:
        parts = s.split(".")
        s = "".join(parts[:-1]) + "." + parts[-1]   # keep last as decimal

    try:
        return float(s)
    except ValueError:
        return np.nan


# Standardization
df = df_raw.copy()

# Cleaning and normalizing
for col in ["employer_name", "job_title", "platform", "position_link", "career_website", "salary_raw", "salary_min", "salary_max"]:
    df[col] = df[col].map(clean_string)

platform_map = {
    "website": "Website",
    "career website": "Website",
    "handshake": "Handshake"
}
df["platform"] = df["platform"].str.lower().map(lambda x: platform_map.get(x, x.title() if isinstance(x, str) else x))

# Parse to floats
df["salary_min"] = df["salary_min"].map(parse_currency)
df["salary_max"] = df["salary_max"].map(parse_currency)

# Optional: if salary_min==salary_max treat as fixed (not needed, but sanity)
# df["salary_is_range"] = (df["salary_min"].notna()) & (df["salary_max"].notna()) & (df["salary_min"] != df["salary_max"])

# Check for anomalies
df.loc[
    df["salary_max"].astype(str).str.count(r"\.") > 1,
    ["salary_raw", "salary_min", "salary_max"]
]

# Deduplication
KEYS = ["employer_name", "job_title", "platform"]

# completeness score: count non-null across high-value columns
score_cols = ["position_link", "career_website", "salary_min", "salary_max", "salary_raw"]
df["_completeness"] = df[score_cols].notna().sum(axis=1)

before = len(df)

df = (
    df.sort_values(by="_completeness", ascending=False)
      .drop_duplicates(subset=KEYS, keep="first")
      .drop(columns=["_completeness"])
      .reset_index(drop=True)
)

after = len(df)
print(f"Rows before: {before:,} | after dedupe: {after:,} | removed: {before-after:,}")


df.isna().mean().sort_values(ascending=False).head(10)
df["platform"].value_counts(dropna=False)
# check salary parsing didn’t explode
df[["salary_min", "salary_max"]].describe()

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_CSV, index=False)
OUT_CSV, OUT_CSV.exists()
