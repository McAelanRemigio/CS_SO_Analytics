# Data Dictionary

This document describes the schema for the manufacturing job posting dataset used in the *Manufacturing Workforce Decision Support System (Prototype)* project.

The original dataset is stored in an Excel workbook and treated as **immutable source data**. All cleaning, standardization, and feature engineering steps are performed programmatically downstream. This data dictionary reflects the **raw schema** prior to any derived features.

---

## Raw Variables

### `employer_name`

* **Description:** Name of the employer associated with the job posting.
* **Type:** String
* **Notes:** Used to analyze employer demand concentration and to group postings by organization.

---

### `job_title`

* **Description:** Job title as listed in the original posting.
* **Type:** String
* **Notes:** Serves as the primary input for role family classification, pipeline level inference, and accessibility scoring.

---

### `salary_raw`

* **Description:** Salary value as provided or calculated from the job posting.
* **Type:** Numeric (currency, double)
* **Notes:** Included for completeness and reference only. Not used in analytical or modeling components of this project.

---

### `salary_min`

* **Description:** Lower bound of the salary range if provided; if a fixed salary is listed, this value equals the fixed amount.
* **Type:** Numeric (currency, double)
* **Notes:** Not used in modeling due to inconsistent availability across postings.

---

### `salary_max`

* **Description:** Upper bound of the salary range if provided.
* **Type:** Numeric (currency, double)
* **Notes:** Primarily relevant when salary ranges are provided; excluded from core analysis.

---

### `platform`

* **Description:** Source platform where the job posting was found (e.g., Handshake, employer career website).
* **Type:** String
* **Notes:** Used to compare student-facing platforms versus external hiring channels.

---

### `position_link`

* **Description:** Direct link to the job posting, if available.
* **Type:** String (URL)
* **Notes:** Retained for traceability and verification; not used in analysis.

---

### `career_website`

* **Description:** Link to the employer's general careers website.
* **Type:** String (URL)
* **Notes:** Informational only.

---

## Derived Variables (Created Downstream)

The following variables are **not present** in the raw dataset and are generated during feature engineering:

* `role_family`
* `pipeline_level`
* `accessibility_score`
* `employer_concentration_score`

Definitions and assumptions for derived variables are documented in the modeling notebooks.

---

## Data Usage Notes

* The dataset represents a snapshot of manufacturing job postings collected for workforce development analysis.
* Salary information is incomplete and excluded from decision modeling.
* Job titles are used as proxies for role and pipeline inference.
* Results should be interpreted as illustrative rather than exhaustive.

---

## Versioning

* Raw schema reflects the original Excel file used during grant-related work.
* No manual edits are made to the source file.
* All transformations are reproducible via code in this reposit
