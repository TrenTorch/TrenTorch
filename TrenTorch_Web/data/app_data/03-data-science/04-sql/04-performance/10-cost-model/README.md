---
name: db-sql-perf-cost-model
title: 'A Tiny Cost Model: Selectivity'
tags: [db]
difficulty: Advanced
---

## Statement

Query planners are _cost-based_: they estimate the cost of each plan and pick the cheapest. A key input is **selectivity**, the fraction of rows a condition keeps. A condition that keeps a small fraction favours an index; one that keeps most rows favours a plain scan (reading an index and then the table for most rows is slower than just reading the table).

Using a simple rule, an index lookup is worth it when selectivity is **below 0.15**. For each `status` in `orders`, return:

- `status`,
- `row_count`,
- `selectivity` = `row_count` ÷ total number of orders, rounded to 3 decimals,
- `use_index` = 1 if the selectivity is below 0.15, otherwise 0.

Order the result by `status`.

### Constraints

- Columns, in order: `status`, `row_count`, `selectivity`, `use_index`
- `selectivity` is rounded to 3 decimals
- `use_index` is 1 when `selectivity < 0.15`, else 0
- Order by `status`

### Hints

<details>
<summary>Hint 1</summary>

A CTE can compute the counts and selectivity first; a second `SELECT` can then apply `CASE` to it.

</details>

<details>
<summary>Hint 2</summary>

Use `1.0 *` before dividing so the division is not an integer division.

</details>

## Theory

### The simple version

The database picks the plan with the lowest estimated cost. Selectivity (the fraction of rows kept) is the main input: small fractions favour an index.

### Cost-based optimisation

For every query the planner enumerates candidate plans (which index, which join order) and estimates a cost for each, usually "how many rows or pages will be read". It then runs the cheapest.

### Selectivity

```
selectivity = rows matching the condition / total rows
```

- **Low (0.001):** very selective. An index finds the few rows quickly.
- **High (0.6):** most of the table matches. A sequential scan is cheaper, because index lookups jump around the table (random access) while a scan reads pages in order.

### The break-even point

The exact threshold depends on the engine and hardware; a classic rule of thumb is somewhere around 5-20% of the rows. This question uses 15% to make a clear, testable rule.

### Cost from statistics

The estimates come from statistics (`ANALYZE`, histograms). Wrong or stale statistics lead to wrong selectivity guesses, and therefore to bad plans.

## Explanation

Selectivity is 0.6 for paid, 0.2 for shipped and 0.1 for new and returned. With the 0.15 rule only `new` and `returned` use the index. The tests check the exact table and the two extreme decisions.
