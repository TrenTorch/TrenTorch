---
name: db-sql-subquery
title: 'Subqueries: Nested Queries'
tags: [db]
difficulty: Advanced
---

## Statement

Your dashboard needs to find all users whose age is above average. You can't use GROUP BY for this; instead, use a subquery to compute the average, then filter against it.

## Theory

### Subqueries solve multi-step problems

A subquery is a SELECT inside another SELECT. It lets you break complex logic into steps:

SELECT * FROM users WHERE age > (SELECT AVG(age) FROM users);

This reads as:
1. Inner query: Calculate the average age across all users
2. Outer query: Return users whose age exceeds that average

### Execution order

The inner query runs first, computing a single value (average age). The outer query then compares each user's age to that value.

### Why subqueries matter

- Break complex logic into readable steps
- Avoid pre-computing values in application code
- Enable dynamic thresholds (average, percentiles, max of groups)
- Support correlation (inner query references outer query columns)

### Types of subqueries

- Scalar subquery: returns one row, one column (used in WHERE, SELECT)
- Row subquery: returns one row, multiple columns
- Table subquery: returns multiple rows

## Explanation

The solution uses a scalar subquery in WHERE to filter users. The inner query computes average age; the outer query returns users exceeding it.
