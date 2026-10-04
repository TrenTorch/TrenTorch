---
name: db-sql-lag
title: 'LAG: Access Previous Row'
tags: [db]
difficulty: Advanced
---

## Statement

Analyze user age changes: for each user, show their current age and previous recorded age. Use LAG() to access the previous row's value.

## Theory

### LAG accesses the previous row's value

LAG(column, offset, default) accesses values from previous rows:

SELECT user_id, age, LAG(age) OVER (PARTITION BY user_id ORDER BY date) as prev_age FROM age_history;

For each user's age record (ordered by date), LAG returns the previous age. If no previous record exists, it returns NULL (or a default value).

### LAG parameters

- column: the column to retrieve from the previous row
- offset: how many rows back (default 1)
- default: value if no previous row exists (default NULL)

### Practical use cases

- Change detection: compare current to previous value
- Growth calculation: (current - previous) / previous
- Time-series analysis: lag between events
- Session detection: split data where lag exceeds threshold

### PARTITION BY and ORDER BY

LAG respects PARTITION BY (compute within groups) and ORDER BY (determine row sequence).

## Explanation

The solution uses LAG(age) OVER (PARTITION BY user_id ORDER BY date) to retrieve each age record alongside the previous record for the same user, enabling change detection.
