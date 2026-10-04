---
name: db-sql-select-all
title: 'SELECT All Rows'
tags: [db]
difficulty: Beginner
---

## Statement

You're building a reporting dashboard for a user management system. The first page needs to display every user's full profile (id, name, email, age) with no filtering or sorting — just the raw data as it exists in the database.

Write a query that returns all rows and all columns from the `users` table.

### Constraints

- Return every row in the table
- Include all columns (id, name, email, age)
- No filtering or sorting required
- The order of rows may be arbitrary

### Hints

<details>
<summary>Hint 1</summary>

In SQL, `SELECT *` means "all columns." What keyword controls which rows you want?

</details>

<details>
<summary>Hint 2</summary>

The `FROM` clause names the table. If you want every row, you don't add a `WHERE` clause.

</details>

## Theory

### The simplest query

Every SQL query that reads data starts with `SELECT` (which columns?) and `FROM` (which table?). The wildcard `*` means "every column":

```sql
SELECT * FROM users;
```

This is the foundation of SQL. It says: "I want every column from the users table, and I want every row because I haven't said otherwise."

### What `SELECT *` actually does

When you write `SELECT *`, the database returns columns in the order they were defined in the table schema (id, name, email, age in this case). A `*` is shorthand — the database translates it to the actual column list behind the scenes. In production systems, many style guides discourage `SELECT *` and require explicit column names instead, because if the table schema changes (someone adds a column), your code's behavior changes silently. For this exercise, `SELECT *` is fine.

### The implicit `FROM` to results pipeline

1. **FROM users** — start with every row in the users table
2. **SELECT \*** — for each row, output every column
3. No `WHERE`, `ORDER BY`, or other clauses — so the result is the table as-is

### Why this is query #1

Before filtering (WHERE), sorting (ORDER BY), or aggregating (COUNT, SUM), you need to see raw data. This is how you explore a new dataset, sanity-check the schema, and understand what you're working with. Every larger query builds on this foundation.

## Explanation

The solution is simply `SELECT * FROM users;` — it retrieves every row and every column. There's no WHERE clause (which would filter rows), no ORDER BY (which would sort), and no aggregation (which would combine rows). The query returns the table untouched. Tests verify that all 3 rows are returned and that each row has all 4 columns (id, name, email, age).
