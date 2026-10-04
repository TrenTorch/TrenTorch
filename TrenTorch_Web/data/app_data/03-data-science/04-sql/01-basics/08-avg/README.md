---
name: db-sql-avg
title: 'AVG Averaging'
tags: [db]
difficulty: Beginner
---

## Statement

Your reporting system needs to calculate the average age of all users. Instead of fetching every age and computing the mean in application code, calculate it in SQL.

Write a query that returns the average age of all users in the `users` table.

### Constraints

- Return a single value: the average age
- Include all users (no filtering)

### Hints

<details>
<summary>Hint 1</summary>

The AVG function calculates the arithmetic mean of a column.

</details>

<details>
<summary>Hint 2</summary>

AVG(age) computes the sum of all ages divided by the count of non-NULL ages.

</details>

## Theory

### AVG aggregates multiple values into one

Like COUNT, AVG is an aggregation function that combines multiple rows into a single result. It computes the arithmetic mean (sum divided by count).

### Aggregation functions in SQL

- COUNT: number of rows
- SUM: total of a column
- AVG: arithmetic mean
- MIN: smallest value
- MAX: largest value

### Why aggregation matters

- Statistics: average customer purchase, median response time
- Monitoring: average query latency, mean time between failures
- Analytics: average user session duration
- Reporting: aggregate metrics across time periods

## Explanation

The solution is SELECT AVG(age) FROM users;. The database sums all age values and divides by the count of non-NULL ages, returning the average as a single number.
