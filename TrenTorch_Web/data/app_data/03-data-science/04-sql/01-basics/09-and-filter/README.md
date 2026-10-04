---
name: db-sql-and-filter
title: 'AND Compound Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

Your dashboard filters users by multiple criteria: you want adult users (age >= 18) whose names contain a specific pattern. Write a query that requires both conditions to be true.

Write a query returning all columns from `users` where `age >= 18` AND `name` starts with 'A'.

### Constraints

- Return all columns
- age >= 18 AND name starts with 'A'

### Hints

<details>
<summary>Hint 1</summary>

The AND operator combines multiple conditions; both must be true.

</details>

<details>
<summary>Hint 2</summary>

For "starts with", use LIKE 'A%' (% is a wildcard for any characters).

</details>

## Theory

### AND requires both conditions to be true

WHERE age >= 18 AND name LIKE 'A%' returns rows where BOTH conditions hold.

### Logical operators

- AND: both conditions must be true
- OR: at least one condition must be true
- NOT: negates a condition

### LIKE for pattern matching

- LIKE 'A%': starts with A
- LIKE '%com': ends with com
- LIKE '%arr%': contains arr anywhere

## Explanation

The solution is SELECT * FROM users WHERE age >= 18 AND name LIKE 'A%';. The database returns rows satisfying both the age and name conditions.
