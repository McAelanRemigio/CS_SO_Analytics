from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt

DATA_PATH = Path(".../Research Grant Project - Manufacturing Jobs - Manufacturing Information.csv")
df = pd.read_csv(DATA_PATH)

df.shape, df.head()

employer_counts = (
    df["employer_name"]
    .value_counts()
    .rename("posting_count")
    .reset_index()
    .rename(columns={"index": "employer_name"})
)

employer_counts.head(10)

employer_counts.to_csv(".../employer_posting_counts.csv", index=False)

top_employers = employer_counts.head(10)["employer_name"]

platform_by_employer = (
    df[df["employer_name"].isin(top_employers)]
    .groupby(["employer_name", "platform"])
    .size()
    .unstack(fill_value=0)
)

platform_by_employer.plot(kind="bar", stacked=True)
plt.ylabel("Number of Postings")
plt.title("Top Employers: Job Postings by Platform")
plt.tight_layout()
plt.show()

platform_counts = (
    df["platform"]
    .value_counts(dropna=False)
    .rename("count")
    .reset_index()
    .rename(columns={"index": "platform"})
)

platform_counts["percent"] = (
    platform_counts["count"] / platform_counts["count"].sum() * 100
).round(1)

platform_counts

plt.figure()
plt.bar(platform_counts["platform"], platform_counts["count"])
plt.xlabel("Platform")
plt.ylabel("Number of Postings")
plt.title("Distribution of Job Postings by Platform")
plt.tight_layout()
plt.show()

job_title_counts = (
    df["job_title"]
    .value_counts()
    .rename("count")
    .reset_index()
    .rename(columns={"index": "job_title"})
)

job_title_counts.head(15)

salary_coverage = pd.DataFrame({
    "field": ["salary_min", "salary_max"],
    "percent_non_null": [
        df["salary_min"].notna().mean() * 100,
        df["salary_max"].notna().mean() * 100
    ]
})

salary_coverage
