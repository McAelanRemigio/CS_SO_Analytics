# Data Pipeline Overview

This document explains the simplified analytics pipeline used in the anonymized Program Lifecycle Management project.

The goal of the pipeline is to turn fragmented operational exports into consistent reporting tables, charts, and summary metrics.

---

## 1. Pipeline Summary

The workflow follows five basic steps:

```text
Raw exports or sample data
        ↓
Clean column names and date fields
        ↓
Add month and academic-year labels
        ↓
Calculate metrics and summary tables
        ↓
Create charts and report-ready outputs
```

In the public portfolio version, raw workplace data is replaced with synthetic or sample data.

---

## 2. Source Files

A real workflow may include many files from different systems. Examples include:

| Source Type | Example Content | Common Issue |
|---|---|---|
| Service activity exports | appointments, sessions, attendance | inconsistent status labels |
| Event tracking files | event name, date, attendees | missing attendance or duplicated events |
| Partner engagement files | organizations, contacts, event attendance | inconsistent partner names |
| Platform exports | logins, profile completions, postings | changing column names over time |
| Manual trackers | program outcomes or notes | free-text fields and inconsistent formatting |

The public version does not include the original files.

---

## 3. Cleaning Process

The cleaning step prepares each dataset for analysis.

Typical cleaning tasks include:

1. Standardizing column names
2. Removing extra spaces
3. Converting dates into a consistent format
4. Creating month labels
5. Creating academic-year labels
6. Filling missing numeric values with zero where appropriate
7. Grouping detailed categories into broader reporting categories

Example:

```python
from src.plm_cleaning import load_data, clean_column_names, add_date_fields

raw = load_data("data/sample_program_activity.csv")
clean = clean_column_names(raw)
clean = add_date_fields(clean, date_column="date")
```

---

## 4. Metric Calculation

After cleaning, the metric functions summarize the data.

Common summaries include:

- Monthly totals
- Academic-year totals
- Category counts
- Average attendance per event
- Rate calculations
- Year-over-year comparisons

Example:

```python
from src.plm_metrics import monthly_totals, academic_year_totals

monthly = monthly_totals(clean, value_column="participant_count")
yearly = academic_year_totals(clean, value_column="participant_count")
```

---

## 5. Visualization

The visualization functions are intentionally simple. They create charts that are easy to explain and easy to reuse in notebooks or reports.

Common visuals include:

- Monthly bar charts
- Grouped bar charts
- Horizontal category charts
- Line charts
- Pie charts
- Rate comparison charts

Example:

```python
from src.plm_visuals import plot_monthly_bar

plot_monthly_bar(monthly, value_column="participant_count", title="Monthly Participant Activity")
```

---

## 6. Reporting Outputs

The final outputs can be used in notebooks, Markdown reports, slides, or dashboards.

Suggested output folders:

```text
outputs/
├── charts/
└── tables/
```

Example outputs:

| Output | Purpose |
|---|---|
| Monthly trend chart | Shows activity over time |
| Academic-year summary table | Supports year-over-year comparison |
| Category breakdown chart | Shows composition of activity |
| KPI summary table | Gives leadership a quick overview |

---

## 7. Folder Structure

Recommended public repo structure:

```text
PLM_Analytics/
├── notebooks/
│   ├── 01_program_activity_metrics.ipynb
│   ├── 02_partner_engagement_metrics.ipynb
│   └── 03_platform_activity_and_outcomes.ipynb
├── src/
│   ├── plm_config.py
│   ├── plm_cleaning.py
│   ├── plm_metrics.py
│   └── plm_visuals.py
├── docs/
│   ├── metric_dictionary.md
│   ├── data_pipeline_overview.md
│   └── privacy_notes.md
├── reports/
│   └── report_template_anonymized.md
├── data/
│   └── README.md
└── outputs/
    ├── charts/
    └── tables/
```

---

## 8. Design Choices

This project keeps the code simple on purpose.

The helper files are split by task:

| File | Role |
|---|---|
| `plm_config.py` | Shared settings like month order and generic labels |
| `plm_cleaning.py` | Basic data preparation |
| `plm_metrics.py` | Summary tables and KPI calculations |
| `plm_visuals.py` | Reusable chart functions |

This structure makes the project easier to explain, maintain, and adapt.

---

## 9. Limitations

- The public version uses synthetic or sample data.
- It does not reproduce private workplace results.
- The pipeline is descriptive, not causal.
- Some metrics require clear source definitions before being used in real reporting.
- If source files change format, cleaning functions may need to be adjusted.
