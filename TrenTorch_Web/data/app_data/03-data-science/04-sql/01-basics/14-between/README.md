---
name: db-sql-between
title: 'BETWEEN Range Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

Your analytics needs users in a specific age range for a study (30 to 40 years old, inclusive). Write a query that returns all such users efficiently.

Write a query returning all columns from `users` where `age` is between 30 and 40 (inclusive).

### Constraints

- Return all columns
- age between 30 and 40 (inclusive on both ends)

### Hints

<details>
<summary>Hint 1</summary>

BETWEEN is shorthand for a range check.

</details>

<details>
<summary>Hint 2</summary>

BETWEEN 30 AND 40 includes both 30 and 40.

</details>

## Theory

### BETWEEN checks range membership

WHERE age BETWEEN 30 AND 40 returns rows where 30 <= age <= 40.

### BETWEEN vs comparison operators

These are equivalent:
- WHERE age BETWEEN 30 AND 40
- WHERE age >= 30 AND age <= 40

BETWEEN is clearer for ranges.

### BETWEEN includes endpoints

BETWEEN 30 AND 40 includes both 30 and 40 (not 30 < age < 40).

## Explanation

The solution is SELECT * FROM users WHERE age BETWEEN 30 AND 40;. The database returns rows where age falls within the range, inclusive.
