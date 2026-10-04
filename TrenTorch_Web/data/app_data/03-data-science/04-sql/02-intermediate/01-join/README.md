---
name: db-sql-join
title: 'INNER JOIN Combining Tables'
tags: [db]
difficulty: Intermediate
---

## Statement

Your system has two tables: `users` (id, name) and `orders` (user_id, product). You need to display each order with its corresponding user's name. Match rows where the user_id from orders equals the id from users (an inner join).

Write a query returning `orders.user_id`, `orders.product`, and `users.name` for all matching user-order pairs.

### Constraints

- Include only rows where a match exists (user in both tables)
- Return user_id, product, and name

### Hints

<details>
<summary>Hint 1</summary>

JOIN combines rows from two tables based on a condition.

</details>

<details>
<summary>Hint 2</summary>

ON specifies the matching condition (usually a foreign key).

</details>

## Theory

### JOIN combines multiple tables

While SELECT * FROM users returns users alone, JOIN brings in related data from another table:

```sql
SELECT orders.user_id, orders.product, users.name 
FROM orders 
INNER JOIN users ON orders.user_id = users.id;
```

This says: for each order, find the user whose id matches that order's user_id, then show both the order and the user's name.

### INNER JOIN returns only matches

INNER JOIN (the default) returns rows where both tables have matching data. If an order references a user_id that doesn't exist in users, that order is excluded.

### Why JOIN matters

- Normalization: split data across tables to avoid repetition
- Relationships: connect users to orders, orders to products
- Analytics: correlate data from different sources
- Reporting: combine data for comprehensive views

## Explanation

The solution joins orders and users on the matching condition (orders.user_id = users.id). Only rows where both tables have a match appear in the result.
