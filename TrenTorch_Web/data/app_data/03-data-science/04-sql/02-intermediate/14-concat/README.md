---
name: db-sql-concat
title: 'String CONCAT'
tags: [db]
difficulty: Intermediate
---

## Statement

The profile page shows each user's full name in one column: first name, a space, then last name. Some people have only one name (the `last_name` column is NULL) and must show just their first name, with no trailing space and not a blank value.

Write a query returning one column, `full_name`.

### Constraints

- One column named `full_name`
- `first_name` + space + `last_name`
- If `last_name` is NULL, return only `first_name`

### Hints

<details>
<summary>Hint 1</summary>

SQL's concatenation operator is `||`; SQLite (3.39) has no `CONCAT()` function.

</details>

<details>
<summary>Hint 2</summary>

Concatenating with NULL gives NULL; `COALESCE(x, '')` swaps NULL for an empty string.

</details>

## Theory

### The simple version

`||` sticks pieces of text together. If any piece is NULL the whole result becomes NULL, so give optional pieces a default.

### Joining text

```sql
SELECT first_name || ' ' || last_name AS full_name FROM users;
```

`||` concatenates strings. SQLite does **not** have a `CONCAT()` function in the version used here (3.39), so `CONCAT(first_name, ' ', last_name)` fails with _no such function: CONCAT_. MySQL and newer versions of other databases do have it.

### NULL poisons concatenation

`'Prince' || ' ' || NULL` is `NULL`, so the whole name disappears. Handle optional parts explicitly:

```sql
first_name || COALESCE(' ' || last_name, '')
```

If `last_name` is NULL, `' ' || last_name` is NULL, `COALESCE` replaces it with `''`, and the space is dropped as well.

### COALESCE

`COALESCE(a, b, c)` returns the first argument that is not NULL. It is the standard way to supply defaults.

### Other helpers

`UPPER`, `LOWER`, `TRIM`, `LENGTH`, `SUBSTR` and `REPLACE` cover most day-to-day text work.

## Explanation

`first_name || COALESCE(' ' || last_name, '')` builds "John Doe", "Jane Smith" and just "Prince". A plain `first_name || ' ' || last_name` returns NULL for Prince, and `CONCAT` raises an error in this SQLite version.
