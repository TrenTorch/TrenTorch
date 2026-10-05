---
name: db-sql-perf-join-order
title: 'Join Order Optimization'
tags: [db]
difficulty: Advanced
---

## Statement

`regions` has 5 rows and `customers` has 1,000 rows with an index `idx_customers_region` on `region_id`. To list the customers of the region named `'EU'`, the efficient plan is:

1. look at the (tiny) `regions` table and find `EU`,
2. use `idx_customers_region` to fetch only that region's customers.

SQLite normally finds this plan by itself, but in a `CROSS JOIN` it will **never** reorder the tables, so you can dictate the loop order yourself.

Write the query with `CROSS JOIN` so that `regions` is the outer loop and `customers` the inner, index-driven loop. Return only the customer `name`. Do not use table aliases (so the plan text stays readable).

### Constraints

- Return one column: the customer `name`
- Use `regions CROSS JOIN customers ON ...` (outer loop `regions`)
- Do not alias the tables
- `customers` must be searched through `idx_customers_region`

### Hints

<details>
<summary>Hint 1</summary>

In SQLite the left table of a `CROSS JOIN` is always the outer loop.

</details>

<details>
<summary>Hint 2</summary>

Put the matching condition in `ON customers.region_id = regions.id` and the filter in `WHERE regions.name = 'EU'`.

</details>

## Theory

### The simple version

A join is a loop inside a loop. Looping over the small table on the outside and using an index on the inside is usually much faster.

### Nested loops

A join is executed as nested loops: for each row of the _outer_ table, look for matches in the _inner_ table. Which table is outer matters enormously:

- Outer = `regions` (5 rows): 5 iterations, each an index search in `customers`.
- Outer = `customers` (1,000 rows): 1,000 iterations, each a lookup in `regions`.

```sql
SELECT customers.name
FROM regions CROSS JOIN customers ON customers.region_id = regions.id
WHERE regions.name = 'EU';
```

### How the planner decides

For ordinary `JOIN`s SQLite is free to reorder the tables using its cost estimates, usually correctly. In a `CROSS JOIN` it keeps the order you wrote, which is SQLite's way of letting you force a plan.

### Reading the plan

```
SCAN regions
SEARCH customers USING INDEX idx_customers_region (region_id=?)
```

The first line is the outer loop, the second the inner loop. An index on the join column of the inner table is what makes the nested loop cheap.

### Rule of thumb

Put the table that produces fewer rows (after filtering) first, and make sure the inner table has an index on the join column.

## Explanation

`regions CROSS JOIN customers` fixes the loop order: scan the small `regions` table, then `SEARCH customers USING INDEX idx_customers_region`. The tests check the 200 returned names, the `CROSS JOIN`, and the two plan steps in order.
