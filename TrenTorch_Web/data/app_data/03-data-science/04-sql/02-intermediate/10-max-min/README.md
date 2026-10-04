---
name: db-sql-max-min
title: 'MAX and MIN'
tags: [db]
difficulty: Intermediate
---

## Statement

The catalogue page shows, for every product category, the price range of its items.

Write a query returning each `category` of `products` with its highest price as `max_price` and its lowest price as `min_price`.

### Constraints

- Columns, in order: `category`, `max_price`, `min_price`
- One row per category

### Hints

<details>
<summary>Hint 1</summary>

`MAX` and `MIN` are aggregates, so they need `GROUP BY category`.

</details>

<details>
<summary>Hint 2</summary>

Both can appear in the same `SELECT`.

</details>

## Theory

### The simple version

`MAX` and `MIN` find the largest and smallest value. With `GROUP BY` you get them per group.

### Extremes per group

```sql
SELECT category, MAX(price) AS max_price, MIN(price) AS min_price
FROM products
GROUP BY category;
```

`MAX` and `MIN` return the largest and smallest non-NULL value in each group. They work on numbers, text (alphabetical order) and dates.

### Getting the whole row of the maximum

`MAX(price)` gives you the number, not the product that has it. Selecting `name` next to `MAX(price)` is a special case SQLite allows (it returns the name from the row holding the max), but it is not portable, and it is easy to misread. The robust approach is a window function or a join back to the table; you will see both later.

### Without GROUP BY

`SELECT MAX(price) FROM products;` returns the single most expensive price across the whole table.

### Empty input

For an empty group or table, `MAX` and `MIN` return NULL.

## Explanation

Grouping by category and applying `MAX` and `MIN` yields Electronics 900/20, Furniture 150/30 and Stationery 2/2. The alias names are checked, and the hidden rows change two of the ranges.
