---
name: db-sql-where-filter
title: 'WHERE Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

For compliance reasons the dashboard may only show adult users (age 18 or older). The `users` table holds people of all ages.

Write a query that returns all columns of `users`, but only the rows where `age` is greater than or equal to 18.

### Constraints

- Return all columns (id, name, email, age)
- Only rows where `age >= 18` (someone who is exactly 18 counts)
- No sorting required

### Hints

<details>
<summary>Hint 1</summary>

`WHERE` goes after `FROM` and holds a condition each row must satisfy.

</details>

<details>
<summary>Hint 2</summary>

Be careful with the boundary: `>` and `>=` treat 18 differently.

</details>

## Theory

### The simple version

`WHERE` is a bouncer for rows: only rows that satisfy the condition get through.

### Filtering rows with WHERE

`WHERE` keeps only the rows for which a condition is true:

```sql
SELECT * FROM users WHERE age >= 18;
```

Comparison operators are `=`, `<>` (or `!=`), `<`, `<=`, `>`, `>=`. Text values go in single quotes (`WHERE name = 'Alice'`); double quotes are for identifiers in standard SQL.

### Where it runs in the pipeline

Logically the database evaluates `FROM` first, then `WHERE` row by row, and only then `SELECT`. That is why you can filter on a column you do not select.

### Boundary conditions

Off-by-one mistakes at the edge of a range are the classic WHERE bug. `age > 18` excludes eighteen-year-olds, `age >= 18` includes them. Always test the exact boundary value, as the tests here do.

### NULL never matches

If `age` is `NULL`, the comparison `age >= 18` is neither true nor false but _unknown_, and `WHERE` only keeps rows where the condition is true. Rows with unknown ages are therefore dropped; the IS NULL question covers how to find them.

## Explanation

`WHERE age >= 18` keeps rows whose age satisfies the comparison. Using `>` would drop the 18-year-old, which the tests catch because both the visible data and the hidden data contain someone who is exactly 18.
