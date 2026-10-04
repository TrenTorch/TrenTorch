---
name: db-sql-perf-statistics
title: 'Table Statistics with ANALYZE'
tags: [db]
difficulty: Advanced
---

## Statement

The query planner chooses between plans by estimating how many rows each step touches. Those estimates come from **statistics** about your data. SQLite keeps them in a table called `sqlite_stat1`, which is created and filled by the `ANALYZE` command.

The `orders` table (5,000 rows) has two indexes: `idx_orders_customer` and `idx_orders_status`. Run `ANALYZE`, then return the columns `tbl`, `idx` and `stat` from `sqlite_stat1`, ordered by `tbl` and then `idx`.

### Constraints

- Run `ANALYZE;` first
- Return `tbl`, `idx`, `stat` from `sqlite_stat1`
- Order by `tbl`, then `idx`

### Hints

<details>
<summary>Hint 1</summary>

`ANALYZE;` has no arguments for the whole database.

</details>

<details>
<summary>Hint 2</summary>

`sqlite_stat1` appears only after `ANALYZE` has run.

</details>

## Theory

### The simple version

The database guesses how many rows a condition will match from statistics it collects with `ANALYZE`. Better guesses mean better plans.

### Why statistics matter

For `WHERE customer_id = 42` the planner must guess how many rows match. If it thinks "almost all", a full scan is cheaper; if it thinks "very few", the index wins. Guesses come from statistics.

### ANALYZE and sqlite_stat1

```sql
ANALYZE;
SELECT tbl, idx, stat FROM sqlite_stat1;
```

Each row describes a table or index. The `stat` text starts with the **number of rows** in the table, followed by the **average number of rows per distinct key** for each indexed column. For example:

```
orders | idx_orders_customer | 5000 10      -- 500 distinct customers, ~10 rows each
orders | idx_orders_status   | 5000 1250    -- 4 distinct statuses, ~1250 rows each
```

### Reading it

`5000 10` tells the planner that an equality lookup on `customer_id` returns about 10 rows (very selective, use the index), while `5000 1250` says a status lookup returns a quarter of the table (not selective).

### Keeping it fresh

Statistics are a snapshot. After large changes re-run `ANALYZE` (or `PRAGMA optimize`, which does it only where it helps).

## Explanation

`ANALYZE` populates `sqlite_stat1`, one row per index. 500 customers over 5,000 orders gives `5000 10`; 4 distinct statuses give `5000 1250`. The tests compare the exact rows, so the statistics must really have been collected.
