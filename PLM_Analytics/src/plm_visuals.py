import matplotlib.pyplot as plt

from plm_config import MONTH_COL


def monthly_bar_chart(df, title, x_col=MONTH_COL, y_col="monthly_total", y_label="Total"):
    plt.figure(figsize=(10, 5))
    plt.bar(df[x_col].astype(str), df[y_col])
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def grouped_monthly_bar_chart(df, title, group_col="academic_year", x_col=MONTH_COL, y_col="monthly_total"):
    """Create side-by-side monthly bars by academic year or another group"""
    chart_data = df.pivot(index=x_col, columns=group_col, values=y_col)

    chart_data.plot(kind="bar", figsize=(11, 5))
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Total")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def horizontal_bar_chart(df, category_col, value_col, title):
    chart_data = df.sort_values(value_col, ascending=True)

    plt.figure(figsize=(9, 5))
    plt.barh(chart_data[category_col].astype(str), chart_data[value_col])
    plt.title(title)
    plt.xlabel("Count")
    plt.tight_layout()
    plt.show()


def line_chart(df, title, x_col=MONTH_COL, y_col="monthly_total", group_col="academic_year"):
    plt.figure(figsize=(10, 5))

    if group_col in df.columns:
        for group_name, group_data in df.groupby(group_col):
            plt.plot(group_data[x_col].astype(str), group_data[y_col], marker="o", label=str(group_name))
        plt.legend(title=group_col.replace("_", " ").title())
    else:
        plt.plot(df[x_col].astype(str), df[y_col], marker="o")

    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Total")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def pie_chart(df, label_col, value_col, title):
    plt.figure(figsize=(7, 7))
    plt.pie(df[value_col], labels=df[label_col].astype(str), autopct="%1.1f%%", startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def rate_bar_chart(df, x_col, rate_col, title):
    plt.figure(figsize=(10, 5))
    plt.bar(df[x_col].astype(str), df[rate_col])
    plt.title(title)
    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel("Percent")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
