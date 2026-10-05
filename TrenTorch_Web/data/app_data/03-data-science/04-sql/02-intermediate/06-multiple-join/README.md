---
name: db-sql-multiple-join
title: 'MULTIPLE JOIN'
tags: [db]
difficulty: Intermediate
---

## Statement

An order only stores ids: the buyer's `user_id` and the `product_id`. To produce a readable order list you must join **three** tables: `orders`, `users` and `products`.

Write a query returning the buyer's name as `user_name`, the product's name as `product_name`, and the order's `quantity`.

### Constraints

- Columns, in order: `user_name`, `product_name`, `quantity`
- Join all three tables (one row per order)
- Both `users.name` and `products.name` need aliases because the names collide

### Hints

<details>
<summary>Hint 1</summary>

Start from `orders` and add one `JOIN ... ON` per table.

</details>

<details>
<summary>Hint 2</summary>

Both `users` and `products` have a `name` column; give each output column a distinct alias.

</details>

## Theory

### The simple version

Joins can be chained: join the second table, then the third, each with its own matching condition.

### Chaining joins

Each `JOIN` adds one more table to the result so far:

```sql
SELECT u.name AS user_name, p.name AS product_name, o.quantity
FROM orders o
JOIN users u    ON u.id = o.user_id
JOIN products p ON p.id = o.product_id;
```

Read it top to bottom: start with `orders`, attach the matching user, then attach the matching product.

### The fact table in the middle

`orders` links the other two tables with foreign keys (`user_id`, `product_id`). Such a "fact" table sits at the centre and each dimension table (`users`, `products`) hangs off it. Starting from the fact table makes the joins easy to follow.

### Column name clashes

`users.name` and `products.name` are both called `name`. If you select them without aliases the result has two columns called `name`, which is confusing and breaks code that reads columns by name. Alias them.

### Join count and cost

Each extra join multiplies the work the planner must consider. Join on indexed keys (the primary keys here) and select only the columns you need.

## Explanation

Starting from `orders`, the first join attaches the buyer and the second attaches the product, giving one row per order. The two `name` columns are aliased to `user_name` and `product_name`, which the tests check.
