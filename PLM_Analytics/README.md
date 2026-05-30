# Program Lifecycle Management Analytics

This repository is an anonymized portfolio reconstruction of a program lifecycle management analytics workflow.

The original workflow was designed to standardize fragmented operational exports into reusable reporting logic for planning, engagement, internal operations, and program evaluation. Raw workplace data, organization-specific names, internal file paths, and original report outputs are excluded.

## Project Summary

This project demonstrates how fragmented program activity data can be cleaned, standardized, summarized, and converted into leadership-ready reporting outputs.

The public version uses synthetic data and generic labels to show the logic without exposing confidential workplace information.

## Key Goals

- Combine fragmented operational exports into a consistent reporting structure
- Standardize month and academic-year reporting logic
- Define reusable KPI calculations across program areas
- Create monthly trend charts and academic-year summary tables
- Reduce manual reconciliation across inconsistent source files
- Preserve the reporting framework without sharing private data

## Repository Structure

```text
PLM_Analytics/
├── README.md
├── requirements.txt
├── data/
│   └── sample_synthetic_data.csv
├── docs/
│   ├── metric_dictionary.md
│   ├── data_pipeline_overview.md
│   └── privacy_notes.md
├── notebooks/
│   ├── 01_program_activity_metrics.ipynb
│   ├── 02_partner_engagement_metrics.ipynb
│   └── 03_platform_activity_and_outcomes.ipynb
├── reports/
│   └── report_template_anonymized.md
└── src/
    ├── plm_config.py
    ├── plm_cleaning.py
    ├── plm_metrics.py
    └── plm_visuals.py
```

## Notebook Sections

| Notebook | Focus |
|---|---|
| `01_program_activity_metrics.ipynb` | Participant-facing activity, service interactions, outreach sessions, workshops, and program participation |
| `02_partner_engagement_metrics.ipynb` | Partner engagement, communications, events, mentor-style matching, and large-scale engagement activities |
| `03_platform_activity_and_outcomes.ipynb` | Platform usage, profile completion, partner growth, contacts, and opportunity volume |

## Source Files

| File | Purpose |
|---|---|
| `plm_config.py` | Shared settings such as month order and common column names |
| `plm_cleaning.py` | Basic data loading and preparation functions |
| `plm_metrics.py` | Reusable KPI and summary-table calculations |
| `plm_visuals.py` | Simple plotting functions for reports and notebooks |

## Data

The sample dataset in `data/sample_synthetic_data.csv` is fully synthetic. It is included only to demonstrate the structure expected by the notebooks and helper functions.

The original raw data is not included because it was workplace-specific and may contain confidential operational information.

## Example Metrics

The project includes reusable logic for metrics such as:

- Monthly activity volume
- Academic-year totals
- Average activity per month
- Event attendance
- Average attendance per event
- Partner engagement counts
- Platform logins
- Profile completions
- Completion rates
- Opportunity volume
- Year-over-year comparison tables

## How to Run

1. Clone the repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Open the notebooks in Jupyter Lab, Jupyter Notebook, or VS Code.
4. Run the notebooks using the synthetic sample data or replace it with an approved local dataset using the same column structure.

## Privacy Note

This repository does not contain raw workplace data, private reports, internal branding, or organization-specific metrics. The goal is to demonstrate the analytics workflow and reporting logic in a public, reusable format.

## Portfolio Context

This project represents an anonymized version of a larger reporting workflow that involved rebuilding multi-year fragmented operational data into a standardized analytics pipeline. The public version focuses on the technical structure: cleaning, KPI logic, monthly summaries, academic-year comparisons, and reporting documentation.
