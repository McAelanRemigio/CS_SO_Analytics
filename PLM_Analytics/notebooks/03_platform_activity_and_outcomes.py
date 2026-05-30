
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

MONTH_ORDER = [
    "July", "August", "September", "October", "November", "December",
    "January", "February", "March", "April", "May", "June"
]

ACADEMIC_YEARS = ["Year 1", "Year 2"]


def standardize_months(df, month_col="Month"):
    """Apply July-June academic-year ordering to a month column."""
    out = df.copy()
    out[month_col] = pd.Categorical(
        out[month_col].astype(str).str.strip(),
        categories=MONTH_ORDER,
        ordered=True,
    )
    return out


def monthly_summary(df, value_col, group_cols=("Academic Year", "Month"), agg="sum"):
    """Return a tidy monthly summary for a metric."""
    grouped = (
        df.groupby(list(group_cols), observed=False)[value_col]
        .agg(agg)
        .reset_index()
    )
    return standardize_months(grouped).sort_values(list(group_cols))


def summary_table(df, value_col, agg="sum"):
    """Create an academic-year comparison table with months as rows."""
    grouped = monthly_summary(df, value_col=value_col, agg=agg)
    pivot = (
        grouped.pivot(index="Month", columns="Academic Year", values=value_col)
        .reindex(MONTH_ORDER)
        .fillna(0)
    )
    pivot.loc["Total"] = pivot.sum(numeric_only=True)
    return pivot.round(2)


def plot_monthly_comparison(df, value_col, title, agg="sum", ylabel=None):
    """Plot side-by-side monthly bars by academic year with a combined trend line."""
    grouped = monthly_summary(df, value_col=value_col, agg=agg)
    pivot = (
        grouped.pivot(index="Month", columns="Academic Year", values=value_col)
        .reindex(MONTH_ORDER)
        .fillna(0)
    )

    ax = pivot.plot(kind="bar", figsize=(14, 5), width=0.8, edgecolor="black")
    pivot.sum(axis=1).plot(ax=ax, marker="o", linewidth=2, label="Combined monthly total")

    ax.set_title(title)
    ax.set_xlabel("Academic month")
    ax.set_ylabel(ylabel or value_col)
    ax.legend(title="Academic year / trend")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    return pivot


def safe_rate(numerator, denominator):
    """Return a percent rate while avoiding division-by-zero errors."""
    denominator = denominator.replace(0, np.nan) if isinstance(denominator, pd.Series) else denominator
    return (numerator / denominator * 100).round(1)


def load_platform_activity_data(path):
    """Load a cleaned or approved platform activity export."""
    required = {"Academic Year", "Month", "Metric", "Category", "Value"}
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return standardize_months(df)


def create_synthetic_platform_activity(seed=23):
    rng = np.random.default_rng(seed)
    rows = []
    metrics = [
        "Unique Participant Logins", "Profile Completions",
        "New Partners Approved", "New Partner Contacts"
    ]
    posting_categories = ["Internship", "Full-Time", "Part-Time", "Experiential Learning"]

    for ay in ACADEMIC_YEARS:
        for i, month in enumerate(MONTH_ORDER):
            seasonal = 1.3 if month in ["August", "September", "October", "February"] else 1.0
            for metric in metrics:
                base = {
                    "Unique Participant Logins": 4200,
                    "Profile Completions": 850,
                    "New Partners Approved": 110,
                    "New Partner Contacts": 180,
                }[metric]
                value = max(0, int(rng.normal(base * seasonal, base * 0.18)))
                rows.append({
                    "Academic Year": ay,
                    "Month": month,
                    "Metric": metric,
                    "Category": "All",
                    "Value": value,
                })
            for category in posting_categories:
                base = {"Internship": 320, "Full-Time": 510, "Part-Time": 210, "Experiential Learning": 120}[category]
                rows.append({
                    "Academic Year": ay,
                    "Month": month,
                    "Metric": "Opportunity Postings",
                    "Category": category,
                    "Value": max(0, int(rng.normal(base * seasonal, base * 0.25))),
                })
    return standardize_months(pd.DataFrame(rows))

# Public demo data. Replace with: df = load_platform_activity_data("data/approved_platform_activity.csv")
df = create_synthetic_platform_activity()
df.head()


logins = df[df["Metric"] == "Unique Participant Logins"].copy()
profiles = df[df["Metric"] == "Profile Completions"].copy()

plot_monthly_comparison(logins, "Value", "Unique Participant Logins by Academic Month", ylabel="Unique logins")
plot_monthly_comparison(profiles, "Value", "Profile Completions by Academic Month", ylabel="Profile completions")

activity_summary = pd.concat([
    summary_table(logins, "Value").assign(Metric="Unique Participant Logins"),
    summary_table(profiles, "Value").assign(Metric="Profile Completions"),
])
activity_summary


login_monthly = monthly_summary(logins, "Value").rename(columns={"Value": "Unique Logins"})
profile_monthly = monthly_summary(profiles, "Value").rename(columns={"Value": "Profile Completions"})
completion = login_monthly.merge(profile_monthly, on=["Academic Year", "Month"], how="left")
completion["Profile Completion Rate"] = safe_rate(completion["Profile Completions"], completion["Unique Logins"])
completion.head(12)


approved = df[df["Metric"] == "New Partners Approved"].copy()
contacts = df[df["Metric"] == "New Partner Contacts"].copy()

plot_monthly_comparison(approved, "Value", "New Partners Approved by Academic Month", ylabel="Approved partners")
plot_monthly_comparison(contacts, "Value", "New Partner Contacts by Academic Month", ylabel="Partner contacts")

partner_growth = pd.DataFrame({
    "Approved Partners": approved.groupby("Academic Year")["Value"].sum(),
    "Partner Contacts": contacts.groupby("Academic Year")["Value"].sum(),
})
partner_growth["Contacts per Approved Partner"] = (
    partner_growth["Partner Contacts"] / partner_growth["Approved Partners"]
).round(2)
partner_growth


postings = df[df["Metric"] == "Opportunity Postings"].copy()

posting_monthly = (
    postings.groupby(["Academic Year", "Month", "Category"], observed=False)["Value"]
    .sum()
    .reset_index()
)
posting_monthly = standardize_months(posting_monthly)

for ay in ACADEMIC_YEARS:
    pivot = (
        posting_monthly[posting_monthly["Academic Year"] == ay]
        .pivot(index="Month", columns="Category", values="Value")
        .reindex(MONTH_ORDER)
        .fillna(0)
    )
    ax = pivot.plot(kind="bar", stacked=True, figsize=(14, 5), edgecolor="black")
    ax.set_title(f"Opportunity Postings by Category - {ay}")
    ax.set_xlabel("Academic month")
    ax.set_ylabel("Postings")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

posting_summary = postings.groupby(["Academic Year", "Category"])["Value"].sum().unstack(fill_value=0)
posting_summary["Total"] = posting_summary.sum(axis=1)
posting_summary


kpi_rows = []
for ay in ACADEMIC_YEARS:
    subset = df[df["Academic Year"] == ay]
    kpi_rows.append({
        "Academic Year": ay,
        "Unique Logins": subset.loc[subset["Metric"] == "Unique Participant Logins", "Value"].sum(),
        "Profile Completions": subset.loc[subset["Metric"] == "Profile Completions", "Value"].sum(),
        "New Partners Approved": subset.loc[subset["Metric"] == "New Partners Approved", "Value"].sum(),
        "New Partner Contacts": subset.loc[subset["Metric"] == "New Partner Contacts", "Value"].sum(),
        "Opportunity Postings": subset.loc[subset["Metric"] == "Opportunity Postings", "Value"].sum(),
    })

kpi_summary = pd.DataFrame(kpi_rows)
kpi_summary["Profile Completion Rate"] = safe_rate(kpi_summary["Profile Completions"], kpi_summary["Unique Logins"])
kpi_summary
