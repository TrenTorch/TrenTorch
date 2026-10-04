---
name: db-sql-not
title: 'NOT Negation'
tags: [db]
difficulty: Beginner
---

## Statement

A report must exclude a group of users: everyone whose name starts with the letter C. Remember that SQLite's `LIKE` ignores case, so `chris` counts as starting with C.

Write a query returning all columns of `users` where the name does NOT start with 'C'.

### Constraints

- Return all columns
- Exclude every name starting with C or c

### Hints

<details>
<summary>Hint 1</summary>

`NOT` can be placed in front of a condition or in the operator: `NOT LIKE`.

</details>

<details>
<summary>Hint 2</summary>

Reuse the pattern `'C%'`.

</details>

## Theory

### The simple version

`NOT` flips a condition: keep the rows that fail it.

### Negating a condition

```sql
SELECT * FROM users WHERE name NOT LIKE 'C%';
-- same result:
SELECT * FROM users WHERE NOT (name LIKE 'C%');
```

`NOT` flips true and false. Many operators have a built-in negated form: `NOT LIKE`, `NOT IN`, `NOT BETWEEN`, `IS NOT NULL`, `<>`.

### Parentheses

`NOT a OR b` means `(NOT a) OR b`. Write `NOT (a OR b)` when you want to negate the whole group. By De Morgan's laws `NOT (a OR b)` equals `NOT a AND NOT b`.

### NULL surprises

If `name` could be NULL, `name NOT LIKE 'C%'` would be unknown for that row, so the row is dropped. Add `OR name IS NULL` if you want to keep it. Here `name` is `NOT NULL`, so the issue does not arise.

### Case sensitivity

Because SQLite's `LIKE` ignores case, `'chris'` matches `'C%'`; use `GLOB 'C*'` if you need a case-sensitive match.

## Explanation

`NOT LIKE 'C%'` excludes both `Carl` and `chris` because `LIKE` is case-insensitive in SQLite. The expected result keeps Alice, Bob, Dana and Eli. The hidden data adds another C-name (Cleo) that must be excluded.
