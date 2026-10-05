---
name: db-sql-avg
title: 'AVG Averaging'
tags: [db]
difficulty: Beginner
---

## Statement

The reporting screen shows the average age of your users. Calculate it in SQL. One user has no recorded age; that user should not drag the average down.

Write a query that returns a single value: the average of the `age` column of `users`.

### Constraints

- Return a single row with a single column
- Users whose age is NULL are ignored (AVG does this for you)

### Hints

<details>
<summary>Hint 1</summary>

`AVG(column)` averages a numeric column.

</details>

<details>
<summary>Hint 2</summary>

You do not need `WHERE age IS NOT NULL`; aggregates skip NULLs already.

</details>

## Theory

### The simple version

`AVG` adds up the known values and divides by how many there were. Missing (NULL) values are left out.

### Averages in SQL

```sql
SELECT AVG(age) FROM users;
```

`AVG` adds up the non-NULL values and divides by how many there were. The result is a floating-point number, even when the inputs are integers.

### NULLs are skipped, not counted as zero

With ages `20, 30, 40, NULL, 50` the average is `(20+30+40+50)/4 = 35.0`, not `140/5 = 28.0`. That is usually what you want, but it is worth knowing: `NULL` means "unknown", so it is left out instead of being treated as 0.

### Related aggregates

`SUM`, `MIN`, `MAX` and `COUNT` follow the same NULL rule. To rename the output column use an alias: `SELECT AVG(age) AS avg_age FROM users;`.

### Rounding

If you want fewer decimals use `ROUND(AVG(age), 1)`. Avoid rounding too early when the value feeds another calculation.

## Explanation

`AVG(age)` averages the non-NULL ages (20, 30, 40, 50) and returns 35.0. If you divide `SUM(age)` by `COUNT(*)` you get 28.0, which the test rejects. A second dataset changes the average, so the query must compute it.
