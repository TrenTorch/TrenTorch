---
name: db-sql-in-list
title: 'IN List Matching'
tags: [db]
difficulty: Beginner
---

## Statement

Your permissions system applies special rules to a few specific ages. Instead of writing three `OR` conditions, use a list.

Write a query returning all columns of `users` where `age` is one of 12, 16 or 66.

### Constraints

- Return all columns
- Only ages 12, 16 and 66 (exact matches)

### Hints

<details>
<summary>Hint 1</summary>

`IN (...)` takes a comma-separated list of values.

</details>

<details>
<summary>Hint 2</summary>

`age IN (12, 16, 66)` is shorthand for three `=` tests joined with `OR`.

</details>

## Theory

### The simple version

`IN (...)` is a short way to write "equals this, or this, or this".

### Matching against a list

```sql
SELECT * FROM users WHERE age IN (12, 16, 66);
```

`x IN (a, b, c)` is true when `x` equals any item. It reads better than `x = a OR x = b OR x = c` and works for text as well: `department IN ('Sales', 'HR')`.

### NOT IN and NULL

`x NOT IN (a, b)` is the negation. Beware of `NULL` in the list: `x NOT IN (1, NULL)` is never true, because comparing with NULL is unknown. This matters most when the list comes from a subquery.

### Lists from subqueries

The list can be produced by a query:

```sql
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
```

You will use this form in the subquery question.

### When to use BETWEEN instead

`IN` is for a set of specific values. For a continuous range, `BETWEEN` (next question) is the right tool.

## Explanation

`age IN (12, 16, 66)` keeps ages that exactly equal one of the three numbers. Neighbouring ages (13, 15, 17) are in the data to catch queries that use a range instead of a list.
