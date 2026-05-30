# Privacy Notes

This document explains how the public version of the Program Lifecycle Management analytics project protects confidential workplace information.

---

## 1. Public Version Scope

This repository is an anonymized portfolio reconstruction. It is intended to show the structure, logic, and reporting approach of an analytics workflow without exposing private data or internal materials.

The public version may include:

- Generic helper code
- Synthetic or sample data
- Anonymized report templates
- Generic metric definitions
- Generalized documentation

The public version does not include:

- Raw workplace data
- Internal exports
- Private dashboards
- Original confidential reports
- Institution-specific branding
- Personally identifiable information
- Internal system paths or credentials

---

## 2. Removed or Generalized Information

The following items should be removed or replaced before publishing:

| Original Type | Public Replacement |
|---|---|
| Organization name | `Organization`, `Program Office`, or `Service Unit` |
| Department or office name | `Program Area` or `Student Services Unit` |
| Platform names | `Engagement Platform` or `Operational Platform` |
| Student names or IDs | Synthetic IDs or omitted entirely |
| Employer or partner names | `Partner A`, `Partner B`, or grouped categories |
| Staff names | Generic roles, such as `analyst` or `program lead` |
| Internal file paths | Relative paths like `data/sample_file.csv` |
| Real counts or rates | Synthetic values or placeholders |
| Original charts | Recreated charts using synthetic data |

---

## 3. Data Handling Rules

Before adding files to the public repository, check that they follow these rules:

1. No raw workplace data is included.
2. No personally identifiable information is included.
3. No internal-only report, memo, or presentation is included.
4. No screenshots of private dashboards or systems are included.
5. No file path reveals a workplace drive, username, or internal folder.
6. No chart or table displays confidential actual figures.
7. No API keys, credentials, or tokens are included.
8. No small-cell data could identify a person or organization.

---

## 4. Synthetic Data Guidance

Use synthetic data when demonstrating the pipeline.

Synthetic data should:

- Match the structure of the original workflow
- Use fake names and categories
- Use generated counts and rates
- Preserve realistic date ranges and column types
- Avoid copying exact totals from private reports

Synthetic data should not:

- Reproduce exact private counts
- Use real participant, employer, or staff names
- Include real IDs from source systems
- Include confidential program labels

---

## 5. Final Note

The purpose of this repository is to show analytical thinking, workflow design, and reusable reporting logic. It should not expose confidential workplace information or imply that private data is publicly available.
