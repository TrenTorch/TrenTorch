---
name: db-sql-order-by
title: 'ORDER BY Sorting'
tags: [db]
difficulty: Beginner
---

## Statement

Your app shows a leaderboard of users, oldest first. The table stores users in no particular order, so the query has to do the sorting.

Write a query that returns all columns of `users`, sorted by `age` in descending order (highest age first).

### Constraints

- Return all columns
- Sort by `age`, highest first
- The row order is part of the answer

### Hints

<details>
<summary>Hint 1</summary>

`ORDER BY` is the last clause of the query.

</details>

<details>
<summary>Hint 2</summary>

`ASC` is the default direction; you need the opposite.

</details>

## Theory

### The simple version

A table has no natural order. `ORDER BY` is how you ask for one: smallest to largest, or largest to smallest.

### Sorting with ORDER BY

```sql
SELECT * FROM users ORDER BY age DESC;
```

`ORDER BY` sorts the result by one or more expressions. `ASC` (ascending, the default) goes small to large; `DESC` goes large to small.

### No ORDER BY, no guaranteed order

A table is a _set_ of rows. Without `ORDER BY` the database may return rows in whatever order is cheapest, and that order can change after an insert or an index change. If order matters, say so explicitly.

### Tie-breakers

You can sort by several columns: `ORDER BY age DESC, name ASC` sorts by age and, among people of the same age, by name. Adding a unique column last (such as `id`) makes the order fully deterministic, which is important for pagination.

### NULLs

In SQLite, `NULL` sorts as the smallest value: first in `ASC`, last in `DESC`.

## Explanation

`ORDER BY age DESC` sorts largest to smallest. Here the tests compare the rows _in order_, using both the visible data and a second dataset whose largest and smallest ages sit at the ends, so a query that is sorted ascending or not sorted at all fails.
