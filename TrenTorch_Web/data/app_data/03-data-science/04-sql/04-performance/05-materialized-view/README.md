---
name: db-sql-perf-materialized-view
title: 'Materialized Views (Emulated in SQLite)'
tags: [db]
difficulty: Advanced
---

## Statement

A dashboard repeatedly asks for the total sales and order count per region from the 2,000-row `sales` table. Re-aggregating on every page view is wasteful when the numbers change only once a day.

Many databases offer _materialized views_ for this. SQLite does not, but you can emulate one with a regular table filled from a query. Create a table named `sales_by_region` with the columns `region`, `total_amount` (sum of `amount`) and `order_count` (number of sales), then select all of its rows ordered by `region`.

### Constraints

- Create the table `sales_by_region` with `CREATE TABLE ... AS SELECT`
- Columns: `region`, `total_amount`, `order_count`
- Finish with `SELECT * FROM sales_by_region ORDER BY region;`

### Hints

<details>
<summary>Hint 1</summary>

`CREATE TABLE name AS SELECT ...` stores the query result as a real table.

</details>

<details>
<summary>Hint 2</summary>

Use `GROUP BY region` with `SUM(amount)` and `COUNT(*)` and alias them.

</details>

## Theory

### The simple version

A materialized view stores the result of a query as a table so reading it is instant, at the price of being slightly out of date.

### View vs materialized view

- A **view** is a saved query. Reading it re-runs the query every time, so it is always fresh and never faster.
- A **materialized view** stores the query _result_ on disk. Reading it is cheap, but it can become **stale** until you refresh it.

### Emulating one in SQLite

```sql
CREATE TABLE sales_by_region AS
SELECT region, SUM(amount) AS total_amount, COUNT(*) AS order_count
FROM sales
GROUP BY region;
```

Reads of `sales_by_region` touch 4 rows instead of aggregating 2,000.

### Refreshing

Because it is a snapshot you must update it yourself, for example on a schedule:

```sql
DELETE FROM sales_by_region;
INSERT INTO sales_by_region SELECT region, SUM(amount), COUNT(*) FROM sales GROUP BY region;
```

or incrementally with triggers on `sales`.

### When it pays off

Expensive aggregates read much more often than they change, and slightly old numbers are acceptable. When freshness is critical, use a plain view or an index instead.

## Explanation

`CREATE TABLE ... AS SELECT` stores the aggregated result. The last test inserts a new sale after your script ran and checks that the summary did **not** change: that is the defining property (and the cost) of a materialized view, staleness.
