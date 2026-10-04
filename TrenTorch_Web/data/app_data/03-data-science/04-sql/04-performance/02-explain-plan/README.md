---
name: db-sql-perf-explain-plan
title: 'Reading EXPLAIN QUERY PLAN'
tags: [db]
difficulty: Advanced
---

## Statement

Before you can speed up a query you have to know how SQLite will run it. `EXPLAIN QUERY PLAN` shows the strategy chosen by the planner without running the query.

The `orders` table (5,000 rows) has no index on `total`. Prefix this query with `EXPLAIN QUERY PLAN` and run it:

```sql
SELECT * FROM orders WHERE total > 90;
```

The result should show a full table scan.

### Constraints

- Run `EXPLAIN QUERY PLAN` on exactly `SELECT * FROM orders WHERE total > 90`
- Do not create any index; the plan must show a `SCAN` of `orders`

### Hints

<details>
<summary>Hint 1</summary>

The statement is `EXPLAIN QUERY PLAN` followed by the query.

</details>

<details>
<summary>Hint 2</summary>

Read the `detail` column: `SCAN orders` means every row is read.

</details>

## Theory

### The simple version

`EXPLAIN QUERY PLAN` shows how the database will run your query: whether it reads every row (SCAN) or jumps via an index (SEARCH).

### Asking the planner

```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE total > 90;
```

returns rows with the columns `id`, `parent`, `notused` and `detail`. The `detail` text is the plan. The `id`/`parent` pair describes how steps nest.

### The words to know

| Detail                                              | Meaning                                                          |
| --------------------------------------------------- | ---------------------------------------------------------------- |
| `SCAN orders`                                       | reads every row of the table                                     |
| `SEARCH orders USING INDEX idx (col=?)`             | jumps to matching rows through an index                          |
| `SEARCH orders USING INTEGER PRIMARY KEY (rowid=?)` | direct lookup by primary key                                     |
| `USING COVERING INDEX`                              | the index alone has all needed columns; the table is not touched |
| `USE TEMP B-TREE FOR ORDER BY`                      | an extra sort is needed                                          |

### How to use it

1. Run the plan for a slow query.
2. Look for `SCAN` on big tables and for temporary B-trees.
3. Change the query or add an index.
4. Run the plan again and compare.

### Not a timing

The plan tells you _how_ the query runs, not how long it takes. It is deterministic for the same schema, statistics and query, which is what makes it good for tests.

## Explanation

With no usable index on `total`, SQLite plans `SCAN orders`. The tests confirm that your statement begins with `EXPLAIN QUERY PLAN`, that it explains the requested query, and that the plan is a scan and not a search.
