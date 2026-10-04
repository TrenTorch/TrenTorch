---
name: db-sql-perf-query-cache
title: 'Query Caching with Materialized CTEs'
tags: [db]
difficulty: Advanced
---

## Statement

Finding the top spenders above the average needs the per-customer totals **twice**: once to compare each customer with the average, and once to produce the rows. Aggregating 5,000 orders two times is wasteful. In SQLite you can tell the engine to compute a CTE once and reuse the stored result for the rest of the statement with `AS MATERIALIZED`, a small in-query cache.

Write a query that defines `totals` (customer_id and the sum of `total` as `spend`) as a materialized CTE, then returns `customer_id` and `spend` for the 5 highest customers whose spend is greater than the average spend of all customers. Order by `spend` descending, then `customer_id`.

### Constraints

- Columns, in order: `customer_id`, `spend`
- Define the totals with `WITH totals AS MATERIALIZED (...)`
- Only customers above the average spend, top 5, ordered by `spend` descending then `customer_id`

### Hints

<details>
<summary>Hint 1</summary>

Reference `totals` both in the main query and in the subquery that computes the average.

</details>

<details>
<summary>Hint 2</summary>

`LIMIT 5` after the `ORDER BY`.

</details>

## Theory

### The simple version

If a query needs the same expensive result twice, compute it once and reuse it. `AS MATERIALIZED` asks SQLite to do that for a CTE.

### The same work twice

```sql
SELECT customer_id, SUM(total) AS spend FROM orders GROUP BY customer_id
```

is needed to find the average _and_ to list who is above it. If SQLite inlines a CTE into both places it may do the aggregation twice.

### Materializing

```sql
WITH totals AS MATERIALIZED (
  SELECT customer_id, SUM(total) AS spend
  FROM orders
  GROUP BY customer_id
)
SELECT customer_id, spend
FROM totals
WHERE spend > (SELECT AVG(spend) FROM totals)
ORDER BY spend DESC, customer_id
LIMIT 5;
```

`AS MATERIALIZED` (SQLite 3.35+) makes SQLite compute `totals` once, keep it in a temporary table, and let every reference read that. `AS NOT MATERIALIZED` asks for the opposite (inline it, which lets filters be pushed down).

### Caches at other levels

- **Inside a query:** materialized CTEs, temporary tables.
- **Between queries:** a stored summary table (previous question) refreshed on a schedule.
- **In the application:** a result cache keyed by the query text and parameters, with an expiry. Databases such as MySQL used to have a built-in query cache; it was removed because invalidating it correctly under writes costs more than it saves.

### The price of caching

Cached data can be stale and uses memory or disk. Cache what is expensive to compute and read often.

## Explanation

`totals` is computed once and referenced twice: for the average and for the final rows. The tests check the `AS MATERIALIZED` clause and the five rows, ordered by spend (ties by customer_id).
