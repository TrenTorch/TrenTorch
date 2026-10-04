---
name: db-sql-not
title: 'NOT Negation'
tags: [db]
difficulty: Beginner
---

## Statement

Your system needs to exclude a specific set of users from a report. You want all users whose name does NOT start with 'C'.

Write a query returning all columns from `users` where the name does NOT start with 'C'.

### Constraints

- Return all columns
- Only rows where name does NOT start with 'C'

### Hints

<details>
<summary>Hint 1</summary>

NOT reverses the truth value of a condition.

</details>

<details>
<summary>Hint 2</summary>

NOT LIKE 'C%' means "does not start with C."

</details>

## Theory

### NOT reverses a condition

WHERE NOT LIKE 'C%' returns rows that do NOT match the pattern.

### Equivalent forms

These are equivalent:
- WHERE NOT name LIKE 'C%'
- WHERE name NOT LIKE 'C%'

### NOT with common operators

- NOT IN: value is not in the list
- NOT LIKE: does not match pattern
- IS NOT NULL: value is not missing

### When to use NOT

- Exclusion: exclude specific groups
- Negation: "not yet processed," "not active"
- Complex conditions: clarify intent

## Explanation

The solution is SELECT * FROM users WHERE NOT name LIKE 'C%';. The database returns rows where the name doesn't start with 'C'.
