import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from google.colab import drive
drive.mount('/content/drive')

# 2024 - 2025
df1 = pd.read_csv('2024_2025.csv')
# 2025 - 2026
df2 = pd.read_csv('2025_2026.csv')

# combined
df = pd.concat([df1, df2], ignore_index=True)

# Month order: July → June
month_order = ['July','August','September','October','November','December',
               'January','February','March','April','May','June']

df['Month'] = pd.Categorical(df['Month'].astype(str).str.strip(),
                             categories=month_order, ordered=True)

ay_colors = {
    '2024-2025': '#1f77b4',  # blue
    '2025-2026': '#ff7f0e',  # orange
}

def combo_chart(df_metric, metric_name, title):
    # By Month + AY
    df_group = df_metric.groupby(['Month', 'Academic Year'], observed=False)[metric_name].sum().reset_index()
    df_group = df_group.sort_values(['Month','Academic Year'])

    # Side by side Bar Chart Plot + Line Graphing per AY
    df_pivot = df_group.pivot(index='Month', columns='Academic Year', values=metric_name).fillna(0)

    fig, ax = plt.subplots(figsize=(16,6))

    df_pivot.plot(kind='bar', ax=ax, width=0.8, color=[ay_colors.get(col,col) for col in df_pivot.columns], edgecolor='black')

    df_pivot.sum(axis=1).plot(ax=ax, color='black', marker='o', linewidth=2, label='Chronological Trend')

    ax.set_title(title)
    ax.set_ylabel(metric_name)
    ax.set_xlabel('Month')
    ax.legend(title='Academic Year / Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def summary_table(df_metric, metric_name):
    # By Month + AY
    df_group = df_metric.groupby(['Month', 'Academic Year'], observed=False)[metric_name].sum().reset_index()

    df_pivot = df_group.pivot(index='Month', columns='Academic Year', values=metric_name).fillna(0)
    df_pivot = df_pivot.reindex(month_order)

    df_pivot.loc['Total'] = df_pivot.sum()

    return df_pivot.astype(int)

logins = df[df['Name'].str.contains('Login', case=False, na=False)].copy()
profiles = df[df['Name'].str.contains('Profile', case=False, na=False)].copy()
combo_chart(logins, 'Numbers', 'Monthly Unique A (Side-by-Side by AY + Trend)')
combo_chart(profiles, 'Numbers', 'Monthly B Completions (Side-by-Side by AY + Trend)')
logins_table = summary_table(logins, 'Numbers')
logins_table
profiles_table = summary_table(profiles, 'Numbers')
profiles_table

approved = df[df['Name'].str.contains('Number Of New X\\(Approved\\)', case=False, na=False)].copy()
contacts = df[df['Name'].str.contains('New Employer Contacts', case=False, na=False)].copy()

combo_chart(approved, 'Numbers', 'Monthly New C (Side-by-Side by AY + Trend)')
combo_chart(contacts, 'Numbers', 'Monthly New D (Side-by-Side by AY + Trend)')
approved_table = summary_table(approved, 'Numbers')
approved_table
contacts_table = summary_table(contacts, 'Numbers')
contacts_table

postings = df[df['Sub-Category'] == 'E']

postings_detail = (
    postings.groupby(['Academic Year','Month','Category'], observed=False)['Numbers']
    .sum()
    .reset_index()
)

# Order months
postings_detail['Month'] = pd.Categorical(
    postings_detail['Month'],
    categories=month_order,
    ordered=True
)

postings_detail = postings_detail.sort_values(['Academic Year','Month','Category'])

# Pivot
for ay in postings_detail['Academic Year'].unique():
    df_ay = postings_detail[postings_detail['Academic Year'] == ay]
    pivot_ay = df_ay.pivot(index='Month', columns='Category', values='Numbers').fillna(0).astype(int)
    print(f"E: {ay}")
    display(pivot_ay)
    print("\n")
