---
name: db-sql-correlated
title: 'Correlated Subqueries: Row-by-Row'
tags: [db]
difficulty: Advanced
---

## Statement

HR wants to see who is paid above their own team's norm. Engineering earns more than Sales on average, so comparing everyone to one company-wide average would give the wrong answer.

Write a query returning `name`, `department` and `salary` of every employee whose salary is greater than the average salary **of their own department**. Use a correlated subquery.

### Constraints

- Columns, in order: `name`, `department`, `salary`
- Compare each employee with their _own_ department's average
- A department with a single employee has no one above its average

### Hints

<details>
<summary>Hint 1</summary>

The subquery can refer to a column of the outer row, e.g. `e.department`.

</details>

<details>
<summary>Hint 2</summary>

Give the outer table an alias so the inner query can reach it.

</details>

## Theory

### The simple version

A correlated subquery peeks at the current row of the outer query, so it can answer "compared with my own group".

### A subquery that looks at the outer row

```sql
SELECT name, department, salary
FROM employees e
WHERE salary > (
  SELECT AVG(salary)
  FROM employees
  WHERE department = e.department
);
```

Unlike the previous question, the inner query mentions `e.department` from the **outer** query, so its answer changes from row to row. That is what makes it _correlated_.

### How it executes (conceptually)

For each employee `e`, the database computes the average salary of `e`'s department and compares it with `e.salary`. Engineering employees are compared with 66,666, Sales with 42,000, and so on.

### Cost

Naively that is one subquery per row, so it can be slow on big tables. Planners often optimise it, but an equivalent join to a grouped subquery (or a window function such as `AVG(salary) OVER (PARTITION BY department)`) is a good alternative to know.

### Typical uses

"Above the group average", "the latest row per customer", "does a related row exist" (`WHERE EXISTS (SELECT 1 ...)`).

## Explanation

Per department averages are Engineering 66,667, Sales 42,000 and HR 52,000. Only Charlie (90,000) and Eve (44,000) are above their own department's average; Frank is alone in HR, so he equals the average and is excluded. Comparing with a single company average would produce a different list.
