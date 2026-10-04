---
name: db-sql-union
title: 'UNION Combining Queries'
tags: [db]
difficulty: Intermediate
---

## Statement

Active users live in `users`; people who closed their account were moved to `archive_users` (same columns). Cara exists in both tables because she was copied rather than moved.

Write a query returning `id`, `name` and `email` of everyone from either table, with exact duplicate rows listed only once.

### Constraints

- Columns, in order: `id`, `name`, `email`
- Combine both tables into one result
- A row present in both tables appears once

### Hints

<details>
<summary>Hint 1</summary>

`UNION` stacks the results of two `SELECT`s.

</details>

<details>
<summary>Hint 2</summary>

Both `SELECT`s must return the same number of columns, in compatible types.

</details>

## Theory

### The simple version

`UNION` puts the rows of two queries into one list and removes exact duplicates.

### Stacking results

```sql
SELECT id, name, email FROM users
UNION
SELECT id, name, email FROM archive_users;
```

`UNION` appends the second result to the first and **removes duplicate rows**. `UNION ALL` keeps duplicates and is faster because it skips the de-duplication.

### Rules

- Both queries must return the same number of columns.
- Column names come from the **first** query.
- Types should be compatible column by column (SQLite is lenient, other databases are strict).

### UNION vs JOIN

A join places columns of two tables side by side (wider rows). A union places rows of two queries one after the other (more rows).

### Other set operators

`INTERSECT` keeps rows found in both queries and `EXCEPT` keeps rows of the first that are not in the second. All three compare entire rows.

### ORDER BY

An `ORDER BY` at the end applies to the combined result, not to the second query alone.

## Explanation

`UNION` concatenates both tables and removes duplicates, so Cara (present in both with identical values) appears once. Using `UNION ALL` would list her twice and fail the row-count check.
