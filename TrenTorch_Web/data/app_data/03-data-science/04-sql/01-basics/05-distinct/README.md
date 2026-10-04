---
name: db-sql-distinct
title: 'DISTINCT Deduplication'
tags: [db]
difficulty: Beginner
---

## Statement

Your analytics dashboard reports how many different email domains are represented in your user base. You need to extract just the email column and remove duplicates so you can count unique domains.

Write a query that returns the `email` column from the `users` table, removing duplicate email values so each email appears exactly once.

### Constraints

- Return only the email column
- Remove duplicates (each email appears once)

### Hints

<details>
<summary>Hint 1</summary>

The DISTINCT keyword removes duplicate rows from the result.

</details>

<details>
<summary>Hint 2</summary>

SELECT DISTINCT applies to all selected columns.

</details>

## Theory

### DISTINCT removes duplicate rows

When you SELECT email FROM users, you get one row per user. DISTINCT eliminates duplicates so each unique value appears exactly once.

### Why DISTINCT matters

- Analytics: "How many unique customers?" instead of total orders
- Data quality: Find all values a column takes
- Reporting: Remove accidental duplicates for cleaner dashboards
- Exploration: Understand the range of values in a dataset

### Performance warning

DISTINCT can be slow on large datasets because the database must compare every row to find uniqueness. Use it carefully in production on millions of rows.

## Explanation

The solution is SELECT DISTINCT email FROM users;. The database returns only one copy of each unique email value. Tests verify that the result contains exactly the unique email addresses with no repeats.
