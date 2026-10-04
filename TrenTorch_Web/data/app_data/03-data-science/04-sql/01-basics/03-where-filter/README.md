---
name: db-sql-where-filter
title: 'WHERE Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

Your user management dashboard needs to show only adult users (age 18 or older) for compliance reasons. The full users table contains people of all ages.

Write a query that returns all columns from the `users` table, but only for rows where `age` is greater than or equal to 18.

### Constraints

- Return all columns (id, name, email, age)
- Only rows where age >= 18
- No sorting required

### Hints

<details>
<summary>Hint 1</summary>

The `WHERE` clause filters rows based on a condition.

</details>

<details>
<summary>Hint 2</summary>

Use `>=` for 'greater than or equal to'.

</details>

## Theory

### The WHERE clause filters rows

While `FROM` chooses the table and `SELECT` chooses the columns, `WHERE` chooses the rows:

```sql
SELECT * FROM users WHERE age >= 18;
```

This reads as: start with all rows from `users`, then keep only those where the condition `age >= 18` is true.

### WHERE in the pipeline

The conceptual order is: FROM (get all data) → WHERE (filter rows) → SELECT (pick columns). The database optimizes the actual execution order.

### Comparison operators

- `=` — equal
- `>=` — greater than or equal
- `>` — greater than
- `<=` — less than or equal
- `<` — less than
- `<>` or `!=` — not equal

### Why filtering matters

In production databases with millions of rows, filtering is essential. Without WHERE, you'd send massive amounts of unused data. With WHERE, you only retrieve what you use. The database can also optimize by using indexes on filtered columns to skip irrelevant data.

## Explanation

The solution adds a WHERE clause: `SELECT * FROM users WHERE age >= 18;`. The database evaluates the condition for each row and returns only those that match. Tests verify that matching rows are returned and non-matching rows are excluded.
