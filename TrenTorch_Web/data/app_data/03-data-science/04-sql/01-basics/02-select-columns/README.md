---
name: db-sql-select-columns
title: 'SELECT Specific Columns'
tags: [db]
difficulty: Beginner
---

## Statement

Your application needs to display a user contact list. Each entry shows only the person's name and email address—their age and user ID are not relevant for this display and would add clutter.

Write a query that returns only the `name` and `email` columns from the `users` table, in that order.

### Constraints

- Return only `name` and `email` columns
- Return all rows in the users table
- Columns must appear in the order: name, email

### Hints

<details>
<summary>Hint 1</summary>

Instead of `SELECT *`, list the column names you want, separated by commas.

</details>

<details>
<summary>Hint 2</summary>

Order matters: the first column you name will appear first in the result.

</details>

## Theory

### Being specific about columns

While `SELECT *` retrieves everything, real queries usually name the columns they need. This is better for clarity (readers see exactly what you're fetching) and robustness (if the table gains new columns, your query's output doesn't change).

```sql
SELECT name, email FROM users;
```

### Column order is preserved

SQL returns columns in the order you list them. If you write `SELECT email, name FROM users`, the email column comes first, then name.

### Why selective columns matter

- Network bandwidth: Unnecessary columns waste network resources
- Clarity: Explicit column names make code reviews easier
- Security: Selective columns let you exclude sensitive data
- Performance: Less data to transfer and process

### The mental model

Think of `SELECT` as a projection: you have all the data, but you're choosing which columns to project onto the result.

## Explanation

The solution lists the desired columns in the SELECT clause: `SELECT name, email FROM users;`. The table's other columns (id, age) are not retrieved. The FROM clause still references the full users table, so all rows are returned—we're just showing fewer columns for each row. Tests verify both the column count (exactly 2) and the column order (name first, email second).