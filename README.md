# Manufacturing Workforce Decision Support System (Prototype)

## What this project is

This repository contains a **decision-support prototype** built from manufacturing job postings I assembled together that were associated with CSU partner employers and the Handshake platform. The goal of the project is simple:

> **Help a university system understand where its current employer partnerships create real opportunities for undergraduates, and where targeted effort could improve alignment.**

This is not a production system or a predictive model. I built this project to simulate and learn from what it might look like to approach a real workforce planning problem using limited but realistic data.

---

## Why I made this project

During work on a statewide workforce development grant, I was asked to collect manufacturing job postings from companies already engaged with CSU. While the data showed what jobs existed, it didn’t clearly answer questions like:

* Are these jobs actually accessible to undergraduates?
* Is hiring demand concentrated among certain employers?
* Where are the biggest gaps in the undergraduate pipeline?
* What kinds of investments might realistically help?

Because I’m interested in operations, strategy, and applied data science, I used this opportunity to turn a raw list of job postings into something that could support decision-making, not just describe the data.

---

## Main question

> **Given the manufacturing companies CSU already works with, where would investing effort help students the most?**

Supporting questions:

* Which employers dominate hiring demand?
* What types of roles are most common?
* How many postings are realistically accessible to undergraduates?
* Where do gaps exist between demand and CSU’s ability to place students?

---

## What data is used

The dataset consists of manufacturing-related job postings collected from:

* Employer career websites
* Student-facing platforms (e.g., Handshake)

I manually reviewed each posting and organized the information into a structured format suitable for data analysis.

**Raw fields include:**

* Employer name
* Job title
* Posting platform
* Optional salary information

The dataset consists of manufacturing job postings assembled during workforce development work with Career Services. 
All job postings were sourced from publicly accessible employer career pages and student-facing platforms and compiled into a structured format for analysis.

---

## What the project adds to the data

Raw job postings alone are not enough to answer pipeline-related questions. This project adds structure by creating a few interpretable features:

* **Role family** – broad grouping of job types (e.g., engineering, manufacturing operations)
* **Pipeline level** – internship, entry-level, or experienced
* **Accessibility score** – a simple numeric estimate of how suitable a role is for undergraduates

These features are based on explicit rules and assumptions.

---

## How the analysis is organized

The project is split into four stages, with each stage answering a different kind of question.

### 1. Descriptive (Business Intelligence)

**Question:** What does manufacturing demand look like?

* Counts by employer
* Counts by role type
* Distribution by platform

---

### 2. Diagnostic (Data Analysis)

**Question:** Why does the data look this way?

* Employer concentration
* Fragmentation of job titles
* Share of postings accessible to undergraduates

---

### 3. Decision Support (Applied Data Science)

**Question:** What would help the most?

* Compare accessible demand to CSU placement capacity
* Test simple “what if” scenarios
* Identify high-impact focus areas

Scenarios are illustrative and assumption-driven, not predictions.

---

## Methods (plain language)

* Clean and standardize job posting data
* Apply rule-based interpretations to job titles
* Convert qualitative judgments into simple numeric signals
* Compare outcomes across scenarios

The emphasis is on **clarity and interpretability.**

---

## What this project does *not* claim

* It does not model the entire manufacturing labor market
* It does not predict future job growth
* It does not estimate causal effects

Results should be interpreted as reasoning tools, not final answers.

---

## Why this matters

Even with limited data, institutions often need to make decisions about:

* where to invest partnership effort
* which employers to prioritize
* how to align student pipelines with real opportunities

I made this project to demonstrate how even a small, realistic dataset can be used to support funding and workforce strategy discussions in a structured and transparent way.

---

## Repository structure

```
manufacturing-workforce-decision-support/
├── data/                 # Raw, processed, and sample datasets
├── notebooks/            # Step-by-step analysis and modeling
├── src/                  # Optional reusable logic (scaffolded)
├── outputs/              # Generated figures and tables (may be empty)
└── README.md
```

---

## Author

**McAelan Remigio**
Statistics & Data Science, San Diego State University

---

## License

The MIT License applies to the code and analysis in this repository. 
Job posting content remains the property of the original employers.

Shared for educational and portfolio purposes only.
