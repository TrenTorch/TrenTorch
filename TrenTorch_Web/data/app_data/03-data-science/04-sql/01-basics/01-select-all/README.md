---
name: db-sql-select-all
title: 'SELECT All Rows'
tags: [db]
difficulty: Beginner
---

## Statement

You are building the first page of a user-management dashboard. It must show every user's full profile (id, name, email, age) exactly as stored, with no filtering and no sorting.

Write a query that returns all rows and all columns from the `users` table.

### Constraints

- Return every row of `users`
- Return every column: id, name, email, age (in table order)
- No `WHERE` or `ORDER BY` is needed; row order does not matter

### Hints

<details>
<summary>Hint 1</summary>

`*` is shorthand for "all columns".

</details>

<details>
<summary>Hint 2</summary>

The table name goes after `FROM`. With no `WHERE`, every row is returned.

</details>

## Theory

### The simple version

A table is a grid of rows and columns. `SELECT * FROM users` says: show me the whole grid.

### The simplest query

Every query that reads data is built from `SELECT` (which columns?) and `FROM` (which table?). The wildcard `*` means "every column":

```sql
SELECT * FROM users;
```

Conceptually the database starts from the whole table (`FROM users`) and then keeps the requested columns (`SELECT *`). Nothing removes rows, so the result is the table as it is stored.

### Why `SELECT *` is a tool for exploring, not for shipping

`*` expands to whatever columns exist _right now_. If a teammate adds a column later, every query that used `*` silently returns more data. Production code usually names its columns; `*` is ideal for peeking at an unfamiliar table, which is exactly how you will use it here.

### Reading the result

A query returns a _result set_: a header row of column names and zero or more rows. SQL tables have no inherent row order, so unless you add `ORDER BY` you must not rely on one.

## Explanation

`SELECT * FROM users;` reads the whole table. There is no `WHERE`, so no row is filtered out, and `*` keeps every column. The tests check the column names, compare the rows (order ignored) and re-run your query against a different set of users, so a query that simply types out the four visible rows would fail.
