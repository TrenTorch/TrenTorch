---
name: db-sql-group-by
title: 'GROUP BY Aggregation'
tags: [db]
difficulty: Intermediate
---

## Statement

The dashboard shows order volume per customer instead of individual orders.

Write a query returning each `user_id` from `orders` together with the number of orders that user placed, named `order_count`.

### Constraints

- Columns, in order: `user_id`, `order_count`
- One row per distinct `user_id`
- Row order does not matter

### Hints

<details>
<summary>Hint 1</summary>

`GROUP BY` forms one group per distinct value of a column.

</details>

<details>
<summary>Hint 2</summary>

Aggregate functions like `COUNT(*)` are computed once per group.

</details>

## Theory

### The simple version

`GROUP BY` sorts rows into piles (one per value) and then you can summarise each pile, for example count it.

### Collapsing rows into groups

```sql
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id;
```

`GROUP BY user_id` puts all rows with the same `user_id` into one group, and the aggregate (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) is computed per group. The result has one row per group.

### What can appear in SELECT

Every selected column must either be in the `GROUP BY` or be wrapped in an aggregate. Selecting `product` here would be meaningless: which of the user's products should represent the group? (SQLite lets you do it and picks an arbitrary row's value, which hides bugs; other databases reject the query.)

### Multiple grouping columns

`GROUP BY user_id, product` makes one group per unique pair.

### Order of the pipeline

`FROM` → `WHERE` (filters rows) → `GROUP BY` → `HAVING` (filters groups) → `SELECT` → `ORDER BY`. The next question covers `HAVING`.

## Explanation

`GROUP BY user_id` produces one row per user and `COUNT(*)` counts the orders in each group. The tests check the column names, so the count must be aliased `order_count`, and a second dataset with new users confirms the grouping is computed.
