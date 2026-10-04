---
name: db-sql-multiple-join
title: 'MULTIPLE JOIN'
tags: [db]
difficulty: Intermediate
---

## Statement

Your system has users, orders, and products tables. Display order information with both the customer name and product name by joining all three tables.

Write a query returning user name, product name, and order details by joining users, orders, and products.

### Constraints

- Join all three tables
- Return name from users, name from products, and relevant order columns

### Hints

<details>
<summary>Hint 1</summary>

Chain joins: FROM orders JOIN users ON ... JOIN products ON ...

</details>

<details>
<summary>Hint 2</summary>

Each join condition connects tables via foreign keys.

</details>

## Theory

### Multiple JOINs chain together

You can join more than two tables by chaining join conditions. Each join adds another table's data:

```sql
SELECT users.name, products.name, orders.quantity 
FROM orders 
JOIN users ON orders.user_id = users.id 
JOIN products ON orders.product_id = products.id;
```

## Explanation

The solution joins orders to users (to get customer name) and then joins orders to products (to get product name), combining data from all three tables.
