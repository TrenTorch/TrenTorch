---
name: db-sql-distinct
title: 'DISTINCT Deduplication'
tags: [db]
difficulty: Beginner
---

## Statement

A signup form has a "city" dropdown that should list every city where at least one of your users lives, with each city appearing only once even if many users share it.

Write a query that returns the distinct values of the `city` column of `users`.

### Constraints

- Return only the `city` column
- Each city appears exactly once
- Row order does not matter

### Hints

<details>
<summary>Hint 1</summary>

`DISTINCT` goes right after `SELECT`.

</details>

<details>
<summary>Hint 2</summary>

Selecting `name` as well would make every row unique again, so select only `city`.

</details>

## Theory

### The simple version

`DISTINCT` removes repeated rows, so a value that appears ten times in the table is listed once.

### Removing duplicates

```sql
SELECT DISTINCT city FROM users;
```

`DISTINCT` removes duplicate rows from the _result_. Two rows are duplicates when every selected column is equal.

### It applies to the whole row

`SELECT DISTINCT city, age` keeps one row per unique _pair_ of city and age, not one per city. If you add a column that differs between rows, the duplicates disappear and `DISTINCT` no longer does what you wanted.

### Cost

To find duplicates the database has to sort or hash the result, which gets expensive on large tables. Use `DISTINCT` when you truly need unique values; do not sprinkle it on a query to hide an accidental join duplication.

### NULL

For `DISTINCT`, all `NULL`s are treated as equal, so they collapse into a single `NULL` row.

## Explanation

`SELECT DISTINCT city FROM users;` returns one row per unique city. Selecting more columns would defeat `DISTINCT`. The tests compare the set of cities on both the visible data and a second dataset, and a result that still contains duplicates has the wrong row count.
