---
name: db-sql-like
title: 'LIKE Pattern Matching'
tags: [db]
difficulty: Beginner
---

## Statement

Your search feature lets users find other users by email domain. You want to return all users whose email ends with 'example.com'.

Write a query returning all columns from `users` where `email` ends with 'example.com'.

### Constraints

- Return all columns
- Only rows where email ends with 'example.com'

### Hints

<details>
<summary>Hint 1</summary>

Use LIKE with % wildcard. % matches any characters.

</details>

<details>
<summary>Hint 2</summary>

LIKE '%example.com' matches anything ending with 'example.com'.

</details>

## Theory

### LIKE enables pattern matching

LIKE is a string pattern operator. Key wildcards are:
- %: matches zero or more characters
- _: matches exactly one character

### Common LIKE patterns

- LIKE 'A%': starts with A
- LIKE '%com': ends with com
- LIKE '%arr%': contains arr anywhere
- LIKE 'A_c': starts with A, has any middle character, ends with c

### Case sensitivity

LIKE is typically case-insensitive (depends on database collation).

## Explanation

The solution is SELECT * FROM users WHERE email LIKE '%example.com';. The % wildcard matches anything, so this query returns all email addresses ending with 'example.com'.
