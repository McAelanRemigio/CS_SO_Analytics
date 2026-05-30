
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


def load_program_activity_data(path):
    """Load a cleaned or approved program activity export."""
    required = {
        "Academic Year", "Month", "Activity Type", "Participant Count",
        "Partner Count", "Delivery Mode"
    }
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return standardize_months(df)


def create_synthetic_program_activity(seed=7):
    """Create anonymized demo data that mirrors common PLM reporting structure."""
    rng = np.random.default_rng(seed)
    rows = []
    activity_types = [
        "Advising Appointment", "Drop-in Consultation", "Orientation",
        "Classroom Presentation", "Workshop", "Specialized Program Enrollment",
        "Specialized Program Placement"
    ]
    modes = ["In-person", "Virtual", "Hybrid"]

    for ay in ACADEMIC_YEARS:
        for month in MONTH_ORDER:
            for activity in activity_types:
                base = {
                    "Advising Appointment": 80,
                    "Drop-in Consultation": 22,
                    "Orientation": 5,
                    "Classroom Presentation": 8,
                    "Workshop": 7,
                    "Specialized Program Enrollment": 4,
                    "Specialized Program Placement": 2,
                }[activity]
                n_events = max(0, int(rng.normal(base, max(1, base * 0.25))))
                if activity in ["Advising Appointment", "Drop-in Consultation"]:
                    for _ in range(n_events):
                        rows.append({
                            "Academic Year": ay,
                            "Month": month,
                            "Activity Type": activity,
                            "Participant Count": int(rng.integers(1, 3)),
                            "Partner Count": 0,
                            "Delivery Mode": rng.choice(modes, p=[0.45, 0.45, 0.10]),
                        })
                else:
                    for _ in range(n_events):
                        rows.append({
                            "Academic Year": ay,
                            "Month": month,
                            "Activity Type": activity,
                            "Participant Count": int(rng.integers(8, 85)),
                            "Partner Count": int(rng.integers(0, 4)),
                            "Delivery Mode": rng.choice(modes, p=[0.55, 0.25, 0.20]),
                        })
    df = pd.DataFrame(rows)
    return standardize_months(df)

# Public demo data. Replace with: df = load_program_activity_data("data/approved_program_activity.csv")
df = create_synthetic_program_activity()
df.head()


service_interactions = df[df["Activity Type"].isin(["Advising Appointment", "Drop-in Consultation"])].copy()
service_interactions["Interaction Count"] = 1

plot_monthly_comparison(
    service_interactions,
    value_col="Interaction Count",
    title="Completed Service Interactions by Academic Month",
    ylabel="Interactions",
)

summary_table(service_interactions, "Interaction Count")


mode_counts = (
    service_interactions
    .groupby(["Academic Year", "Month", "Delivery Mode"], observed=False)["Interaction Count"]
    .sum()
    .reset_index()
)

for ay in ACADEMIC_YEARS:
    pivot = (
        mode_counts[mode_counts["Academic Year"] == ay]
        .pivot(index="Month", columns="Delivery Mode", values="Interaction Count")
        .reindex(MONTH_ORDER)
        .fillna(0)
    )
    ax = pivot.plot(kind="bar", stacked=True, figsize=(14, 5), edgecolor="black")
    ax.set_title(f"Delivery Mode Mix - {ay}")
    ax.set_xlabel("Academic month")
    ax.set_ylabel("Interactions")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

mode_share = (
    service_interactions.groupby(["Academic Year", "Delivery Mode"])["Interaction Count"]
    .sum()
    .reset_index()
)
mode_share["Share of AY Total"] = mode_share.groupby("Academic Year")["Interaction Count"].transform(lambda x: (x / x.sum() * 100).round(1))
mode_share


outreach = df[df["Activity Type"].isin(["Orientation", "Classroom Presentation"])].copy()
outreach["Event Count"] = 1

plot_monthly_comparison(outreach, "Event Count", "Outreach Events by Academic Month", ylabel="Events")
plot_monthly_comparison(outreach, "Participant Count", "Outreach Attendance by Academic Month", ylabel="Participants")

outreach_summary = (
    outreach.groupby("Academic Year")
    .agg(
        Total_Events=("Event Count", "sum"),
        Total_Attendance=("Participant Count", "sum"),
    )
)
outreach_summary["Average Attendance per Event"] = (
    outreach_summary["Total_Attendance"] / outreach_summary["Total_Events"]
).round(1)
outreach_summary


workshops = df[df["Activity Type"] == "Workshop"].copy()
workshops["Workshop Count"] = 1

plot_monthly_comparison(workshops, "Workshop Count", "Workshops by Academic Month", ylabel="Workshops")
plot_monthly_comparison(workshops, "Participant Count", "Workshop Attendance by Academic Month", ylabel="Participants")

workshop_summary = (
    workshops.groupby("Academic Year")
    .agg(
        Total_Workshops=("Workshop Count", "sum"),
        Total_Attendance=("Participant Count", "sum"),
    )
)
workshop_summary["Average Attendance per Workshop"] = (
    workshop_summary["Total_Attendance"] / workshop_summary["Total_Workshops"]
).round(1)
workshop_summary


specialized = df[df["Activity Type"].str.contains("Specialized Program", na=False)].copy()

participation = (
    specialized.groupby(["Academic Year", "Activity Type"], observed=False)["Participant Count"]
    .sum()
    .unstack(fill_value=0)
)
participation["Placement Rate"] = safe_rate(
    participation.get("Specialized Program Placement", 0),
    participation.get("Specialized Program Enrollment", 0),
)
participation
