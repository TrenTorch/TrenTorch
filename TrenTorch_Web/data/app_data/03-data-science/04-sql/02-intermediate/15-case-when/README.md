---
name: db-sql-case-when
title: 'CASE WHEN'
tags: [db]
difficulty: Intermediate
---

## Statement

The reporting layer groups users into age bands: `minor` (under 18), `adult` (18 to 64) and `senior` (65 and over).

Write a query returning each user's `name` and their band as `age_group`.

### Constraints

- Columns, in order: `name`, `age_group`
- Values are exactly `minor`, `adult`, `senior` (lowercase)
- 17 is a minor, 18 an adult, 64 an adult, 65 a senior

### Hints

<details>
<summary>Hint 1</summary>

`CASE WHEN condition THEN value ... ELSE value END` is SQL's if/else.

</details>

<details>
<summary>Hint 2</summary>

Branches are checked top to bottom; the first true one wins.

</details>

## Theory

### The simple version

`CASE WHEN` is if / else-if / else for SQL: it picks a value depending on conditions.

### Conditional values

```sql
SELECT name,
       CASE
         WHEN age < 18 THEN 'minor'
         WHEN age < 65 THEN 'adult'
         ELSE 'senior'
       END AS age_group
FROM users;
```

`CASE` evaluates the `WHEN` conditions in order and returns the value of the first one that is true; `ELSE` covers everything else.

### Order matters

Because the first match wins, the second branch only needs `age < 65`: anyone younger than 18 was already handled by the first branch. Re-ordering the branches changes the result.

### Missing ELSE

Without `ELSE`, rows that match no branch get `NULL`. That is easy to overlook, so add an `ELSE` unless NULL is what you want.

### Where CASE can be used

Anywhere an expression is allowed: `SELECT`, `WHERE`, `ORDER BY`, and inside aggregates, e.g. `SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END)` for a conditional total.

## Explanation

Branches are evaluated in order: `< 18` gives minor, otherwise `< 65` gives adult, otherwise senior. The data contains 17/18 and 64/65 to test both boundaries.
