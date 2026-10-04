---
name: db-sql-sum-group
title: 'SUM with GROUP BY'
tags: [db]
difficulty: Intermediate
---

## Statement

The sales dashboard shows revenue per region.

Write a query returning each `region` of `sales` and the sum of its `amount` values, named `total_revenue`.

### Constraints

- Columns, in order: `region`, `total_revenue`
- One row per region

### Hints

<details>
<summary>Hint 1</summary>

`SUM(amount)` adds up numbers; combine it with `GROUP BY region`.

</details>

<details>
<summary>Hint 2</summary>

Give the sum an alias with `AS total_revenue`.

</details>

## Theory

### The simple version

`SUM` adds up a column. With `GROUP BY` you get one total per group.

### SUM per group

```sql
SELECT region, SUM(amount) AS total_revenue
FROM sales
GROUP BY region;
```

`SUM` adds up the non-NULL values in each group. It combines with `GROUP BY` exactly like `COUNT` does.

### Empty and NULL cases

- `SUM` of no rows, or of only NULLs, is `NULL`, not 0. Use `COALESCE(SUM(amount), 0)` when you need a number.
- NULL values are skipped, like in every aggregate.

### Integers vs decimals

`SUM` of integers returns an integer, but for money prefer storing whole cents or using `ROUND(SUM(price), 2)`, because floating-point addition can produce results like `0.30000000000000004`.

### Several aggregates at once

Nothing stops you from computing `SUM(amount)`, `COUNT(*)` and `AVG(amount)` in the same query; they all share the same groups.

## Explanation

`SUM(amount)` per region gives North 275, South 300 and East 80. The alias `total_revenue` is verified by the column check, and hidden rows (a new region and extra East sales) show that the totals are computed.
