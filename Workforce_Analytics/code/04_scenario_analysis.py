from pathlib import Path
import pandas as pd
import numpy as np
DATA_PATH = Path("./data/processed/manufacturing_jobs_clean.csv")
df = pd.read_csv(DATA_PATH)

print("Rows:", len(df))
print("Columns:", df.columns.tolist())


df.head(3)

required = ["role_family", "pipeline_level", "accessibility_score"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing expected modeled columns: {missing}")

# helper
def total_accessible_demand(df_in):
    return df_in["accessibility_score"].sum()

def role_family_summary(df_in):
    return (
        df_in.groupby("role_family")
             .agg(total_postings=("job_title", "count"),
                  accessible_demand=("accessibility_score", "sum"))
             .sort_values("accessible_demand", ascending=False)
             .reset_index()
    )

# baseline numbers
baseline_accessible = total_accessible_demand(df)
role_summary = role_family_summary(df)
print(f"Baseline accessible demand (placement units): {baseline_accessible:.1f}")
role_summary.head()

# Tunable parameter
csu_supply_default = 200.0 # for future reference, if you have actual real data, replace this value
csu_supply_default

def compute_gap_metrics(df_in, csu_supply):
    total_demand = total_accessible_demand(df_in)
    placements_possible = min(total_demand, csu_supply)
    unmet_gap = max(total_demand - csu_supply, 0.0)
    percent_fulfilled = 100.0 * placements_possible / total_demand if total_demand > 0 else np.nan
    return {
        "total_accessible_demand": total_demand,
        "csu_supply": csu_supply,
        "placements_possible": placements_possible,
        "unmet_gap": unmet_gap,
        "percent_fulfilled": percent_fulfilled
    }

baseline_metrics = compute_gap_metrics(df, csu_supply_default)
baseline_metrics

# Scenario parameters
supply_increase_pct = 0.20
target_top_k = 5
target_accessibility_delta = 0.25

# Compute top-K employers by posting count
employer_counts = df["employer_name"].value_counts().rename_axis("employer_name").reset_index(name="posting_count")
top_employers = employer_counts.head(target_top_k)["employer_name"].tolist()
top_employers

def scenario_supply_increase(df_in, csu_supply, pct_increase):
    new_supply = csu_supply * (1 + pct_increase)
    metrics = compute_gap_metrics(df_in, new_supply)
    metrics["scenario"] = f"Supply +{int(pct_increase*100)}%"
    metrics["csu_supply_used"] = new_supply
    return metrics

def scenario_target_employers(df_in, csu_supply, employers, delta):
    df_mod = df_in.copy()
    mask = df_mod["employer_name"].isin(employers)
    # raise accessibility where mask True
    df_mod.loc[mask, "accessibility_score"] = (
        df_mod.loc[mask, "accessibility_score"] + delta
    ).clip(upper=1.0)
    metrics = compute_gap_metrics(df_mod, csu_supply)
    metrics["scenario"] = f"Target Top {len(employers)} Employers (+{delta:.2f} acc)"
    metrics["affected_postings"] = int(mask.sum())
    return metrics, df_mod

def scenario_combined(df_in, csu_supply, pct_increase, employers, delta):
    # apply employer targeting then increase supply
    metrics_target, df_mod = scenario_target_employers(df_in, csu_supply, employers, delta)
    new_supply = csu_supply * (1 + pct_increase)
    metrics = compute_gap_metrics(df_mod, new_supply)
    metrics["scenario"] = f"Combined: Supply +{int(pct_increase*100)}% & Target Top {len(employers)}"
    metrics["affected_postings"] = int(df_in["employer_name"].isin(employers).sum())
    metrics["csu_supply_used"] = new_supply
    return metrics, df_mod


scenarios = []

# Baseline
scenarios.append({
    "scenario": "Baseline",
    **baseline_metrics
})

# Scenario A: supply increase
scenarios.append(scenario_supply_increase(df, csu_supply_default, supply_increase_pct))

# Scenario B: target top employers
metrics_target, df_targeted = scenario_target_employers(df, csu_supply_default, top_employers, target_accessibility_delta)
scenarios.append(metrics_target)

# Scenario C: combined
metrics_combined, df_combined = scenario_combined(df, csu_supply_default, supply_increase_pct, top_employers, target_accessibility_delta)
scenarios.append(metrics_combined)

scenarios_df = pd.DataFrame(scenarios).set_index("scenario")
scenarios_df[[
    "total_accessible_demand",
    "csu_supply",
    "csu_supply_used",
    "placements_possible",
    "unmet_gap",
    "percent_fulfilled",
    "affected_postings"
]].fillna("").T

# Baseline placements
baseline_placements = baseline_metrics["placements_possible"]

def placements_from_metrics(m):
    return m["placements_possible"]

impact_rows = []
for s in scenarios:
    name = s["scenario"]
    placements = placements_from_metrics(s)
    delta = placements - baseline_placements
    impact_rows.append({
        "scenario": name,
        "placements": placements,
        "delta_vs_baseline": delta,
        "percent_fulfilled": s.get("percent_fulfilled", np.nan),
        "affected_postings": s.get("affected_postings", 0)
    })

impact_df = pd.DataFrame(impact_rows).set_index("scenario")
impact_df

# role-family summary for baseline vs combined
role_baseline = role_family_summary(df).set_index("role_family")
role_combined = role_family_summary(df_combined).set_index("role_family")

role_compare = role_baseline.join(role_combined, lsuffix="_baseline", rsuffix="_combined", how="outer").fillna(0)
role_compare["additional_accessible_demand"] = role_compare["accessible_demand_combined"] - role_compare["accessible_demand_baseline"]
role_compare = role_compare.sort_values("accessible_demand_baseline", ascending=False)
role_compare[[
    "total_postings_baseline", "accessible_demand_baseline", 
    "total_postings_combined", "accessible_demand_combined",
    "additional_accessible_demand"
]]

from textwrap import dedent

print(dedent(f"""
BASELINE:
- Accessible demand (placement units): {baseline_metrics['total_accessible_demand']:.1f}
- CSU supply (default param): {baseline_metrics['csu_supply']:.1f}
- Placements possible: {baseline_metrics['placements_possible']:.1f}
- Percent of accessible demand CSU can meet: {baseline_metrics['percent_fulfilled']:.1f}%

SCENARIO COMPARISON (deltas vs baseline):
{impact_df.to_string()}
"""))
