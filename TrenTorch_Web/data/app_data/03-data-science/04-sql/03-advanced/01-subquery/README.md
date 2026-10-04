---
name: db-sql-subquery
title: 'Subqueries: Nested Queries'
tags: [db]
difficulty: Advanced
---

## Statement

You want to highlight users who are older than average. You cannot compare against `AVG(age)` directly in a `WHERE` clause, because the average has to be computed first.

Write a query returning `id`, `name` and `age` of every user whose age is strictly greater than the average age of all users. Use a subquery for the average.

### Constraints

- Columns, in order: `id`, `name`, `age`
- Strictly greater than the average (not equal)
- Compute the average inside the query; do not type it in

### Hints

<details>
<summary>Hint 1</summary>

A subquery is a `SELECT` in parentheses used as a value.

</details>

<details>
<summary>Hint 2</summary>

`WHERE age > (SELECT AVG(age) FROM users)`

</details>

## Theory

### The simple version

A subquery is a query in brackets whose answer is used by the outer query, for example "the average" to compare each row against.

### A query inside a query

```sql
SELECT id, name, age
FROM users
WHERE age > (SELECT AVG(age) FROM users);
```

The part in parentheses is a _scalar subquery_: it returns exactly one value (one row, one column), which the outer query then uses like a constant. Here it runs once and yields 30.

### Why not just use AVG in WHERE?

Aggregates are computed **after** `WHERE` filters rows, so `WHERE age > AVG(age)` is an error (_misuse of aggregate_). A subquery computes the average in a separate step first.

### Kinds of subqueries

| Kind       | Returns                  | Used with         |
| ---------- | ------------------------ | ----------------- |
| Scalar     | one value                | `=`, `>`, `<` ... |
| List       | one column, many rows    | `IN`, `NOT IN`    |
| Table      | many columns and rows    | `FROM (...)`      |
| Correlated | depends on the outer row | next question     |

### Watch out

A scalar subquery that returns more than one row does not error in SQLite; it silently uses the first row. Make sure the subquery is guaranteed to return one row (an aggregate without `GROUP BY` always does).

## Explanation

The average age is 30, so `age > 30` keeps Charlie (35) and Diana (40); Bob is exactly average and is excluded. The hidden dataset changes the average, so a hard-coded `30` fails.
