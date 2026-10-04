---
name: db-sql-self-join
title: 'SELF JOIN'
tags: [db]
difficulty: Intermediate
---

## Statement

The `employees` table has a `manager_id` column that points at another row in the same table (the manager's `id`). The top person has `manager_id` NULL.

Write a query returning each employee's `name` as `employee` and their manager's `name` as `manager`. Employees without a manager (the top of the chart) are not listed.

### Constraints

- Columns, in order: `employee`, `manager`
- Join `employees` to itself
- Employees with no manager are excluded

### Hints

<details>
<summary>Hint 1</summary>

Use the table twice with two different aliases, e.g. `employees e` and `employees m`.

</details>

<details>
<summary>Hint 2</summary>

Match `e.manager_id` to `m.id`.

</details>

## Theory

### The simple version

A table can be joined to itself when one of its columns points to another row of the same table, like an employee pointing to their manager.

### A table joined to itself

When rows refer to other rows of the same table (an org chart, a category tree, "friend of") you join the table to itself. The two copies need different aliases:

```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
JOIN employees m ON m.id = e.manager_id;
```

Think of `e` as the employee's row and `m` as the manager's row.

### Inner vs left

With an inner join, employees whose `manager_id` is NULL find no match and are dropped. A `LEFT JOIN` keeps them with `manager` = NULL, which is the way to list _everyone_ alongside their (possible) manager.

### Beyond one level

A self-join follows one hop. To walk a whole hierarchy (all reports, however deep) you need a recursive CTE, covered in the advanced track.

### Aliases are mandatory

Both copies have the same column names, so without distinct aliases SQLite cannot tell which `name` you mean.

## Explanation

Joining `employees e` to `employees m` on `m.id = e.manager_id` pairs each employee with their manager. Alice has no manager, so the inner join drops her. Aliasing the output columns `employee` and `manager` is checked by the tests.
