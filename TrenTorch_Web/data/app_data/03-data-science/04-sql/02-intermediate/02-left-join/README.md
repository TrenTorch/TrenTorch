---
name: db-sql-left-join
title: 'LEFT JOIN Preserving Left Table'
tags: [db]
difficulty: Intermediate
---

## Statement

Your user analytics needs to show all users along with their order count, even if some users have never placed an order. A LEFT JOIN keeps all rows from the left table and matches data from the right table where available.

Write a query returning `users.id`, `users.name`, and the count of orders for each user (using GROUP BY).

### Constraints

- Include all users, even those without orders
- Show order count per user

### Hints

<details>
<summary>Hint 1</summary>

LEFT JOIN keeps all rows from the left table (users).

</details>

<details>
<summary>Hint 2</summary>

Combine LEFT JOIN with COUNT and GROUP BY to aggregate.

</details>

## Theory

### LEFT JOIN preserves all left table rows

INNER JOIN returns only matches. LEFT JOIN returns all rows from the left table, with NULL values where the right table has no match.

### LEFT vs INNER JOIN

- INNER: only matching rows
- LEFT: all left rows, plus matches from right
- RIGHT: all right rows, plus matches from left
- FULL: all rows from both tables

### NULL in joined results

When a user has no orders, the order columns contain NULL.

## Explanation

The solution uses LEFT JOIN to include all users and COUNT with GROUP BY to aggregate order counts per user.
