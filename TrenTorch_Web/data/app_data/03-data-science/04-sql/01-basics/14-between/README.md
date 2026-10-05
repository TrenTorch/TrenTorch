---
name: db-sql-between
title: 'BETWEEN Range Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

A research study recruits users aged 30 to 40 inclusive.

Write a query returning all columns of `users` where `age` is between 30 and 40, including both 30 and 40.

### Constraints

- Return all columns
- 30 and 40 are both included

### Hints

<details>
<summary>Hint 1</summary>

`BETWEEN low AND high` is a shorthand for a pair of comparisons.

</details>

<details>
<summary>Hint 2</summary>

It is inclusive at both ends.

</details>

## Theory

### The simple version

`BETWEEN low AND high` keeps values from `low` up to and including `high`.

### Ranges with BETWEEN

```sql
SELECT * FROM users WHERE age BETWEEN 30 AND 40;
```

`x BETWEEN a AND b` means `x >= a AND x <= b`. **Both ends are inclusive**, which surprises people coming from programming languages where ranges exclude the end.

### Order matters

`BETWEEN 40 AND 30` returns nothing, because no number is at least 40 and at most 30. Put the smaller bound first.

### Dates and text

It works on any comparable type: `WHERE created_on BETWEEN '2024-01-01' AND '2024-01-31'`. With timestamps be careful: `'2024-01-31'` is smaller than `'2024-01-31 10:00:00'`, so a half-open range (`>= start AND < next_day`) is safer.

### NOT BETWEEN

`age NOT BETWEEN 30 AND 40` is true outside the range.

## Explanation

`BETWEEN 30 AND 40` expands to `age >= 30 AND age <= 40`. The visible data has 29 and 41 just outside the range, and the hidden data adds more users exactly on 30 and 40 to verify that both ends are included.
