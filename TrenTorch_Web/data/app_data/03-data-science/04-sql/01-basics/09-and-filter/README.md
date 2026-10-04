---
name: db-sql-and-filter
title: 'AND Compound Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

A mailing campaign targets adult users (age 18 or older) whose name starts with "A". A user has to satisfy **both** conditions to be included.

Write a query returning all columns of `users` where `age >= 18` AND `name` starts with `'A'`.

### Constraints

- Return all columns
- Both conditions must hold: `age >= 18` and the name starts with A
- Row order does not matter

### Hints

<details>
<summary>Hint 1</summary>

Combine the conditions with `AND`.

</details>

<details>
<summary>Hint 2</summary>

`LIKE 'A%'` matches text that starts with A (`%` stands for any run of characters).

</details>

## Theory

### The simple version

`AND` means both conditions must be true for a row to be kept.

### Combining conditions with AND

```sql
SELECT * FROM users WHERE age >= 18 AND name LIKE 'A%';
```

`AND` keeps a row only when **both** sides are true. Each extra `AND` makes the filter stricter and the result smaller.

### Operator precedence

`AND` binds tighter than `OR`. When you mix them, add parentheses so the intent is explicit:

```sql
WHERE (age >= 18 OR parent_consent = 1) AND country = 'IN'
```

### Pattern matching with LIKE

In `LIKE`, `%` matches any run of characters (including none) and `_` matches exactly one. In SQLite `LIKE` is **case-insensitive** for ASCII letters, so `'A%'` also matches `'adam'`.

### Order of evaluation

SQL does not promise that the left condition is checked first, so do not rely on `AND` to protect a later condition from an error.

## Explanation

`age >= 18 AND name LIKE 'A%'` keeps Alice, Anna and Aaron. Adam starts with A but is 17; Bob is an adult but does not start with A. Each half of the filter is exercised by the data, and the hidden rows add another under-age A name and an adult A name.
