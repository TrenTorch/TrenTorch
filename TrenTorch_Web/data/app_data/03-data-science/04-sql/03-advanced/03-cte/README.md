---
name: db-sql-cte
title: 'Common Table Expressions (CTE): Named Queries'
tags: [db]
difficulty: Advanced
---

## Statement

The previous question solved "above their department's average" with a correlated subquery. A **common table expression** (CTE) makes the same logic easier to read by naming the intermediate step.

Write a query that first defines a CTE with each department's average salary, then returns `name`, `department` and `salary` of every employee earning more than the average of their department. The query must use a `WITH` clause.

### Constraints

- Columns, in order: `name`, `department`, `salary`
- Define the department averages in a `WITH` clause
- Join the CTE back to `employees`

### Hints

<details>
<summary>Hint 1</summary>

`WITH name AS (SELECT ...) SELECT ... FROM name` defines a temporary named result.

</details>

<details>
<summary>Hint 2</summary>

Join the CTE to `employees` on `department`, then filter with `WHERE`.

</details>

## Theory

### The simple version

A CTE (`WITH`) gives a name to an intermediate result so a long query can be read as small steps.

### Naming a step

```sql
WITH dept_avg AS (
  SELECT department, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department
)
SELECT e.name, e.department, e.salary
FROM employees e
JOIN dept_avg d ON d.department = e.department
WHERE e.salary > d.avg_salary;
```

A CTE is a named subquery that lives for one statement. You can then use `dept_avg` like a table.

### Why use it

- **Readability.** Break a big query into named steps, read top to bottom.
- **Reuse.** Refer to the same intermediate result several times.
- **Chaining.** Define several CTEs separated by commas; later ones can use earlier ones.

### CTE vs subquery vs temp table

A CTE is not stored anywhere; it is just a labelled query. Since SQLite 3.35 you can add `AS MATERIALIZED` to ask SQLite to compute it once and keep the result for the duration of the statement, or `AS NOT MATERIALIZED` to let it be inlined.

### Recursive CTEs

Adding `RECURSIVE` lets a CTE refer to itself, which is how hierarchies are traversed (see the recursive CTE question).

## Explanation

The `dept_avg` CTE computes one row per department; joining it back to `employees` lets each employee be compared with their own department's average. The test also verifies that the query text contains a `WITH` clause.
