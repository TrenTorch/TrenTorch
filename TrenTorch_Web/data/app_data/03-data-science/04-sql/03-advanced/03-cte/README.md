---
name: db-sql-cte
title: 'Common Table Expressions (CTE): Named Queries'
tags: [db]
difficulty: Advanced
---

## Statement

Build a multi-step analysis: first calculate department averages, then find employees above their department's average. Use WITH to name intermediate results.

## Theory

### CTEs make complex queries readable

A CTE (Common Table Expression) names an intermediate query with WITH:

WITH dept_avg AS (SELECT department, AVG(salary) as avg_sal FROM employees GROUP BY department) SELECT e.* FROM employees e JOIN dept_avg da ON e.department = da.department WHERE e.salary > da.avg_sal;

CTEs break complex logic into named steps, improving readability.

### CTE vs subquery

Both solve multi-step problems:
- Subqueries are inline; CTEs are named
- Multiple CTEs can reference each other (chaining)
- CTEs can be recursive (self-referencing)

### Why CTEs matter

- Readability: name intermediate results
- Reusability: reference the same CTE multiple times
- Maintainability: easier to modify and debug
- Recursion: CTEs support recursive logic (hierarchies, paths)

### CTE syntax

WITH name AS (query) is the foundation. You can chain: WITH a AS (...), b AS (SELECT ... FROM a).

## Explanation

The solution defines a CTE to pre-compute department averages, then joins employees to that CTE and filters for above-average earners in each department.
