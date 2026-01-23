import pandas as pd
import numpy as np

df = pd.read_csv(".../Research Grant Project - Manufacturing Jobs - Manufacturing Information.csv")
df.shape

def infer_role_family(title: str) -> str:
    if pd.isna(title):
        return "Unknown"

    t = title.lower()

    if any(k in t for k in ["engineer", "engineering"]):
        return "Engineering"

    if any(k in t for k in ["technician", "operator", "manufacturing", "assembly", "production"]):
        return "Manufacturing Operations"

    if any(k in t for k in ["quality", "validation", "inspection", "compliance"]):
        return "Quality & Compliance"

    if any(k in t for k in ["supply", "logistics", "procurement", "materials"]):
        return "Supply Chain"

    if any(k in t for k in ["project", "program", "planner"]):
        return "Project Management"

    if any(k in t for k in ["design", "cad"]):
        return "Design"

    return "Other"

df["role_family"] = df["job_title"].map(infer_role_family)
df["role_family"].value_counts()

def infer_pipeline_level(title: str) -> str:
    if pd.isna(title):
        return "Unknown"

    t = title.lower()

    if any(k in t for k in ["intern", "internship", "co-op", "coop"]):
        return "Internship"

    if any(k in t for k in ["entry", "junior", "associate", "i ", " i"]):
        return "Entry-Level"

    if any(k in t for k in ["senior", "sr", "lead", "principal", "manager", "director"]):
        return "Experienced"

    return "Unspecified"

df["pipeline_level"] = df["job_title"].map(infer_pipeline_level)
df["pipeline_level"].value_counts()

ACCESSIBILITY_MAP = {
    "Internship": 1.0,
    "Entry-Level": 0.7,
    "Unspecified": 0.4,
    "Experienced": 0.1,
    "Unknown": 0.0
}

df["accessibility_score"] = df["pipeline_level"].map(ACCESSIBILITY_MAP)
df["accessibility_score"].describe()

role_summary = (
    df.groupby("role_family")
      .agg(
          total_postings=("job_title", "count"),
          accessible_demand=("accessibility_score", "sum")
      )
      .sort_values("total_postings", ascending=False)
)

role_summary

OUT_PATH = ".../manufacturing_jobs_modeled.csv"
df.to_csv(OUT_PATH, index=False)
OUT_PATH