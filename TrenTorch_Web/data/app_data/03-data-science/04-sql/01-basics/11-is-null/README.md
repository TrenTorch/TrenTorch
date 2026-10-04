---
name: db-sql-is-null
title: 'IS NULL Checking'
tags: [db]
difficulty: Beginner
---

## Statement

Your data quality audit needs to find incomplete user records. Some users have missing email addresses (NULL values). Find all users without a recorded email.

Write a query returning all columns from `users` where `email` IS NULL.

### Constraints

- Return all columns
- Only rows where email is NULL

### Hints

<details>
<summary>Hint 1</summary>

Use IS NULL to check for missing values (not = NULL, which doesn't work).

</details>

<details>
<summary>Hint 2</summary>

NULL is not "empty string" or 0; it means "value missing" or "unknown."

</details>

## Theory

### NULL is special in SQL

NULL means "missing value" or "unknown." You cannot compare NULL with = because NULL = NULL evaluates to NULL, not TRUE.

### IS NULL and IS NOT NULL

- IS NULL: value is missing
- IS NOT NULL: value is present

### NULL in aggregation

COUNT(*) counts all rows; COUNT(email) counts only rows where email is NOT NULL.

### Why NULL matters

- Data quality: Find incomplete records
- Reporting: Distinguish "not applicable" from "not provided"
- Queries: Avoid unexpected NULL propagation

## Explanation

The solution is SELECT * FROM users WHERE email IS NULL;. The database returns only rows where the email column contains NULL (missing value).
