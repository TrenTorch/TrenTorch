---
name: db-sql-join
title: 'INNER JOIN Combining Tables'
tags: [db]
difficulty: Intermediate
---

## Statement

Your shop has two tables: `users` (id, name) and `orders` (id, user_id, product). To display an order together with the customer's name you must match each order's `user_id` to a user's `id`. Orders that point to a user who does not exist (order 4 here) should not be listed.

Write a query returning `orders.user_id`, `orders.product` and `users.name` for every order that has a matching user (an inner join).

### Constraints

- Columns, in order: `user_id`, `product`, `name`
- Only orders that have a matching user (inner join)
- Row order does not matter

### Hints

<details>
<summary>Hint 1</summary>

`JOIN ... ON` connects rows from two tables where the condition is true.

</details>

<details>
<summary>Hint 2</summary>

Table aliases (`orders o`, `users u`) keep long conditions short.

</details>

## Theory

### The simple version

A join glues two tables together by matching a column in one with a column in the other. An inner join keeps only the rows that found a partner.

### Combining tables

Data is split across tables to avoid repeating it; a join stitches it back together:

```sql
SELECT o.user_id, o.product, u.name
FROM orders o
JOIN users u ON u.id = o.user_id;
```

`JOIN` (short for `INNER JOIN`) pairs every order with the user whose `id` equals its `user_id`, and keeps **only pairs that match**.

### How it behaves

- An order whose `user_id` has no matching user disappears from the result.
- A user with no orders disappears too.
- If a user has two orders, that user appears twice, once per order.

### Always write the ON condition

A join without a condition pairs every row with every row (a cross join). Forgetting `ON` is a classic cause of results with millions of rows.

### Aliases

`orders o` gives the table a short name so you can write `o.product`. When two tables share a column name (`id`) you **must** qualify it, otherwise SQLite reports an _ambiguous column name_ error.

## Explanation

`JOIN users u ON u.id = o.user_id` keeps only orders with a matching user, so the orphan order 4 is dropped. Alice appears twice because she has two orders. Cara has no orders and does not appear.
