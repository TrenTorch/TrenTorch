---
name: db-sql-distinct-count
title: 'DISTINCT COUNT'
tags: [db]
difficulty: Intermediate
---

## Statement

The sales report headline says "orders from N customers". There are six orders, but several customers ordered more than once, so counting rows overstates N.

Write a query returning a single value, the number of distinct `user_id`s in `orders`, named `customer_count`.

### Constraints

- Return a single row with the column `customer_count`
- Each customer counts once however many orders they placed

### Hints

<details>
<summary>Hint 1</summary>

`COUNT(DISTINCT column)` counts unique values.

</details>

<details>
<summary>Hint 2</summary>

`COUNT(*)` would return 6, the number of orders.

</details>

## Theory

### The simple version

`COUNT(DISTINCT x)` counts how many different values there are, not how many rows.

### Counting unique values

```sql
SELECT COUNT(DISTINCT user_id) AS customer_count FROM orders;
```

`COUNT(DISTINCT x)` counts how many different non-NULL values `x` takes. Orders by users 1, 1, 2, 3, 3, 3 contain three distinct customers.

### Compare the variants

| Expression                | Result on this data |
| ------------------------- | ------------------- |
| `COUNT(*)`                | 6 (rows)            |
| `COUNT(user_id)`          | 6 (non-NULL values) |
| `COUNT(DISTINCT user_id)` | 3 (unique values)   |

### Per group

It combines with `GROUP BY` to answer questions like "how many distinct customers per month":

```sql
SELECT strftime('%Y-%m', ordered_on) AS month,
       COUNT(DISTINCT user_id) AS customers
FROM orders
GROUP BY month;
```

### Cost and alternatives

Counting distinct values needs to remember every value seen, so it is slower and uses more memory than a plain count. `SELECT COUNT(*) FROM (SELECT DISTINCT user_id FROM orders)` is an equivalent form.

## Explanation

`COUNT(DISTINCT user_id)` counts three unique customers; `COUNT(*)` would return 6. The hidden data adds orders from three more customers (and extra orders for an existing one), so the result changes from 3 to 5.
