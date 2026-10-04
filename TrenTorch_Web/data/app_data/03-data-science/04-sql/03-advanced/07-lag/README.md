---
name: db-sql-lag
title: 'LAG: Access Previous Row'
tags: [db]
difficulty: Advanced
---

## Statement

A finance report compares each month's revenue with the month before. The first month has no previous value, so it shows NULL.

Write a query returning `month`, `revenue` and the previous month's revenue as `prev_revenue`, using `LAG()`, with the rows ordered by `month`.

### Constraints

- Columns, in order: `month`, `revenue`, `prev_revenue`
- The first month's `prev_revenue` is NULL
- Rows ordered by `month` ascending

### Hints

<details>
<summary>Hint 1</summary>

`LAG(column) OVER (ORDER BY ...)` reads the value from the previous row.

</details>

<details>
<summary>Hint 2</summary>

Add a normal `ORDER BY month` at the end to order the output.

</details>

## Theory

### The simple version

`LAG` lets a row look at the row before it, which is how you compare a month with the previous month.

### Looking at the previous row

```sql
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_revenue
FROM monthly_sales
ORDER BY month;
```

`LAG(x)` returns the value of `x` from the previous row of the window (in the window's order). For the first row there is none, so the result is `NULL`.

### Optional arguments

`LAG(x, 2)` looks two rows back, and `LAG(x, 1, 0)` returns `0` instead of NULL when there is no previous row.

### Two different ORDER BYs

The `ORDER BY` inside `OVER (...)` defines what "previous" means. The `ORDER BY` at the end of the query only sorts the final output. They are independent, so write both.

### Computing change

Month-over-month growth is `revenue - LAG(revenue) OVER (ORDER BY month)`, or in percent: `100.0 * (revenue - prev) / prev`. Guard against a NULL or zero `prev`.

### With PARTITION BY

Add `PARTITION BY customer_id` to compare each customer's rows only with their own earlier rows.

## Explanation

`LAG(revenue) OVER (ORDER BY month)` shifts revenue down by one row, so each month sees the one before it. The test checks the row order and uses hidden data with an earlier month, which becomes the new first row with NULL.
