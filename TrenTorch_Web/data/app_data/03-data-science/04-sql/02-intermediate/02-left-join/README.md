---
name: db-sql-left-join
title: 'LEFT JOIN Preserving Left Table'
tags: [db]
difficulty: Intermediate
---

## Statement

The analytics page lists every user with the number of orders they have placed. Users who have never ordered must still appear, with a count of 0.

Write a query returning `users.id`, `users.name` and the number of their orders as `order_count`, using a `LEFT JOIN` and `GROUP BY`.

### Constraints

- Columns, in order: `id`, `name`, `order_count`
- Include users with no orders (count 0)
- One row per user

### Hints

<details>
<summary>Hint 1</summary>

`LEFT JOIN` keeps every row of the left table even without a match.

</details>

<details>
<summary>Hint 2</summary>

Count a column of the _orders_ table: `COUNT(*)` would count the NULL-filled row as 1.

</details>

## Theory

### The simple version

A left join keeps every row of the first table. When there is no partner, the other table's columns are filled with NULL.

### Keeping unmatched rows

```sql
SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```

A `LEFT JOIN` returns every row from the left table. When there is no match on the right, the right-hand columns are filled with `NULL`.

### Counting through a LEFT JOIN

For a user with no orders the join produces one row where `o.id` is `NULL`.

- `COUNT(*)` counts that row, so it returns 1 (wrong).
- `COUNT(o.id)` skips NULLs, so it returns 0 (right).

This is the single most common mistake with left joins.

### Finding the unmatched

A left join plus `WHERE o.id IS NULL` returns exactly the users with no orders (an _anti-join_).

### Filters in ON vs WHERE

A condition on the right table placed in `WHERE` removes the NULL-filled rows and silently turns the left join into an inner join. Put such conditions in the `ON` clause.

## Explanation

`LEFT JOIN` keeps Cara (no orders) with `NULL` order columns, and `COUNT(o.id)` turns that into 0. The orphan order (user 99) is ignored because no user matches it. Using `COUNT(*)` gives Cara a count of 1 and fails.
