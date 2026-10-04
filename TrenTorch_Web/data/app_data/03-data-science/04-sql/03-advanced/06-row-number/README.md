---
name: db-sql-row-number
title: 'ROW_NUMBER: Unique Sequential Numbering'
tags: [db]
difficulty: Advanced
---

## Statement

To paginate a list ("page 1 is rows 1-10") you need a stable, unique position for every row. Users must be numbered by age, youngest first, and when two users have the same age the one with the smaller `id` comes first, so the numbering never changes between runs.

Write a query returning `name`, `age` and the position as `row_num` using `ROW_NUMBER()`.

### Constraints

- Columns, in order: `name`, `age`, `row_num`
- `row_num` goes 1, 2, 3, ... with no repeats
- Order by `age` ascending, ties by `id` ascending

### Hints

<details>
<summary>Hint 1</summary>

`ROW_NUMBER() OVER (ORDER BY ...)` numbers rows in the given order.

</details>

<details>
<summary>Hint 2</summary>

Add `id` as a second sort key to make ties deterministic.

</details>

## Theory

### The simple version

`ROW_NUMBER()` hands out 1, 2, 3, ... to rows in a chosen order. Nobody shares a number.

### Numbering rows

```sql
SELECT name, age,
       ROW_NUMBER() OVER (ORDER BY age, id) AS row_num
FROM users;
```

`ROW_NUMBER()` assigns 1, 2, 3, ... following the window's `ORDER BY`. Unlike `RANK`, it never repeats a number, even for ties.

### The tie-breaker matters

If two rows tie on the sort key, the database may number them in either order, and different runs can disagree. Adding a unique column such as `id` makes the numbering deterministic.

### Typical uses

- **Pagination:** `WHERE row_num BETWEEN 11 AND 20` (apply it in an outer query).
- **De-duplication:** keep `row_num = 1` within each `PARTITION BY` group to choose one row per key (for example the latest).
- **Top-N per group:** partition by the group, order by the metric, keep `row_num <= N`.

### Filtering

Window functions cannot appear in `WHERE`; put the query in a CTE and filter in the outer `SELECT`.

## Explanation

Sorting by `(age, id)` gives Diana 1, Bob 2, Alice 3, Charlie 4, Eve 5. Alice and Charlie share age 30, so the `id` tie-breaker decides: Alice first. The hidden data adds another 22-year-old to check the tie-break again.
