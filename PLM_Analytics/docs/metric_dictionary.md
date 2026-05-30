#  Metric Dictionary

This document defines the generic metrics used in the anonymized Program Lifecycle Management analytics workflow.

The terms below are intentionally broad so the project can be applied to different organizations, programs, or service units without exposing workplace-specific language.

---

## 1. Time Fields

| Metric / Field | Definition | Example Use |
|---|---|---|
| `date` | Original date of the activity, event, or record | Used to create month and academic-year fields |
| `month` | Calendar month extracted from the date | Used for monthly trend charts |
| `month_name` | Month label, such as `July` or `August` | Used for readable charts |
| `academic_year` | Reporting year based on a July-June cycle | Used for year-over-year summaries |

### Academic Year Rule

This project uses a July-June academic year.

Example:

- July 2024 through June 2025 = `2024-2025`
- July 2025 through June 2026 = `2025-2026`

---

## 2. Program Activity Metrics

| Metric | Definition | Formula / Logic |
|---|---|---|
| Service interactions | Count of participant-facing appointments, meetings, or service contacts | Count records or sum an interaction column |
| Participants served | Number of participants who engaged with a service | Count unique participant IDs, if available |
| No-show rate | Share of scheduled interactions that were missed | `no_shows / scheduled_interactions` |
| Event count | Number of workshops, orientations, sessions, or presentations | Count event records |
| Attendance | Number of attendees across program activities | Sum attendance values |
| Average attendance per event | Average reach per event or session | `total_attendance / event_count` |
| Modality count | Count of activities by delivery format | Group by modality, such as in-person or virtual |

### Notes

- Attendance may include duplicated participants if the same person attended multiple events.
- Service interaction counts depend on how the source system defines a completed interaction.
- If two sources contain conflicting counts, the analyst should document which source is used and why.

---

## 3. Partner Engagement Metrics

| Metric | Definition | Formula / Logic |
|---|---|---|
| Partner events | Number of events involving external or internal partners | Count event records where event type is partner-facing |
| Partners engaged | Number of partner attendees, organizations, or contacts | Sum attendance or count unique partner IDs, depending on source |
| Event type count | Number of events by category | Group by event type |
| Partners per event | Average partner attendance per event | `partners_engaged / partner_events` |
| Orientation count | Number of onboarding or orientation sessions | Count orientation records |
| Communication open rate | Share of delivered messages that were opened | `opens / delivered_messages` |
| Communication click rate | Share of delivered or opened messages that received clicks | Usually `clicks / delivered_messages`; document source definition |
| Match rate | Share of participants successfully matched | `matched_participants / total_participants` |

### Notes

- Communication platforms may define open and click rates differently.
- Partner counts may represent individuals, organizations, or contacts depending on the source file.
- Match-rate denominators should be clearly documented.

---

## 4. Platform Activity and Outcome Metrics

| Metric | Definition | Formula / Logic |
|---|---|---|
| Unique logins | Number of distinct users who logged into a platform | Count unique user IDs or use exported system total |
| Profile completions | Number of users who completed a profile | Count completion records or sum exported total |
| Profile completion rate | Share of active users with completed profiles | `profile_completions / active_users` |
| New partners | Number of newly approved organizations or partners | Count new partner records |
| New contacts | Number of newly added contacts | Count new contact records |
| Opportunity postings | Number of posted opportunities | Count posting records |
| Opportunity category count | Number of postings by category | Group by opportunity type |

### Notes

- Platform activity does not always equal meaningful engagement.
- Opportunity postings may include duplicates, reposts, expired listings, or imported records.
- Completion rates require a clear denominator.

---

## 5. Summary and Comparison Metrics

| Metric | Definition | Formula / Logic |
|---|---|---|
| Monthly total | Total count or sum for each month | Group by month and sum value column |
| Academic-year total | Total count or sum for each academic year | Group by academic year and sum value column |
| Monthly average | Average monthly activity within an academic year | `academic_year_total / number_of_months_reported` |
| Year-over-year change | Difference between two academic years | `current_year_value - prior_year_value` |
| Year-over-year percent change | Relative change between two academic years | `(current - prior) / prior` |
| Category share | Percent of total represented by a category | `category_count / total_count` |
| Rate | Percent of eligible records meeting a condition | `numerator / denominator` |

---

## 6. Suggested Column Names for Public Demo Data

These names are generic and safe for public use.

| Column | Description |
|---|---|
| `date` | Activity or event date |
| `academic_year` | Academic-year label |
| `month_name` | Month name |
| `program_area` | Broad reporting area |
| `activity_type` | Type of activity or event |
| `category` | Grouped category for charts |
| `modality` | Delivery format |
| `participant_count` | Number of participants |
| `partner_count` | Number of partners or contacts |
| `event_count` | Number of events |
| `value` | Generic numeric value used for summaries |
| `status` | Outcome or match status |

---

## 7. Interpretation Guidelines

- Use descriptive language unless the analysis supports stronger conclusions.
- Clearly define denominators for all rates.
- Avoid comparing periods with incomplete data unless marked as partial.
- Document any manual reconciliation decisions.
- Treat synthetic data as demonstration data only.
