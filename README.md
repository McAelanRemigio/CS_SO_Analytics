# Manufacturing Workforce Decision Support System (Prototype)

## Overview

This repository presents a prototype **workforce decision support system** designed to help institutional leaders evaluate how well current manufacturing labor demand aligns with the undergraduate talent pipeline. The project demonstrates how job posting data can be transformed into structured insights and decision-oriented models to support workforce development strategy, particularly in the context of higher education and public-sector investment.

The work was motivated by participation in a statewide workforce development grant proposal and is intended as a **proof of concept** rather than a production system.

---

## Decision Context

Universities and public institutions face a constrained resource allocation problem:

> *Where should limited workforce development investments be directed to maximize alignment with regional labor market demand?*

This project frames manufacturing hiring demand as a decision problem rather than a purely descriptive exercise. Instead of asking only *what jobs exist*, the analysis focuses on:

* Which roles are realistically accessible to undergraduate students
* Where demand is concentrated across employers and role families
* Where mismatches exist between labor demand and educational pipelines
* Which interventions are likely to produce the highest marginal impact

---

## Core Question

**Primary question:**

> Where should a university system invest workforce development resources to best align undergraduate manufacturing pipelines with employer demand?

**Supporting questions:**

* Which employers account for the majority of manufacturing hiring demand?
* What role families dominate current postings?
* What proportion of roles are accessible at the internship or entry level?
* Where do the largest pipeline gaps exist?

---

## Dataset Description

The dataset consists of manufacturing-related job postings collected from employer career pages and student-facing hiring platforms (e.g., Handshake). Each posting was manually reviewed and structured into a tabular format.

### Key raw fields include:

* Employer name
* Job title
* Posting platform
* Sector classification (manufacturing)

To ensure ethical and professional use, this repository includes only **sample or de-identified data**. The full raw dataset used during the grant work is not publicly shared.

---

## Feature Engineering & Abstractions

Rather than relying solely on raw job titles, the project introduces several **designed features** to support analysis:

* **Role family** (e.g., engineering, manufacturing operations, quality, supply chain)
* **Pipeline level** (internship, entry-level, experienced)
* **Accessibility score** (heuristic measure of undergraduate suitability)
* **Employer concentration indicators**

These abstractions reflect deliberate modeling choices and are documented in the data dictionary.

---

## Analytical Layers

This project is intentionally structured into three analytical layers:

### 1. Business Intelligence (Descriptive)

* Job counts by employer
* Job counts by role family
* Distribution of postings by platform

**Purpose:** Establish baseline visibility into manufacturing demand.

---

### 2. Data Analysis (Diagnostic)

* Employer demand concentration
* Role fragmentation across titles
* Internship vs. full-time balance
* Undergraduate accessibility patterns

**Purpose:** Explain why demand appears as it does and identify structural patterns.

---

### 3. Data Science (Decision Support)

The data science layer models **pipeline gaps** between labor demand and undergraduate supply.

Key components:

* Formal assumptions about undergraduate workforce capacity
* Gap estimation by role family and employer concentration
* Scenario analysis simulating alternative investment strategies

Example scenarios include:

* Increasing internship availability
* Targeting top-demand employers
* Prioritizing specific role families

**Purpose:** Support resource allocation decisions under uncertainty.

---

## Methods

* Manual data curation and cleaning
* Rule-based feature engineering
* Heuristic scoring models
* Scenario-based simulation (non-predictive)

No machine learning models are used in this prototype; emphasis is placed on interpretability and decision relevance.

---

## Limitations

* Job postings represent a snapshot in time and may not reflect long-term demand
* Skill requirements are inferred from job titles rather than full descriptions
* Accessibility scores rely on modeling assumptions
* Results are illustrative rather than definitive

These limitations are explicitly acknowledged to avoid overinterpretation.

---

## Implications for Workforce Strategy

While exploratory, this prototype demonstrates how even modest job posting data can be transformed into actionable insights when paired with careful problem framing and modeling. The approach is applicable to:

* Workforce development planning
* University–industry partnership design
* Grant-supported pipeline initiatives

---

## Repository Structure

```
manufacturing-workforce-decision-support/
├── data/
│   ├── sample_job_postings.csv
│   ├── data_dictionary.md
├── notebooks/
│   ├── 01_data_import_and_cleaning.ipynb
│   ├── 02_bi_descriptive_metrics.ipynb
│   ├── 03_role_and_pipeline_modeling.ipynb
│   ├── 04_scenario_analysis.ipynb
├── src/
│   ├── clean_data.py
│   ├── feature_engineering.py
│   ├── pipeline_model.py
├── outputs/
│   ├── figures/
│   ├── summary_tables/
└── README.md
```

---

## Author

McAelan Remigio

Statistics & Data Science, San Diego State University

---

## License

This project is shared for educational and portfolio purposes only.
