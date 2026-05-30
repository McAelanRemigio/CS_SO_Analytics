
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


def load_partner_engagement_data(path):
    """Load a cleaned or approved partner engagement export."""
    required = {
        "Academic Year", "Month", "Activity Type", "Event Type", "Partner Count",
        "Participant Count", "Open Rate", "Click Rate", "Industry"
    }
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return standardize_months(df)


def create_synthetic_partner_engagement(seed=11):
    rng = np.random.default_rng(seed)
    rows = []
    event_types = ["Info Session", "Workshop/Webinar", "Tabling", "Networking", "Special Event"]
    industries = ["Technology", "Healthcare", "Education", "Business", "Government", "Nonprofit", "Other"]

    for ay in ACADEMIC_YEARS:
        for month in MONTH_ORDER:
            # Partner orientations
            for _ in range(max(1, int(rng.normal(3, 1)))):
                rows.append({
                    "Academic Year": ay, "Month": month, "Activity Type": "Partner Orientation",
                    "Event Type": "Orientation", "Partner Count": int(rng.integers(6, 25)),
                    "Participant Count": 0, "Open Rate": np.nan, "Click Rate": np.nan,
                    "Industry": rng.choice(industries)
                })
            # Newsletters
            rows.append({
                "Academic Year": ay, "Month": month, "Activity Type": "Newsletter",
                "Event Type": "Communication", "Partner Count": 0, "Participant Count": 0,
                "Open Rate": round(rng.uniform(0.32, 0.58), 3),
                "Click Rate": round(rng.uniform(0.04, 0.16), 3),
                "Industry": "Not Applicable"
            })
            # Partner events
            for event_type in event_types:
                for _ in range(max(0, int(rng.normal(4, 2)))):
                    rows.append({
                        "Academic Year": ay, "Month": month, "Activity Type": "Partner Event",
                        "Event Type": event_type, "Partner Count": int(rng.integers(1, 12)),
                        "Participant Count": int(rng.integers(5, 120)), "Open Rate": np.nan,
                        "Click Rate": np.nan, "Industry": rng.choice(industries)
                    })
            # Mentoring-style program monthly summary
            mentees = int(rng.integers(20, 80))
            matched = int(mentees * rng.uniform(0.55, 0.85))
            rows.append({
                "Academic Year": ay, "Month": month, "Activity Type": "Mentor Program",
                "Event Type": "Mentor Matching", "Partner Count": int(rng.integers(15, 60)),
                "Participant Count": mentees, "Matched Participants": matched,
                "Open Rate": np.nan, "Click Rate": np.nan, "Industry": rng.choice(industries)
            })
            # Large-scale engagement events
            for _ in range(max(0, int(rng.normal(1.5, 0.8)))):
                rows.append({
                    "Academic Year": ay, "Month": month, "Activity Type": "Large-Scale Engagement Event",
                    "Event Type": "Large Event", "Partner Count": int(rng.integers(20, 120)),
                    "Participant Count": int(rng.integers(250, 1800)), "Open Rate": np.nan,
                    "Click Rate": np.nan, "Industry": "Multiple"
                })
    df = pd.DataFrame(rows)
    if "Matched Participants" not in df.columns:
        df["Matched Participants"] = np.nan
    return standardize_months(df)

# Public demo data. Replace with: df = load_partner_engagement_data("data/approved_partner_engagement.csv")
df = create_synthetic_partner_engagement()
df.head()


orientations = df[df["Activity Type"] == "Partner Orientation"].copy()
orientations["Orientation Count"] = 1

plot_monthly_comparison(orientations, "Orientation Count", "Partner Orientations by Academic Month", ylabel="Orientations")
plot_monthly_comparison(orientations, "Partner Count", "Partners Attending Orientations", ylabel="Partners")

orientation_summary = (
    orientations.groupby("Academic Year")
    .agg(Total_Orientations=("Orientation Count", "sum"), Total_Partners=("Partner Count", "sum"))
)
orientation_summary["Partners per Orientation"] = (
    orientation_summary["Total_Partners"] / orientation_summary["Total_Orientations"]
).round(1)
orientation_summary


newsletters = df[df["Activity Type"] == "Newsletter"].copy()

rate_summary = (
    newsletters.groupby(["Academic Year", "Month"], observed=False)
    .agg(Open_Rate=("Open Rate", "mean"), Click_Rate=("Click Rate", "mean"))
    .reset_index()
)
rate_summary = standardize_months(rate_summary)

for metric in ["Open_Rate", "Click_Rate"]:
    plot_monthly_comparison(
        rate_summary,
        value_col=metric,
        title=f"Monthly Newsletter {metric.replace('_', ' ')}",
        agg="mean",
        ylabel="Rate"
    )

annual_rates = (
    newsletters.groupby("Academic Year")
    .agg(Average_Open_Rate=("Open Rate", "mean"), Average_Click_Rate=("Click Rate", "mean"))
    .mul(100)
    .round(1)
)
annual_rates


partner_events = df[df["Activity Type"] == "Partner Event"].copy()
partner_events["Event Count"] = 1

event_mix = (
    partner_events.groupby("Event Type")
    .agg(
        Events=("Event Count", "sum"),
        Partners=("Partner Count", "sum"),
        Participants=("Participant Count", "sum"),
    )
    .sort_values("Events", ascending=True)
)
event_mix["Partners per Event"] = (event_mix["Partners"] / event_mix["Events"]).round(1)

ax = event_mix["Events"].plot(kind="barh", figsize=(10, 5), edgecolor="black")
ax.set_title("Partner Events by Type")
ax.set_xlabel("Event count")
plt.tight_layout()
plt.show()

event_mix.sort_values("Events", ascending=False)


mentor = df[df["Activity Type"] == "Mentor Program"].copy()
mentor_summary = (
    mentor.groupby("Academic Year")
    .agg(
        Participants=("Participant Count", "sum"),
        Matched=("Matched Participants", "sum"),
        Mentors_or_Partners=("Partner Count", "sum"),
    )
)
mentor_summary["Unmatched"] = mentor_summary["Participants"] - mentor_summary["Matched"]
mentor_summary["Match Rate"] = safe_rate(mentor_summary["Matched"], mentor_summary["Participants"])
mentor_summary


industry_counts = (
    df[df["Industry"].notna() & ~df["Industry"].isin(["Not Applicable", "Multiple"])]
    .groupby("Industry")
    .size()
    .sort_values(ascending=True)
)

ax = industry_counts.plot(kind="barh", figsize=(10, 5), edgecolor="black")
ax.set_title("Partner Engagement Records by Industry")
ax.set_xlabel("Records")
plt.tight_layout()
plt.show()


large_events = df[df["Activity Type"] == "Large-Scale Engagement Event"].copy()
large_events["Event Count"] = 1

large_event_summary = (
    large_events.groupby(["Academic Year", "Month"], observed=False)
    .agg(Events=("Event Count", "sum"), Participant_Checkins=("Participant Count", "sum"), Partners=("Partner Count", "sum"))
    .reset_index()
)
large_event_summary = standardize_months(large_event_summary)

plot_monthly_comparison(large_event_summary, "Participant_Checkins", "Large-Scale Event Participant Check-ins", ylabel="Check-ins")

large_events.groupby("Academic Year").agg(
    Events=("Event Count", "sum"),
    Participant_Checkins=("Participant Count", "sum"),
    Partners=("Partner Count", "sum"),
)
