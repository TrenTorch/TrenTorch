---
name: db-sql-lead
title: 'LEAD: Access Next Row'
tags: [db]
difficulty: Advanced
---

## Statement

Predict retention: for each user event, show the current event and the next event (if any). Use LEAD() to look ahead.

## Theory

### LEAD accesses the next row's value

LEAD(column, offset, default) is the forward-looking counterpart to LAG:

SELECT user_id, event, LEAD(event) OVER (PARTITION BY user_id ORDER BY date) as next_event FROM events;

For each event, LEAD returns the next event for that user. If no next event exists, it returns NULL.

### LAG vs LEAD

- LAG: look backward (previous row)
- LEAD: look forward (next row)

Both are essential for time-series, event sequencing, and change analysis.

### Practical use cases

- Retention analysis: does user return after first purchase?
- Event sequencing: what event follows a login?
- Churn prediction: gap between events predicts churn
- Funnel analysis: which users progress to the next step?

### Combined LAG and LEAD

Using both together enables before-after comparisons in a single query.

## Explanation

The solution uses LEAD(event) OVER (PARTITION BY user_id ORDER BY date) to show each event alongside the next event for that user, enabling churn and retention analysis.
