---
name: db-sql-count
title: 'COUNT Aggregation'
tags: [db]
difficulty: Beginner
---

## Statement

The dashboard header shows "N users". Compute N in SQL instead of downloading every row and counting in application code. Some users have not given an email address yet, and they still count as users.

Write a query that returns a single number: how many rows `users` has.

### Constraints

- Return a single row with a single column
- Count every row, including users whose `email` is NULL

### Hints

<details>
<summary>Hint 1</summary>

`COUNT(*)` counts rows.

</details>

<details>
<summary>Hint 2</summary>

`COUNT(column)` skips rows where that column is NULL, which would undercount here.

</details>

## Theory

### The simple version

`COUNT(*)` turns many rows into one number: how many rows there are.

### Counting rows

```sql
SELECT COUNT(*) FROM users;
```

`COUNT(*)` returns the number of rows. An _aggregate function_ like this collapses many rows into one.

### COUNT(*) vs COUNT(column)

| Expression              | Counts                             |
| ----------------------- | ---------------------------------- |
| `COUNT(*)`              | every row                          |
| `COUNT(email)`          | rows where `email` is **not** NULL |
| `COUNT(DISTINCT email)` | distinct non-NULL emails           |

Mixing these up is one of the most common silent SQL bugs: the query runs, returns a number, and the number is wrong.

### Aggregates without GROUP BY

A query that uses an aggregate and no `GROUP BY` treats the whole table (after `WHERE`) as one group, so you always get exactly one row, even for an empty table (where `COUNT(*)` is `0`).

## Explanation

`COUNT(*)` counts rows regardless of NULLs. `COUNT(email)` would return 3 instead of 5 because it skips the two NULL emails, which is exactly the trap this dataset sets. A second dataset with more rows ensures the number is computed and not typed in.
