---
name: db-sql-limit
title: 'LIMIT Pagination'
tags: [db]
difficulty: Beginner
---

## Statement

The admin screen lists users two per page, ordered by `id`. Page 1 shows users 1 and 2; page 2 shows users 3 and 4.

Write a query that returns page 2: all columns of `users`, ordered by `id`, skipping the first 2 rows and returning the next 2.

### Constraints

- Order the rows by `id` ascending
- Skip the first 2 rows and return exactly the next 2
- Return all columns

### Hints

<details>
<summary>Hint 1</summary>

`LIMIT n` caps the number of rows; `OFFSET m` skips rows first.

</details>

<details>
<summary>Hint 2</summary>

Pagination only makes sense with an `ORDER BY`, otherwise pages are arbitrary.

</details>

## Theory

### The simple version

`LIMIT` says how many rows you want and `OFFSET` says how many to skip first. Together they give you pages.

### LIMIT and OFFSET

```sql
SELECT * FROM users ORDER BY id LIMIT 2 OFFSET 2;
```

`LIMIT 2` returns at most two rows; `OFFSET 2` first discards the first two. For page number `p` with page size `n`, use `LIMIT n OFFSET (p - 1) * n`.

### Always pair it with ORDER BY

Without `ORDER BY` the database may return rows in any order, so "the first 2 rows" is not well defined and two pages could even overlap. Sort by a unique column so each page is stable.

### The cost of deep pages

`OFFSET` still has to walk past all the skipped rows. Page 10,000 is slower than page 1. For large tables, _keyset pagination_ (`WHERE id > :last_seen_id ORDER BY id LIMIT 2`) avoids that.

### SQLite shorthand

SQLite also accepts `LIMIT offset, count`, but the order of those two numbers is the opposite of what most people expect, so the explicit `OFFSET` form is easier to read.

## Explanation

`ORDER BY id LIMIT 2 OFFSET 2` sorts, discards two rows, and returns the next two. The order of the rows is checked, and a hidden dataset with one extra user confirms that you are not just selecting ids 3 and 4 by value.
