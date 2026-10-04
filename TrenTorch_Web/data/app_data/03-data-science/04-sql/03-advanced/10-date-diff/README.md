---
name: db-sql-date-diff
title: 'Date Functions: Time Calculations'
tags: [db]
difficulty: Advanced
---

## Statement

Calculate user age from birth_date, days since registration, and time until expiration. Use date functions to compute time spans in years, days, hours.

## Theory

### Date functions compute time spans

SQL provides functions to calculate differences and intervals:

SELECT user_id, birth_date, FLOOR(DATEDIFF(YEAR, birth_date, GETDATE())) as age, DATEDIFF(DAY, created_at, GETDATE()) as days_since_signup FROM users;

DATEDIFF returns the number of time units between two dates.

### Common date functions

- DATEDIFF(unit, start_date, end_date): difference in specified unit
- DATE_ADD / DATE_SUB: add/subtract intervals
- YEAR, MONTH, DAY: extract components
- DATEPART: extract specific parts

### Units for DATEDIFF

- YEAR: years between dates
- MONTH: months
- DAY: days
- HOUR: hours
- MINUTE: minutes
- SECOND: seconds

### Practical use cases

- Age calculation: years since birth_date
- Churn prediction: days since last activity
- SLA tracking: hours until deadline
- Retention: days between registration and first purchase
- Cohort analysis: group users by signup month

## Explanation

The solution uses DATEDIFF to calculate user age (from birth_date to today), days since account creation, and other time-based metrics for analytics and reporting.
