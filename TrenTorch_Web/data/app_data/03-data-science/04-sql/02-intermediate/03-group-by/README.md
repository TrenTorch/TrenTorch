---
name: db-sql-group-by
title: 'GROUP BY Aggregation'
tags: [db]
difficulty: Intermediate
---

## Statement

Your dashboard displays order volume per user. Instead of showing individual orders, aggregate them by user to see how many orders each user has placed.

Write a query returning `user_id` and the COUNT of orders for each user, grouped by user_id.

### Constraints

- Return user_id and order count
- Group by user_id (one row per unique user_id)

### Hints

<details>
<summary>Hint 1</summary>

GROUP BY creates groups of rows sharing the same value in the grouping column.

</details>

<details>
<summary>Hint 2</summary>

With GROUP BY user_id, aggregation functions like COUNT apply to each group separately.

</details>

## Theory

### GROUP BY creates groups and aggregates per group

While COUNT(*) FROM orders returns total orders, COUNT(*) with GROUP BY returns orders per group:

```sql
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;
```

This returns one row per unique user_id, with the count of orders in each group.

### Why GROUP BY matters

- Summaries: sales per region, users per age group, orders per customer
- Segmentation: break down data by categories
- Analytics: identify patterns within groups

## Explanation

The solution groups orders by user_id and counts the rows in each group, returning one row per user with their order count.
