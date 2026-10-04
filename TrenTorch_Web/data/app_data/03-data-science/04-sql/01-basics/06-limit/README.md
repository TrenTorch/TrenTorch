---
name: db-sql-limit
title: 'LIMIT Pagination'
tags: [db]
difficulty: Beginner
---

## Statement

Your user management interface displays users in pages. For performance, fetch only the first 2 users from the table.

Write a query that returns all columns from the `users` table, but only the first 2 rows.

### Constraints

- Return all columns
- Return only the first 2 rows

### Hints

<details>
<summary>Hint 1</summary>

The LIMIT clause restricts how many rows are returned.

</details>

<details>
<summary>Hint 2</summary>

LIMIT 2 means "give me the first 2 rows."

</details>

## Theory

### LIMIT restricts the result count

By default, SELECT returns every matching row. LIMIT caps that and is essential for large tables.

### LIMIT with ORDER BY enables pagination

SELECT * FROM users ORDER BY id LIMIT 2 OFFSET 2 skips the first 2 rows and returns the next 2.

### Why LIMIT matters

- Pagination: Show 50 users per page
- Exploration: Preview data without waiting for millions of rows
- Safety: Prevent queries that paralyze the database
- Testing: Quick validation without full result sets

## Explanation

The solution is SELECT * FROM users LIMIT 2;. The database returns all columns but stops after the first 2 rows.
