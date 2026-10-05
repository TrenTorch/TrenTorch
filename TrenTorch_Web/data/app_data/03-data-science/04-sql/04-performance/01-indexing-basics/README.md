---
name: db-sql-perf-indexing-basics
title: 'Indexes: Turning Scans into Searches'
tags: [db]
difficulty: Advanced
---

## Statement

The `orders` table holds 5,000 rows and customers constantly look up their own orders:

```sql
SELECT * FROM orders WHERE customer_id = 42;
```

With no index on `customer_id`, SQLite has to read **every** row to find the matching ones (a _table scan_). Add an index so it can jump straight to them (an _index search_).

Create an index named `idx_orders_customer` on `orders(customer_id)`, and then run the lookup for customer 42 so the result is returned.

### Constraints

- The index must be named `idx_orders_customer` and cover only `customer_id`
- End your script with the lookup `SELECT * FROM orders WHERE customer_id = 42;`
- The lookup must use the index (checked with `EXPLAIN QUERY PLAN`)

### Hints

<details>
<summary>Hint 1</summary>

`CREATE INDEX name ON table(column);`

</details>

<details>
<summary>Hint 2</summary>

Run `EXPLAIN QUERY PLAN SELECT ...` yourself: `SCAN orders` is slow, `SEARCH orders USING INDEX ...` is fast.

</details>

## Theory

### The simple version

An index is a sorted lookup structure, like the index of a book. It lets the database jump straight to matching rows instead of reading the whole table.

### What an index is

An index is a second, sorted structure (a B-tree) that maps column values to the rows holding them, like the index at the back of a book:

```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

Looking up `customer_id = 42` then takes a handful of page reads (logarithmic in the table size) instead of reading every row.

### Seeing the difference

`EXPLAIN QUERY PLAN` shows how SQLite will run a query:

```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 42;
-- before: SCAN orders
-- after:  SEARCH orders USING INDEX idx_orders_customer (customer_id=?)
```

### The trade-offs

- Every index makes `INSERT`, `UPDATE` and `DELETE` a little slower because the index must be maintained.
- Every index takes disk space.
- An index helps when a query is **selective**: here 10 of 5,000 rows match. If most rows match, the scan is just as good.

### Which columns to index

Columns used in `WHERE`, `JOIN ... ON` and `ORDER BY` of frequent queries. Primary keys are indexed automatically.

## Explanation

`CREATE INDEX idx_orders_customer ON orders(customer_id)` builds the sorted structure; the following lookup can then use it, which `EXPLAIN QUERY PLAN` reports as `SEARCH orders USING INDEX idx_orders_customer`. The tests check the index name and column, the 10 returned rows, and the query plan.
