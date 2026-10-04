---
name: db-sql-right-join
title: 'RIGHT JOIN'
tags: [db]
difficulty: Intermediate
---

## Statement

A data-integrity report lists **every order**, together with the buyer's name when the buyer exists. Order 4 refers to user 99, who is not in `users`; it must still be listed, with a NULL name. Users who have placed no orders are not part of this report.

Write a query returning `orders.id` as `order_id` and `users.name`, keeping every order, using a `RIGHT JOIN` with `users` on the left and `orders` on the right.

### Constraints

- Columns, in order: `order_id`, `name`
- Every order appears once, even without a matching user
- Use `users` as the left table and `orders` as the right table

### Hints

<details>
<summary>Hint 1</summary>

A right join keeps all rows from the table written _after_ `JOIN`.

</details>

<details>
<summary>Hint 2</summary>

`FROM users u RIGHT JOIN orders o ON ...`

</details>

## Theory

### The simple version

A right join is a left join seen from the other side: it keeps every row of the second table.

### Mirror image of LEFT JOIN

```sql
SELECT o.id AS order_id, u.name
FROM users u
RIGHT JOIN orders o ON o.user_id = u.id;
```

`RIGHT JOIN` keeps every row of the table on the right (`orders`) and fills the left table's columns with `NULL` when there is no match. It is exactly `orders LEFT JOIN users` with the tables swapped.

### Why it is rare in practice

Most people write `LEFT JOIN` and put the "keep everything" table first, because reading a query as "start from X, then optionally add Y" is more natural. SQLite only supports `RIGHT JOIN` since version 3.39 (this editor runs 3.39).

### Finding orphans

Adding `WHERE u.id IS NULL` returns only the orders without a user: a quick referential-integrity check.

### FULL JOIN

`FULL JOIN` keeps unmatched rows from both sides; it is also available from SQLite 3.39.

## Explanation

`users u RIGHT JOIN orders o` keeps all four orders; order 4 (user 99) gets `NULL` for `name`. Cara has no orders and is not listed, because the right join keeps only unmatched rows from the right side.
