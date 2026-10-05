---
name: db-sql-perf-query-hints
title: 'Query Hints: INDEXED BY'
tags: [db]
difficulty: Advanced
---

## Statement

`orders` has two indexes, `idx_orders_status` and `idx_orders_created`. For this query either could be used, and the planner picks one on its own:

```sql
SELECT COUNT(*) FROM orders WHERE status = 'paid' AND created_on >= '2024-06-01';
```

Sometimes you know better than the planner (or you want to be sure a particular plan is used). SQLite lets you _hint_ an index with `INDEXED BY`.

Write the count so that it must use `idx_orders_created`.

### Constraints

- Return a single count of paid orders with `created_on >= '2024-06-01'`
- Use `INDEXED BY idx_orders_created`
- The plan must use that index

### Hints

<details>
<summary>Hint 1</summary>

Syntax: `FROM orders INDEXED BY idx_orders_created`.

</details>

<details>
<summary>Hint 2</summary>

If the named index cannot be used for the query, SQLite raises an error instead of falling back.

</details>

## Theory

### The simple version

A hint tells the database which index to use instead of letting it decide. `INDEXED BY` is SQLite's version.

### Overriding the planner

```sql
SELECT COUNT(*)
FROM orders INDEXED BY idx_orders_created
WHERE status = 'paid' AND created_on >= '2024-06-01';
```

`INDEXED BY idx` requires SQLite to use that index; `NOT INDEXED` forbids all indexes. Other databases call this a _hint_ (`USE INDEX` in MySQL, `/*+ INDEX(...) */` in Oracle).

### It fails loudly

If SQLite cannot use the named index for the query (for example it does not exist or the `WHERE` cannot use it), you get `Runtime error: no query solution` instead of silently picking another plan. This makes it a useful debugging tool and a risky production tool.

### Why the planner might choose wrongly

The planner estimates how many rows match using statistics (see the statistics question). If the statistics are missing or stale, it can pick a poor index. Prefer fixing the statistics (`ANALYZE`) or the index design first, and hint only as a last resort: a hint silently becomes wrong when the data changes.

### Checking the effect

Compare `EXPLAIN QUERY PLAN` with and without the hint to see which index is chosen.

## Explanation

`INDEXED BY idx_orders_created` forces the plan to use the date index, so the plan mentions `idx_orders_created`. The tests verify the hint is present, that the count is right, and that the plan really uses the forced index.
