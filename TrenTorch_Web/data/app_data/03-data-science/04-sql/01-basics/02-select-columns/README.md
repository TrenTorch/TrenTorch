---
name: db-sql-select-columns
title: 'SELECT Specific Columns'
tags: [db]
difficulty: Beginner
---

## Statement

Your app shows a contact list. Each entry needs only the person's name and email address; id and age would just add clutter.

Write a query that returns only the `name` and `email` columns of `users`, in that order.

### Constraints

- Return exactly two columns: `name`, then `email`
- Return every row of `users`

### Hints

<details>
<summary>Hint 1</summary>

Replace `*` with a comma-separated list of column names.

</details>

<details>
<summary>Hint 2</summary>

Order in the list is the order in the result.

</details>

## Theory

### The simple version

Instead of the whole grid you can ask for just the columns you care about, in the order you want.

### Choosing columns

Instead of `*`, list the columns you want, separated by commas:

```sql
SELECT name, email FROM users;
```

This is called a _projection_: the result keeps every row but only the columns you named, in the order you named them.

### Why it matters

- **Less data moves.** On wide tables, fetching two columns instead of thirty is much cheaper.
- **Stable contracts.** Naming columns means a new column in the table cannot change what your code receives.
- **Intent is visible.** Anyone reading the query sees exactly which fields it depends on.

### Reordering and renaming

You are free to list columns in any order, and `AS` renames a column in the output: `SELECT email AS contact FROM users;`. The table itself is never changed.

## Explanation

`SELECT name, email FROM users;` is a projection: all rows, two columns. The tests check the column names _and their order_, then compare rows against a second dataset. Returning `id` or `age` as well, or swapping the two columns, fails.
