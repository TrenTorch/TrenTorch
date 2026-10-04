---
name: db-sql-perf-histogram-stats
title: 'Value Distributions (Histograms)'
tags: [db]
difficulty: Advanced
---

## Statement

Real data is rarely uniform. In the `orders` table most orders are `paid`, and only a few are `returned`. A query planner needs to know this _distribution_ (a histogram of values) to judge how selective a filter is: `status = 'returned'` matches few rows, `status = 'paid'` matches most.

Write a query returning, for every `status`, the number of orders as `row_count` and the share of all orders as `pct` (a percentage rounded to 1 decimal place). Order by `row_count` descending, then by `status`.

### Constraints

- Columns, in order: `status`, `row_count`, `pct`
- `pct` = 100 × row_count ÷ total orders, rounded to 1 decimal
- Order by `row_count` descending, then `status`

### Hints

<details>
<summary>Hint 1</summary>

Group by `status` and divide each count by `(SELECT COUNT(*) FROM orders)`.

</details>

<details>
<summary>Hint 2</summary>

Use `100.0 *` (not `100 *`) so the division is not an integer division.

</details>

## Theory

### The simple version

A histogram counts how often each value occurs. Knowing that most orders are `paid` tells the database that filtering on `paid` keeps most of the table.

### A histogram with GROUP BY

```sql
SELECT status,
       COUNT(*) AS row_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1) AS pct
FROM orders
GROUP BY status
ORDER BY row_count DESC, status;
```

This is the simplest histogram: one bucket per distinct value with its frequency. For numeric columns you bucket values first, for example `(price / 100) * 100` for buckets of 100.

### Why skew matters

| Filter                | Matches | Best plan                                |
| --------------------- | ------- | ---------------------------------------- |
| `status = 'returned'` | ~10%    | an index may pay off                     |
| `status = 'paid'`     | ~60%    | scan the table; an index would be slower |

The same query text needs different plans depending on the value. Databases such as PostgreSQL store a histogram per column and use it to choose; SQLite keeps average rows per key (`sqlite_stat1`) and optionally more detail (`sqlite_stat4`).

### Integer division trap

`100 * COUNT(*) / total` with integers truncates the result. Writing `100.0` makes the whole expression floating-point.

## Explanation

Grouping by status gives paid 60.0%, shipped 20.0%, then `new` and `returned` at 10.0% each (ties broken by name). The percentage must be computed from the total with a decimal literal: integer division would return 0 for the small groups.
