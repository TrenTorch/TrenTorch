---
name: db-sql-count
title: 'COUNT Aggregation'
tags: [db]
difficulty: Beginner
---

## Statement

Your dashboard needs to display the total number of users in the system. Compute this directly in SQL instead of fetching all rows to your application.

Write a query that returns the total number of rows in the `users` table.

### Constraints

- Return a single number: the count of all rows
- Count every row (no filtering)

### Hints

<details>
<summary>Hint 1</summary>

The COUNT function returns the number of rows that match a condition.

</details>

<details>
<summary>Hint 2</summary>

COUNT(*) counts all rows, including those with NULL values.

</details>

## Theory

### COUNT aggregates rows into a single value

While SELECT * returns one row per stored row, aggregation functions like COUNT combine multiple rows into a single result.

### COUNT(*) vs COUNT(column)

- COUNT(*): count all rows
- COUNT(email): count rows where email is NOT NULL

### Why COUNT matters

- Dashboards: "How many users do we have?"
- Data quality: "How many rows have missing emails?"
- Business metrics: "Total orders this month?"
- Monitoring: Track table growth over time

## Explanation

The solution is SELECT COUNT(*) FROM users;. The database scans the entire table, counts every row, and returns a single number.
