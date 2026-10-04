---
name: db-sql-is-null
title: 'IS NULL Checking'
tags: [db]
difficulty: Beginner
---

## Statement

A data-quality audit needs to find incomplete user records. Some users have no email recorded at all (the value is `NULL`). One user has an _empty string_ instead, which is a different thing and is not part of this audit.

Write a query returning all columns of `users` where `email` IS NULL.

### Constraints

- Return all columns
- Only rows where `email` is NULL
- An empty string `''` is not NULL

### Hints

<details>
<summary>Hint 1</summary>

`= NULL` never matches anything; SQL has a dedicated operator.

</details>

<details>
<summary>Hint 2</summary>

Use `IS NULL`, and `IS NOT NULL` for the opposite.

</details>

## Theory

### The simple version

`NULL` means "unknown", and nothing is equal to unknown, not even another NULL. That is why you ask `IS NULL` instead of `= NULL`.

### NULL means "unknown"

`NULL` is not zero and not an empty string; it marks a missing or unknown value. Because it is unknown, comparing it to anything yields _unknown_, not true:

```sql
SELECT NULL = NULL;   -- NULL (unknown), not 1
SELECT * FROM users WHERE email = NULL;   -- always returns no rows
```

### Testing for NULL

Use the dedicated operators:

```sql
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;
```

### Three-valued logic

SQL conditions are _true_, _false_ or _unknown_, and `WHERE` keeps only the true ones. That is why `email <> 'x'` also drops rows whose email is NULL: `NULL <> 'x'` is unknown. If you want those rows too, say so: `email <> 'x' OR email IS NULL`.

### Empty string vs NULL

`''` is a real value of length zero; it is not NULL, and `email IS NULL` does not match it. Data-cleaning queries often need to check both.

## Explanation

`WHERE email IS NULL` is the only correct way to find missing values. `email = NULL` returns nothing, and `email = ''` finds the wrong user (Cara). The expected rows are Bob and Dan.
