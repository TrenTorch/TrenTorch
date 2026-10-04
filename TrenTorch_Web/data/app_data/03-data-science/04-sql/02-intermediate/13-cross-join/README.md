---
name: db-sql-cross-join
title: 'CROSS JOIN'
tags: [db]
difficulty: Intermediate
---

## Statement

A T-shirt shop wants a list of every variant it could stock: each color in each size.

Write a query returning every combination of a row from `colors` and a row from `sizes`, with the columns `color` and `size`.

### Constraints

- Columns, in order: `color`, `size`
- Every color paired with every size (2 × 3 = 6 rows here)

### Hints

<details>
<summary>Hint 1</summary>

A cross join needs no `ON` condition.

</details>

<details>
<summary>Hint 2</summary>

Alias both `name` columns, since both tables have one.

</details>

## Theory

### The simple version

A cross join pairs every row of one table with every row of another, giving all combinations.

### The Cartesian product

```sql
SELECT c.name AS color, s.name AS size
FROM colors c
CROSS JOIN sizes s;
```

`CROSS JOIN` pairs **every** row of the first table with **every** row of the second. With 2 colors and 3 sizes you get 6 rows; in general `rows(A) × rows(B)`.

### When it is useful

- Generating all combinations (variants, test matrices, calendars × rooms).
- Pairing a single-row result (such as an overall average) with every row of another table.

### When it is a bug

A normal join whose `ON` clause was forgotten (or that matches nothing) degenerates into a cross join. Two tables of 10,000 rows produce 100,000,000 rows, which is why a surprisingly slow query is the first thing to check for a missing `ON`.

### Equivalent forms

`FROM colors, sizes` (the old comma syntax) and `JOIN` without `ON` mean the same in SQLite; writing `CROSS JOIN` states your intention.

## Explanation

`CROSS JOIN` produces all 2 × 3 combinations. The hidden data adds a color and a size, giving 3 × 4 = 12 rows, so the result must come from the join and not be typed out.
