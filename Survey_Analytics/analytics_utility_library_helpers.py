import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


YES_NO_MAP = {
    "Yes": 1,
    "No": 0,
    "Y": 1,
    "N": 0,
    "True": 1,
    "False": 0,
    True: 1,
    False: 0,
    1: 1,
    0: 0,
}


def load_survey_data(path):
    return pd.read_csv(path)


def add_engagement_score(df, activity_columns):
    df = df.copy()

    df["engagement_score"] = (
        df[activity_columns]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .sum(axis=1)
    )

    return df


def add_binary_total(df, indicator_columns):
    df = df.copy()

    for col in indicator_columns:
        df[col] = (
            df[col]
            .replace(YES_NO_MAP)
            .pipe(pd.to_numeric, errors="coerce")
            .fillna(0)
        )

    df["experience_total"] = df[indicator_columns].sum(axis=1)

    return df


def summarize_mean_by_group(df, group_column, value_column):
    return (
        df.groupby(group_column)[value_column]
        .agg(["count", "mean", "std"])
        .round(3)
        .reset_index()
    )


def summarize_binary_rate_by_group(df, group_column, binary_column):
    temp = df.copy()

    temp[binary_column] = (
        temp[binary_column]
        .replace(YES_NO_MAP)
        .pipe(pd.to_numeric, errors="coerce")
    )

    summary = (
        temp.groupby(group_column)[binary_column]
        .agg(responses="count", rate="mean")
        .reset_index()
    )

    summary["rate_pct"] = (summary["rate"] * 100).round(2)

    return summary


def satisfaction_summary(rating_counts):
    ratings = []

    for rating, count in rating_counts.items():
        ratings.extend([rating] * count)

    ratings = np.array(ratings)

    return {
        "total_responses": len(ratings),
        "mean_rating": round(ratings.mean(), 3),
        "median_rating": round(np.median(ratings), 3),
        "negative_pct": round((ratings <= 4).mean() * 100, 3),
        "neutral_pct": round((ratings == 5).mean() * 100, 3),
        "positive_pct": round((ratings >= 6).mean() * 100, 3),
    }


def compare_satisfaction_periods(periods):
    rows = []

    for period, counts in periods.items():
        summary = satisfaction_summary(counts)

        rows.append({
            "period": period,
            **summary
        })

    return pd.DataFrame(rows)


def plot_rating_distribution(rating_counts, title="Satisfaction Rating Distribution"):
    ratings = sorted(rating_counts.keys())
    counts = [rating_counts[r] for r in ratings]

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(ratings, counts)
    ax.set_title(title)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")

    summary = satisfaction_summary(rating_counts)

    subtitle = (
        f"n={summary['total_responses']} | "
        f"mean={summary['mean_rating']:.2f} | "
        f"median={summary['median_rating']:.1f} | "
        f"positive={summary['positive_pct']:.1f}%"
    )

    ax.text(
        0.5,
        -0.18,
        subtitle,
        transform=ax.transAxes,
        ha="center"
    )

    plt.tight_layout()

    return fig


def run_survey_analysis(
    df,
    activity_columns,
    outcome_column,
    experience_columns,
    key_experience_column=None
):
    df = add_engagement_score(df, activity_columns)
    df = add_binary_total(df, experience_columns)

    results = {
        "engagement_by_outcome":
            summarize_mean_by_group(
                df,
                outcome_column,
                "engagement_score"
            ),

        "experience_total_by_outcome":
            summarize_mean_by_group(
                df,
                outcome_column,
                "experience_total"
            )
    }

    if key_experience_column:
        results["outcome_by_key_experience"] = (
            summarize_mean_by_group(
                df,
                key_experience_column,
                "engagement_score"
            )
        )

    return results


# Example

if __name__ == "__main__":

    periods = {
        "Period A": {
            0: 3,
            1: 5,
            2: 8,
            3: 10,
            4: 15,
            5: 25,
            6: 30,
            7: 45,
            8: 40,
            9: 22,
            10: 35,
        },
        "Period B": {
            0: 4,
            1: 4,
            2: 7,
            3: 12,
            4: 14,
            5: 23,
            6: 34,
            7: 50,
            8: 44,
            9: 28,
            10: 42,
        },
    }

    comparison = compare_satisfaction_periods(periods)

    print(comparison)
