import pandas as pd

from plm_config import ACADEMIC_YEAR_COL, CATEGORY_COL, MONTH_COL, VALUE_COL


def monthly_totals(df, value_col=VALUE_COL):
    return (
        df.groupby([ACADEMIC_YEAR_COL, MONTH_COL], observed=False)[value_col]
        .sum()
        .reset_index(name="monthly_total")
    )


def academic_year_totals(df, value_col=VALUE_COL):
    return (
        df.groupby(ACADEMIC_YEAR_COL)[value_col]
        .agg(
            academic_year_total="sum",
            monthly_average="mean",
            records="count",
        )
        .reset_index()
    )


def category_counts(df, category_col=CATEGORY_COL, value_col=None):
    """
    Count records by category.

    If value_col is provided, the function sums that value instead of counting rows.
    """
    if value_col is None:
        result = df.groupby(category_col).size().reset_index(name="count")
    else:
        result = df.groupby(category_col)[value_col].sum().reset_index(name="count")

    total = result["count"].sum()
    result["percent"] = (result["count"] / total * 100).round(1)
    return result.sort_values("count", ascending=False).reset_index(drop=True)


def top_categories(df, category_col=CATEGORY_COL, value_col=None, top_n=8):
    """Keep the top categories and combine everything else as Other."""
    counts = category_counts(df, category_col=category_col, value_col=value_col)

    if len(counts) <= top_n:
        return counts

    top = counts.head(top_n).copy()
    other_count = counts.iloc[top_n:]["count"].sum()

    other = pd.DataFrame({
        category_col: ["Other"],
        "count": [other_count],
    })

    result = pd.concat([top[[category_col, "count"]], other], ignore_index=True)
    total = result["count"].sum()
    result["percent"] = (result["count"] / total * 100).round(1)
    return result


def make_rate(numerator, denominator):
    """Return a safe percentage. If denominator is 0, return 0."""
    if denominator == 0 or pd.isna(denominator):
        return 0
    return round(numerator / denominator * 100, 1)


def add_rate(df, numerator_col, denominator_col, rate_col="rate_percent"):
    """Add a percentage column to a dataframe."""
    df = df.copy()
    df[rate_col] = df.apply(
        lambda row: make_rate(row[numerator_col], row[denominator_col]),
        axis=1,
    )
    return df


def year_over_year_change(summary_df, value_col="academic_year_total"):
    df = summary_df.sort_values(ACADEMIC_YEAR_COL).copy()
    df["previous_year_value"] = df[value_col].shift(1)
    df["change"] = df[value_col] - df["previous_year_value"]
    df["change_percent"] = df.apply(
        lambda row: make_rate(row["change"], row["previous_year_value"]),
        axis=1,
    )
    return df


def communication_rates(df, sent_col="sent", opened_col="opened", clicked_col="clicked"):
    summary = (
        df.groupby([ACADEMIC_YEAR_COL, MONTH_COL], observed=False)
        .agg(
            sent=(sent_col, "sum"),
            opened=(opened_col, "sum"),
            clicked=(clicked_col, "sum"),
        )
        .reset_index()
    )

    summary = add_rate(summary, "opened", "sent", "open_rate_percent")
    summary = add_rate(summary, "clicked", "sent", "click_rate_percent")
    return summary


def kpi_table(kpis):
    return pd.DataFrame({
        "metric": list(kpis.keys()),
        "value": list(kpis.values()),
    })
