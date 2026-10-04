---
name: db-sql-correlated
title: 'Correlated Subqueries: Row-by-Row'
tags: [db]
difficulty: Advanced
---

## Statement

Find all employees who earn more than the average salary in their department. A correlated subquery evaluates for each row independently.

## Theory

### Correlated subqueries reference the outer query

A correlated subquery references columns from the outer query, executing once per outer row:

SELECT * FROM employees e1 WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department = e1.department);

For each employee (e1), the inner query computes the average salary in that employee's department (e2), then checks if e1's salary exceeds it.

### Execution model

Unlike scalar subqueries (which execute once), correlated subqueries execute repeatedly—once per outer row. This is slower but enables row-by-row comparisons.

### When to use correlated subqueries

- Compare a row to aggregates within its group
- Find outliers (employees earning above their department average)
- Row-level conditional logic that depends on the row itself

### Performance trade-off

Correlated subqueries can be slow on large tables. Modern SQL often replaces them with window functions or JOINs.

## Explanation

The solution correlates the inner query to the outer query via department, computing per-department averages and comparing each employee's salary to their own department's average.
